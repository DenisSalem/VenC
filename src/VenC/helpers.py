#! /usr/bin/python3

import math
import base64
import datetime
import os
import pygments
import shutil

MsgFormat = {
    "END" : '\033[0m',
    "GREEN" : '\033[92m',
    "RED" : '\033[91m',
    "YELLOW" : '\033[33m'
}

# hold error messages
errors=list()

def HighlightValue(text, value, color="RED"):
    return text.replace(
        value,
        MsgFormat[color]+value+MsgFormat["END"]
    )

def Die(msg,color="RED"):
    Notify(msg, color)
    exit()

def Notify(msg, color="GREEN"):
    print(GetFormattedMessage(msg, color))

def GetFormattedMessage(msg, color="GREEN"):
    return MsgFormat[color]+"\033[1mVenC: \033[0m"+MsgFormat[color]+msg+MsgFormat["END"]

def ToBase64(argv):
    return "~§CodeHighlight§§"+argv[0]+"§§"+argv[1]+"§§"+base64.b64encode(bytes('\:\:'.join(argv[2:]),encoding='utf-8')).decode("utf-8", "strict")+"§~"

def OrderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def MergeDictionnaries(current,public):
    d = current.copy()
    d.update(public)
    return d 

# deprecated
def GetFormattedDate(unformattedDate, dateFormat):
    data = unformattedDate.split('-')
    return data.strftime(
        dateFormat
    )

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

def RmTreeErrorHandler(function, path, excinfo):
    if path == "blog" and excinfo[0] == FileNotFoundError:
        Die(Messages.blogFolderDoesntExists)

    Notify(function,"RED")
    Notify(path,"RED")
    Notify(excinfo[0],"RED")
    exit()

def GetFilename(indexFileName, pageCounter):
    return indexFileName.format(page_number=(str(pageCounter) if pageCounter != 0 else str()))

def ExportExtraData(origin, destination=""):
    try:
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    os.mkdir(os.getcwd()+"/blog/"+destination+item)
                    ExportExtraData(origin+'/'+item, item+'/')
                except:
                    raise
            else:
                shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)
    except:
        raise

