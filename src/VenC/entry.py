#! /usr/bin/python3

import datetime
import os
import time
import yaml

class Entry:
    def __init__(self, filename):
        ''' Loading '''
        rawData = open(os.getcwd()+"/entries/"+filename,'r').read()
        try:
            metadata = yaml.load(rawData.split("---\n")[0])

        if metadata == None:
            Die(Messages.possibleMalformedEntry.format(entryFilename))

        ''' Setting up optional metadata '''

        for key in metadata.keys():
            if not key in ["authors","tags","categories","entry_name","doNotUseMarkdown"]:
                setattr(self, key, metadata[key])
    
        ''' Are we using markdown? '''
        if "doNotUseMarkdown" in metadata.keys():
            self.doNotUseMarkdown = True
        else:
            self.doNotUseMarkdown = False
    
        ''' Set up id '''
        self.id = entryFilename.split('__')[0]
        
        ''' Set up date '''
        rawDate = entryFilename.split('__')[1].split('-')
        self.date = datetime.datetime(
            year=int(rawDate[2]),
            month=int(rawDate[0]),
            day=int(rawDate[1]),
            hour=int(rawDate[3]),
            minute=int(rawDate[4])
        )
        
        ''' Setting up title '''
        try:
            self.title = metadata["title"]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("title", self.id))

        ''' Setting up authors '''
        try:
            self.authors = [ e for e in list(metadata["authors"].split(",") if metadata["authors"] != str() else list()) ]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("authors", self.id))

        ''' Setting up the actual entry '''
        try:
            output["EntryContent"] = rawData.split("---\n")[1]

        except
            Die(Messages.possibleMalformedEntry.format(output["EntryID"]))

        ''' Setting up tags '''
        try:
            self.tags = [ {"tag":e} for e in list(metadata["tags"].split(",") if metadata["tags"] != str() else list())]

        except KeyError:
            Die(Messages.missingMandatoryFieldInEntry.format("tags", self.id))

def GetSortedEntriesList(inputEntries, threadOrder):
    return sorted(inputEntries, key = lambda e : int(e.split("__")[0]), reverse=(threadOrder.strip() == "latest first"))

def GetEntriesList():
    try:
        files = os.listdir(os.getcwd()+"/entries")

    except FileNotFoundError as e:
        Die(Messages.fileNotFound.format(os.getcwd()+"/entries"))
    
    entries = list()
    for filename in files:
        explodedFilename = filename.split("__")
        try:
            date = explodedFilename[1].split('-')
            entryID = int(explodedFilename[0])
            datetime.datetime(
                year=int(date[2]),
                month=int(date[0]),
                day=int(date[1]),
                hour=int(date[3]),
                minute=int(date[4])
            ) 
            if entryID > 0:
                entries.append(filename)
        except ValueError:
            Notify(Messages.invalidEntryFilename.format(filename), "YELLOW")

        except IndexError:
            Notify(Messages.invalidEntryFilename.format(filename), "YELLOW")

    return entries

''' 
def GetLatestEntryID():
    entriesList = sorted(GetEntriesList(), key = lambda entry : int(entry.split("__")[0]))
    
    if len(entriesList) != 0:
        return int(entriesList[-1].split("__")[0])
    else:
        return 0

def SetNewEntryMetadata(entryDate, entryName, blogConfiguration):
    entry = dict()
    entry["EntryID"] = GetLatestEntryID()+1
    entry["EntryName"] = entryName
    entry["EntryMonth"] = entryDate.month
    entry["EntryYear"] = entryDate.year
    entry["EntryDay"] = entryDate.day
    entry["EntryHour"] = entryDate.hour
    entry["EntryMinute"] = entryDate.minute

    publicDataFromBlogConf = GetPublicDataFromBlogConf(blogConfiguration)
    for key in publicDataFromBlogConf:
        entry[key] = publicDataFromBlogConf[key]  

    return entry

def GetEntriesPerDates(entries, datesDirectoryName):
    entriesPerDates = list()
    for entry in entries.keys():
        date = time.strftime(datesDirectoryName, time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S"))
        try:
            selectedKey = GetKeyByName(entriesPerDates, date)
            selectedKey.relatedTo.append(entry)
            selectedKey.count+=1
        except:
            entriesPerDates.append(Metadata(date,entry))

    return entriesPerDates

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
            Die(Messages.possibleMalformedEntry.format(entry))

        except yaml.parser.ParserError:
            Die(Messages.possibleMalformedEntry.format(entry))

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
                                selectedKey = Metadata(subCategory.strip(), entry)
                                selectedKey.path = path
                                nodes.append(selectedKey)
                            
                            nodes = selectedKey.childs
                
            except TypeError:
                Die(Messages.possibleMalformedEntry.format(entry))

    return entriesPerCategories

def GetEntry(entryFilename):



        
    
    try:
        output["EntryCategoriesLeaves"] = list()
        for category in dump["categories"].split(','):
            categoryLeaf= category.split(' > ')[-1].strip()
            if len(categoryLeaf) != 0:
                categoryLeafUrl=str()
                for subCategory in category.split(' > '):
                    categoryLeafUrl +=subCategory.strip()+'/'
                
                output["EntryCategoriesLeaves"].append({
                    "categoryLeaf": categoryLeaf,
                    "categoryLeafPath":categoryLeafUrl
                })
    except:
        output["EntryCategories"] = dict()
        output["EntryCategoriesLeaves"] = list()

    return output 
'''
