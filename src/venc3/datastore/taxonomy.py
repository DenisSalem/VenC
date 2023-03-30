#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
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

from venc3.datastore.metadata import MetadataNode
from venc3.datastore.metadata import WeightTracker
from venc3.helpers import quirk_encoding

def categories_to_keywords(branch):
    for item, sub_items in flatten_current_level(branch):
        if len(sub_items):
            for sub_item in catecories_to_keyword(sub_items):
                yield sub_item
        else:
            yield item
    
def flatten_current_level(items):
    for item in items:
        if type(item) == dict:
            for key in item.keys():
                if type(item[key]) != list:
                    # TODO : for end user it might be difficult to identify where it's gone wrong
                    from venc3.exceptions import VenCException
                    raise VenCException(("categories_parse_error", key))
                    
                yield key, item[key]
        else:
            yield item, []
            
def filter_categories(categories, entry_index):
    return [
            category for category in categories \
            if entry_index == None or (entry_index in category.related_to)
        ]
        
class Taxonomy:       
    def init_taxonomy(self):
        self.entries_per_categories = None
        self.categories_leaves = None
        self.categories_weight_tracker = WeightTracker()
        self.html_categories_tree = {}
        self.html_categories_leaves = {}
        
        if self.entries_per_categories == None:
            self.entries_per_categories = []
            self.categories_leaves = []
            path = self.blog_configuration["path"]["categories_sub_folders"]
            for entry_index in range(0, len(self.entries)):
                current_entry = self.entries[entry_index]
                self.build_tree(
                    entry_index,
                    current_entry.raw_categories,
                    self.entries_per_categories,
                    self.categories_leaves,
                    self.categories_weight_tracker,
                    sub_folders="\x1a"+path
                )
                
            self.categories_leaves = self.extract_leaves(None)
    
    def build_tree(self, entry_index, input_list, blog_output_tree, blog_output_leaves, weight_tracker, sub_folders=''):     
        from venc3.datastore.configuration import get_blog_configuration
        category_directory_name = get_blog_configuration()["path"]["category_directory_name"]
        for item, sub_items in flatten_current_level(input_list):
            if not len(item):
                continue
    
            match = None
            path = sub_folders+quirk_encoding(category_directory_name.format(**{"category":item}))
            for node in blog_output_tree:
                if node.value == item:
                    node.count +=1
                    node.weight_tracker.update()
                    node.related_to.append(entry_index)
                    match = node
                    break
    
            if match == None:
                metadata = MetadataNode(
                    item, 
                    entry_index,
                    quirk_encoding(path),
                    weight_tracker
                )
    
                blog_output_tree.append(metadata) 
                blog_output_leaves.append(metadata)
                
            if len(sub_items):
                self.build_tree(entry_index, sub_items, match.childs if match != None else metadata.childs, blog_output_leaves, weight_tracker, path)
            
    def extract_leaves(self, filter_by_entry_index, branch=None):
        if branch == None:
            branch = self.entries_per_categories
        
        output = [category for category in filter_categories(branch, filter_by_entry_index)]
        for category in filter_categories(branch, filter_by_entry_index):
            output += self.extract_leaves(filter_by_entry_index, category.childs)
        
        return output
