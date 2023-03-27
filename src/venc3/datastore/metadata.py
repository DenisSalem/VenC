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
