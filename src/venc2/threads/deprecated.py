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

import base64
import codecs
import markdown
import os
import time

import VenC.pattern as Pattern

from VenC.helpers import Die
from VenC.helpers import MergeDictionnaries
from VenC.helpers import Notify
from VenC.helpers import GetListOfPages
from VenC.helpers import GetFilename
from VenC.helpers import ExportExtraData
from VenC.l10n import Messages
from VenC.theme import Theme

''' deprecated '''
class Blog:
    def __init__(self,themeFolder, blogConfiguration):
        self.dataStore = DataStore() 
        self.theme = Theme(themeFolder)
        self.themeFolder = themeFolder
        self.entriesPerDates = GetEntriesPerDates(self.entriesList, self.blogConfiguration["path"]["dates_directory_name"])
        self.entriesPerCategories = GetEntriesPerCategories(self.entriesList)
        self.publicDataFromBlogConf = GetPublicDataFromBlogConf(self.blogConfiguration)
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.columns = list()
        self.inThread = True
        self.entry = dict()
        self.destinationPath = str()
        self.relativeOrigin = str()
        self.ressource = str()
        self.initPatternProcessor()
        self.warnings = list()

    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]
        else:
            return argv[1]

    def initPatternProcessor(self): 
        self.patternProcessor = Pattern.Processor(".:",":.","::")
        
        self.patternProcessor.preProcess("header", self.theme.header)
        self.patternProcessor.preProcess("entry", self.theme.entry)
        self.patternProcessor.preProcess("footer", self.theme.footer)
        self.patternProcessor.preProcess("rssHeader", self.theme.rssHeader)
        self.patternProcessor.preProcess("rssEntry", self.theme.rssEntry)
        self.patternProcessor.preProcess("rssFooter",self.theme.rssFooter)
        
        self.patternProcessor.SetFunction("IfInThread", self.IfInThread)
        self.patternProcessor.SetFunction("PagesList", self.GetPagesList)
        self.patternProcessor.SetFunction("CodeHighlight", self.CodeHighlight)

    def initStates(self, inputEntries, inThread):
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = inThread
        self.entriesNumber = len(inputEntries)

        categoriesTree = GetMetadataTree(self.entriesPerCategories, self.relativeOrigin, dict(), maxWeight=GetMetadataTreeMaxWeight(self.entriesPerCategories))
        
        self.patternProcessor.Set("PagesList", GetListOfPages(int(self.blogConfiguration["entries_per_pages"]),len(inputEntries)))
        self.patternProcessor.Set("BlogCategories", categoriesTree)
        self.patternProcessor.Set("BlogDates", GetDatesList(self.entriesPerDates, self.relativeOrigin, self.blogConfiguration["path"]["dates_directory_name"]))
        self.patternProcessor.Set("RelativeOrigin", self.relativeOrigin)
        self.patternProcessor.Set("RelativeLocation", self.destinationPath)
        self.patternProcessor.Set("SingleEntry", not inThread)
            
        if inThread:
            self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousPageInThread)
            self.patternProcessor.SetFunction("GetNextPage", self.GetNextPageInThread)
        else:
            self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousEntry)
            self.patternProcessor.SetFunction("GetNextPage", self.GetNextEntry)

        for key in self.publicDataFromBlogConf:
           self.patternProcessor.Set(key, self.publicDataFromBlogConf[key])

    def WritePage(self, folderDestination, entry):
        try:
            os.chdir("blog/")
            os.makedirs(folderDestination)
            os.chdir("../")
        except:
            os.chdir("../")
        if entry == -1:
            stream = codecs.open(
                (
                    "blog/"+
                    folderDestination+
                    GetFilename(
                        self.blogConfiguration["path"]["index_file_name"],
                        self.pageCounter-1
                    )
                ),
                'w',
                encoding="utf-8"
            )
        else:
            stream = codecs.open(
                (
                    "blog/"+
                    folderDestination+
                    self.blogConfiguration["path"]["entry_file_name"].format(entry_id=entry)
                ),
                'w',
                encoding="utf-8"
            )
        stream.write(self.outputPage)
        stream.close()

    def export(self):
        # Main thread
        Notify(Messages.exportMainThread)
        self.exportThread(self.entriesList, True)
        # Entries
        self.exportThread(self.entriesList, False)
        
        self.relativeOrigin += "../"
        
        # Dates
        for e in self.entriesPerDates:
            self.relativeLocation = e.value+'/'
            Notify(Messages.exportArchives.format(e.value))
            self.exportThread(e.relatedTo, True, folderDestination=e.value+'/')
        self.relativeOrigin = str()
        self.relativeLocation = str()
        
        # Categories
        self.exportCategories(self.entriesPerCategories)
        self.relativeOrigin = str()
        self.relativeLocation = str()
        
        Notify(Messages.exportMainThreadRss)
        self.exportRss(self.entriesList)

        # Extra data
        ExportExtraData(self.themeFolder+"/assets")
        ExportExtraData(os.getcwd()+"/extra")
        
    def exportCategories(self, categories):
        for category in categories:
            Notify(Messages.exportCategories.format(category.value))
            self.destinationPath += self.blogConfiguration["path"]["category_directory_name"].format(category=category.value+'/')
            self.relativeOrigin += "../"
            self.exportThread(category.relatedTo, True, folderDestination=self.destinationPath)
            Notify(Messages.exportCategoriesRss.format(category.value))
            self.exportRss(category.relatedTo, folderDestination=self.destinationPath)
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
            
            if len(pagesList) == 1 or self.patternProcessor.Get(["SingleEntry"]):
                return str()

            output = str()
            for e in pagesList:
                if (not int(e["pageNumber"]) < int(currentPage) - listLenght) and (not int(e["pageNumber"]) > int(currentPage) + listLenght):
                    output += pattern.format(e) + separator

            return output[:-len(separator)]

        except Exception as e:
            return str(e)

    def GetPreviousEntry(self, argv):
        trigger = False
        output = dict()

        try:
            pattern = argv[0]

        except IndexError:
            return self.handleError("GetPreviousEntry: "+VenC.core.Messages.notEnoughArgs,"~§GetPreviousEntry§§"+"§§".join(argv)+"§~",True)

        sortedEntries = GetSortedEntriesList(
            self.entriesList.keys(),
            self.blogConfiguration["thread_order"]
        )

        for i in range(0, len(sortedEntries)):
            if trigger == True:
                output["destinationPageUrl"] = self.blogConfiguration["path"]["entry_file_name"].format(entry_id=sortedEntries[i].split("__")[0])
                output["destinationPage"] = sortedEntries[i].split("__")[0]
                output["entryName"] = self.GetEntry(sortedEntries[i])["EntryName"]
                return pattern.format(output)
            
            if sortedEntries[i].split("__")[0] == self.entry["EntryID"]:
                trigger = True;

        return str()

    def GetNextEntry(self, argv):
        trigger = False
        output = dict()
        try:
            pattern = argv[0]
        except IndexError:
            return self.handleError("GetPreviousEntry: "+VenC.core.Messages.notEnoughArgs,"~§GetNextEntry§§"+"§§".join(argv)+"§~",True)

        sortedEntries = list(reversed(
            GetSortedEntriesList(
                self.entriesList,
                self.blogConfiguration["thread_order"]
            )
        ))
        for i in range(0, len(sortedEntries)):
            if trigger == True:
                output["destinationPageUrl"] = VenC.core.blogConfiguration["path"]["entry_file_name"].format(entry_id=sortedEntries[i].split("__")[0])
                output["destinationPage"] = sortedEntries[i].split("__")[0]
                output["entryName"] = self.GetEntry(sortedEntries[i])["EntryName"]
                return pattern.format(output)
            
            if sortedEntries[i].split("__")[0] == self.entry["EntryID"]:
                trigger = True;

        return str()

    def GetNextPageInThread(self, argv):
        try:
            pattern = argv[0]
        except IndexError:
            return self.handleError("GetPreviousEntry: "+VenC.core.Messages.notEnoughArgs,"~§GetPreviousEntry§§"+"§§".join(argv)+"§~",True)
        currentPage = self.patternProcessor.Get(["PageNumber"])
        pagesCount = len(self.patternProcessor.Get(["PagesList"]))
        destinationPage = currentPage + 1
        destinationPageUrl = self.blogConfiguration["path"]["index_file_name"].format(page_number=str(destinationPage))
        if destinationPage > pagesCount - 1 or self.patternProcessor.Get(["SingleEntry"]):
            return str()
        else:
            try:
                return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl,"entryName":""})
            except KeyError as e:
                err = VenC.core.OutputColors.FAIL+"VenC: GetNextPage: "+VenC.core.Messages.unknownContextual.format(e)+"\n"
                if self.ressource != str():
            	    err +="VenC: "+VenC.core.Messages.inRessource.format(self.ressource)+"\n"
                
                if not err in VenC.core.errors:
                    VenC.core.errors.append(err)
                    err += ".:GetNextPage::"+"::".join(argv)+":."+VenC.core.OutputColors.END+"\n\n"
                    print(err)
                return "<!-- ~§GetNextPage§§"+"§§".join(argv)+"§~ -->"
	        
    def GetPreviousPageInThread(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        destinationPage = currentPage - 1
        destinationPageUrl = self.blogConfiguration["path"]["index_file_name"].format(
            page_number = "" if currentPage - 1 == 0 else str(currentPage - 1)
        )
        if destinationPage < 0 or self.patternProcessor.Get(["SingleEntry"]):
            return str()
        else:
            try:
                return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl,"entryName":""})
            except KeyError as e:
                err = VenC.core.OutputColors.FAIL+"VenC: GetPreviousPage: "+VenC.core.Messages.unknownContextual.format(e)+"\n"
                if self.ressource != str():
            	    err +="VenC: "+VenC.core.Messages.inRessource.format(self.ressource)+"\n"
                
                if not err in VenC.core.errors:
                    VenC.core.errors.append(err)
                    err += ".:GetPreviousPage::"+"::".join(argv)+":."+VenC.core.OutputColors.END+"\n\n"
                    print(err)
                return "<!-- ~§GetPreviousPage§§"+"§§".join(argv)+"§~ -->"

    def initEntryStates(self, entry):
        self.entry = MergeDictionnaries(
            GetEntry(
                self.entriesList,
                entry,
                self.blogConfiguration["date_format"],
                self.relativeOrigin
            ),
            self.publicDataFromBlogConf
        )
        
        self.entry["EntryContent"] = self.entry["EntryContent"].replace("~§",".:").replace("§§","::").replace("§~",":.")
        if self.entry == None:
            Die(Messages.possibleMalformedEntry.format(entry))

        self.patternProcessor.Set("PageNumber", self.pageCounter)
        self.patternProcessor.Set(
            "EntryDateUrl",
            self.relativeOrigin+time.strftime(
                self.blogConfiguration["path"]["dates_directory_name"],
                time.strptime(entry.split("__")[1],
                "%m-%d-%Y-%M-%S")
            )
        )
        self.patternProcessor.Set(
            "EntryUrl",
            self.relativeOrigin+"entry"+self.entry["EntryID"]+".html"
        )
        self.patternProcessor.SetWholeDictionnary(self.entry)
        self.patternProcessor.ressource = str()
        self.ressource = str()

    def exportRss(self, inputEntries, folderDestination=""):
        self.initStates(inputEntries, True)
        self.outputPage = str()
        self.patternProcessor.ressource = "theme/chunks/rssHeader.html"
        self.ressource = "theme/chunks/rssHeader.html"
        self.outputPage += self.patternProcessor.parse("rssHeader")

        sortedEntries = GetSortedEntriesList(
            inputEntries,
            self.blogConfiguration["thread_order"]
        )
        for entry in sortedEntries[:int(self.blogConfiguration["rss_thread_lenght"])]:
            self.initEntryStates(entry)
            self.patternProcessor.ressource = "theme/chunks/rssEntry.html"
            self.ressource = "theme/chunks/rssEntry.html"
            self.outputPage += self.patternProcessor.parse("rssEntry")
        self.patternProcessor.ressource = "theme/chunks/rssFooter.html"
        self.ressource = "theme/chunks/rssFooter.html"
        self.outputPage += self.patternProcessor.parse("rssFooter")
       	self.outputPage = self.outputPage.replace("<p><div","<div").replace("</div>\n</p>","</div>") # sanitize
       
        stream = codecs.open("blog/"+folderDestination+"/feed.xml",'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def exportThread(self, inputEntries, inThread, folderDestination=""):
        self.initStates(inputEntries, inThread)

        # Configure patternProcessor instance with some fixed values and functions
        # Process actual entries
        if not inThread:
            columnsNumber = 1
            entries_per_pages = 1
        else:
            entries_per_pages  = self.blogConfiguration["entries_per_pages"]
            columnsNumber = 1 if self.blogConfiguration["columns"] < 1 else int(self.blogConfiguration["columns"])

        sortedEntries = GetSortedEntriesList(inputEntries,self.blogConfiguration["thread_order"])
        total = float()
        for entry in sortedEntries:
            self.initEntryStates(entry)
            if self.entryCounter == 0:
                self.columns = [ "<div id=\"__VENC_COLUMN_"+str(i)+"__\" class=\"__VENC_COLUMN__\">" for i in range(0,columnsNumber) ]
                self.outputPage = str()
                self.patternProcessor.ressource = "theme/chunks/header.html"
                self.ressource = "theme/chunks/header.html"
                self.outputPage += self.patternProcessor.parse("header")
           
            self.patternProcessor.ressource = entry
            self.ressource = entry
            self.columns[ self.entryCounter % columnsNumber ] += self.patternProcessor.parse("entry")+"\n"
            self.entryCounter += 1
            if self.entryCounter >= int(entries_per_pages) or entry == sortedEntries[-1]:
                self.columns = [ column+"</div>" for column in self.columns ]
                for column in self.columns:
                    self.outputPage += column
                self.patternProcessor.ressource = "theme/chunks/footer.html"
                self.ressource = "theme/chunks/footer.html"
                self.outputPage += self.patternProcessor.parse("footer")
       	        self.outputPage = self.outputPage.replace("<p><div","<div").replace("</div>\n</p>","</div>") #sanitize
                self.pageCounter += 1
                self.entryCounter = 0
                self.WritePage(
                    folderDestination,
                    (int(entry.split("__")[0]) if not inThread else -1)
                )
