#! /usr/bin/python
# -*- coding: utf-8 -*-

import VenC.core

def blog(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    currentBlog = Blog()

class Blog:
    def __init__(self):
        self.theme = VenC.core.Theme()
        self.entriesList = VenC.core.GetEntriesList()
        self.entriesPerTags = VenC.core.GetEntriesPerKeys(self.entriesList,"tags")
        self.entriesPerAuthors = VenC.core.GetEntriesPerKeys(self.entriesList,"authors")
        self.entriesPerDates = VenC.core.GetEntriesPerDates(self.entriesList)
        self.entriesPerCategories = VenC.core.GetEntriesPerCategories(self.entriesList)
