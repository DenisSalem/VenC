#! /usr/bin/python3

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

import datetime
import os
import time
import yaml

from venc2.helpers import die
from venc2.helpers import notify

from venc2.l10n import messages
from venc2.datastore.metadata import MetadataNode
from venc2.patterns.processor import PreProcessor

class EntryWrapper:
    def __init__(self, wrapper):
        try:
            w = wrapper.split(".:GetEntryContent:.")
            self.above = PreProcessor(w[0])
            self.below = PreProcessor(w[1])

        except IndexError:
            die(messages.missing_entry_content_inclusion)

class Entry:
    def __init__(self, filename):
        # Loading
        raw_data = open(os.getcwd()+"/entries/"+filename,'r').read()
        try:
            raw_content = raw_data.split("\n---\n")[1]

        except: #empty entry
            raw_content = ''

        try:
            metadata = yaml.load(raw_data.split("---\n")[0])

        except yaml.scanner.ScannerError:
            die(messages.possible_malformed_entry.format(filename))

        if metadata == None:
            die(messages.possible_malformed_entry.format(filename))

        # Setting up optional metadata
        for key in metadata.keys():
            if not key in ["authors","tags","categories","entry_name"]:
                setattr(self, key, metadata[key])
    
        self.filename = filename
        self.id = filename.split('__')[0]
        
        raw_date = filename.split('__')[1].split('-')
        self.date = datetime.datetime(
            year=int(raw_date[2]),
            month=int(raw_date[0]),
            day=int(raw_date[1]),
            hour=int(raw_date[3]),
            minute=int(raw_date[4])
        )
        
        try:
            self.title = metadata["title"]

        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("title", self.id))

        try:
            self.authors = [ {"author":e} for e in list(metadata["authors"].split(",") if metadata["authors"] != str() else list()) ]

        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("authors", self.id))

        try:
            self.content = PreProcessor(raw_content)

        except:
            raise
            die(messages.possible_malformed_entry.format(self.id))

        try:
            self.tags = [ {"tag":e} for e in list(metadata["tags"].split(",") if metadata["tags"] != str() else list())]

        except KeyError:
            die(messages.missing_mandatory_field_in_entry.format("tags", self.id))

        self.categories_leaves = list()
        self.categories_nodes_reference = list()
        self.raw_categories = metadata["categories"].split(',')
        try:
            for category in self.raw_categories:
                category_leaf = category.split(' > ')[-1].strip()
                if len(category_leaf) != 0:
                    category_leaf_url = str()
                    for sub_category in category.split(' > '):
                        category_leaf_url +=sub_category.strip()+'/'
                
                    self.categories_leaves.append({
                        "categoryLeaf": category_leaf,
                        "categoryLeafPath":category_leaf_url
                    })

        except IndexError : # when list is empty
            pass

    def SetupCategoriesNodesReference(self, categoriesTree):
        pass

''' Iterate through entries folder '''
def yield_entries_content():
    try:
        for filename in sorted(
            os.listdir(os.getcwd()+"/entries"),
            key = lambda entry_id : int(entry_id.split("__")[0])
        ):
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
                if entry_id > 0:
                    yield filename

                else:
                    raise ValueError

            except ValueError:
                notify(messages.invalid_entry_filename.format(filename), "YELLOW")

            except IndexError:
                notify(messages.invalid_entry_filename.format(filename), "YELLOW")
    
    except FileNotFoundError:
        die(messages.file_not_found.format(os.getcwd()+"/entries"))


''' User for set the id of new entry '''
def get_latest_entryID():
    entries_list = sorted(yield_entries_content(), key = lambda entry : int(entry.split("__")[0]))
    if len(entries_list) != 0:
        return int(entries_list[-1].split("__")[0])
    else:
        return 0

'''

def GetCategoriesList(entries):
    output = list()
    for entry in entries.keys():
        stream = entries[entry].split("---\n")[0]
        data = yaml.load(stream)
        if data != None:
            for category in data["categories"].split(","):
                if (not category in output) and category != '':
                    output.append(category)

    return output

def GetEntriesPerCategories(entries):
    entriesPerCategories = list()
    for entry in entries.keys():
        stream = entries[entry].split("---\n")[0]
        try:
            data = yaml.load(stream)
        except yaml.scanner.ScannerError:
            Die(Messages.possibleMalformedEntry.format(entry))

        except yaml.parser.ParserError:
            Die(Messages.possibleMalformedEntry.format(entry))

        if data != None:
            try:
                for category in data["categories"].split(","):
                    if category != '':
                        nodes = entriesPerCategories
                        path = str()
                        for subCategory in category.split(" > "):
                            path += subCategory+'/'
                            try:
                                selectedKey = GetKeyByName(nodes, subCategory.strip())
                                selectedKey.relatedTo.append(entry)
                                selectedKey.count += 1
                                selectedKey.relatedTo = list(set(selectedKey.relatedTo))
                            except Exception as e:
                                selectedKey = Metadata(subCategory.strip(), entry)
                                selectedKey.path = path
                                nodes.append(selectedKey)
                            
                            nodes = selectedKey.childs
                
            except TypeError:
                Die(Messages.possibleMalformedEntry.format(entry))

    return entriesPerCategories

'''
