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

import os
import yaml
import codecs
import datetime
import subprocess

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.datastore.entry import YieldEntriesContent
from VenC.helpers import Notify
from VenC.helpers import Die
from VenC.l10n import Messages

import VenC.datastore.entry as Entry
import VenC.pattern as Pattern
import VenC.helpers as Helpers

# Hold methods associated to patterns
class MinimalEntry:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data["key"])

def NewEntry(argv):
    blogConfiguration = GetBlogConfiguration()
    if len(argv) < 1:
        Die(Messages.missingParams.format("--new-entry"))
            
    content =   {"authors":	"",
		"tags":		"",
		"categories":	"",
                "title":argv[0]}

    try:
        wd = os.listdir(os.getcwd())

    except OSError:
        Die(Messages.cannotReadIn.format(os.getcwd()))

    date = datetime.datetime.now()

    entry = dict()
    rawEntryDate = datetime.datetime.now()
    try:
        entry["ID"] = max([ int(filename.split("__")[0]) for filename in YieldEntriesContent()]) + 1
    except ValueError:
        entry["ID"] = 1

    entry["title"] = argv[0]
    entry["month"] = rawEntryDate.month
    entry["year"] = rawEntryDate.year
    entry["day"] = rawEntryDate.day
    entry["hour"] = rawEntryDate.hour
    entry["minute"] = rawEntryDate.minute
    entry["date"] = rawEntryDate



    entryDate = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    outputFilename = os.getcwd()+'/entries/'+str(entry["ID"])+"__"+entryDate+"__"+entry["title"].replace(' ','_')

    stream = codecs.open(outputFilename,'w',encoding="utf-8")
    if len(argv) == 1:
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---\n"
   
    else:
        try:
            output = open(os.getcwd()+'/templates/'+argv[1], 'r').read()

        except FileNotFoundError as e:
            Die(Messages.fileNotFound.format(os.getcwd()+"/templates/"+argv[1]))

    stream.write(output)
    stream.close()

    try:
        command = blogConfiguration["textEditor"].split(' ')
        command.append(outputFilename)
        subprocess.call(command) 

    except FileNotFoundError:
        Die(Messages.unknownCommand.format(blogConfiguration["textEditor"]))

    Notify(Messages.entryWritten)

def NewBlog(argv):
    if len(argv) < 1:
        Die(Messages.missingParams.format("--new-blog"))

    default_configuration =	{"blogName":			Messages.blogName,
                                "textEditor":                   "nano",
                                "dateFormat":                  "%A %d. %B %Y",
				"authorName":			Messages.yourName,
				"blogDescription":		Messages.blogDescription,
				"blogKeywords":		        Messages.blogKeywords,
				"authorDescription":		Messages.aboutYou,
				"license":			Messages.license,
				"blogUrl":			Messages.blogUrl,
                                "ftpHost":                      Messages.ftpHost,
				"blogLanguage":		        Messages.blogLanguage,
				"authorEmail":			Messages.yourEmail,
				"path":				{"ftp":                         Messages.ftpPath,
                                                                "indexFileName":		"index{0[pageNumber]}.html",
								"categoryDirectoryName":	"{category}",
								"datesDirectoryName":		"%Y-%m",
								"entryFileName":		"entry{0[entryId]}.html",
								"rssFileName":		"feed.xml"},
				"entriesPerPages":		10,
				"columns":			1,
				"rssThreadLenght":		5,
				"reverseThreadOrder":		True}
    for folder_name in argv:
        try:
            os.mkdir(folder_name)

        except OSError:
            Die(Messages.fileAlreadyExists.format("--new-blog",os.getcwd()+'/'+folder_name))

        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blogConfiguration.yaml', 'w',encoding="utf-8")
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)

    Notify(Messages.blogCreated)
