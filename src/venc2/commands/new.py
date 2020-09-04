#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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
from venc2.prompt import notify
from venc2.prompt import die
from venc2.l10n import messages

import venc2.datastore.entry as Entry

# Hold methods associated to patterns
class MinimalEntry:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data["key"])

def new_entry(argv):
    if len(argv) < 1:
        die(messages.missing_params.format("--new-entry"))
        
    blog_configuration = get_blog_configuration()            
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

    entry_date = date.strftime("%m-%d-%Y-%H-%M")
    output_filename = os.getcwd()+'/entries/'+str(entry["ID"])+"__"+entry_date+"__"+entry["title"].replace(' ','_')

    stream = codecs.open(output_filename, 'w', encoding="utf-8")
    if len(argv) == 1:
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---VENC-BEGIN-PREVIEW---\n---VENC-END-PREVIEW---\n"
   
    else:
        found_template = False
        templates_paths = [
            os.getcwd()+'/templates/'+argv[1],
            os.path.expanduser("~/.local/share/VenC/themes_templates/"+argv[1])
        ]
        for template_path in templates_paths:
            try:
                output = open(template_path, 'r').read().replace(".:GetEntryTitle:.", argv[0])
                found_template = True
                break
                
            except FileNotFoundError:
                pass
                
            except PermissionError:
                os.remove(output_filename)
                die(messages.wrong_permissions.format(template_path))
        
        if not found_template:
            os.remove(output_filename)
            notify(messages.file_not_found.format(templates_paths[0]), color="RED")
            die(messages.file_not_found.format(templates_paths[1]))
            
    stream.write(output)
    stream.close()

    try:
        command = [arg for arg in blog_configuration["text_editor"].split(' ') if arg != '']
        command.append(output_filename)
        subprocess.call(command) 

    except FileNotFoundError:
        os.remove(output_filename)
        die(messages.unknown_command.format(blog_configuration["text_editor"]))

    notify(messages.entry_written)

def new_blog(argv):
    if len(argv) < 1:
        die(messages.missing_params.format("--new-blog"))

    default_configuration =	{
        "blog_name":			        messages.blog_name,
        "disable_threads":              "",
        "disable_archives":             False,
        "disable_categories":           False,
        "disable_chapters":             True,
        "disable_single_entries":       False,
        "disable_main_thread":          False,
        "disable_rss_feed":             False,
        "disable_atom_feed":            False,
        "text_editor":                  "nano",
        "date_format":                  "%A %d. %B %Y",
        "author_name":			        messages.your_name,
        "blog_description":		        messages.blog_description,
        "blog_keywords":	            messages.blog_keywords,
        "author_description":		    messages.about_you,
        "license":			            messages.license,
        "blog_url":			            messages.blog_url,
        "ftp_host":                     messages.ftp_host,
        "blog_language":	            messages.blog_language,
        "author_email":	                messages.your_email,
        "code_highlight_css_override":  False,
        "path":	{
            "ftp":                      messages.ftp_path,
            "entries_sub_folders":      "",
            "categories_sub_folders":   "",
            "archives_sub_folders":        "",
            "chapters_sub_folders":     "chapters",
            "index_file_name":		    "index{page_number}.html",
            "category_directory_name":	"{category}",
            "chapter_directory_name":	"{chapter_name}",
			"archives_directory_name":	"%Y-%m",
			"entry_file_name":		    "entry{entry_id}.html",
			"rss_file_name":		    "rss.xml",
			"atom_file_name":		    "atom.xml"
        },
        "entries_per_pages":		    10,
        "columns":			            1,
        "feed_lenght":	        	    5,
        "reverse_thread_order":		    True,
        "markup_language":              "Markdown",
        "path_encoding":                "",
        "server_port":                  8888,
        "sort_by":                      "id",
        "enable_jsonld":                False,
        "enable_jsonp":					False
    }
    for folder_name in argv:
        try:
            os.mkdir(folder_name)

        except OSError:
            die(messages.file_already_exists.format("--new-blog",os.getcwd()+'/'+folder_name))

        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"includes")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blog_configuration.yaml', 'w',encoding="utf-8")
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)

    notify(messages.blog_created)
