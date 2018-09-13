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

class MetadataNode:
    def __init__(self, value, entry_index):
        self.count = 1
        self.weight = 1 # computed later
        self.path = str()
        self.value = value
        self.related_to = [entry_index]
        self.childs = list()

def get_metadata_by_name(keys, name):
    for key in keys:
        if key.value == name:
            return key
    return None

''' Need refactorisation '''
def get_dates_list(keys):
    output = list()
    max_weight = 0
    for key in keys:
        if max_weight < key.count:
            max_weight = key.count
        output.append({"date": key.value, "count":key.count,"dateUrl":key.value})

    for key in output:
        key["weight"] = str(int((key["count"]/max_weight)*10))

    return sorted(output, key = lambda date: datetime.datetime.strptime(date["date"], dates_directory_name))

def get_metadata_tree_max_weight(metadata, maxWeight=0):
    current_max_weight = max_weight
    for current in metadata:
        if current.count > current_max_weight:
            current_max_weight = current.count
        m = get_metadata_tree_max_weight(current.childs, max_weight=current_max_weight)
        if m > current_max_weight:
            current_max_weight = m

    return current_max_weight

def get_metadata_tree(metadata, root=list(), max_weight=None):
    nodes = root

    for current in metadata:
        nodes.append()
        nodes[current.value] = dict()
        nodes[current.value]["__categoryPath"] = current.path
        if max_weight != None:
            node[current.value]["__count"] = current.count
            node[current.value]["__weight"] = int((current.count/max_weight) * 10)
        if len(current.childs) != 0:
            node[current.value]["_nodes"] = dict()
            get_metadatas_tree(current.childs, node[metadata.value]["_nodes"], max_weight)

    return node
