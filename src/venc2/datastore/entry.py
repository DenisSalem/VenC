#! /usr/bin/env python3

#    Copyright 2016, 2021 Denis Salem
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

import datetime
import os
import time
import unidecode
import urllib.parse
import yaml

from venc2.helpers import quirk_encoding
from venc2.prompt import die
from venc2.prompt import notify

from venc2.l10n import messages
from venc2.datastore.metadata import build_categories_tree
from venc2.datastore.metadata import MetadataNode
from venc2.patterns.processor import ProcessedString
from venc2.patterns.exceptions import IllegalUseOfEscape

class EntryWrapper:
    def __init__(self, wrapper, filename):
        pattern_replacement = {
            ".:GetEntryContent:." : "---VENC-GET-ENTRY-CONTENT---", 
            ".:GetEntryPreview:." : "---VENC-GET-ENTRY-PREVIEW---", 
            ".:PreviewIfInThreadElseContent:." : "---VENC-PREVIEW-IF-IN-THREAD-ELSE-CONTENT---"
        }
        self.content_type_flag = 0
        wrapper_len = len(wrapper)
        
        self.process_get_entry_content = 1  if ".:GetEntryContent:." in wrapper else 0
        self.process_get_entry_preview = 1  if ".:GetEntryPreview:." in wrapper else 0
        if ".:PreviewIfInThreadElseContent:." in wrapper:
            self.process_get_entry_content = 1
            self.process_get_entry_preview = 1
        
        for content_pattern in pattern_replacement.keys():                
            wrapper = wrapper.replace(content_pattern, pattern_replacement[content_pattern])

        if len(wrapper) == wrapper_len:
            die(messages.missing_entry_content_inclusion.format(filename))
            
        self.processed_string = ProcessedString(wrapper, filename, True)

class MinimalEntryMetadata:
    def __init__(self, entry):
        self.id = entry.id
        self.url = entry.url
        self.title = entry.title
        self.chapter = entry.chapter
        self.index = entry.index

class Entry:
    def __init__(self, index, filename, paths, jsonld_callback, date_format, encoding="utf-8", ):
        self.index = index
        self.previous_entry = None
        self.next_entry = None
        self.chapter = None
        self.schemadotorg = {}

        # Loading
        raw_data = open(os.getcwd()+"/entries/"+filename,'r').read()

        entry_parted = raw_data.split("---VENC-BEGIN-PREVIEW---\n")
        if len(entry_parted) == 2:
            entry_parted = [entry_parted[0]] + entry_parted[1].split("---VENC-END-PREVIEW---\n")
            if len(entry_parted) == 3:
                try:
                    self.preview = ProcessedString(entry_parted[1], filename)
                    self.content = ProcessedString(entry_parted[2], filename)
                except IllegalUseOfEscape:
                    die(messages.illegal_use_of_escape.format(filename))
                    
                try:
                    metadata = yaml.load(entry_parted[0], Loader=yaml.FullLoader)

                except yaml.scanner.ScannerError as e:
                    die(messages.possible_malformed_entry.format(filename, ''), extra=str(e))

            else:
                cause = messages.missing_separator_in_entry.format("---VENC-END-PREVIEW---")
                die(messages.possible_malformed_entry.format(filename, cause))
        else:
            cause = messages.missing_separator_in_entry.format("---VENC-BEGIN-PREVIEW---")
            die(messages.possible_malformed_entry.format(filename, cause))
        
        # Setting up optional metadata
        for key in metadata.keys():
            if not key in ["authors", "tags", "categories", "title"]:
                if metadata[key] != None:
                    if key == "https://schema.org":
                        self.schemadotorg = metadata[key]
                    else:
                        setattr(self, key, metadata[key])
                        
                else:
                    notify(messages.invalid_or_missing_metadata.format(key, filename), color="YELLOW")
                    setattr(self, key, '')

        # Fix missing or incorrect metadata
        for key in ["authors", "tags", "categories", "title"]:
            if key not in metadata.keys() or metadata[key] == None:
                notify(messages.invalid_or_missing_metadata.format(key, filename), color="YELLOW")
                metadata[key] = ''
    
        self.raw_metadata = metadata
        self.filename = filename
        self.id = int(filename.split('__')[0])
        
        raw_date = filename.split('__')[1].split('-')
        self.date = datetime.datetime(
            year=int(raw_date[2]),
            month=int(raw_date[0]),
            day=int(raw_date[1]),
            hour=int(raw_date[3]),
            minute=int(raw_date[4])
        )
        self.formatted_date = self.date.strftime(date_format)

        try:
            self.title = metadata["title"].replace(".:GetEntryTitle:.",'')

        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("title", self.id))

        try:
            self.authors = [ e.strip() for e in metadata["authors"].split(",")] if type(metadata["authors"]) == str else metadata["authors"]
            if type(self.authors) != list:
                raise GenericMessage(messages.entry_metadata_is_not_a_list.format("authors", self.id))
                
        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("authors", self.id))

        try:
            self.tags = [ e.strip() for e in metadata["tags"].split(",")] if type(metadata["tags"]) == str else metadata["tags"]
            if type(self.tags) != list:
                raise GenericMessage(messages.entry_metadata_is_not_a_list.format("tags", self.id))
                
        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("tags", self.id))

        params = {
            "entry_id": self.id,
            "entry_title": self.title
        }
        # TODO MAY BE OPTIMIZED
        sf = paths["entries_sub_folders"].format(**params)
        if encoding == '':
            self.sub_folder = quirk_encoding(unidecode.unidecode(sf))+'/' if sf != '' else ''
            self.url = "\x1a"+self.sub_folder
            if self.sub_folder == '' or paths["entry_file_name"] != "index.html":
                self.url += quirk_encoding(
                    unidecode.unidecode(
                        paths["entry_file_name"].format(**params)
                    )
                )
            
        else:
            try:
                self.sub_folder = urllib.parse.quote(sf, encoding=encoding)+'/' if sf != '' else ''
                self.url = "\x1a"+self.sub_folder
                if self.sub_folder == '' or paths["entry_file_name"] != "index.html":
                    self.url += urllib.parse.quote(paths["entry_file_name"].format(**params), encoding=encoding)


            except UnicodeEncodeError as e:
                self.url = "\x1a"+self.sub_folder+paths["entry_file_name"].format(**params)
                notify("\"{0}\": ".format(sf+paths["entry_file_name"].format(**params))+str(e), color="YELLOW")
        
        self.categories_leaves = list()
        self.raw_categories = [ c.strip() for c in metadata["categories"].split(',')]
        try:
            for category in self.raw_categories:
                category_leaf = category.split(' > ')[-1].strip()
                if len(category_leaf) != 0:
                    category_leaf_path = "\x1a"
                    for sub_category in category.split(' > '):
                        category_leaf_path +=sub_category.strip()+'/'
                
                    self.categories_leaves.append({
                        "value": category_leaf,
                        "path": category_leaf_path,
                        "branch" : category
                    })

        except IndexError : # when list is empty
            pass

        self.categories_tree = []
        build_categories_tree(-1, self.raw_categories, self.categories_tree, None, -1, encoding=encoding, sub_folders=paths["categories_sub_folders"])
        self.html_categories_tree = {}
        self.html_tags = {}
        self.html_authors = {}
        self.html_categories_leaves = {}
        self.html_for_metadata = {}
        if jsonld_callback != None:
            jsonld_callback(self)

''' Iterate through entries folder '''
def yield_entries_content():
    try:
        for filename in os.listdir(os.getcwd()+"/entries"):
            exploded_filename = filename.split("__")
            try:
                date = exploded_filename[1].split('-')
                entry_id = int(exploded_filename[0])
                datetime.datetime(
                    year=int(date[2]),
                    month=int(date[0]),
                    day=int(date[1]),
                    hour=int(date[3]),
                    minute=int(date[4])
                ) 
                if entry_id >= 0:
                    yield filename

                else:
                    raise ValueError

            except ValueError:
                notify(messages.invalid_entry_filename.format(filename), "YELLOW")

            except IndexError:
                notify(messages.invalid_entry_filename.format(filename), "YELLOW")
    
    except FileNotFoundError:
        die(messages.file_not_found.format(os.getcwd()+"/entries"))

def get_latest_entryID():
    entries_list = sorted(yield_entries_content(), key = lambda entry : int(entry.split("__")[0]))
    if len(entries_list) != 0:
        return int(entries_list[-1].split("__")[0])
    else:
        return 0
