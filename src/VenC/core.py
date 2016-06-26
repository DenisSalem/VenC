#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import time
import datetime
import VenC.pattern

def GetMessages():
    import locale
    currentLocale = locale.getlocale()[0].split('_')[0]
    if currentLocale == 'fr':
        from VenC.languages import fr as language

    return language.Messages()

Messages = GetMessages()

def GetConfigurationFile():
    try:
        return yaml.load(open(os.getcwd()+"/blog_configuration.yaml",'r').read())
    except:
        return None

blogConfiguration = GetConfigurationFile()

def orderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def GetLatestEntryID():
    entriesList = GetEntriesList()
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
    for filename in sorted(files, key = lambda filename: orderableStrToInt(filename.split("__")[0])):
        explodedFilename = filename.split("__")
        try:
            date = explodedFilename[1].split('-')
            entryID = int(explodedFilename[0])
            datetime.datetime(year=int(date[2]),month=int(date[0]),day=int(date[1]),hour=int(date[3]),minute=int(date[4])) 
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
    print("VenC 1.0.0")

def GetEntriesPerKeys(entries, key):
    entriesPerKeys = dict()
    for entry in entries:
        stream = open(os.getcwd()+"/entries/"+entry,'r').read().split("---\n")[0]
        data = yaml.load(stream)
        for tag in data[key].split(","):
            try:
                entriesPerKeys[tag.strip()].append(entry)
            except KeyError as e:
                entriesPerKeys[tag.strip()] = [entry]

    return entriesPerKeys

def GetEntriesPerDates(entries):
    entriesPerDates = dict()
    for entry in entries:
        date = time.strftime(blogConfiguration["path"]["dates_directory_name"], time.strptime(entry.split("__")[1],"%m-%d-%Y-%M-%S"))
        try:
            entriesPerDates[date].append(entry)
        except KeyError as e:
            entriesPerDates[date] = [entry]

    return entriesPerDates

def GetEntriesPerCategories(entries):
    entriesPerCategories = dict()
        

class theme:
    def __init__(self):
        self.header = str()
        self.footer = str()
        self.entry = str()
        self.rssHeader = str()
        self.rssFooter = str()
        self.rssEntry = str()

        try:
            self.header = open(os.getcwd()+"/theme/chunk/header.html",'r').read()
            self.footer = open(os.getcwd()+"/theme/chunk/footer.html",'r').read()
            self.entry = open(os.getcwd()+"/theme/chunk/entry.html",'r').read()
            self.rssHeader = open(os.getcwd()+"/theme/chunk/rssHeader.html",'r').read()
            self.rssFooter = open(os.getcwd()+"/theme/chunk/rssFooter.html",'r').read()
            self.rssEntry = open(os.getcwd()+"/theme/chunk/rssEntry.html",'r').read()

        except FileNotFoundError as e:
            print("VenC: "+VenC.core.Messages.fileNotFound.format(str(e.filename)))
            exit()
