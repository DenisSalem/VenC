#! /usr/bin/python

from VenC.configuration import GetBlogConfiguration
from VenC.entry import YieldEntriesContent
from VenC.entry import GetEntry

class DataStore:
    def __init__(self):
        self.blogConfiguration = GetBlogConfiguration()
        self.entries = list()
        
        ''' Entry index is different from entry id.'''
        for entryIndex, filename in YieldEntriesContent():
            self.entries.append(GetEntry(filename))
            entryIndex+=1
               
    def GetEntries(reverse=False):
        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry

        '''
        self.entriesPerDates = GetEntriesPerDates(self.entriesList, self.blogConfiguration["path"]["dates_directory_name"])
        self.entriesPerCategories = GetEntriesPerCategories(self.entriesList)
        self.publicDataFromBlogConf = GetPublicDataFromBlogConf(self.blogConfiguration)
        '''
