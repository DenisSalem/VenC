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

from venc3.datastore.configuration import get_blog_configuration
from venc3.datastore.entry import yield_entries_content
from venc3.datastore.entry import Entry
from venc3.datastore.metadata import MetadataNode
from venc3.datastore.metadata import Chapter
from venc3.datastore.metadata import categories_to_keywords
from venc3.datastore.metadata import WeightTracker
from venc3.helpers import quirk_encoding
from venc3.prompt import notify
from venc3.l10n import messages
from venc3.exceptions import MalformedPatterns, VenCException
from venc3.patterns.non_contextual import get_embed_content
from venc3.patterns.datastore import DatastorePatterns
        
class DataStore(DatastorePatterns):
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
        self.entries_per_categories = None
        self.categories_leaves = None
        self.archives_weight_tracker = WeightTracker()
        self.categories_weight_tracker = WeightTracker()
        self.workers_count = 1

        try:
            from multiprocessing import cpu_count
            self.workers_count = cpu_count()
            if int(self.blog_configuration["parallel_processing"]) < self.workers_count:
                 self.workers_count  =  int(self.blog_configuration["parallel_processing"])
      
        except ImportError:
            pass
            
        except KeyError:
            pass
            
        except ValueError:
            pass

        self.requested_entry = None
            
        self.max_category_weight = 1
        self.embed_providers = {}
        self.html_categories_tree = {}
        self.html_categories_leaves = {}
        self.html_blog_archives = {}
        self.html_for_metadata = {}
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
        jsonld_required = self.blog_configuration["enable_jsonld"] or self.blog_configuration["enable_jsonp"]
        try:
            if self.workers_count > 1:
                # There we setup chunks of entries send to workers throught dispatchers
                global multiprocessing_thread_params
                multiprocessing_thread_params = {
                    "chunked_filenames" :[],
                    "workers_count" : self.workers_count,
                    "entries": self.entries,
                    "paths": self.blog_configuration["path"],
                    "encoding": self.path_encoding,
                    "jsonld_required" : jsonld_required,
                    "cut_threads_kill_workers" : False
                }
                for i in range(0, self.workers_count):
                    multiprocessing_thread_params["chunked_filenames"].append(filenames[:self.chunks_len])
                    filenames = filenames[self.chunks_len:]
                    
                filenames = None
                
                from venc3.parallelism import Parallelism
                from venc3.parallelism.build_entries import dispatcher
                from venc3.parallelism.build_entries import finish
                from venc3.parallelism.build_entries import worker
                
                parallelism = Parallelism(
                    worker,
                    finish,
                    dispatcher,
                    self.workers_count,
                    self.blog_configuration["pipe_flow"]
                )
                
                parallelism.start()
                parallelism.join()
                    
            else:
                for filename in filenames:
                    self.entries.append(Entry(
                        filename,
                        self.blog_configuration["path"],
                        jsonld_required,
                        self.path_encoding
                    ))
                    
        except VenCException as e:
            if self.workers_count > 1:
                parallelism.kill()
                
            e.die()

        self.entries = sorted(self.entries, key = lambda entry : self.sort(entry))
        for i in range(0, len(self.entries)):
            self.entries[i].index = i

        path_archives_directory_name = self.blog_configuration["path"]["archives_directory_name"]
        
        # Once entries are loaded, build datastore
        jsonld_callback = self.entry_to_jsonld_callback if (self.enable_jsonld or self.enable_jsonp) else None
        for entry_index in range(0, len(self.entries)):
            current_entry = self.entries[entry_index]
            if jsonld_callback != None:
                jsonld_callback(current_entry)

            # Update entriesPerDates
            # TODO could be done only if necessary
            if path_archives_directory_name != '':
                formatted_date = current_entry.formatted_date
                entries_index = self.get_entries_index_for_given_date(formatted_date)
                if entries_index != None:
                    self.entries_per_archives[entries_index].count +=1
                    self.entries_per_archives[entries_index].weight_tracker.update()
                    self.entries_per_archives[entries_index].related_to.append(entry_index)

                else:
                    self.entries_per_archives.append(MetadataNode(formatted_date, entry_index,weight_tracker=self.archives_weight_tracker))
                    
            # Update categories tree           
            if jsonld_required:
                if self.entries_per_categories == None:
                    self.entries_per_categories = []
                    self.categories_leaves = []
                self.setup_categories_tree_base_sub_folder()
                from venc3.datastore.metadata import build_categories_tree
                build_categories_tree(
                    entry_index,
                    current_entry.raw_categories,
                    self.entries_per_categories,
                    self.categories_leaves,
                    self.categories_weight_tracker,
                    encoding=self.path_encoding,
                    sub_folders=self.categories_tree_base_sub_folders
                )
                    
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
                "weight": round(node.count / node.weight_tracker.value,2)
            })
        
    def build_chapter_indexes(self):
        # build chapters index
        path_chapters_sub_folders = self.blog_configuration["path"]["chapters_sub_folders"]
        path_chapter_folder_name = self.blog_configuration["path"]["chapter_directory_name"]
        
        #TODO: IS not safe, must test level if is actually an int. Test as well the whole sequence.
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
                            from venc3.helpers import die
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

    # BROKEN
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
            "keywords" : ','.join(tuple(set( [keyword.strip() for keyword in entry.tags + tuple(categories_to_keywords(entry.raw_categories))] ))),
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
            "relatedLink" : [ c.path for c in entry.categories_leaves],
            **optionals
        }
        self.entries_as_jsonld[entry.id] = doc
        # TODO 3.x.x : TRY AVOID DEREFERENCE HERE
        
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

        # ~ # Setup categories as jsonld if any
        for category in entry.categories_leaves:
            complete_path = category.path.replace('\x1a','')
            path = ''
            for sub_path in complete_path.split('/')[:-1]:
                path += sub_path+'/'
                if path not in self.categories_as_jsonld.keys():
                    self.categories_to_jsonld(path, sub_path)
                
                self.categories_as_jsonld[path]["blogPost"].append(blog_post)
        
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
            output += self.build_html_chapters(lo, io, ic, lc, sub_chapter.sub_chapters, level+1)
            output += ic
        output += lc

        return output

    def update_chapters(self, entry):
        try:
            chapter = str(entry.chapter)
            [ int(level) for level in chapter.split('.') if level != '']

        except ValueError as e: # weak test to check attribute conformity
            notify(messages.chapter_has_a_wrong_index.format(entry.id, chapter), color="YELLOW")
            return

        except AttributeError as e: # does entry has chapter?
            return

        if chapter in self.raw_chapters.keys():
            from venc3.helpers import die
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

    def build_html_categories_tree(self, pattern, opening_node, opening_branch, closing_branch, closing_node, tree):
        output_string = opening_node
        for node in sorted(tree, key = lambda x : x.value):
            if node.value in self.disable_threads:
                continue

            variables = {
                "value" : node.value,
                "count" : node.count,
                "weight" : round(node.count / node.weight_tracker.value,2),
                "path" : node.path
            }

            if len(node.childs) == 0:
                output_string += opening_branch.format(**variables) + closing_branch.format(**variables)

            else:
                output_string += opening_branch.format(**variables) + self.build_html_categories_tree(
                    pattern,
                    opening_node,
                    opening_branch,
                    closing_branch,
                    closing_node,
                    node.childs
                ) + closing_branch.format(**variables)

        if output_string == opening_node+closing_node:
            return ""

        return output_string + closing_node
        
    def cache_embed_exists(self, link):
        cache_filename = hashlib.md5(link.encode('utf-8')).hexdigest()
        try:
            return open("caches/embed/"+cache_filename,"r").read()

        except FileNotFoundError:
            return ""

    def setup_categories_tree_base_sub_folder(self):
        path_categories_sub_folders = self.blog_configuration["path"]["categories_sub_folders"]+'/'
        try:
            if self.path_encoding == '':
                sub_folders = quirk_encoding(unidecode.unidecode(path_categories_sub_folders))
            else:
                sub_folders = urllib_parse_quote(path_categories_sub_folders, encoding=self.path_encoding)

        except UnicodeEncodeError as e:
            from venc3.exceptions import VenCException
            raise VenCException("ERREUR D'ENCODAGE DANS LE SOUS DOSSIER DES CATEGORIES")
                        
        self.categories_tree_base_sub_folders = sub_folders if sub_folders != '/' else ''

datastore = None
multiprocessing_thread_params = None

def init_datastore():
    global datastore
    datastore = DataStore()
    return datastore
