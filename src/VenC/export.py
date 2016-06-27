#! /usr/bin/python
# -*- coding: utf-8 -*-

import VenC.core
import VenC.pattern
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
        self.publicDataFromBlogConf = VenC.core.GetPublicDataFromBlogConf()

    def exportMainThread():
        patternProcessor = VenC.pattern.processor(".:",":.","::")
        for key in self.publicDataFromBlogConf:
            patternProcessor.Set(key, self.publicDataFromBlogConf[key])

        count = 0
        for entry in self.entriesList:
            if count == 0:
                outputPage = str()

            if count >= int(self.blogConfiguration["entries_per_page"]):
                pass

