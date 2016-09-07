#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import shutil
import ftplib
import codecs
import getpass
import subprocess
import VenC.core
import VenC.pattern


def ftpExportRecursively(origin, ftp):
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    ftp.mkd(item)
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftpExportRecursively(origin+"/"+item, ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])
                except:
                    try:
                        ftp.cwd(ftp.pwd()+"/"+item)
                        ftpExportRecursively(origin+"/"+item, ftp)
                        ftp.cwd(ftp.pwd()[:-len("/"+item)])
                    except:
                        raise

            else:
                ftp.storbinary("STOR "+ftp.pwd()+"/"+item, open(origin+"/"+item, 'rb'))
                #shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)

def ftpCleanDestination(ftp):
    listing = list()
    listing = ftp.nlst()
    for item in listing:
        if item not in ['.','..']:
            try:
                ftp.delete(item)
            except Exception:
                try:
                    ftp.rmd(item)
                except:
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftpCleanDestination(ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])

def ftp(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    ftp = ftplib.FTP(VenC.core.blogConfiguration["ftp_host"])
    username = input(VenC.core.Messages.username)
    userPasswd = getpass.getpass(prompt=VenC.core.Messages.userPasswd)
    try:
        ftp.login(user=username,passwd=userPasswd)
        ftp.cwd(VenC.core.blogConfiguration["path"]["ftp"])
        print("VenC:", VenC.core.Messages.cleanFtpDirectory)
        ftpCleanDestination(ftp)
        print("VenC:", VenC.core.Messages.copyToFtpDirectory)
        ftpExportRecursively(os.getcwd()+"/blog", ftp)
    
    except ftplib.error_perm as e:
        print(e)
        return
        

def blog(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    currentBlog = Blog()
    currentBlog.export()

def edit(argv):
    try:
        proc = subprocess.Popen([VenC.core.blogConfiguration["textEditor"], argv[0]])
        while proc.poll() == None:
            pass
    except:
        raise
    blog(list())

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
        self.columns = list()
        self.inThread = False
        self.entry = dict()
        self.destinationPath = str()
        self.relativeOrigin = str()

    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]
        else:
            return argv[1]

    def initStates(self,inputEntries, singleEntry, inThread=False):
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = inThread
        self.entriesNumber = len(inputEntries)
        self.patternProcessor = VenC.pattern.processor(".:",":.","::")
        self.patternProcessor.SetFunction("IfInThread", self.IfInThread)
        self.patternProcessor.Set("PagesList", VenC.core.GetListOfPages(int(VenC.core.blogConfiguration["entries_per_pages"]),len(inputEntries)))
        self.patternProcessor.Set("BlogCategories", VenC.core.GetCategoriesTree(VenC.core.GetCategoriesList(self.entriesList), self.relativeOrigin))
        self.patternProcessor.Set("BlogDates", VenC.core.GetDatesList(self.entriesPerDates, self.relativeOrigin))
        self.patternProcessor.Set("RelativeOrigin", self.relativeOrigin)
        self.patternProcessor.Set("SingleEntry", singleEntry)
        self.patternProcessor.SetFunction("PagesList", self.GetPagesList)
        self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousPage)
        self.patternProcessor.SetFunction("GetNextPage", self.GetNextPage)
        self.patternProcessor.SetFunction("CodeHighlight", VenC.core.CodeHighlight)
        
        for key in self.publicDataFromBlogConf:
            self.patternProcessor.Set(key, self.publicDataFromBlogConf[key])


    def WritePage(self, folderDestination, singleEntry):
        try:
            os.chdir("blog/")
            os.makedirs(folderDestination)
            os.chdir("../")
        except:
            os.chdir("../")
        stream = codecs.open("blog/"+folderDestination+self.GetFilename(self.pageCounter-1, singleEntry),'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def GetFilename(self, pageCounter, singleEntry):
        if singleEntry:
            return VenC.core.blogConfiguration["path"]["entry_file_name"].format(entry_id=  str(self.entriesNumber - pageCounter))
        else:  
            return VenC.core.blogConfiguration["path"]["index_file_name"].format(page_number=(str(pageCounter) if pageCounter != 0 else str()))

    def export(self):
        self.exportThread(self.entriesList)
        self.exportRss(self.entriesList)
        self.relativeOrigin += "../"
        for e in self.entriesPerDates:
            self.exportThread(e.relatedTo, folderDestination=e.value+'/')
        self.relativeOrigin = str()
        
        self.exportCategories(self.entriesPerCategories)
        self.relativeOrigin = str()
        
        self.exportThread(self.entriesList, singleEntry=True)
        self.exportExtraData(os.getcwd()+"/theme/assets")
        self.exportExtraData(os.getcwd()+"/extra")
    
    def exportExtraData(self,origin, destination=""):
        try:
            folder = os.listdir(origin)
            for item in folder:
                if os.path.isdir(origin+"/"+item):
                    try:
                        os.mkdir(os.getcwd()+"/blog/"+destination+item)
                        self.exportExtraData(origin+'/'+item, item+'/')
                    except:
                        raise
                else:
                    shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)
        except:
            raise
        
    def exportCategories(self, categories):
        for category in categories:
            self.destinationPath+= VenC.core.blogConfiguration["path"]["category_directory_name"].format(category=category.value+'/')
            self.relativeOrigin += "../"
            self.exportThread(category.relatedTo, folderDestination=self.destinationPath)
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

    def GetNextPage(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        pagesCount = len(self.patternProcessor.Get(["PagesList"]))
        destinationPage = currentPage + 1
        destinationPageUrl = "index"+str(destinationPage)+".html"
        if destinationPage > pagesCount - 1 or self.patternProcessor.Get(["SingleEntry"]) :
            return str()
        else:
            return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})

    def GetPreviousPage(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        destinationPage = currentPage - 1
        destinationPageUrl = "index.html" if currentPage - 1 == 0 else "index"+str(currentPage - 1)+".html"
        if destinationPage < 0 or self.patternProcessor.Get(["SingleEntry"]):
            return str()
        else:
            return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})

    def initEntryStates(self, entry):
        self.entry = VenC.core.GetEntry(entry, self.relativeOrigin)
        if self.entry == None:
            print("VenC:", VenC.core.Messages.possibleMalformedEntry.format(entry))
            exit()

        self.patternProcessor.Set("PageNumber", self.pageCounter)
        self.patternProcessor.Set("EntryDateUrl", self.relativeOrigin+time.strftime(VenC.core.blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S")))
        self.patternProcessor.Set("EntryUrl", self.relativeOrigin+"entry"+self.entry["EntryID"]+".html")
        self.patternProcessor.SetWholeDictionnary(self.entry)

    def exportRss(self, inputEntries, folderDestination=""):
        self.initStates(inputEntries, False, inThread=True)
        self.outputPage = str()
        self.outputPage += self.patternProcessor.parse(self.theme.rssHeader)

        for entry in inputEntries[:int(VenC.core.blogConfiguration["rss_thread_lenght"])]:
            self.initEntryStates(entry)
            self.outputPage += self.patternProcessor.parse(self.theme.rssEntry)
        self.outputPage += self.patternProcessor.parse(self.theme.rssFooter)
        
        stream = codecs.open("blog/"+folderDestination+"/feed.xml",'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def exportThread(self, inputEntries, folderDestination="", singleEntry=False):
        self.initStates(inputEntries, singleEntry, inThread=True)
        # Configure patternProcessor instance with some fixed values and functions
        # Process actual entries
        if singleEntry:
            columnsNumber = 1
            VenC.core.blogConfiguration["entries_per_pages"] = 1
        else:
            columnsNumber = 1 if VenC.core.blogConfiguration["columns"] < 1 else int(VenC.core.blogConfiguration["columns"])

        for entry in inputEntries:
            self.initEntryStates(entry)
            
            if self.entryCounter == 0:
                self.columns = [ "<div id=\"__VENC_COLUMN_"+str(i)+"__\" class=\"__VENC_COLUMN__\">" for i in range(0,columnsNumber) ]
                self.outputPage = str()
                self.outputPage += self.patternProcessor.parse(self.theme.header)
            
            self.columns[ self.entryCounter % columnsNumber ] += self.patternProcessor.parse(self.theme.entry)+"\n"
            self.entryCounter += 1
            if self.entryCounter >= int(VenC.core.blogConfiguration["entries_per_pages"]) or entry == inputEntries[-1]:
                self.columns = [ column+"</div>" for column in self.columns ]
                for column in self.columns:
                    self.outputPage += column
                self.outputPage += self.patternProcessor.parse(self.theme.footer)
                self.pageCounter += 1
                self.entryCounter = 0

                self.WritePage(folderDestination, singleEntry)


            
                

