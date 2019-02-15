#! /usr/bin/python

#    Copyright 2016, 2018 Denis Salem
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

import hashlib
import os
import datetime
import urllib.parse

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.entry import yield_entries_content
from venc2.datastore.entry import Entry
from venc2.datastore.metadata import build_categories_tree
from venc2.datastore.metadata import MetadataNode
from venc2.datastore.metadata import Chapter
from venc2.prompt import notify
from venc2.l10n import messages
from venc2.patterns.non_contextual import get_embed_content
from venc2.patterns.exceptions import MalformedPatterns

def merge(iterable, argv):
    return argv[1].join([argv[0].format(**something) for something in iterable])

class DataStore:
    def __init__(self):
        notify("┌─ "+messages.loading_data)
        self.blog_configuration = get_blog_configuration()
        self.sort_by = self.blog_configuration["sort_by"]
        self.enable_jsonld = self.blog_configuration["enable_jsonld"]
        self.disable_threads = [thread_name.strip() for thread_name in self.blog_configuration["disable_threads"].split(',')]
        self.entries = list()
        self.entries_per_dates = list()
        self.entries_per_categories = list()
        self.requested_entry_index = 0
        self.max_category_weight = 1
        self.categories_leaves = []
        self.embed_providers = {}
        self.html_categories_tree = {}
        self.html_categories_leaves = {}
        self.html_blog_dates = {}
        self.generation_timestamp = datetime.datetime.now()
        self.raw_chapters = {}
        self.chapters_index = []
        self.html_chapters = {}
        
        # Build JSON-LD doc if any
        if self.enable_jsonld:
            self.entries_as_jsonld = {}
            self.root_site_to_jsonld()
            
        # Build entries
        try:
            jsonld_callback = self.entry_to_jsonld_callback if self.enable_jsonld else None
            for filename in yield_entries_content():
                self.entries.append(Entry(filename, self.blog_configuration["path"], jsonld_callback=jsonld_callback, encoding=self.blog_configuration["path_encoding"]))

        except MalformedPatterns as e:
            from venc2.helpers import handle_malformed_patterns
            handle_malformed_patterns(e)

        self.entries = sorted(self.entries, key = lambda entry : self.sort(entry))

        for entry_index in range(0, len(self.entries)):
            current_entry = self.entries[entry_index]
            if entry_index > 0:
                self.entries[entry_index-1].next_entry = current_entry
                current_entry.previous_entry = self.entries[entry_index-1]

            # Update entriesPerDates
            if self.blog_configuration["path"]["dates_directory_name"] != '':
                formatted_date = current_entry.date.strftime(self.blog_configuration["path"]["dates_directory_name"])
                entries_indexes = self.get_entries_index_for_given_date(formatted_date)
                if entries_indexes != None:
                    self.entries_per_dates[entries_indexes].count +=1
                    self.entries_per_dates[entries_indexes].related_to.append(entry_index)

                else:
                    self.entries_per_dates.append(MetadataNode(formatted_date, entry_index))

            # Update entriesPerCategories
            try:
                sub_folders = urllib.parse.quote(self.blog_configuration["path"]["categories_sub_folders"]+'/', encoding=self.blog_configuration["path_encoding"])

            except UnicodeEncodeError as e:
                sub_folders = self.blog_configuration["path"]["categories_sub_folders"]+'/'
                notify("\"{0}\": ".format(sub_folders)+str(e), color="YELLOW")
            
            sub_folders = sub_folders if sub_folders != '/' else ''
            build_categories_tree(entry_index, current_entry.raw_categories, self.entries_per_categories, self.categories_leaves, self.max_category_weight, self.set_max_category_weight, encoding=self.blog_configuration["path_encoding"], sub_folders=sub_folders)
            self.update_chapters(current_entry)
    
        # build chapters index
        for chapter in sorted(self.raw_chapters.keys()):
            top = self.chapters_index
            index = ''
            levels = [str(level) for level in chapter.split('.') if str(level) != '']
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
                    try:
                        top.append(
                            Chapter(index, self.raw_chapters[index][1], self.raw_chapters[index][2])
                        )
                    except KeyError:
                        top.append(
                            Chapter(index, '', '')
                        )
                        top = top[-1].sub_chapters


        # Setup BlogDates Data
        self.blog_dates = list()
        for node in self.entries_per_dates:
            try:
                sub_folders = urllib.parse.quote(self.blog_configuration["path"]["dates_sub_folders"]+'/', encoding=self.blog_configuration["path_encoding"])

            except UnicodeEncodeError as e:
                sub_folders = self.blog_configuration["path"]["dates_sub_folders"]+'/'
                notify("\"{0}\": ".format(sub_folders)+str(e), color="YELLOW")

            sub_folders = sub_folders if sub_folders != '/' else ''

            self.blog_dates.append({
                "value":node.value,
                "path": ".:GetRelativeOrigin:."+sub_folders+node.value,
                "count": node.count,
                "weight": node.weight
            })

    def root_site_to_jsonld(self):
        if "https://schema.org" in self.blog_configuration.keys():
            optionals = self.blog_configuration["https://schema.org"]
                
        else:
            optionals = {}

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
            **optionals
        }

    def entry_to_jsonld_callback(self, entry):
        if hasattr(entry, "schemadotorg"):
            optionals = entry.schemadotorg
                
        else:
            optionals = {}
        
        doc = {
            "@context": "http://schema.org",
            "@type" : ["BlogPosting", "WebPage"],
            "@id" : self.blog_configuration["blog_url"]+"/entry"+str(entry.id)+".jsonld",
            "keywords" : entry.raw_metadata["tags"],
            "headline" : entry.title,
            "name" : entry.title,
            "date" : entry.date.isoformat(),
            "inLanguage" : self.blog_configuration["blog_language"],
            "author" : [{"name":author["value"], "@type": "Person"} for author in entry.authors],
            "url" : entry.url.replace(".:GetRelativeOrigin:.", self.blog_configuration["blog_url"]+"/"),
            "breadcrumb" : {
                "itemListElement": [
                ]
            },
            "relatedLink" : [ c["path"] for c in entry.categories_leaves],
            **optionals
        }

        self.entries_as_jsonld[entry.id] = doc
        
    def get_chapters(self, argv):
        key = ''.join(argv)
        if not key in self.html_chapters.keys():
            self.html_chapters[key] = self.build_html_chapters(argv, self.chapters_index, 0)

        return self.html_chapters[key]

    def build_html_chapters(self, argv, top, level):
        lo, io, ic, lc = argv
        if top == []:
            return ''

        output = lo.format(**{"level" :level})
        for sub_chapters in top:
            output += io.format(**{
                "index": sub_chapters.index,
                "title": sub_chapters.title,
                "path": sub_chapters.path,
                "level": level
            })
            output += self.build_html_chapters(argv, sub_chapters.sub_chapters, level+1)
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
                self.raw_chapters[chapter][1],
                self.raw_chapters[chapter][0],
                chapter
            ))
        else:
            self.raw_chapters[chapter] = (entry.id, entry.title, entry.url)

    def sort(self, entry):
        try:
            return getattr(entry, self.sort_by)

        except AttributeError:
            return ''

    def set_max_category_weight(self, value):
        self.max_category_weight = value
        return value

    def get_generation_timestamp(self, argv):
        return datetime.datetime.strftime(self.generation_timestamp, argv[0])

    def get_blog_metadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return self.blog_configuration[argv[0]]
    
    def get_blog_metadata_if_exists(self, argv):
        try:
            return self.blog_configuration[argv[0]]
            
        except KeyError:
            return str()

    def get_entry_metadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return str( getattr(self.entries[self.requested_entry_index], argv[0]))
    
    def get_entry_metadata_if_exists(self, argv):
        try:
            return str( getattr(self.entries[self.requested_entry_index], argv[0]))

        except AttributeError:
            return str()

    def get_entries_index_for_given_date(self, value):
        index = 0
        for metadata in self.entries_per_dates:
            if value == metadata.value:
                return index
            index += 1

    def get_entries_for_given_date(self, value, reverse):
        index = 0
        for metadata in self.entries_per_dates:
            if value == metadata.value:
                break
            index += 1

        for entry in (self.entries_per_dates[index].related_to[::-1] if reverse else self.entries_per_dates[index].related_to):
            self.requested_entry_index = entry
            yield self.entries[entry]
            
    def get_entries(self, reverse=False):
        self.requested_entry_index = 0 if not reverse else len(self.entries) - 1

        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry

            if not reverse:
                self.requested_entry_index += 1

            else:
                self.requested_entry_index -= 1
    
    def get_entry_title(self, argv=list()):
        title = self.entries[self.requested_entry_index].title
        return title if title != None else str()
    
    def get_entry_id(self, argv=list()):
        return self.entries[self.requested_entry_index].id

    def get_entry_year(self, argv=list()):
        return self.entries[self.requested_entry_index].date.year

    def get_entry_month(self, argv=list()):
        return self.entries[self.requested_entry_index].date.month
        
    def get_entry_day(self, argv=list()):
        return self.entries[self.requested_entry_index].date.day

    def get_entry_hour(self, argv=list()):
        return self.entries[self.requested_entry_index].date.hour
    
    def get_entry_minute(self, argv=list()):
        return self.entries[self.requested_entry_index].date.minute

    def get_entry_date(self, argv=list()):
        return self.entries[self.requested_entry_index].date.strftime(self.blog_configuration["date_format"])

    def get_entry_date_url(self, argv=list()):
        return self.entries[self.requested_entry_index].date.strftime(self.blog_configuration["path"]["dates_directory_name"])

    def get_entry_url(self, argv=list()):
        if self.blog_configuration["disable_single_entries"]:
            return ''

        return self.entries[self.requested_entry_index].url

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

    def for_blog_dates(self, argv):
        key = ''.join(argv)
        if not key in self.html_blog_dates.keys():
            if self.blog_configuration["disable_archives"]:
                self.html_blog_dates[key] = ''

            else:
                dates = [o for o in self.blog_dates if o["value"] not in self.disable_threads]
                self.html_blog_dates[key] = merge(dates, argv)

        return self.html_blog_dates[key]

    def get_root_page(self, argv):
        return ".:GetRelativeOrigin:."+self.blog_configuration["path"]["index_file_name"].format(**{"page_number":''})

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
        if not key in self.entries[self.requested_entry_index].html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                self.entries[self.requested_entry_index].html_categories_tree[key] = ''

            else:
                self.entries[self.requested_entry_index].html_categories_tree[key] = self.build_html_categories_tree(
                    argv[0], #opening_node
                    argv[1], #opening_branch
                    argv[2], #closing_branch
                    argv[3], #closing_node
                    self.entries[self.requested_entry_index].categories_tree
                )
        
        return self.entries[self.requested_entry_index].html_categories_tree[key]

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

    def for_entry_tags(self, argv):
        key = ''.join(argv)
        if not key in self.entries[self.requested_entry_index].html_tags.keys():
            self.entries[self.requested_entry_index].html_tags[key] = merge(self.entries[self.requested_entry_index].tags, argv)

        return self.entries[self.requested_entry_index].html_tags[key]
    
    def for_entry_authors(self, argv):
        key = ''.join(argv)
        if not key in self.entries[self.requested_entry_index].html_authors.keys():
            self.entries[self.requested_entry_index].html_authors[key] = merge(self.entries[self.requested_entry_index].authors, argv)

        return self.entries[self.requested_entry_index].html_authors[key]

    """ TODO in 2.x.x: Access {count} and {weight} from LeavesForEntrycategories by taking benefit of preprocessing. """
    def leaves_for_entry_categories(self, argv):
        key = ''.join(argv)
        if not key in self.entries[self.requested_entry_index].html_categories_leaves.keys():
            if self.blog_configuration["disable_categories"]:
                self.entries[self.requested_entry_index].html_categories_leaves[key] = ''

            else:
                self.entries[self.requested_entry_index].html_categories_leaves[key] = merge(self.entries[self.requested_entry_index].categories_leaves, argv)
        
        return self.entries[self.requested_entry_index].html_categories_leaves[key]

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
        cache = self.cache_embed_exists(argv[0])
        if cache != "":
            return cache

        else:
            if self.embed_providers == dict():
                f = open(os.path.expanduser("~")+"/.local/share/VenC/embed_providers/oembed.json")
                self.embed_providers["oembed"] = {}
                j =json.load(f)
                for p in j:
                    self.embed_providers["oembed"][p["provider_url"]] = []
                    for e in p["endpoints"]:
                        self.embed_providers["oembed"][p["provider_url"]].append(e["url"])

        return get_embed_content(self.embed_providers, argv)
