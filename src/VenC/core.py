#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import time
import math
import markdown
import datetime
import pygments
import pygments.lexers
import pygments.formatters
import VenC.pattern


def GetMessages():
    import locale
    currentLocale = locale.getlocale()[0].split('_')[0]
    if currentLocale == 'fr':
        from VenC.languages import fr as language

    return language.Messages()

Messages = GetMessages()

def CodeHighlight(argv):
    try:
        lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)
        formatter = pygments.formatters.HtmlFormatter(linenos=(argv[1]=="True"),cssclass="venc_source_"+argv[0])
        code = argv[2]
        result = pygments.highlight(code, lexer, formatter)
        css  = formatter.get_style_defs('.venc_source_'+argv[0])
    
        if not os.path.exists(os.getcwd()+"/extra/venc_source_"+argv[0]+".css"):
            print(Messages.doNotForgetToIncludeCSSFileInHeader.format("venc_source_"+argv[0]+".css"))
            stream = open(os.getcwd()+"/extra/venc_source_"+argv[0]+".css",'w')
            stream.write(css)

        return result
    except Exception as e:
        print("VenC:", e)
        return str()

class Key:
    def __init__(self, value, entry):
        self.weight = 1
        self.value = value
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
    
    validFilenames = list()
    for filename in sorted(files, key = lambda filename: orderableStrToInt(filename.split("__")[0]), reverse=(blogConfiguration["thread_order"].strip() == "latest first")):
        explodedFilename = filename.split("__")
        try:
            date = explodedFilename[1].split('-')
            entryID = int(explodedFilename[0])
            datetime.datetime(year=int(date[2]),month=int(date[0]),day=int(date[1]),hour=int(date[3]),minute=int(date[4])) 
            if entryID > 0:
                validFilenames.append(filename)
        except ValueError:
            pass

        except IndexError:
            pass

    return validFilenames

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
    print("VenC 1.1.0")


def GetKeyByName(keys, name):
    for key in keys:
        if key.value == name:
            return key
    return None

def GetEntriesPerKeys(entries, keyType):
    entriesPerKeys = list()
    for entry in entries:
        stream = open(os.getcwd()+"/entries/"+entry,'r').read().split("---\n")[0]
        data = yaml.load(stream)
        try:
            for tag in data[keyType].split(","):
                try:
                    selectedKey = GetKeyByName(entriesPerKeys, tag)
                    selectedKey.relatedTo.append(entry)
                    # Must implement weight exploitation in upcoming version
                    selectedKey.weight+=1
                except:
                    entriesPerKeys.append(Key(tag,entry))
        except:
            return list()

    return entriesPerKeys

def GetEntriesPerDates(entries):
    entriesPerDates = list()
    for entry in entries:
        date = time.strftime(blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S"))
        try:
            selectedKey = GetKeyByName(entriesPerDates, date)
            selectedKey.relatedTo.append(entry)
            selectedKey.weight+=1
        except:
            entriesPerDates.append(Key(date,entry))

    return entriesPerDates

def GetDatesList(keys, relativeOrigin):
    output = list()
    for key in keys:
        output.append({"date": key.value, "weight":key.weight,"dateUrl":relativeOrigin+key.value})

    return output

def GetCategoriesList(entries):
    output = list()
    for entry in entries:
        stream = open(os.getcwd()+"/entries/"+entry,'r').read().split("---\n")[0]
        data = yaml.load(stream)
        if data != None:
            for category in data["categories"].split(","):
                if (not category in output) and category != '':
                    output.append(category)

    return output
            

def GetEntriesPerCategories(entries):
    entriesPerCategories = list()
    for entry in entries:
        stream = open(os.getcwd()+"/entries/"+entry,'r').read().split("---\n")[0]
        data = yaml.load(stream)
        if data != None:
            for category in data["categories"].split(","):
                if category != '':
                    nodes = entriesPerCategories
                    for subCategory in category.split(" > "):
                        try:
                            selectedKey = GetKeyByName(nodes, subCategory.strip())
                            selectedKey.relatedTo.append(entry)
                            selectedKey.relatedTo = list(set(selectedKey.relatedTo))
                            selectedKey.weight+=1
                        except:
                            selectedKey = Key(subCategory.strip(), entry)
                            nodes.append(selectedKey)

                        nodes = selectedKey.childs

    return entriesPerCategories 

def GetCategoriesTree(categories, relativeOrigin):
    output = {"_nodes":dict()}
    for category in categories:
        path = str()
        node = output["_nodes"]
        for subCategory in category.split(' > '):
            path += subCategory+'/'
            if not subCategory.strip() in node.keys():
                node[subCategory.strip()] = {"_nodes":dict()}
                node[subCategory.strip()]["__categoryPath"] = path.strip()
                node[subCategory.strip()]["__relativeOrigin"] = relativeOrigin
            node = node[subCategory.strip()]["_nodes"]

    return output

def GetEntry(entryFilename, relativeOrigin):
    stream = open(os.getcwd()+"/entries/"+entryFilename,'r').read()
    dump = yaml.load(stream.split("---\n")[0])
    if dump == None:
        return None
    output = dict()
    output["EntryContent"] = markdown.markdown(stream.split("---\n")[1])
    output["EntryID"] = entryFilename.split('__')[0]
    output["EntryName"] = dump["entry_name"]
    output["EntryDate"] = VenC.core.GetFormattedDate(entryFilename.split('__')[1])
    output["EntryAuthors"] = [ {"author":e} for e in list(dump["authors"].split(",") if dump["authors"] != str() else list()) ]
    try:
        output["EntryTags"] = [ {"tag":e} for e in list(dump["tags"].split(",") if dump["tags"] != str() else list())]
    except:
        output["entryTags"] = list()
    try:
        output["EntryCategories"] = GetCategoriesTree(dump["categories"].split(','), relativeOrigin)
        output["EntryCategoriesTop"] = list()
        for category in dump["categories"].split(','):
            categoryLeaf= category.split(' > ')[-1].strip()
            categoryLeafUrl=str()
            for subCategory in category.split(' > '):
                categoryLeafUrl +=subCategory.strip()+'/'
            output["EntryCategoriesTop"].append({"relativeOrigin":relativeOrigin, "categoryLeaf": categoryLeaf, "categoryLeafUrl":categoryLeafUrl})
    except:
        output["EntryCategories"] = dict()
        output["EntryCategoriesTop"] = list()

    return output

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
