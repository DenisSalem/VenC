#! /usr/bin/python3

#    Copyright 2016, 2018 Denis Salem
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

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.entry import yield_entries_content
from venc2.helpers import notify
from venc2.helpers import die
from venc2.l10n import messages

import venc2.datastore.entry as Entry
import venc2.pattern as Pattern
import venc2.helpers as Helpers

# Hold methods associated to patterns
class MinimalEntry:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data["key"])

def new_entry(argv):
    blog_configuration = get_blog_configuration()
    if len(argv) < 1:
        die(messages.missing_params.format("--new-entry"))
            
    content =   {"authors":	"",
		"tags":		"",
		"categories":	"",
                "title":argv[0]}

    try:
        wd = os.listdir(os.getcwd())

    except OSError:
        die(messages.cannot_read_in.format(os.getcwd()))

    date = datetime.datetime.now()

    entry = dict()
    raw_entry_date = datetime.datetime.now()
    try:
        entry["ID"] = max([ int(filename.split("__")[0]) for filename in yield_entries_content()]) + 1

    except ValueError:
        entry["ID"] = 1

    entry["title"] = argv[0]
    entry["month"] = raw_entry_date.month
    entry["year"] = raw_entry_date.year
    entry["day"] = raw_entry_date.day
    entry["hour"] = raw_entry_date.hour
    entry["minute"] = raw_entry_date.minute
    entry["date"] = raw_entry_date



    entry_date = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    output_filename = os.getcwd()+'/entries/'+str(entry["ID"])+"__"+entry_date+"__"+entry["title"].replace(' ','_')

    stream = codecs.open(output_filename, 'w', encoding="utf-8")
    if len(argv) == 1:
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---\n"
   
    else:
        try:
            output = open(os.getcwd()+'/templates/'+argv[1], 'r').read()

        except FileNotFoundError as e:
            die(messages.file_not_found.format(os.getcwd()+"/templates/"+argv[1]))

    stream.write(output)
    stream.close()

    try:
        command = blog_configuration["textEditor"].split(' ')
        command.append(output_filename)
        subprocess.call(command) 

    except FileNotFoundError:
        die(messages.unknown_command.format(blog_configuration["textEditor"]))

    notify(messages.entry_written)

def new_blog(argv):
    if len(argv) < 1:
        die(Messages.missingParams.format("--new-blog"))

    default_configuration =	{"blogName":			messages.blog_name,
                                "textEditor":                   "nano",
                                "dateFormat":                  "%A %d. %B %Y",
				"authorName":			messages.your_name,
				"blogDescription":		messages.blog_description,
				"blogKeywords":		        messages.blog_keywords,
				"authorDescription":		messages.about_you,
				"license":			messages.license,
				"blogUrl":			messages.blog_url,
                                "ftpHost":                      messages.ftp_host,
				"blogLanguage":		        messages.blog_language,
				"authorEmail":			messages.your_email,
				"path":				{"ftp":                         messages.ftp_path,
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
            die(messages.file_already_exists.format("--new-blog",os.getcwd()+'/'+folder_name))

        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blogConfiguration.yaml', 'w',encoding="utf-8")
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)

    notify(messages.blog_created)
