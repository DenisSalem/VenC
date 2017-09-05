#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
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
import markdown
import os
import time
import yaml

from VenC.helpers import Die
from VenC.helpers import Notify

from VenC.l10n import Messages
from VenC.datastore.metadata import MetadataNode
from VenC.pattern.processor import PreProcessor

class EntryWrapper:
    def __init__(self, wrapper):
        try:
            w = wrapper.split(".:GetEntryContent:.")
            self.above = PreProcessor(w[0])
            self.below = PreProcessor(w[1])

        except IndexError:
            Die(Messages.missingEntryContentInclusion)

class Entry:
    def __init__(self, filename):
        # Loading
        rawData = open(os.getcwd()+"/entries/"+filename,'r').read()
        rawContent = rawData.split("---\n")[1]
        try:
            metadata = yaml.load(rawData.split("---\n")[0])

        except yaml.scanner.ScannerError:
            Die(Messages.possibleMalformedEntry.format(entryFilename))

        if metadata == None:
            Die(Messages.possibleMalformedEntry.format(entryFilename))

        # Setting up optional metadata
        for key in metadata.keys():
            if not key in ["authors","tags","categories","entry_name","doNotUseMarkdown"]:
                setattr(self, key, metadata[key])
    
        # Are we using markdown?
        if "doNotUseMarkdown" in metadata.keys():
            self.doNotUseMarkdown = True
        else:
            self.doNotUseMarkdown = False
            rawContent = markdown.markdown(rawContent)
    
        # Set up id
        self.id = filename.split('__')[0]
        
        # Set up date
        rawDate = filename.split('__')[1].split('-')
        self.date = datetime.datetime(
            year=int(rawDate[2]),
            month=int(rawDate[0]),
            day=int(rawDate[1]),
            hour=int(rawDate[3]),
            minute=int(rawDate[4])
        )
        
        # Setting up title
        try:
            self.title = metadata["title"]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("title", self.id))

        # Setting up authors
        try:
            self.authors = [ e for e in list(metadata["authors"].split(",") if metadata["authors"] != str() else list()) ]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("authors", self.id))

        # Setting up content
        try:
            self.content = PreProcessor(rawContent)

        except:
            raise
            Die(Messages.possibleMalformedEntry.format(self.id))

        ''' Setting up tags '''
        try:
            self.tags = [ {"tag":e} for e in list(metadata["tags"].split(",") if metadata["tags"] != str() else list())]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("tags", self.id))



        ''' Setting up categories'''
        self.categoriesLeaves = list()
        self.categoriesNodesReference = list()
        self.rawCategories = metadata["categories"].split(',')
        try:
            for category in self.rawCategories:
                categoryLeaf = category.split(' > ')[-1].strip()
                if len(categoryLeaf) != 0:
                    categoryLeafUrl = str()
                    for subCategory in category.split(' > '):
                        categoryLeafUrl +=subCategory.strip()+'/'
                
                    self.categoriesLeaves.append({
                        "categoryLeaf": categoryLeaf,
                        "categoryLeafPath":categoryLeafUrl
                    })

        except IndexError : # when list is empty
            pass

    def SetupCategoriesNodesReference(self, categoriesTree):
        pass

''' Iterate through entries folder '''
def YieldEntriesContent():
    try:
        for filename in sorted(
            os.listdir(os.getcwd()+"/entries"),
            key = lambda entryId : int(entryId.split("__")[0])
        ):
            explodedFilename = filename.split("__")
            try:
                date = explodedFilename[1].split('-')
                entryID = int(explodedFilename[0])
                datetime.datetime(
                    year=int(date[2]),
                    month=int(date[0]),
                    day=int(date[1]),
                    hour=int(date[3]),
                    minute=int(date[4])
                ) 
                if entryID > 0:
                    yield filename

                else:
                    raise ValueError

            except ValueError:
                Notify(Messages.invalidEntryFilename.format(filename), "YELLOW")

            except IndexError:
                Notify(Messages.invalidEntryFilename.format(filename), "YELLOW")
    
    except FileNotFoundError:
        Die(Messages.fileNotFound.format(os.getcwd()+"/entries"))


''' User for set the id of new entry '''
def GetLatestEntryID():
    entriesList = sorted(YieldEntriesContent(), key = lambda entry : int(entry.split("__")[0]))
    if len(entriesList) != 0:
        return int(entriesList[-1].split("__")[0])
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
