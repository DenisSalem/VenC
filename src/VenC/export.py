#! /usr/bin/python3

import os
import time
import yaml
import base64
import shutil
import ftplib
import codecs
import getpass
import markdown
import subprocess
import VenC.core
import VenC.pattern
import pygments.lexers
import pygments.formatters



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
    themeFolder = os.getcwd()+"/theme/"
    if len(argv) == 1:
        if not argv[0] in VenC.core.themes.keys(): 
            print("VenC:", VenC.core.Messages.themeDoesntExists.format(argv[0]))
            exit()
        else:
            themeFolder = os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0]+"/"
        
        for param in VenC.core.themes[argv[0]].keys():
            if param[0] != "_": # marker to detect what's we are looking for
                VenC.core.blogConfiguration[param] = VenC.core.themes[argv[0]][param]


    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return

    # cleaning direcoty
    shutil.rmtree("blog", ignore_errors=False, onerror=rmTreeErrorHandler)
    os.makedirs("blog")
    currentBlog = Blog(themeFolder)
    currentBlog.export()

def edit(argv):
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        exit()

    if len(argv) != 1:
        print("VenC:", VenC.core.Messages.missingParams.format("--edit-and-export"))
        exit()
    
    try:
        proc = subprocess.Popen([VenC.core.blogConfiguration["textEditor"], argv[0]])
        while proc.poll() == None:
            pass
    except TypeError:
        print("VenC:", VenC.core.Messages.unknownTextEditor.format(VenC.core.blogConfiguration["textEditor"]))
        exit()
    except:
        raise
    blog(list())

class Blog:
    def __init__(self,themeFolder):
        self.theme = VenC.core.Theme(themeFolder)
        self.themeFolder = themeFolder
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
        self.initPatternProcessor()
        self.warnings = list()

    def CodeHighlight(self, argv):
        try:
            lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)

            formatter = pygments.formatters.HtmlFormatter(linenos=("inline" if argv[1]=="True" else False),cssclass="venc_source_"+argv[0].replace('+','Plus'))
            code = base64.b64decode(bytes(argv[2],encoding='utf-8'))
            result = pygments.highlight(code.decode("utf-8").replace("\:",":"), lexer, formatter)
            css  = formatter.get_style_defs('.venc_source_'+argv[0].replace('+','Plus'))
    
            msg = VenC.core.Messages.doNotForgetToIncludeCSSFileInHeader.format("venc_source_"+argv[0].replace('+','Plus')+".css")
            if not msg in self.warnings:
                print(msg)
                self.warnings.append(msg)

            if not os.path.exists(os.getcwd()+"/extra/venc_source_"+argv[0].replace('+','Plus')+".css"):
                stream = open(os.getcwd()+"/extra/venc_source_"+argv[0].replace('+','Plus')+".css",'w')
                stream.write(css)

            return result
    
        except Exception as e:
            raise
            print("VenC:", e)
            return str()

    def GetEntry(self, entryFilename, relativeOrigin=""):
        dump = yaml.load(self.entriesList[entryFilename].split("---\n")[0])
        if dump == None:
            return None

        output = dict()
        for key in dump.keys():
            if not key in ["authors","tags","categories","entry_name","doNotUseMarkdown"]:
                output["Entry"+key] = dump[key]
    

        # Optional since 1.2.0
        if "doNotUseMarkdown" in dump.keys():
            output["doNotUseMarkdown"] = True
        else:
            output["doNotUseMarkdown"] = False
   
        if "CSS" not in dump.keys():
            output["EntryCSS"] = ""

        output["EntryID"] = entryFilename.split('__')[0]
        output["EntryDate"] = VenC.core.GetFormattedDate(entryFilename.split('__')[1])

        try:
            output["EntryName"] = dump["entry_name"]
        except KeyError:
            print("VenC:",VenC.core.Messages.missingMandatoryFieldInEntry.format("entry_name", output["EntryID"]))
            exit()

        try:
            output["EntryAuthors"] = [ {"author":e} for e in list(dump["authors"].split(",") if dump["authors"] != str() else list()) ]
        except KeyError:
            print("VenC:",VenC.core.Messages.missingMandatoryFieldInEntry.format("authors", output["EntryID"]))
            exit()

        try:
            toBase64 = VenC.pattern.processor(".:",":.","::")
            toBase64.ressource = entryFilename
            toBase64.strict = False
            toBase64.SetFunction("CodeHighlight", VenC.core.ToBase64_)
            toBase64.preProcess(entryFilename,self.entriesList[entryFilename].split("---\n")[1])
            if output["doNotUseMarkdown"]:
                output["EntryContent"] = toBase64.parse(entryFilename)
            else:
                output["EntryContent"] = markdown.markdown( toBase64.parse(entryFilename) )
        except Exception as e:
            raise
            print("VenC:",VenC.core.Messages.possibleMalformedEntry.format(output["EntryID"]))
            exit()
        
        try:
            output["EntryTags"] = [ {"tag":e} for e in list(dump["tags"].split(",") if dump["tags"] != str() else list())]
        except KeyError:
            print("VenC:",VenC.core.Messages.missingMandatoryFieldInEntry.format("tags", output["EntryID"]))
            exit()
        except:
            output["EntryTags"] = list()
        try:
            entryPerCategories = GetEntriesPerCategories([entryFilename])
            output["EntryCategories"] = GetCategoriesTree(entryPerCategories, relativeOrigin, dict())
            output["EntryCategoriesLeaves"] = list()
            for category in dump["categories"].split(','):
                categoryLeaf= category.split(' > ')[-1].strip()
                if len(categoryLeaf) != 0:
                    categoryLeafUrl=str()
                    for subCategory in category.split(' > '):
                        categoryLeafUrl +=subCategory.strip()+'/'
                    output["EntryCategoriesLeaves"].append({"relativeOrigin":relativeOrigin, "categoryLeaf": categoryLeaf, "categoryLeafPath":categoryLeafUrl})
        except:
            output["EntryCategories"] = dict()
            output["EntryCategoriesLeaves"] = list()

        return output

    def IfInThread(self, argv):
        if self.inThread:
            return argv[0]
        else:
            return argv[1]

    def initPatternProcessor(self): 
        self.patternProcessor = VenC.pattern.processor(".:",":.","::")
        
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

        categoriesTree = VenC.core.GetCategoriesTree(self.entriesPerCategories, self.relativeOrigin, dict(), maxWeight=VenC.core.GetCategoriesTreeMaxWeight(self.entriesPerCategories))
        
        self.patternProcessor.Set("PagesList", VenC.core.GetListOfPages(int(VenC.core.blogConfiguration["entries_per_pages"]),len(inputEntries)))
        self.patternProcessor.Set("BlogCategories", categoriesTree)
        self.patternProcessor.Set("BlogDates", VenC.core.GetDatesList(self.entriesPerDates, self.relativeOrigin))
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
        self.exportExtraData(self.themeFolder+"/assets")
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

    def GetPreviousEntry(self, argv):

        trigger = False
        output = dict()
        try:
            pattern = argv[0]
        except IndexError:
            return self.handleError("GetPreviousEntry: "+VenC.core.Messages.notEnoughArgs,"~§GetPreviousEntry§§"+"§§".join(argv)+"§~",True)

        sortedEntries = VenC.core.GetSortedEntriesList(self.entriesList.keys())
        for i in range(0, len(sortedEntries)):
            if trigger == True:
                output["destinationPageUrl"] = VenC.core.blogConfiguration["path"]["entry_file_name"].format(entry_id=sortedEntries[i].split("__")[0])
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

        sortedEntries = list(reversed(VenC.core.GetSortedEntriesList(self.entriesList)))
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
        destinationPageUrl = VenC.core.blogConfiguration["path"]["index_file_name"].format(page_number=str(destinationPage))
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
        destinationPageUrl = VenC.core.blogConfiguration["path"]["index_file_name"].format(page_number= ("" if currentPage - 1 == 0 else str(currentPage - 1)))
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
        self.entry = VenC.core.MergeDictionnary(self.GetEntry(entry, self.relativeOrigin), self.publicDataFromBlogConf)
        
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
        self.outputPage += self.patternProcessor.parse("rssHeader")

        sortedEntries = VenC.core.GetSortedEntriesList(inputEntries)
        for entry in sortedEntries[:int(VenC.core.blogConfiguration["rss_thread_lenght"])]:
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
            entries_per_pages  = VenC.core.blogConfiguration["entries_per_pages"]
            columnsNumber = 1 if VenC.core.blogConfiguration["columns"] < 1 else int(VenC.core.blogConfiguration["columns"])

        sortedEntries = VenC.core.GetSortedEntriesList(inputEntries)
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
                self.WritePage(folderDestination, ( int(entry.split("__")[0]) if not inThread else -1))
            
                

