#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import yaml
import codecs
import VenC.core

def entry(argv):
    if len(argv) != 1:
        print("VenC: "+VenC.core.Messages.missingParams.format("--new-entry"))
        return
    default=		{"authors":	"",
		  	"tags":		"",
			"categories":	""}
    try:
        wd = os.listdir(os.getcwd())
    except OSError:
        print(VenC.core.Messages.cannotReadIn.format(os.getcwd()))
        return
    entry_id = VenC.core.GetEntriesList()
    exit
    #default["entry_name"] = argv[0]
    #outputFilename = os.getcwd()+'/entries/'+str(entry_id)+"__"+str(datetime.now().month)+'-'+str(datetime.now().day)+'-'+str(datetime.today().year)+'-'+str(datetime.now().hour)+'-'+str(datetime.now().minute)+"__"+default["entry_name"].replace(' ','_')
    #stream = codecs.open(outputFilename,'w',encoding="utf-8")
    #yaml.dump(default, stream, default_flow_style=False, allow_unicode=True) + "---\n"

def blog(argv):
    default_configuration =	{"blog_name":			VenC.core.Messages.blogName,
				"author_name":			VenC.core.Messages.yourName,
				"blog_description":		VenC.core.Messages.blogDescription,
				"blog_keywords":		VenC.core.Messages.blogKeywords,
				"author_description":		VenC.core.Messages.aboutYou,
				"license":			VenC.core.Messages.license,
				"url":				VenC.core.Messages.blogUrl,
				"blog_language":		VenC.core.Messages.blogLanguage,
				"email":			VenC.core.Messages.yourEmail,
				"path":				{"root": "./",
								"index_file_name":			"index{page_number}.html",
								"categories_directory_name":		"{category}",
								"tags_directory_name":			"{tag}",
								"authors_directory_name":		"{author}",
								"dates_directory_name":			"%Y-%m",
								"entry_file_name":			"entry{entry_id}.html",
								"archives_overview_directory_name":	"overview"},
								"rss_file_name":			"feed.xml",
				"entries_per_pages":		10,
				"columns":			3,
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
