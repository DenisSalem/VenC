#! /usr/bin/python

from VenC.configuration import GetBlogConfiguration
from VenC.entry import GetEntriesList
from VenC.entry import GetEntry

class DataStore:
    def __init__(self):
        self.blogConfiguration = GetBlogConfiguration
        self.entries = dict()
        for entry in GetEntriesList():
            self.entries[entry] = GetEntry()
               
        '''
        self.entriesPerDates = GetEntriesPerDates(self.entriesList, self.blogConfiguration["path"]["dates_directory_name"])
        self.entriesPerCategories = GetEntriesPerCategories(self.entriesList)
        self.publicDataFromBlogConf = GetPublicDataFromBlogConf(self.blogConfiguration)
        '''
