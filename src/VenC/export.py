#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
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
        self.entriesPerDates = VenC.core.GetEntriesPerDates(self.entriesList)
        self.entriesPerCategories = VenC.core.GetEntriesPerCategories(self.entriesList)
        self.publicDataFromBlogConf = VenC.core.GetPublicDataFromBlogConf()
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = False
        self.entry = dict()
        self.destinationPath = str()
        self.relativeOrigin = str()

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
        self.patternProcessor = VenC.pattern.processor(".:",":.","::")

    def WritePage(self, folderDestination):
        try:
            os.chdir("blog/")
            os.makedirs(folderDestination)
            os.chdir("../")
        except:
            os.chdir("../")
        stream = codecs.open("blog/"+folderDestination+self.GetIndexFilename(self.pageCounter-1),'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def GetIndexFilename(self, pageCounter):
        return "index"+ (str(pageCounter) if pageCounter != 0 else str())+".html"

    def export(self):
        self.exportThread(self.entriesList)
        self.relativeOrigin += "../"
        for e in self.entriesPerDates:
            self.exportThread(e.relatedTo, folderDestination=e.value+'/')
        self.relativeOrigin = str()
        self.exportCategories(self.entriesPerCategories)

    def exportCategories(self, categories):
        for category in categories:
            self.destinationPath+= category.value+'/'
            self.relativeOrigin += "../"
            self.exportThread(category.relatedTo, folderDestination=self.destinationPath)
            self.exportCategories(category.childs)
            self.relativeOrigin = self.relativeOrigin[:-3]
            self.destinationPath = self.destinationPath[:-len(category.value+"/")]

    def GetPagesList(self, argv):
        try:
            listLenght = int(argv[0])
            pattern = argv[1]
            separator = argv[2]
            currentPage = self.patternProcessor.Get(["PageNumber"])
            pagesList = self.patternProcessor.Get(["PagesList"])
            output = str()
            for e in pagesList:
                if (not int(e["pageNumber"]) < int(currentPage) - listLenght) and (not int(e["pageNumber"]) > int(currentPage) + listLenght):
                    output += pattern.format(variables) + separator

            
            return output[:-len(separator)]

        except:
            return str()

    def GetNextPage(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        pagesCount = len(self.patternProcessor.Get(["PagesList"]))
        destinationPage = currentPage + 1
        destinationPageUrl = "index"+str(destinationPage)+".html"
        if destinationPage > pagesCount - 1:
            return str()
        else:
            return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})

    def GetPreviousPage(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        destinationPage = currentPage - 1
        destinationPageUrl = "index.html" if currentPage - 1 == 0 else "index"+str(currentPage - 1)+".html"
        if destinationPage < 0:
            return str()
        else:
            return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})

    def exportThread(self, inputEntries, folderDestination=""):
        self.initStates(inThread=True)
        # Configure patternProcessor instance with some fixed values and functions
        self.patternProcessor.SetFunction("IfInThread", self.IfInThread)
        self.patternProcessor.Set("PagesList", VenC.core.GetListOfPages(int(VenC.core.blogConfiguration["entries_per_pages"]),len(inputEntries)))
        self.patternProcessor.Set("BlogCategories", VenC.core.GetCategoriesTree(VenC.core.GetCategoriesList(self.entriesList), self.relativeOrigin))
        self.patternProcessor.Set("BlogDates", VenC.core.GetDatesList(self.entriesPerDates, self.relativeOrigin))
        self.patternProcessor.Set("RelativeOrigin", self.relativeOrigin)
        self.patternProcessor.SetFunction("PagesList", self.GetPagesList)
        self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousPage)
        self.patternProcessor.SetFunction("GetNextPage", self.GetNextPage)
        
        for key in self.publicDataFromBlogConf:
            self.patternProcessor.Set(key, self.publicDataFromBlogConf[key])

        # Process actual entries
        for entry in inputEntries:
            # Update entry datas
            
            self.entry = VenC.core.GetEntry(entry, self.relativeOrigin)
            self.patternProcessor.Set("PageNumber", self.pageCounter)
            self.patternProcessor.Set("EntryDateUrl", self.relativeOrigin+time.strftime(VenC.core.blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S")))
            self.patternProcessor.Set("EntryUrl", self.relativeOrigin+"entry"+self.entry["EntryID"]+".html")
            self.patternProcessor.SetWholeDictionnary(self.entry)

            if self.entryCounter == 0:
                self.outputPage = str()
                self.outputPage += self.patternProcessor.parse(self.theme.header)

            self.outputPage += self.patternProcessor.parse(self.theme.entry)+"\n"
            self.entryCounter += 1
            if self.entryCounter >= int(VenC.core.blogConfiguration["entries_per_pages"]) or entry == inputEntries[-1]:
                self.outputPage+= self.patternProcessor.parse(self.theme.footer)
                self.pageCounter += 1
                self.entryCounter = 0

                self.WritePage(folderDestination)


            
                

