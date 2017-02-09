#! /usr/bin/python3

import os
import time
import math
import yaml
import base64
import datetime
import pygments
import VenC.pattern
import pygments.lexers
import pygments.formatters

errors=list()

class OutputColors:
    FAIL = '\033[91m'
    END     = '\033[0m'

def GetMessages():
    import locale
    currentLocale = locale.getlocale()[0].split('_')[0]
    if currentLocale == 'fr':
        from VenC.languages import fr as language
    else:
        from VenC.languages import en as language
    return language.Messages()

Messages = GetMessages()

def CodeHighlight(argv):
    try:
        lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)

        formatter = pygments.formatters.HtmlFormatter(linenos=("inline" if argv[1]=="True" else False),cssclass="venc_source_"+argv[0])
        code = base64.b64decode(bytes(argv[2],encoding='utf-8'))
        result = pygments.highlight(code, lexer, formatter)
        css  = formatter.get_style_defs('.venc_source_'+argv[0])
    
        if not os.path.exists(os.getcwd()+"/extra/venc_source_"+argv[0]+".css"):
            print(Messages.doNotForgetToIncludeCSSFileInHeader.format("venc_source_"+argv[0]+".css"))
            stream = open(os.getcwd()+"/extra/venc_source_"+argv[0]+".css",'w')
            stream.write(css)

        return result

    except Exception as e:
        raise
        print("VenC:", e)
        return str()

class Key:
    def __init__(self, value, entry):
        self.count = 1
        self.weight = 1
        self.path = str()
        self.value = value
        self.relativeOrigin = str()
        self.relatedTo = [entry]
        self.childs = list()


class Theme:
    def __init__(self):
        self.header = str()
        self.footer = str()
        self.entry = str()
        self.rssHeader = str()
        self.rssFooter = str()
        self.rssEntry = str()

        try:
            self.header = open(os.getcwd()+"/theme/chunks/header.html",'r').read()
            self.footer = open(os.getcwd()+"/theme/chunks/footer.html",'r').read()
            self.entry = open(os.getcwd()+"/theme/chunks/entry.html",'r').read()
            self.rssHeader = open(os.getcwd()+"/theme/chunks/rssHeader.html",'r').read()
            self.rssFooter = open(os.getcwd()+"/theme/chunks/rssFooter.html",'r').read()
            self.rssEntry = open(os.getcwd()+"/theme/chunks/rssEntry.html",'r').read()

        except FileNotFoundError as e:
            print("VenC: "+Messages.fileNotFound.format(str(e.filename)))
            exit()

def GetConfigurationFile():
    try:
        blogConfiguration = yaml.load(open(os.getcwd()+"/blog_configuration.yaml",'r').read())
        
        mandatoryFields = [
            "blog_name",
            "textEditor",
            "date_format",
	    "author_name",
	    "blog_description",
	    "blog_keywords",
	    "author_description",
	    "license",
	    "url",
            "ftp_host",
	    "blog_language",
	    "email",
	    "entries_per_pages",
            "columns",
	    "rss_thread_lenght",
            "thread_order"
        ]

        everythingIsOkay = True
        for field in mandatoryFields:
            if not field in blogConfiguration.keys():
                everythingIsOkay = False
                print("VenC: "+Messages.missingMandatoryFieldInBlogConf.format(field))
        
        mandatoryFields = [
            "index_file_name",
	    "category_directory_name",
	    "dates_directory_name",
	    "entry_file_name",
	    "rss_file_name",
            "ftp"
        ]

        for field in mandatoryFields:
            if not field in blogConfiguration["path"].keys():
                everythingIsOkay = False
                print("VenC: "+Messages.missingMandatoryFieldInBlogConf.format(field))

        if not everythingIsOkay:
            return -1

        return blogConfiguration

    except:
        return None

blogConfiguration = GetConfigurationFile()
if blogConfiguration == -1:
    exit()

def orderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def GetLatestEntryID():
    entriesList = sorted(GetEntriesList(), key = lambda entry : int(entry.split("__")[0]))
    
    if len(entriesList) != 0:
        return int(entriesList[-1].split("__")[0])
    else:
        return 0

def GetEntriesList():
    try:
        files = os.listdir(os.getcwd()+"/entries")

    except FileNotFoundError as e:
        print("VenC: "+Messages.fileNotFound.format(os.getcwd()+"/entries"))
        exit()
    
    entries = dict()
    for filename in files:
        explodedFilename = filename.split("__")
        try:
            date = explodedFilename[1].split('-')
            entryID = int(explodedFilename[0])
            datetime.datetime(year=int(date[2]),month=int(date[0]),day=int(date[1]),hour=int(date[3]),minute=int(date[4])) 
            if entryID > 0:
                entries[filename] = open(os.getcwd()+"/entries/"+filename,'r').read()
        except ValueError:
            pass

        except IndexError:
            pass

    return entries

def GetSortedEntriesList(inputEntries):
    return sorted(inputEntries, key = lambda e : int(e.split("__")[0]), reverse=(blogConfiguration["thread_order"].strip() == "latest first"))

def MergeDictionnary(current,public):
    d = current.copy()
    d.update(public)
    return d

def GetPublicDataFromBlogConf():
    data = dict()
    data["AuthorName"] = blogConfiguration["author_name"]
    data["BlogName"] = blogConfiguration["blog_name"]
    data["BlogDescription"] = blogConfiguration["blog_description"]
    data["BlogKeywords"] = blogConfiguration["blog_keywords"]
    data["AuthorDescription"] = blogConfiguration["author_description"]
    data["License"] = blogConfiguration["license"]
    data["BlogUrl"] =blogConfiguration["url"]
    data["BlogLanguage"] = blogConfiguration["blog_language"]
    data["AuthorEmail"] = blogConfiguration["email"]
    return data

def SetNewEntryMetadata(entryDate, entryName):
    entry = dict()
    entry["EntryID"] = GetLatestEntryID()+1
    entry["EntryName"] = entryName
    entry["EntryMonth"] = entryDate.month
    entry["EntryYear"] = entryDate.year
    entry["EntryDay"] = entryDate.day
    entry["EntryHour"] = entryDate.hour
    entry["EntryMinute"] = entryDate.minute

    publicDataFromBlogConf = GetPublicDataFromBlogConf()
    for key in publicDataFromBlogConf:
        entry[key] = publicDataFromBlogConf[key]  

    return entry
    
def PrintVersion(argv):
    print("VenC 1.2.0")

def GetKeyByName(keys, name):
    for key in keys:
        if key.value == name:
            return key
    return None

def GetEntriesPerDates(entries):
    entriesPerDates = list()
    for entry in entries.keys():
        date = time.strftime(blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S"))
        try:
            selectedKey = GetKeyByName(entriesPerDates, date)
            selectedKey.relatedTo.append(entry)
            selectedKey.count+=1
        except:
            entriesPerDates.append(Key(date,entry))

    return entriesPerDates

def GetDatesList(keys, relativeOrigin):
    output = list()
    maxWeight = 0
    for key in keys:
        if maxWeight < key.count:
            maxWeight = key.count
        output.append({"date": key.value, "count":key.count,"dateUrl":relativeOrigin+key.value})

    for key in output:
        key["weight"] = str(int((key["count"]/maxWeight)*10))

    return sorted(output, key = lambda date: datetime.datetime.strptime(date["date"], blogConfiguration["path"]["dates_directory_name"])) 

def GetCategoriesList(entries):
    output = list()
    for entry in entries.keys():
        stream = entries[entry].split("---\n")[0]
        data = yaml.load(stream)
        if data != None:
            for category in data["categories"].split(","):
                if (not category in output) and category != '':
                    output.append(category)

    return output

def GetEntriesPerCategories(entries):
    entriesPerCategories = list()
    for entry in entries.keys():
        stream = entries[entry].split("---\n")[0]
        try:
            data = yaml.load(stream)
        except yaml.scanner.ScannerError:
            print("VenC:", VenC.core.Messages.possibleMalformedEntry.format(entry))
            exit()
        except yaml.parser.ParserError:
            print("VenC:", VenC.core.Messages.possibleMalformedEntry.format(entry))
            exit()

        if data != None:
            try:
                for category in data["categories"].split(","):
                    if category != '':
                        nodes = entriesPerCategories
                        path = str()
                        for subCategory in category.split(" > "):
                            path += subCategory+'/'
                            try:
                                selectedKey = GetKeyByName(nodes, subCategory.strip())
                                selectedKey.relatedTo.append(entry)
                                selectedKey.count += 1
                                selectedKey.relatedTo = list(set(selectedKey.relatedTo))
                            except Exception as e:
                                selectedKey = Key(subCategory.strip(), entry)
                                selectedKey.path = path
                                nodes.append(selectedKey)
                            
                            nodes = selectedKey.childs
                
            except TypeError:
                print("VenC:", VenC.core.Messages.possibleMalformedEntry.format(entry))
                exit()

    return entriesPerCategories 

def GetCategoriesTreeMaxWeight(categories, maxWeight=0):
    currentMaxWeight = maxWeight
    for category in categories:
        if category.count > currentMaxWeight:
            currentMaxWeight = category.count
        m = GetCategoriesTreeMaxWeight(category.childs, maxWeight=currentMaxWeight)
        if m > currentMaxWeight:
            currentMaxWeight = m

    return currentMaxWeight

def GetCategoriesTree(categories, relativeOrigin, root, maxWeight=None):
    node = root

    if len(categories) != 0:
        node["_nodes"] = dict()

    for category in categories:
        node[category.value] = dict()
        node[category.value]["__categoryPath"] = category.path
        if maxWeight != None:
            node[category.value]["__count"] = category.count
            node[category.value]["__weight"] = int((category.count/maxWeight) * 10)
        node[category.value]["__relativeOrigin"] = relativeOrigin
        if len(category.childs) != 0:
            node[category.value]["_nodes"] = dict()
            GetCategoriesTree(category.childs, relativeOrigin, node[category.value]["_nodes"], maxWeight)
    return node  

def ToBase64_(argv):
    return "~§CodeHighlight§§"+argv[0]+"§§"+argv[1]+"§§"+base64.b64encode(bytes(argv[2],encoding='utf-8')).decode("utf-8", "strict")+"§~"

def GetFormattedDate(unformattedDate):
    data = unformattedDate.split('-')
    return datetime.datetime(
        year=int(data[2]),
        month=int(data[0]),
        day=int(data[1]),
        hour=int(data[3]),
        minute=int(data[4])
    ).strftime(blogConfiguration["date_format"])

def GetListOfPages(entriesPerPage,entriesCount):
    listOfPages = list()
    pagesCount = math.ceil(entriesCount/entriesPerPage)
    for pageNumber in range(0,pagesCount):
        listOfPages.append(
            {
                "pageNumber": pageNumber,
                "pageUrl": "index"+str(pageNumber)+".html" if pageNumber != 0 else "index.html" 
            }
        )
    return listOfPages
