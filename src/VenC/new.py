#! /usr/bin/python3

import os
import yaml
import codecs
import datetime
import subprocess

import VenC.core
import VenC.pattern

def entry(argv):
    if len(argv) < 1:
        print("VenC: "+VenC.core.Messages.missingParams.format("--new-entry"))
        return
    
    if VenC.core.blogConfiguration == None:
        print("VenC: "+VenC.core.Messages.noBlogConfiguration)
        return
            
    content =   {"authors":	"",
		"tags":		"",
		"categories":	"",
                "CSS":     ""}
    try:
        wd = os.listdir(os.getcwd())
    except OSError:
        print(VenC.core.Messages.cannotReadIn.format(os.getcwd()))
        return

    date = datetime.datetime.now()

    entry = VenC.core.SetNewEntryMetadata(date, argv[0])

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
            patternProcessor = VenC.pattern.processor(".:",":.","::")
            currentData = VenC.core.GetPublicDataFromBlogConf()
            currentData["EntryName"] = argv[0]
            currentData["EntryDate"] = VenC.core.GetFormattedDate(entryDate)
            patternProcessor.SetWholeDictionnary(currentData)
            patternProcessor.ressource = '/templates/'+argv[1]
            patternProcessor.preProcess("new",output)
            output = patternProcessor.parse("new")
            stream = codecs.open(outputFilename,'w',encoding="utf-8")
            stream.write(output)

        except FileNotFoundError as e:
            print("VenC: "+VenC.core.Messages.fileNotFound.format(os.getcwd()+"/templates/"+argv[1]))
            return
    stream.close()
    try:
        pass
        subprocess.call([VenC.core.blogConfiguration["textEditor"], outputFilename]) 
    except:
        pass

def blog(argv):
    default_configuration =	{"blog_name":			VenC.core.Messages.blogName,
                                "textEditor":                   "nano",
                                "date_format":                  "%A %d. %B %Y",
				"author_name":			VenC.core.Messages.yourName,
				"blog_description":		VenC.core.Messages.blogDescription,
				"blog_keywords":		VenC.core.Messages.blogKeywords,
				"author_description":		VenC.core.Messages.aboutYou,
				"license":			VenC.core.Messages.license,
				"blog_url":				VenC.core.Messages.blogUrl,
                                "ftp_host":                     VenC.core.Messages.ftpHost,
				"blog_language":		VenC.core.Messages.blogLanguage,
				"author_email":			VenC.core.Messages.yourEmail,
				"path":				{"ftp":                         VenC.core.Messages.ftpPath,
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
            print("VenC: "+VenC.core.Messages.fileAlreadyExists.format("--new-blog",os.getcwd()+'/'+folder_name))
            return
        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blog_configuration.yaml', 'w',encoding="utf-8")
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)
