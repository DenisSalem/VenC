#! /usr/bin/python

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.datastore.entry import YieldEntriesContent
from VenC.datastore.entry import Entry
from VenC.datastore.metadata import MetadataNode

class DataStore:
    def __init__(self):
        self.blogConfiguration = GetBlogConfiguration()
        self.entries = list()
        self.entriesPerDates = list()
        self.entriesPerCategories = list()
        self.requestedEntryIndex = 0
        
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
