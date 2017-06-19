#! /usr/bin/python3

import datetime
import markdown
import os
import time
import yaml

import VenC.pattern as Pattern

from VenC.configuration import GetBlogConfiguration
from VenC.configuration import GetPublicDataFromBlogConf
from VenC.helpers import Die
from VenC.helpers import GetFormattedDate
from VenC.helpers import ToBase64
from VenC.l10n import Messages
from VenC.metadata import Metadata

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
    ''' Loading '''
    rawData = open(os.getcwd()+"/entries/"+filename,'r').read()
    dump = yaml.load(rawData.split("---\n")[0])
    if dump == None:
        Die(Messages.possibleMalformedEntry.format(entryFilename))

    ''' Setting up optional metadata '''

    output = dict()
    for key in dump.keys():
        if not key in ["authors","tags","categories","entry_name","doNotUseMarkdown"]:
            output["Entry"+key] = dump[key]
    

    ''' Are we using markdown? '''
    if "doNotUseMarkdown" in dump.keys():
        output["doNotUseMarkdown"] = True
    else:
        output["doNotUseMarkdown"] = False
   
    output["EntryID"] = entryFilename.split('__')[0]
    output["EntryDate"] = GetFormattedDate(
        entryFilename.split('__')[1],
        dateFormat
    )

    ''' Setting up mandatory metadata ''' 

    try:
        output["EntryName"] = dump["entry_name"]

    except KeyError:
        Die(Messages.missingMandatoryFieldInEntry.format("entry_name", output["EntryID"]))

    try:
        output["EntryAuthors"] = [ {"author":e} for e in list(dump["authors"].split(",") if dump["authors"] != str() else list()) ]

    except KeyError:
        Die(Messages.missingMandatoryFieldInEntry.format("authors", output["EntryID"]))

    ''' Setting up the actual entry '''

    try:

        toBase64.preProcess(entryFilename, )
            output["EntryContent"] = rawData.split("---\n")[1]

    except Exception as e:
        Die(Messages.possibleMalformedEntry.format(output["EntryID"]))
        
    try:
        output["EntryTags"] = [ {"tag":e} for e in list(dump["tags"].split(",") if dump["tags"] != str() else list())]

    except KeyError:
        Die(Messages.missingMandatoryFieldInEntry.format("tags", output["EntryID"]))

    except:
        output["EntryTags"] = list()
    
    try:
        entryPerCategories = GetEntriesPerCategories([entryFilename])
        output["EntryCategories"] = GetMetadataTree(entryPerCategories, relativeOrigin)
        output["EntryCategoriesLeaves"] = list()
        for category in dump["categories"].split(','):
            categoryLeaf= category.split(' > ')[-1].strip()
            if len(categoryLeaf) != 0:
                categoryLeafUrl=str()
                for subCategory in category.split(' > '):
                    categoryLeafUrl +=subCategory.strip()+'/'
                
                output["EntryCategoriesLeaves"].append({
                    "relativeOrigin":relativeOrigin,
                    "categoryLeaf": categoryLeaf,
                    "categoryLeafPath":categoryLeafUrl
                })
    except:
        output["EntryCategories"] = dict()
        output["EntryCategoriesLeaves"] = list()

    return output
