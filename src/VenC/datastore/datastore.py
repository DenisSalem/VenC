#! /usr/bin/python

#   Copyright 2016, 2017 Denis Salem

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

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.datastore.entry import YieldEntriesContent
from VenC.datastore.entry import Entry
from VenC.datastore.metadata import MetadataNode
from VenC.pattern.codeHighlight import CodeHighlight

class DataStore:
    def __init__(self):
        self.blogConfiguration = GetBlogConfiguration()
        self.entries = list()
        self.entriesPerDates = list()
        self.entriesPerCategories = list()
        self.requestedEntryIndex = 0
        self.codeHighlight = CodeHighlight()
        
        ''' Entry index is different from entry id '''
        entryIndex = 0
        for filename in YieldEntriesContent():
            self.entries.append(Entry(filename))

            ''' Update entriesPerDates '''

            formattedDate = self.entries[-1].date.strftime(self.blogConfiguration["path"]["datesDirectoryName"])
            entriesIndex = self.GetEntriesIndexForGivenDate(formattedDate)
            if entriesIndex != None:
                self.entriesPerDates[entriesIndex].count +=1
                self.entriesPerDates[entriesIndex].relatedTo.append(entryIndex)
            else:
                self.entriesPerDates.append(MetadataNode(formattedDate, entryIndex))

            entryIndex += 1

            ''' Update entriesPerCategories '''
    
    def GetBlogMetadata(argv):
        return str(getattr(self.blogConfiguration, argv[0]))
            
    def GetEntryMetadata(argv):
        return str( getattr(self.entries[self.requestedEntryIndex], argv[0]))
            
    def GetEntriesIndexForGivenDate(self, value):
        index = 0
        for metadata in self.entriesPerDates:
            if value == metadata.value:
                return index
            index += 1
        return None

    def GetEntries(reverse=False):
        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry
    
    def GetEntryTitle(argv=list()):
        return self.entries[self.requestedEntriesIndex].title
    
    def GetEntryID(argv=list()):
        return self.entries[self.requestedEntriesIndex].id

    def GetEntryYear(argv=list()):
        return self.entries[self.requestedEntriesIndex].date.year
        
    def GetEntryMonth(argv=list()):
        return self.entries[self.requestedEntriesIndex].date.month
        
    def GetEntryDay(argv=list()):
        return self.entries[self.requestedEntriesIndex].date.day

    def GetEntryHour(argv=list()):
        return self.entries[self.requestedEntriesIndex].date.hour
    
    def GetEntryMinute(argv=list()):
        return self.entries[self.requestedEntriesIndex].date.minute

    def GetAuthorName(argv=list()):
        return self.blogConfiguration["authorName"]

    def GetBlogName(argv=list()):
        return self.blogConfiguration["blogName"]
        
    def GetBlogDescription(argv=list()):
        return self.blogConfiguration["blogDescription"]
        
    def GetBlogKeywords(argv=list()):
        return self.blogConfiguration["blogKeywords"]

    def GetAuthorDescription(argv=list()):
        return self.blogConfiguration["authorDescription"]
        
    def GetBlogLicense(argv=list()):
        return self.blogConfiguration["license"]
    
    def GetBlogURL(argv=list()):
        return self.blogConfiguration["blogUrl"]
    
    def GetBlogLanguage(argv=list()):
        return self.blogConfiguration["blogLanguage"]
    
    def GetAuthorEmail(argv=list()):
        return self.blogConfiguration["authorEmail"]
        
        

        
