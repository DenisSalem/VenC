#! /usr/bin/python3

import os
import yaml
from VenC.l10n import Messages

try:
    BlogConfiguration = yaml.load(open(os.getcwd()+"/blog_configuration.yaml",'r').read())
        
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
        if not field in BlogConfiguration.keys():
            everythingIsOkay = False
            print("VenC: "+Messages.missingMandatoryFieldInBlogConf.format(field))
        
    mandatoryFields = [
        "index_file_name",
	"category_directory_name",
	"dates_directory_name",
	"entry_file_name",
	"rss_file_name",
        "ftp"
    ]

    for field in mandatoryFields:
        if not field in BlogConfiguration["path"].keys():
            everythingIsOkay = False
            print("VenC: "+Messages.missingMandatoryFieldInBlogConf.format(field))

    if not everythingIsOkay:
        exit()

except FileNotFoundError:
    print("VenC: "+Messages.noBlogConfiguration)
    exit()

except PermissionError:
    print("VenC: "+Messages.noBlogConfiguration)
    exit()
