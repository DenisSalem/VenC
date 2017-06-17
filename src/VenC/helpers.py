#! /usr/bin/python3

import os
import time
import math
import yaml
import base64
import datetime
import pygments

from VenC.constants import MsgFormat 

# hold error messages
errors=list()

def Die(msg,color="RED"):
    Notify(msg, color)
    exit()

def Notify(msg, color="GREEN"):
    print(MsgFormat[color]+"\033[1mVenC: \033[0m"+MsgFormat[color]+msg+MsgFormat["END"])

def ToBase64_(argv):
    return "~§CodeHighlight§§"+argv[0]+"§§"+argv[1]+"§§"+base64.b64encode(bytes('\:\:'.join(argv[2:]),encoding='utf-8')).decode("utf-8", "strict")+"§~"

def orderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def MergeDictionnary(current,public):
    d = current.copy()
    d.update(public)
    return d 

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

def rmTreeErrorHandler(function, path, excinfo):
    if path == "blog" and excinfo[0] == FileNotFoundError:
        Die(Messages.blogFolderDoesntExists)

    Notify(function,"RED")
    Notify(path,"RED")
    Notify(excinfo[0],"RED")
    exit()
