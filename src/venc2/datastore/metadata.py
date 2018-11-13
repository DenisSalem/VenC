#! /usr/bin/python3

#   Copyright 2016, 2018 Denis Salem

#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import urllib.parse

class MetadataNode:
    def __init__(self, value, entry_index):
        self.count = 1
        self.weight = 1 # computed later
        self.path = str()
        self.value = value
        self.related_to = [entry_index]
        self.childs = list()

def build_categories_tree(entry_index, input_list, output_tree, output_leaves, max_weight, set_max_weight=None, encoding="utf-8"):
    for category in input_list:
        branch = category.split(' > ')
        if not len(branch):
            continue

        leave = branch[-1]
        path = ""
        root = output_tree
        for node_name in branch:
            if node_name == '':
                continue

            path += node_name+'/'

            if not node_name in [metadata.value for metadata in root]:
                root.append(MetadataNode(node_name, entry_index))
                if output_leaves != None and node_name == leave:
                    output_leaves.append(root[-1])

                root[-1].path = ".:GetRelativeOrigin:."+urllib.parse.quote(path, encoding=encoding)
                root = root[-1].childs

            else:
                for node in root:
                    if node.value == node_name:
                        node.count +=1
                        if set_max_weight != None and node.count > max_weight:
                            max_weight = set_max_weight(node.count)

                        node.related_to.append(entry_index)
                        root = node.childs
