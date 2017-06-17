#! /usr/bin/python3

import os
import yaml
import codecs
import datetime
import subprocess

from VenC.configuration import BlogConfiguration
from VenC.l10n import Messages
from VenC.helpers import Notify
import VenC.helpers as Helpers
import VenC.pattern as Pattern

def NewEntry(argv):
    if len(argv) < 1:
        Notify(Messages.missingParams.format("--new-entry"))
        exit()
            
    content =   {"authors":	"",
		"tags":		"",
		"categories":	"",
                "CSS":     ""}

    try:
        wd = os.listdir(os.getcwd())

    except OSError:
        Notify(Messages.cannotReadIn.format(os.getcwd()))
        exit()

    date = datetime.datetime.now()

    entry = Helpers.SetNewEntryMetadata(date, argv[0])

    content["entry_name"] = argv[0]
    entryDate = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    outputFilename = os.getcwd()+'/entries/'+str(entry["EntryID"])+"__"+entryDate+"__"+content["entry_name"].replace(' ','_')

    if len(argv) == 1:
        stream = codecs.open(outputFilename,'w',encoding="utf-8")
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---\n"
        stream.write(output)
   
    else:
        try:
            output = open(os.getcwd()+'/templates/'+argv[1], 'r').read()
            patternProcessor = Pattern.Processor(".:",":.","::")
            currentData = Helpers.GetPublicDataFromBlogConf()
            currentData["EntryName"] = argv[0]
            currentData["EntryDate"] = Helpers.GetFormattedDate(entryDate)
            patternProcessor.SetWholeDictionnary(currentData)
            patternProcessor.ressource = '/templates/'+argv[1]
            patternProcessor.preProcess("new", output)
            output = patternProcessor.parse("new")
            stream = codecs.open(outputFilename,'w',encoding="utf-8")
            stream.write(output)

        except FileNotFoundError as e:
            Notify(Messages.fileNotFound.format(os.getcwd()+"/templates/"+argv[1]))
            exit()
    stream.close()

    try:
        command = BlogConfiguration["textEditor"].split(' ')
        command.append(outputFilename)
        subprocess.call(command) 

    except FileNotFoundError:
        Notify(Messages.unknownCommand.format(BlogConfiguration["textEditor"]))
        exit()

def NewBlog(argv):
    default_configuration =	{"blog_name":			Messages.blogName,
                                "textEditor":                   "nano",
                                "date_format":                  "%A %d. %B %Y",
				"author_name":			Messages.yourName,
				"blog_description":		Messages.blogDescription,
				"blog_keywords":		Messages.blogKeywords,
				"author_description":		Messages.aboutYou,
				"license":			Messages.license,
				"blog_url":			Messages.blogUrl,
                                "ftp_host":                     Messages.ftpHost,
				"blog_language":		Messages.blogLanguage,
				"author_email":			Messages.yourEmail,
				"path":				{"ftp":                         Messages.ftpPath,
                                                                "index_file_name":		"index{page_number}.html",
								"category_directory_name":	"{category}",
								"dates_directory_name":		"%Y-%m",
								"entry_file_name":		"entry{entry_id}.html",
								"rss_file_name":		"feed.xml"},
				"entries_per_pages":		10,
				"columns":			1,
				"rss_thread_lenght":		5,
				"thread_order":			"latest first"}
    for folder_name in argv:
        try:
            os.mkdir(folder_name)

        except OSError:
            Notify(Messages.fileAlreadyExists.format("--new-blog",os.getcwd()+'/'+folder_name))
            exit()

        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blog_configuration.yaml', 'w',encoding="utf-8")
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)
