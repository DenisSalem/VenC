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

from unidecode import unidecode
from urllib.parse import quote

from venc3.exceptions import VenCException
from venc3.helpers import quirk_encoding

class Chapter:
    def __init__(self, index, entry, path):
        self.sub_chapters = []
        self.index = index
        self.entry_index = entry.index
        self.path = path
        
class MetadataNode:
    def __init__(self, value, entry_index, path="", weight_tracker = None):
        self.count = 1
        if weight_tracker != None:
            weight_tracker.update()
        self.weight_tracker = weight_tracker
        self.path = path
        self.value = value
        self.related_to = [entry_index]
        self.childs = list()

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

class WeightTracker:
    def __init__(self):
        self.value = 0
        
    def update(self):
        print(self, self.value)

def build_categories_tree(entry_index, input_list, output_branch, output_leaves, weight_tracker, sub_folders=''):        
    for item, sub_items in flatten_current_level(input_list):
        if not len(item):
            continue

        match = None
        path = sub_folders
        for node in output_branch:
            if node.value == item:
                node.count +=1
                node.weight_tracker.update()        
                node.related_to.append(entry_index)
                match = node
                break

        if match == None:
            # TODO : THIS IS WRONG, work only if path is set to {category}
            path += quirk_encoding(str(item)+'/')
            metadata = MetadataNode(
                item, 
                entry_index,
                quirk_encoding(path),
                weight_tracker
            )

            output_branch.append(metadata) 
            output_leaves.append(metadata)
            
        if len(sub_items):
            build_categories_tree(entry_index, sub_items, node.childs if match else metadata.childs, output_leaves, weight_tracker, sub_folders=path)
