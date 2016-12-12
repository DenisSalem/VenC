#! /usr/bin/python3

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

def remoteCopy(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    try:
        ftp = ftplib.FTP(VenC.core.blogConfiguration["ftp_host"])
    except Exception as e:
        print("VenC:", e)
        return

    username = input("VenC: "+VenC.core.Messages.username)
    userPasswd = getpass.getpass(prompt="VenC: "+VenC.core.Messages.userPasswd)
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

def ftp(argv):
    print("VenC:", VenC.core.Messages.blogRecompilation)
    blog(argv)
    remoteCopy(argv)

def rmTreeErrorHandler(function, path, excinfo):
    if path == "blog" and excinfo[0] == FileNotFoundError:
      print("VenC: "+VenC.core.Messages.blogFolderDoesntExists)
      return

    print("VenC:",function)
    print("VenC:",path)
    print("VenC:",excinfo[0])
    exit()

def blog(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    # cleaning direcoty
    shutil.rmtree("blog", ignore_errors=False, onerror=rmTreeErrorHandler)
    os.makedirs("blog")
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
        self.inThread = True
        self.entry = dict()
        self.destinationPath = str()
        self.relativeOrigin = str()
        self.ressource = str()

    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]
        else:
            return argv[1]

    def initStates(self,inputEntries, inThread):
        self.entryCounter = 0
        self.pageCounter = 0
        self.outputPage = str()
        self.inThread = inThread
        self.entriesNumber = len(inputEntries)
        self.patternProcessor = VenC.pattern.processor(".:",":.","::")
        self.patternProcessor.SetFunction("IfInThread", self.IfInThread)
        self.patternProcessor.Set("PagesList", VenC.core.GetListOfPages(int(VenC.core.blogConfiguration["entries_per_pages"]),len(inputEntries)))
        categoriesTree = VenC.core.GetCategoriesTree(self.entriesPerCategories, self.relativeOrigin, dict(), maxWeight=VenC.core.GetCategoriesTreeMaxWeight(self.entriesPerCategories))
        self.patternProcessor.Set("BlogCategories", categoriesTree)
        self.patternProcessor.Set("BlogDates", VenC.core.GetDatesList(self.entriesPerDates, self.relativeOrigin))
        self.patternProcessor.Set("RelativeOrigin", self.relativeOrigin)
        self.patternProcessor.Set("RelativeLocation", self.destinationPath)
        self.patternProcessor.Set("SingleEntry", not inThread)
        self.patternProcessor.SetFunction("PagesList", self.GetPagesList)
        if inThread:
            self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousPageInThread)
            self.patternProcessor.SetFunction("GetNextPage", self.GetNextPageInThread)
        else:
            self.patternProcessor.SetFunction("GetPreviousPage", self.GetPreviousEntry)
            self.patternProcessor.SetFunction("GetNextPage", self.GetNextEntry)
            
        self.patternProcessor.SetFunction("CodeHighlight", VenC.core.CodeHighlight)
        
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
            stream = codecs.open("blog/"+folderDestination+self.GetFilename(self.pageCounter-1),'w',encoding="utf-8")
        else:
            stream = codecs.open("blog/"+folderDestination+VenC.core.blogConfiguration["path"]["entry_file_name"].format(entry_id=entry),'w',encoding="utf-8")
        stream.write(self.outputPage)
        stream.close()

    def GetFilename(self, pageCounter):
        return VenC.core.blogConfiguration["path"]["index_file_name"].format(page_number=(str(pageCounter) if pageCounter != 0 else str()))

    def export(self):
        # Main thread
        print("VenC:",VenC.core.Messages.exportMainThread)
        self.exportThread(self.entriesList, True)
        
        # Entries
        self.exportThread(self.entriesList, False)
        
        self.relativeOrigin += "../"
        
        # Dates
        for e in self.entriesPerDates:
            self.relativeLocation = e.value+'/'
            print("VenC:", VenC.core.Messages.exportArchives.format(e.value))
            self.exportThread(e.relatedTo, True, folderDestination=e.value+'/')
        self.relativeOrigin = str()
        self.relativeLocation = str()
        
        # Categories
        self.exportCategories(self.entriesPerCategories)
        self.relativeOrigin = str()
        self.relativeLocation = str()
        
        print("VenC:",VenC.core.Messages.exportMainThreadRss)
        self.exportRss(self.entriesList)

        # Extra data
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
            print("VenC:", VenC.core.Messages.exportCategories.format(category.value))
            self.destinationPath+= VenC.core.blogConfiguration["path"]["category_directory_name"].format(category=category.value+'/')
            self.relativeOrigin += "../"
            self.exportThread(category.relatedTo, True, folderDestination=self.destinationPath)
            print("VenC:",VenC.core.Messages.exportCategoriesRss.format(category.value))
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

    def GetNextEntry(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        pagesCount = len(self.patternProcessor.Get(["PagesList"]))
        return str()

    def GetPreviousEntry(self, argv):
        return str()

    def GetNextPageInThread(self, argv):
        pattern = argv[0]
        currentPage = self.patternProcessor.Get(["PageNumber"])
        pagesCount = len(self.patternProcessor.Get(["PagesList"]))
        destinationPage = currentPage + 1
        destinationPageUrl = "index"+str(destinationPage)+".html"
        if destinationPage > pagesCount - 1 or self.patternProcessor.Get(["SingleEntry"]) :
            return str()
        else:
            try:
                return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})
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
        destinationPageUrl = "index.html" if currentPage - 1 == 0 else "index"+str(currentPage - 1)+".html"
        if destinationPage < 0 or self.patternProcessor.Get(["SingleEntry"]):
            return str()
        else:
            try:
                return pattern.format({"destinationPage":destinationPage,"destinationPageUrl":destinationPageUrl})
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
        self.entry = VenC.core.MergeDictionnary(VenC.core.GetEntry(entry, self.relativeOrigin), self.publicDataFromBlogConf)
        self.entry["EntryContent"] = self.entry["EntryContent"].replace("~§",".:").replace("§§","::").replace("§~",":.")
        if self.entry == None:
            print("VenC:", VenC.core.Messages.possibleMalformedEntry.format(entry))
            exit()

        self.patternProcessor.Set("PageNumber", self.pageCounter)
        self.patternProcessor.Set("EntryDateUrl", self.relativeOrigin+time.strftime(VenC.core.blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S")))
        self.patternProcessor.Set("EntryUrl", self.relativeOrigin+"entry"+self.entry["EntryID"]+".html")
        self.patternProcessor.SetWholeDictionnary(self.entry)
        self.patternProcessor.ressource = str()
        self.ressource = str()

    def exportRss(self, inputEntries, folderDestination=""):
        self.initStates(inputEntries, True)
        self.outputPage = str()
        self.patternProcessor.ressource = "theme/chunks/rssHeader.html"
        self.ressource = "theme/chunks/rssHeader.html"
        self.outputPage += self.patternProcessor.parse(self.theme.rssHeader)

        sortedEntries =  sorted(inputEntries, key = lambda e : int(e.split("__")[0]), reverse=(VenC.core.blogConfiguration["thread_order"].strip() == "latest first"))
        for entry in sortedEntries[:int(VenC.core.blogConfiguration["rss_thread_lenght"])]:
            self.initEntryStates(entry)
            self.patternProcessor.ressource = "theme/chunks/rssEntry.html"
            self.ressource = "theme/chunks/rssEntry.html"
            self.outputPage += self.patternProcessor.parse(self.theme.rssEntry)
        self.patternProcessor.ressource = "theme/chunks/rssFooter.html"
        self.ressource = "theme/chunks/rssFooter.html"
        self.outputPage += self.patternProcessor.parse(self.theme.rssFooter)
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
            entries_per_pages  = VenC.core.blogConfiguration["entries_per_pages"]
            columnsNumber = 1 if VenC.core.blogConfiguration["columns"] < 1 else int(VenC.core.blogConfiguration["columns"])

        sortedEntries =  sorted(inputEntries, key = lambda e : int(e.split("__")[0]), reverse=(VenC.core.blogConfiguration["thread_order"].strip() == "latest first"))
        for entry in sortedEntries:
            self.initEntryStates(entry)
            
            if self.entryCounter == 0:
                self.columns = [ "<div id=\"__VENC_COLUMN_"+str(i)+"__\" class=\"__VENC_COLUMN__\">" for i in range(0,columnsNumber) ]
                self.outputPage = str()
                self.patternProcessor.ressource = "theme/chunks/header.html"
                self.ressource = "theme/chunks/header.html"
                self.outputPage += self.patternProcessor.parse(self.theme.header)
           
            self.patternProcessor.ressource = entry
            self.ressource = entry
            self.columns[ self.entryCounter % columnsNumber ] += self.patternProcessor.parse(self.theme.entry)+"\n"
            self.entryCounter += 1
            if self.entryCounter >= int(entries_per_pages) or entry == sortedEntries[-1]:
                self.columns = [ column+"</div>" for column in self.columns ]
                for column in self.columns:
                    self.outputPage += column
                self.patternProcessor.ressource = "theme/chunks/footer.html"
                self.ressource = "theme/chunks/footer.html"
                self.outputPage += self.patternProcessor.parse(self.theme.footer)
       	        self.outputPage = self.outputPage.replace("<p><div","<div").replace("</div>\n</p>","</div>") #sanitize
                self.pageCounter += 1
                self.entryCounter = 0
                self.WritePage(folderDestination, ( int(entry.split("__")[0]) if not inThread else -1))


            
                

