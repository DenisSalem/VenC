#! /usr/bin/python
# -*- coding: utf-8 -*-

import codecs
import VenC.core
import VenC.pattern

def blog(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    currentBlog = Blog()
    currentBlog.export()

class Blog:
    def __init__(self):
        self.theme = VenC.core.Theme()
        self.entriesList = VenC.core.GetEntriesList()
        self.entriesPerTags = VenC.core.GetEntriesPerKeys(self.entriesList,"tags")
        self.entriesPerAuthors = VenC.core.GetEntriesPerKeys(self.entriesList,"authors")
        self.entriesPerDates = VenC.core.GetEntriesPerDates(self.entriesList)
        self.entriesPerCategories = VenC.core.GetEntriesPerCategories(self.entriesList)
        self.publicDataFromBlogConf = VenC.core.GetPublicDataFromBlogConf()
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = False
        self.entry = dict()

    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]
        else:
            return str()

    def initStates(self,inThread=False):
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = inThread

    def WritePage(self, folderDestination):
        stream = codecs.open("blog/"+folderDestination+self.GetIndexFilename(self.pageCounter-1),'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def GetIndexFilename(self, pageCounter):
        return "index"+ (str(pageCounter) if pageCounter != 0 else str())+".html"

    def export(self):
        self.exportThread(self.entriesList)

    def exportThread(self, inputEntries, folderDestination=""):
        self.initStates(inThread=True)

        # Configure patternProcessor instance with some fixed values and functions
        patternProcessor = VenC.pattern.processor(".:",":.","::")
        patternProcessor.SetFunction("IfInThread", self.IfInThread)
        for key in self.publicDataFromBlogConf:
            patternProcessor.Set(key, self.publicDataFromBlogConf[key])

        # Process actual entries
        for entry in inputEntries:
            self.entry = VenC.core.GetEntry(entry)
            patternProcessor.Set("PageNumber", self.pageCounter)
            patternProcessor.Set("EntryUrl", folderDestination+self.GetIndexFilename(self.pageCounter))
            patternProcessor.SetWholeDictionnary(self.entry)
            if self.entryCounter == 0:
                self.outputPage = str()
                self.outputPage += patternProcessor.parse(self.theme.header)

            self.outputPage += patternProcessor.parse(self.theme.entry)+"\n"
            self.entryCounter += 1
            if self.entryCounter >= int(VenC.core.blogConfiguration["entries_per_pages"]) or entry == inputEntries[-1]:
                self.outputPage+= patternProcessor.parse(self.theme.footer)
                self.pageCounter += 1
                self.entryCounter = 0

                self.WritePage(folderDestination)


            
                

