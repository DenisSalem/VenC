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
        self.entry_id = entry.id
        self.title = entry.title
        self.path = path

    def __str__(self):
        return self.index

class EntryMetadata:
    def __init__(ID, raw_date, metadata):
        self.id = ID
        self.date = datetime.datetime(
            year=int(raw_date[2]),
            month=int(raw_date[0]),
            day=int(raw_date[1]),
            hour=int(raw_date[3]),
            minute=int(raw_date[4])
        )
        self.title = metadata["title"].replace(".:GetEntryTitle:.",'') # sanitize
        self.formatted_date = self.date.strftime(date_format)

        if type(metadata["authors"]) != list:
            from venc3.exceptions import VenCException
            raise VenCException(("entry_metadata_is_not_a_list", "authors", self.id), context=filename)
            
        self.authors = tuple(metadata["authors"])      
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

class WeightTracker:
    def __init__(self):
        self.value = 0
        
    def update(self):
        self.value += 1
