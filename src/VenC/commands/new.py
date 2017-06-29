#! /usr/bin/python3

import os
import yaml
import codecs
import datetime
import subprocess

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.helpers import Notify
from VenC.helpers import Die
from VenC.l10n import Messages

import VenC.datastore.entry as Entry
import VenC.datastore.pattern as Pattern
import VenC.helpers as Helpers

def NewEntry(argv):
    blogConfiguration = GetBlogConfiguration()
    if len(argv) < 1:
        Die(Messages.missingParams.format("--new-entry"))
            
    content =   {"authors":	"",
		"tags":		"",
		"categories":	""}

    try:
        wd = os.listdir(os.getcwd())

    except OSError:
        Die(Messages.cannotReadIn.format(os.getcwd()))

    date = datetime.datetime.now()

    ''' NOT IMPLEMENTED YET
    entry = Entries.SetNewEntryMetadata(date, argv[0],  blogConfiguration)
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
    '''

    content["title"] = argv[0]
    entryDate = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    outputFilename = os.getcwd()+'/entries/'+str(entry["id"])+"__"+entryDate+"__"+content["title"].replace(' ','_')

    if len(argv) == 1:
        stream = codecs.open(outputFilename,'w',encoding="utf-8")
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---\n"
        stream.write(output)
   
    else:
        try:
            output = open(os.getcwd()+'/templates/'+argv[1], 'r').read()
            patternProcessor = Pattern.Processor(".:",":.","::")
            currentData = Helpers.GetPublicDataFromBlogConf(BlogConfiguration)
            currentData["EntryName"] = argv[0]
            currentData["EntryDate"] = Helpers.GetFormattedDate(entryDate)
            patternProcessor.SetWholeDictionnary(currentData)
            patternProcessor.ressource = '/templates/'+argv[1]
            patternProcessor.preProcess("new", output)
            output = patternProcessor.parse("new")
            stream = codecs.open(outputFilename,'w',encoding="utf-8")
            stream.write(output)

        except FileNotFoundError as e:
            Die(Messages.fileNotFound.format(os.getcwd()+"/templates/"+argv[1]))
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
                                                                "indexFileName":		"index{pageNumber}.html",
								"categoryDirectoryName":	"{category}",
								"datesDirectoryName":		"%Y-%m",
								"entryFileName":		"entry{id}.html",
								"rssFileName":		"feed.xml"},
				"entriesPerPages":		10,
				"columns":			1,
				"rssThreadLenght":		5,
				"reverseThreadOrder":		False}
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
