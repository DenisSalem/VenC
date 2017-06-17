#! /usr/bin/python3

import os
import yaml

from VenC.helpers import Notify
from VenC.l10n import Messages

def GetPublicDataFromBlogConf(blogConfiguration):
    data = dict()
    for key in blogConfiguration.keys():
        if not key in ["path","rss_thread_lenght","textEditor","thread_order","ftp_host","date_format"]:
            formatted = "".join([ s.title() for s in  key.split("_")])
            data[formatted] = blogConfiguration[key]
    return data

def GetBlogConfiguration():
    try:
        blogConfiguration = yaml.load(open(os.getcwd()+"/blog_configuration.yaml",'r').read())
        
        mandatoryFields = [
            "blog_name",
            "textEditor",
            "date_format",
	    "author_name",
	    "blog_description",
	    "blog_keywords",
	    "author_description",
	    "license",
	    "blog_url",
            "ftp_host",
	    "blog_language",
	    "author_email",
	    "entries_per_pages",
            "columns",
	    "rss_thread_lenght",
            "thread_order"
        ]

        everythingIsOkay = True
        for field in mandatoryFields:
            if not field in blogConfiguration.keys():
                everythingIsOkay = False
                Notify(Messages.missingMandatoryFieldInBlogConf.format(field),"RED")
        
        mandatoryFields = [
            "index_file_name",
	    "category_directory_name",
	    "dates_directory_name",
	    "entry_file_name",
	    "rss_file_name",
            "ftp"
        ]

        for field in mandatoryFields:
            if not field in blogConfiguration["path"].keys():
                everythingIsOkay = False
                Notify(Messages.missingMandatoryFieldInBlogConf.format(field),"RED")

        if not everythingIsOkay:
            exit()

        return blogConfiguration

    except FileNotFoundError:
        Die(Messages.noBlogConfiguration)

    except PermissionError:
        Die(Messages.noBlogConfiguration)
