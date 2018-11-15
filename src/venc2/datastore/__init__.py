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
import json
import os
import urllib.parse

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.entry import yield_entries_content
from venc2.datastore.entry import Entry
from venc2.datastore.metadata import build_categories_tree
from venc2.datastore.metadata import MetadataNode
from venc2.patterns.non_contextual import embed_content

def merge(iterable, argv):
    return ''.join(
        [
            argv[0].format(**something) for something in iterable
        ]
    )

class DataStore:
    def __init__(self):
        self.blog_configuration = get_blog_configuration()
        self.disable_threads = [thread_name.strip() for thread_name in self.blog_configuration["disable_threads"].split(',')]
        self.entries = list()
        self.entries_per_dates = list()
        self.entries_per_categories = list()
        self.requested_entry_index = 0
        self.max_category_weight = 1
        self.categories_leaves = []
        self.embed_providers = {}
        self.html_categories_tree = None

        ''' Entry index is different from entry id '''
        entry_index = 0
        for filename in yield_entries_content():
            if len(self.entries):
                self.entries.append(Entry(filename, self.blog_configuration["path"], previous_entry = self.entries[-1], encoding=self.blog_configuration["path_encoding"]))
                self.entries[-2].next_entry = self.entries[-1]

            else:
                self.entries.append(Entry(filename, self.blog_configuration["path"], encoding=self.blog_configuration["path_encoding"]))
                
            ''' Update entriesPerDates '''
            if self.blog_configuration["path"]["dates_directory_name"] != '':
                formatted_date = self.entries[-1].date.strftime(self.blog_configuration["path"]["dates_directory_name"])
                entries_index = self.get_entries_index_for_given_date(formatted_date)
                if entries_index != None:
                    self.entries_per_dates[entries_index].count +=1
                    self.entries_per_dates[entries_index].related_to.append(entry_index)
                else:
                    self.entries_per_dates.append(MetadataNode(formatted_date, entry_index))


            ''' Update entriesPerCategories '''
            sub_folders = urllib.parse.quote(self.blog_configuration["path"]["categories_sub_folders"]+'/', encoding=self.blog_configuration["path_encoding"])
            sub_folders = sub_folders if sub_folders != '/' else ''
            build_categories_tree(entry_index, self.entries[-1].raw_categories, self.entries_per_categories, self.categories_leaves, self.max_category_weight, self.set_max_category_weight, encoding=self.blog_configuration["path_encoding"], sub_folders=sub_folders)
            entry_index += 1
    
        ''' Setup BlogDates Data '''
        self.blog_dates = list()
        for node in self.entries_per_dates:
            sub_folders = urllib.parse.quote(self.blog_configuration["path"]["dates_sub_folders"]+'/', encoding=self.blog_configuration["path_encoding"])
            sub_folders = sub_folders if sub_folders != '/' else ''

            self.blog_dates.append({
                "date":node.value,
                "dateUrl": ".:GetRelativeOrigin:."+sub_folders+node.value,
                "count": node.count,
                "weight": node.weight
            })

    def set_max_category_weight(self, value):
        self.max_category_weight = value
        return value

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
        sub_folders = self.blog_configuration["path"]["entries_sub_folders"].format(**{
            "entry_id" : self.entries[self.requested_entry_index].id,
            "entry_title" : self.entries[self.requested_entry_index].title
        })
        sub_folders = sub_folders+'/' if sub_folders != '' else ''
        filename = self.blog_configuration["path"]["entry_file_name"].format(**{
            "entry_id" : self.entries[self.requested_entry_index].id,
            "entry_title" : self.entries[self.requested_entry_index].title
        })
        return urllib.parse.quote(sub_folders+filename, encoding=self.blog_configuration["path_encoding"])

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
        dates = [o for o in self.blog_dates if o["date"] not in self.disable_threads]
        return merge(dates, argv)


    def build_html_categories_tree(self, opening_node, opening_branch, closing_branch, closing_node, tree):
        output_string = opening_node
        for node in sorted(tree, key = lambda x : x.value):
            if node.value in self.disable_threads:
                continue

            variables = {
                "item" : node.value,
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
        # compute once categories tree and deliver baked html
        if self.entries[self.requested_entry_index].html_categories_tree == None:
            self.entries[self.requested_entry_index].html_categories_tree = self.build_html_categories_tree(
                argv[0], #opening_node
                argv[1], #opening_branch
                argv[2], #closing_branch
                argv[3], #closing_node
                self.entries[self.requested_entry_index].categories_tree
            )
        
        return self.entries[self.requested_entry_index].html_categories_tree

    def tree_for_blog_categories(self, argv):
        # compute once categories tree and deliver baked html
        if self.html_categories_tree == None:
            self.html_categories_tree = self.build_html_categories_tree(
                argv[0], #opening_node
                argv[1], #opening_branch
                argv[2], #closing_branch
                argv[3], #closing_node
                self.entries_per_categories
            )

        return self.html_categories_tree

    def for_entry_tags(self, argv):
        return merge(self.entries[self.requested_entry_index].tags, argv)
    
    def for_entry_authors(self, argv):
        return merge(self.entries[self.requested_entry_index].authors, argv)

    """ TODO in 2.x.x: Access {count} and {weight} from LeavesForEntrycategories by taking benefit of preprocessing. """
    def leaves_for_entry_categories(self, argv):
        return merge(self.entries[self.requested_entry_index].categories_leaves, argv)

    def leaves_for_blog_categories(self, argv):
        items = []
        for node in self.categories_leaves:
            items.append({
                "item" : node.value,
                "count" : node.count,
                "weight" : round(node.weight / self.max_category_weight,2),
                "path" : node.path
            })
    
        return merge(items, argv)
        
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

        return embed_content(self.embed_providers, argv)
        
        
        

        
