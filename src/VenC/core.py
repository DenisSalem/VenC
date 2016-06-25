#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime

def GetMessages():
    import locale
    currentLocale = locale.getlocale()[0].split('_')[0]
    if currentLocale == 'fr':
        from VenC.languages import fr as language

    return language.Messages()

Messages = GetMessages()

def orderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def GetEntriesList():
    try:
        entries = os.listdir(os.getcwd()+"/entries")

    except FileNotFoundError as e:
        print("VenC: "+Messages.fileNotFound.format(os.getcwd()+"/entries"))
        exit()
    
    validFileNames = list()
    for filename in sorted(entries, key = lambda filename: orderableStrToInt(filename.split("__")[0])):
        explodedFilename = filename.split("__")
        try:
            entryID = int(explodedFilename[0])  
        
        except ValueError:
            pass

        except IndexError:
            pass

def PrintVersion(argv):
    print("VenC 1.0.0")

