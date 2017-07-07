#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

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

# Some data printed out may exceed few lines so
# it's nicer to highlight specific part of the output
def HighlightValue(text, value, color="RED"):
    return text.replace(
        value,
        MsgFormat[color]+value+MsgFormat["END"]
    )

# Terminate nicely with notification
def Die(msg,color="RED"):
    Notify(msg, color)
    exit()

# Being verborse is nice, with colours it's better
def Notify(msg, color="GREEN"):
    print(GetFormattedMessage(msg, color))

# Take care of setting up colours in printed out message
def GetFormattedMessage(msg, color="GREEN"):
    return MsgFormat[color]+"\033[1mVenC: \033[0m"+MsgFormat[color]+msg+MsgFormat["END"]

def OrderableStrToInt(string):
    try:
        return int(string)

    except:
        return -1

def MergeDictionnaries(current,public):
    d = current.copy()
    d.update(public)
    return d 

''' deprecated
def GetFormattedDate(unformattedDate, dateFormat):
    data = unformattedDate.split('-')
    return data.strftime(
        dateFormat
    )
'''

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

def RemoveByValue(l, v):
    return [x for x in filter(lambda x : x != v, l)]
