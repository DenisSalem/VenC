#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.


from copy import deepcopy

import datetime
import hashlib
import json
import os
import unidecode

from urllib.parse import quote as urllib_parse_quote

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.entry import yield_entries_content
from venc2.datastore.entry import Entry
from venc2.datastore.metadata import build_categories_tree
from venc2.datastore.metadata import MetadataNode
from venc2.datastore.metadata import Chapter
from venc2.helpers import GenericMessage
from venc2.helpers import quirk_encoding
from venc2.prompt import notify
from venc2.l10n import messages
from venc2.patterns.exceptions import MalformedPatterns
from venc2.patterns.exceptions import PatternMissingArguments
from venc2.patterns.exceptions import PatternInvalidArgument
from venc2.patterns.non_contextual import get_embed_content

def merge(iterable, argv):
    if len(argv) != 2:
        raise PatternMissingArguments(expected=2,got=len(argv))
    try:
        return argv[1].join([argv[0].format(**something) for something in iterable])
        
    except IndexError as e:
        if e.args == ('tuple index out of range',):
            raise PatternInvalidArgument(name="string", value=argv[0])
                
        raise e
    
class DataStore:
    def __init__(self):
        self.in_child_process = False
        notify("┌─ "+messages.loading_entries)
        self.root_page = None
        self.blog_configuration = get_blog_configuration()
        self.sort_by = self.blog_configuration["sort_by"]
        self.enable_jsonld = self.blog_configuration["enable_jsonld"]
        self.enable_jsonp =  self.blog_configuration["enable_jsonp"]
        self.blog_url = self.blog_configuration["blog_url"]
        self.path_encoding = self.blog_configuration["path_encoding"]
        self.disable_threads = [thread_name.strip() for thread_name in self.blog_configuration["disable_threads"].split(',')]
        self.entries = []
        self.entries_per_archives = []
        self.entries_per_categories = []
        
        try:
            from multiprocessing import cpu_count
            self.workers_count = cpu_count()
            if int(self.blog_configuration["parallel_processing"]) < self.workers_count:
                 self.workers_count  =  int(self.blog_configuration["parallel_processing"])
            
        except:
            self.workers_count = 1

        self.requested_entry = None
            
        self.max_category_weight = 1
        self.categories_leaves = []
        self.embed_providers = {}
        self.html_categories_tree = {}
        self.html_categories_leaves = {}
        self.html_blog_archives = {}
        self.cache_get_entry_attribute_by_id = {}
        self.cache_get_chapter_attribute_by_index = {}
        self.generation_timestamp = datetime.datetime.now()
        self.raw_chapters = {}
        self.chapters_index = []
        self.html_chapters = {}
        
        # Build JSON-LD doc if any
        if self.enable_jsonld or self.enable_jsonp:
            if "https://schema.org" in self.blog_configuration.keys():
                self.optionals_schemadotorg = self.blog_configuration["https://schema.org"]
                
            else:
                self.optionals_schemadotorg = {}
            
            self.entries_as_jsonld = {}
            self.archives_as_jsonld = {}
            self.categories_as_jsonld = {}
            self.root_site_to_jsonld()
            
        # Build entries
        filenames = [filename for filename in yield_entries_content()]
        self.chunks_len = (len(filenames)//self.workers_count)+1

        if self.workers_count > 1:
            # There we setup chunks of entries send to workers throught dispatchers
            global thread_params
            thread_params = {
                "chunked_filenames" :[],
                "workers_count" : self.workers_count,
                "entries": self.entries,
                "paths": self.blog_configuration["path"],
                "encoding": self.path_encoding,
                "cut_threads_kill_workers" : False,
            }
            for i in range(0, self.workers_count):
                thread_params["chunked_filenames"].append(filenames[:self.chunks_len])
                filenames = filenames[self.chunks_len:]
            filenames = None
            
            from venc2.parallelism import Parallelism
            from venc2.parallelism.buid_entries import dispatcher
            from venc2.parallelism.buid_entries import finish
            from venc2.parallelism.buid_entries import worker
            
            parallelism = Parallelism(
                worker,
                finish,
                dispatcher,
                self.workers_count,
                self.blog_configuration["pipe_flow"]
            )
            parallelism.start()
            parallelism.join()
            if thread_params["cut_threads_kill_workers"]:
                exit(-1)
                
        else:
            for filename in filenames:
                self.entries.append(Entry(
                    filename,
                    self.blog_configuration["path"],
                    self.path_encoding
                ))

        self.entries = sorted(self.entries, key = lambda entry : self.sort(entry))
        for i in range(0, len(self.entries)):
            self.entries[i].index = i

        path_categories_sub_folders = self.blog_configuration["path"]["categories_sub_folders"]+'/'
        path_archives_directory_name = self.blog_configuration["path"]["archives_directory_name"]
        
        # Once entries are loaded, build datastore
        jsonld_callback = self.entry_to_jsonld_callback if (self.enable_jsonld or self.enable_jsonp) else None
        for entry_index in range(0, len(self.entries)):
            current_entry = self.entries[entry_index]
            if jsonld_callback != None:
                jsonld_callback(current_entry)

            # Update entriesPerDates
            if path_archives_directory_name != '':
                formatted_date = current_entry.formatted_date
                entries_index = self.get_entries_index_for_given_date(formatted_date)
                if entries_index != None:
                    self.entries_per_archives[entries_index].count +=1
                    self.entries_per_archives[entries_index].related_to.append(entry_index)

                else:
                    self.entries_per_archives.append(MetadataNode(formatted_date, entry_index))

            # Update entriesPerCategories
            try:
                if self.path_encoding == '':
                    sub_folders = quirk_encoding(unidecode.unidecode(path_categories_sub_folders))
                else:
                    sub_folders = urllib_parse_quote(path_categories_sub_folders, encoding=self.path_encoding)

            except UnicodeEncodeError as e:
                notify("\"{0}\": ".format(path_categories_sub_folders)+str(e), color="YELLOW")
            
            sub_folders = sub_folders if sub_folders != '/' else ''
            
            # TODO : should not be done unless it's necessary
            build_categories_tree(entry_index, current_entry.raw_categories, self.entries_per_categories, self.categories_leaves, self.max_category_weight, self.set_max_category_weight, encoding=self.path_encoding, sub_folders=sub_folders)
                    
        # Setup BlogArchives Data
        self.blog_archives = list()
        
        path_archives_sub_folders = self.blog_configuration["path"]["archives_sub_folders"]+'/'
        for node in self.entries_per_archives:
            try:
                if self.path_encoding == '':
                    sub_folders = quirk_encoding(unidecode.unidecode(path_archives_sub_folders))
                else:
                    sub_folders = urllib_parse_quote(path_archives_sub_folders, encoding=self.path_encoding)

            except UnicodeEncodeError as e:
                notify("\"{0}\": ".format(path_archives_sub_folders)+str(e), color="YELLOW")

            sub_folders = sub_folders if sub_folders != '/' else ''

            self.blog_archives.append({
                "value":node.value,
                "path": "\x1a"+sub_folders+node.value,
                "count": node.count,
                "weight": node.weight
            })
            
    def build_chapter_indexes(self):
        # build chapters index
        path_chapters_sub_folders = self.blog_configuration["path"]["chapters_sub_folders"]
        path_chapter_folder_name = self.blog_configuration["path"]["chapter_directory_name"]
        
        #TODO: Might be not safe, must test level if is actually an int. Test as well the whole sequence.
        for chapter in sorted(self.raw_chapters.keys(), key = lambda x : int(x.replace('.', ''))):
            top = self.chapters_index
            index = ''
            levels = [str(level) for level in chapter.split('.') if level != '']
            len_levels = len(levels)
                    
            for i in range(0, len_levels):
                l = levels[i]
                if index == '':
                    index = l

                else:
                    index += '.'+l

                f = filter(lambda c : c.index == index, top)
                try:
                    top = next(f).sub_chapters
                
                except StopIteration:
                    if index in self.raw_chapters.keys():
                        # TODO: Replace this shitty bloc by a function call building path
                        entry = self.raw_chapters[index]
                        try:
                            path = "\x1a"+((path_chapters_sub_folders+'/' if path_chapters_sub_folders != '' else '')+path_chapter_folder_name).format(**{
                                "chapter_name" : entry.title,
                                "chapter_index" : index
                            })
                            try:
                                if self.path_encoding == '':
                                    path = quirk_encoding(unidecode.unidecode(path))
                                    
                                else:
                                    path = urllib_parse_quote(path, encoding=self.path_encoding)
                                    
                            except UnicodeEncodeError as e:
                                notify("\"{0}\": ".format(path_chapters_sub_folders)+str(e), color="YELLOW")
                            
                        except KeyError as e:
                            from venc2.helpers import die
                            die(messages.variable_error_in_filename.format(e))
                            
                        top.append(
                            Chapter(index, self.raw_chapters[index], path)
                        )
                        entry.chapter = top[-1]
                        
                    else:
                        top.append(
                            Chapter(index, None, '')
                        )
                        top = top[-1].sub_chapters
    
    def build_entry_html_toc(self, entry, open_ul, open_li, content_format, close_li, close_ul):
        output = ""
        for i in range(0, len(entry.toc)):
            current = entry.toc[i]
            if i == 0 or current[0] > entry.toc[i-1][0]:
                output += open_ul
            
            output += open_li
            output += (content_format).format(**{
                "level": current[0],
                "text": current[1],
                "id":current[2]
            })
            
            if i <= len(entry.toc)-2 and current[0] >= entry.toc[i+1][0]:
                output += close_li
            
            if i <= len(entry.toc)-2 and current[0] > entry.toc[i+1][0]:
                output += close_ul
        
        return output
            
    def if_categories(self, if_true, if_false=''):
        if self.entries_per_categories != [] and not self.blog_configuration["disable_categories"]:
            return if_true
            
        else:
            return if_false
    
    def if_chapters(self, if_true, if_false=''):
        if self.chapters_index != [] and not self.blog_configuration["disable_chapters"]:
            return if_true
            
        else:
            return if_false
    
    def if_feeds_enabled(self, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"] and self.blog_configuration["disable_rss_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")
            
        else: 
            return if_true.replace("{relative_origin}", "\x1a")
        
    def if_atom_enabled(self, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")

        else: 
            return if_true.replace("{relative_origin}", "\x1a")

    def if_metadata_is_true(self, key, if_true, if_false, source):            
        try:
            if type(source) == Entry and getattr(source, key):
                return if_true.strip()

            elif source[key]:
                return if_true.strip()
        
        except:
            pass
        
        return if_false.strip()
          
    def if_blog_metadata_is_true(self, key, if_true, if_false=''):
        return self.if_metadata_is_true(key, if_true, if_false, self.blog_configuration)

    def if_entry_metadata_is_true(self, key, if_true, if_false=''):
        return self.if_metadata_is_true(key, if_true, if_false, self.requested_entry)
                
    def if_rss_enabled(self, if_true, if_false=''):
        if self.blog_configuration["disable_rss_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")
            
        else:
            return if_true.replace("{relative_origin}", "\x1a")

    def if_infinite_scroll_enabled(self, if_true, if_false=''):            
        try:
            if self.blog_configuration["disable_infinite_scroll"]:
                return if_false
                                    
            else:
                return if_true
                    
        except KeyError:
            return if_true
                    

    def root_site_to_jsonld(self):
        self.root_as_jsonld = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "@id" : self.blog_configuration["blog_url"]+"/root.jsonld",
            "name": self.blog_configuration["blog_name"],
            "url": self.blog_configuration["blog_url"],
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : {
                "@type": "CreativeWork",
                "name": self.blog_configuration["license"]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }

    def categories_to_jsonld(self, category_value, leaf_name):
        blog_url = self.blog_configuration["blog_url"]
        blog_name = self.blog_configuration["blog_name"]
        self.categories_as_jsonld[category_value] = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "@id" : blog_url+'/'+category_value+"/categories.jsonld",
            "url": blog_url+'/'+category_value,
            "name": blog_name + ' | ' + leaf_name,
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : self.root_as_jsonld["license"],
            "breadcrumb" : {
                "@type": "BreadcrumbList",
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"/root.jsonld",
                        "url": blog_url,
                        "name": blog_name
                    }
                }]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }
                
    def archives_to_jsonld(self, archive_value):
        blog_url = self.blog_configuration["blog_url"]
        blog_name = self.blog_configuration["blog_name"]
        
        self.archives_as_jsonld[archive_value] = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "name": blog_name + ' | ' + archive_value,
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : self.root_as_jsonld["license"],
            "breadcrumb" : {
                "@type": "BreadcrumbList",
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"/root.jsonld",
                        "url": blog_url,
                        "name": blog_name
                    }
                }]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }
        
    def entry_to_jsonld_callback(self, entry):
        if hasattr(entry, "schemadotorg"):
            optionals = entry.schemadotorg
                
        else:
            optionals = {}
        
        authors = [{"name":author, "@type": "Person"} for author in entry.authors]
        if "publisher" in entry.schemadotorg.keys():
            publisher = entry.schemadotorg["publisher"]
            
        elif "publisher" in self.blog_configuration["https://schema.org"].keys():
            publisher = self.blog_configuration["https://schema.org"]["publisher"]
        
        elif authors != []:
            publisher = authors
        
        else:
            publisher = {
                "@type":"Person",
                "name":self.blog_configuration["author_name"]
            }
        blog_url = self.blog_configuration["blog_url"]
        entry_url = '/'.join(entry.url.split('/')[:-1]).replace("\x1a", self.blog_configuration["blog_url"]+'/')
        filename = "entry"+str(entry.id)+".jsonld"
        doc = {
            "@context": "http://schema.org",
            "@type" : ["BlogPosting", "WebPage"],
            "@id" : entry_url+'/'+filename,
            "keywords" : ','.join(list(set( [keyword.strip() for keyword in (entry.raw_metadata["tags"]+", "+entry.raw_metadata["categories"]).split(',')] ))),
            "headline" : entry.title,
            "name" : entry.title,
            "datePublished" : entry.date.isoformat(),
            "inLanguage" : self.blog_configuration["blog_language"],
            "author" : authors if authors != [] else self.blog_configuration["author_name"],
            "publisher" : publisher,
            "url" : entry.url.replace("\x1a", self.blog_configuration["blog_url"]+"/"),
            "breadcrumb" : {
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"/root.jsonld",
                        "url": blog_url,
                        "name": self.blog_configuration["blog_name"]
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": blog_url+entry.sub_folder+filename,
                        "url": entry_url,
                        "name": entry.title
                    }
                }]
            },
            "relatedLink" : [ c["path"] for c in entry.categories_leaves],
            **optionals
        }
        self.entries_as_jsonld[entry.id] = doc
        # TODO 2.x.x : TRY AVOID DEREFERENCE HERE
        
        blog_post = {
            "@type": doc["@type"],
            "@id": doc["@id"],
            "headline":entry.title,
            "author": doc["author"],
            "publisher": doc["publisher"],
            "datePublished": doc["datePublished"],
            "keywords": doc["keywords"],
            "url": doc["url"]
        }
        self.root_as_jsonld["blogPost"].append(blog_post)
        
        # Setup archives as jsonld if any
        entry_formatted_date = entry.formatted_date
        if entry_formatted_date not in self.archives_as_jsonld.keys():
            self.archives_to_jsonld(entry_formatted_date)            
        self.archives_as_jsonld[entry.formatted_date]["blogPost"].append(blog_post)

        # Setup categories as jsonld if any
        for category in entry.categories_leaves:
            complete_path = category["path"].replace('\x1a','')
            path = ''
            for sub_path in complete_path.split('/')[:-1]:
                path += sub_path+'/'
                if path not in self.categories_as_jsonld.keys():
                    self.categories_to_jsonld(path, sub_path)
                
                self.categories_as_jsonld[path]["blogPost"].append(blog_post)
            
    def get_chapters(self, lo, io, ic, lc):
        key = lo+io+ic+lc
        if not key in self.html_chapters.keys():
            self.html_chapters[key] = self.build_html_chapters(lo, io, ic, lc, self.chapters_index, 0)

        return self.html_chapters[key]

    def get_entry_toc(self, open_ul, open_li, content, close_li, close_ul):
        key = open_ul+open_li+content+close_li+close_ul
        if not key in self.html_entry_tocs.keys():
            self.html_entry_tocs[key] = self.build_entry_html_toc(self.requested_entry, open_ul, open_li, content_format, close_li, close_ul)
        return self.html_entry_tocs[key]
        
    #TODO : Raise MissingArgs if... missing args.
    def build_html_chapters(self, lo, io, ic, lc, top, level):          
        if top == []:
            return ''
            
        path_encoding = self.path_encoding
        output = lo.format(**{"level" :level})

        for sub_chapter in top:
            output += io.format(**{
                "index": sub_chapter.index,
                "title": self.entries[sub_chapter.entry_index].title,
                "path":  sub_chapter.path,
                "level": level
            })
            output += self.build_html_chapters(argv, sub_chapter.sub_chapters, level+1)
            output += ic
        output += lc

        return output

    def update_chapters(self, entry):
        try:
            chapter = str(entry.chapter)
            [ int(level) for level in chapter.split('.') if level != '']

        except ValueError as e: # weak test to check attribute conformity
            return

        except AttributeError as e: # does entry has chapter?
            return

        if chapter in self.raw_chapters.keys():
            from venc2.helpers import die
            die(messages.chapter_already_exists.format(
                entry.title,
                entry.id,
                self.raw_chapters[chapter].title,
                self.raw_chapters[chapter].id,
                chapter
            ))
        else:
            self.raw_chapters[chapter] = entry

    def sort(self, entry):
        try:
            value = str(getattr(entry, self.sort_by))
            if self.sort_by == 'id':
                return int(value)
                
            return value

        except AttributeError:
            return ''

    def set_max_category_weight(self, value):
        self.max_category_weight = value
        return value

    def get_generation_timestamp(self, time_format):
            return datetime.datetime.strftime(self.generation_timestamp, time_format)
            
    def get_blog_metadata(self, field_name):
        # if exception is raised it will be automatically be catch by processor.
        try:
            return str(self.blog_configuration[field_name])
            
        except KeyError:
            raise VenCException(
                messages.blog_has_no_metadata_like.format(field_name)
            )
            
    def get_blog_metadata_if_exists(self, field_name, if_true='', if_false='', ok_if_null=True):
        try:
            value = self.blog_configuration[field_name]
            
        except KeyError:
            return if_false
        
        if len(if_true)
             if ok_if_null or len(value):
                  return if_true.format(**{"value" : value,"{relative_origin}":"\x1a"})
                  
              else:
                  return if_false
        else:
            return value

    def get_blog_metadata_if_not_null(self, field_name, if_true='', if_false='', ):
        return self.get_blog_metadata_if_exists(field_name, if_true, if_false, ok_if_null=False)

    def get_entry_metadata(self, metadata_name):
        # if exception is raised it will be automatically be catch by processor.
        try:
            return str(getattr(self.requested_entry, metadata_name))
            
        except AttributeError:
            raise VenCException(
                messages.entry_has_no_metadata_like.format(argv[0]),
                self.requested_entry
            )
            
    def get_entry_metadata_if_exists(self, argv, ok_if_null=True):
        try:
            value = str(getattr(self.requested_entry, argv[0]))

        except AttributeError:
            if len(argv) >= 3:
                return argv[2]
                
            else:
                return str()
            
        try:
            if len(value) or ok_if_null:
                return argv[1].format(**{"value" : value, "relative_origin": "\x1a"})
            
            elif len(argv) >= 3:
                return argv[2]
                
            else:
                return ""
                
        except IndexError:
            return value
            
    def get_entry_metadata_if_not_null(self, argv):
        return self.get_entry_metadata_if_exists(argv, ok_if_null=False)
        
    def get_entries_index_for_given_date(self, value):
        index = 0
        for metadata in self.entries_per_archives:
            if value == metadata.value:
                return index
            index += 1

    def get_entries_for_given_date(self, value, reverse):
        index = 0
        for metadata in self.entries_per_archives:
            if value == metadata.value:
                break
            index += 1

        for entry in (self.entries_per_archives[index].related_to[::-1] if reverse else self.entries_per_archives[index].related_to):
            yield self.entries[entry]
            
    def get_entries(self, reverse=False):
        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry
    
    def get_entry_title(self):
        return self.requested_entry.title
    
    def get_entry_id(self):
        return self.requested_entry.id
            
    def get_entry_year(self):
        return self.requested_entry.date.year

    def get_entry_month(self):
        return self.requested_entry.date.month
        
    def get_entry_day(self):
        return self.requested_entry.date.day

    def get_entry_hour(self):
        return self.requested_entry.date.hour
    
    def get_entry_minute(self):
        return self.requested_entry.date.minute

    def get_entry_date(self, date_format=''):
        return self.requested_entry.date.strftime(
            date_format if len(date_format) else self.blog_configuration["date_format"]
        )

    def get_entry_date_url(self):
        return self.requested_entry.date.strftime(
            self.blog_configuration["path"]["archives_directory_name"]
        )
    
    def get_chapter_attribute_by_index(self, argv=list()):
        if self.blog_configuration["disable_chapters"]:
            return ""
            
        if len(argv) < 2:
            raise PatternMissingArguments(2, len(argv))
        
        key = ''.join(argv[:2])
        if not key in self.cache_get_chapter_attribute_by_index.keys():
            try:
                self.cache_get_chapter_attribute_by_index[key] = getattr(self.raw_chapters[argv[1]].chapter, argv[0])
                
            except KeyError as e:
                print(e, self.cache_get_chapter_attribute_by_index, self.raw_chapters)

                raise PatternInvalidArgument(
                    "index",
                    argv[1],
                    messages.there_is_no_chapter_with_index.format(argv[1])
                )
                
            except AttributeError as e:
                raise PatternInvalidArgument(
                    "attribute",
                    argv[0],
                    messages.chapter_has_no_attribute_like.format(argv[0])
                )
                
        return self.cache_get_chapter_attribute_by_index[key]


    def get_entry_attribute_by_id(self, argv=list()):
        if len(argv) < 2:
            raise PatternMissingArguments(2, len(argv))
            
        key = ''.join(argv[:2])
        if not key in self.cache_get_entry_attribute_by_id.keys():
            try:
                entry = [entry for entry in self.entries if entry.id == int(argv[1])][0]
                self.cache_get_entry_attribute_by_id[key] = getattr(entry, argv[0])
            
            except ValueError:
                raise PatternInvalidArgument(
                    "id",
                    argv[1],
                    messages.id_must_be_an_integer
                )
                
            except AttributeError as e:
                raise PatternInvalidArgument(
                    "attribute",
                    argv[0],
                    messages.entry_has_no_metadata_like.format(argv[0])
                )

            except IndexError:
                raise PatternInvalidArgument(
                    "id",
                    argv[1],
                    messages.cannot_retrieve_entry_attribute_because_wrong_id
                )
            
        return self.cache_get_entry_attribute_by_id[key]
            
    def get_entry_url(self, argv=list()):
        if self.blog_configuration["disable_single_entries"]:
            return ''

        return self.requested_entry.url

    def get_author_name(self, argv=list()):
        return self.blog_configuration["author_name"]

    def get_blog_name(self, argv=list()):
        return self.blog_configuration["blog_name"]
        
    def get_blog_description(self, argv=list()):
        return self.blog_configuration["blog_description"]
        
    def get_blog_keywords(self, argv=list()):
        return self.blog_configuration["blog_keywords"]

    def get_author_description(self, argv=list()):
        return self.blog_configuration["author_description"]
        
    def get_blog_license(self, argv=list()):
        return self.blog_configuration["license"]
    
    def get_blog_url(self, argv=list()):
        return self.blog_configuration["blog_url"]
    
    def get_blog_language(self, argv=list()):
        return self.blog_configuration["blog_language"]
    
    def get_author_email(self, argv=list()):
        return self.blog_configuration["author_email"]

    def for_blog_archives(self, argv):
        key = ''.join(argv)
        if not key in self.html_blog_archives.keys():
            if self.blog_configuration["disable_archives"]:
                self.html_blog_archives[key] = ''

            else:
                archives = [o for o in self.blog_archives if o["value"] not in self.disable_threads]
                self.html_blog_archives[key] = merge(archives, argv)

        return self.html_blog_archives[key]

    def get_root_page(self, argv):
        if self.root_page == None:
            self.root_page =  "\x1a"+self.blog_configuration["path"]["index_file_name"].format(**{"page_number":''})
            
        return self.root_page

    def build_html_categories_tree(self, opening_node, opening_branch, closing_branch, closing_node, tree):
        output_string = opening_node
        for node in sorted(tree, key = lambda x : x.value):
            if node.value in self.disable_threads:
                continue

            variables = {
                "value" : node.value,
                "count" : node.count,
                "weight" : round(node.weight / self.max_category_weight,2),
                "path" : node.path
            }

            if len(node.childs) == 0:
                output_string += opening_branch.format(**variables) + closing_branch.format(**variables)

            else:
                output_string += opening_branch.format(**variables) + self.build_html_categories_tree(
                    opening_node,
                    opening_branch,
                    closing_branch,
                    closing_node,
                    node.childs
                ) + closing_branch.format(**variables)

        if output_string == opening_node+closing_node:
            return ""

        return output_string + closing_node

    def tree_for_entry_categories(self, argv):
        key = ''.join(argv)
        entry = self.requested_entry

        if not key in self.requested_entry.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                entry.html_categories_tree[key] = ''

            else:
                entry.html_categories_tree[key] = self.build_html_categories_tree(
                    argv[0], #opening_node
                    argv[1], #opening_branch
                    argv[2], #closing_branch
                    argv[3], #closing_node
                    entry.categories_tree
                )
        
        return entry.html_categories_tree[key]

    def tree_for_blog_categories(self, argv):
        key = ''.join(argv)
        # compute once categories tree and deliver baked html
        if not key in self.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                self.html_categories_tree[key] = ''

            else:
                self.html_categories_tree[key] = self.build_html_categories_tree(
                    argv[0], #opening_node
                    argv[1], #opening_branch
                    argv[2], #closing_branch
                    argv[3], #closing_node
                    self.entries_per_categories
                )

        return self.html_categories_tree[key]

    # TODO: NOT FINISHED YET
    def for_entry_range(self, argv):
        return ""     # BECAUSE TODO
        if len(argv) != 3:
            raise PatternMissingArguments(expected=2,got=len(argv))
            
        try:
            start_from= int(argv[0])
            
        except TypeError:
            raise GenericMessage(
                messages.wrong_pattern_argument.format("start_from", argv[0])+' '+
                messages.pattern_argument_must_be_integer
            )
        
        try:
            end_from= int(argv[1])
            
        except TypeError:
            raise GenericMessage(
                messages.wrong_pattern_argument.format("end_to", argv[0])+' '+
                messages.pattern_argument_must_be_integer
            )
            
        if end_from <= start_from:
            raise GenericMessage(messages.invalid_range.format(start_from, end_to))
        
        entry = self.requested_entry
        
        output = ""
        #TODO: PREVENT CRASH IN CASE OF WRONG INPUTS
        for i in range(start_from, end_from):
            output += argv[2].replace("[index]}", '['+str(i)+']}').format(**entry.raw_metadata)
        
        return output
    
    def for_entry_metadata(self, variable_name, string, separator=' '):        
        entry = self.requested_entry
        key = variable_name+string+separator
            
        if not key in entry.html_for_metadata:
            try:
                l = getattr(entry, variable_name)
                if type(l) == dict:
                    raise VenCException(messages.entry_metadata_is_not_a_list.format(variable_name, entry))
                    
                elif type(l) == str:
                    l = l.split(",")
                
            except AttributeError as e:
                raise VenCException(messages.entry_has_no_metadata_like.format(variable_name), entry)
                
            try:
                entry.html_for_metadata[key] = separator.join([
                     string.format(**{"value": item.strip()}) for item in l
                ])
                
            except KeyError as e:
                raise VenCException(messages.unknown_contextual.format(e), entry)
            
        return entry.html_for_metadata[key]
            
    def for_entry_authors(self, string, separator=' '):
        return self.for_entry_metadata("authors", string, separator)

    def for_entry_tags(self, string, separator=' '):
        return self.for_entry_metadata("tags", string, separator)

    # TODO in 2.x.x: Access {count} and {weight} from LeavesForEntrycategories by taking benefit of preprocessing.
    def leaves_for_entry_categories(self, argv):
        key = ''.join(argv)
        entry = self.requested_entry
        if not key in entry.html_categories_leaves.keys():
            if self.blog_configuration["disable_categories"]:
                entry.html_categories_leaves[key] = ''

            else:
                entry.html_categories_leaves[key] = merge(entry.categories_leaves, argv)
        
        return entry.html_categories_leaves[key]

    def leaves_for_blog_categories(self, argv):
        key = ''.join(argv)

        if not key in self.html_categories_leaves.keys():
            if self.blog_configuration["disable_categories"]:
                self.html_categories_leaves[key] = ''

            else:
                items = []
                for node in self.categories_leaves:
                    items.append({
                        "value" : node.value,
                        "count" : node.count,
                        "weight" : round(node.weight / self.max_category_weight,2),
                        "path" : node.path
                    })
    
                self.html_categories_leaves[key] = merge(items, argv)
        
        return self.html_categories_leaves[key]
        
    def cache_embed_exists(self, link):
        cache_filename = hashlib.md5(link.encode('utf-8')).hexdigest()
        try:
            return open("caches/embed/"+cache_filename,"r").read()

        except FileNotFoundError:
            return ""

    def wrapper_embed_content(self, argv):
        if len(argv) == 0:
            raise PatternMissingArguments
            
        cache = self.cache_embed_exists(argv[0])
        if cache != "":
            return cache

        else:
            if self.embed_providers == dict():
                f = open(os.path.expanduser("~")+"/.local/share/VenC/embed_providers/oembed.json")
                self.embed_providers["oembed"] = {}
                j = json.load(f)
                for p in j:
                    self.embed_providers["oembed"][p["provider_url"]] = []
                    for e in p["endpoints"]:
                        self.embed_providers["oembed"][p["provider_url"]].append(e["url"])

        return get_embed_content(self.embed_providers, argv)
