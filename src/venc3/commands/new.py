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

from venc3.datastore.configuration import get_blog_configuration
from venc3.datastore.entry import yield_entries_content

import venc3.datastore.entry as Entry

# Hold methods associated to patterns
class MinimalEntry:
    def __init__(self, data):
        for key in data.keys():
            setattr(self, key, data["key"])

def new_entry(params):
    if len(params) == 3:
        entry_name, template_name, template_args = params
        import json
        try:
            template_args = json.loads(template_args)
            template_args["venc_entry_title"] = entry_name
            
        except Exception as e:
            from venc3.exceptions import VenCException
            VenCException(("exception_place_holder", "JSON: "+str(e))).die()

    elif len(params) == 2:
        entry_name, template_name = params
        template_args = {"venc_entry_title":entry_name}
        
    elif len(params) == 1:
      entry_name = params[0]
      template_name = ''
      template_args = {"venc_entry_title":entry_name}

    else:
        from venc3.exceptions import VenCException
        VenCException(("wrong_args_number","< 3",len(params))).die()

    blog_configuration = get_blog_configuration()            
    content =   {
        "authors":	[''],
		    "tags":		[''],
		    "categories":	[''],
        "title":entry_name
    }

    try:
        wd = os.listdir(os.getcwd())

    except OSError:
        from venc3.prompt import die
        die(("cannot_read_in", os.getcwd()))

    date = datetime.datetime.now()

    entry = dict()
    raw_entry_date = datetime.datetime.now()
    try:
        entry["ID"] = max([ int(filename.split("__")[0]) for filename in yield_entries_content()]) + 1

    except ValueError:
        entry["ID"] = 1

    entry["title"] = entry_name
    entry["month"] = raw_entry_date.month
    entry["year"] = raw_entry_date.year
    entry["day"] = raw_entry_date.day
    entry["hour"] = raw_entry_date.hour
    entry["minute"] = raw_entry_date.minute
    entry["date"] = raw_entry_date

    entry_date = date.strftime("%m-%d-%Y-%H-%M")
    output_filename = os.getcwd()+'/entries/'+str(entry["ID"])+"__"+entry_date+"__"+entry["title"].replace(' ','_')

    stream = codecs.open(output_filename, 'w', encoding="utf-8")
    if not len(template_name):
        output = yaml.dump(content, default_flow_style=False, allow_unicode=True) + "---VENC-BEGIN-PREVIEW---\n---VENC-END-PREVIEW---\n"
    else:
        found_template = False
        templates_paths = [
            os.getcwd()+'/templates/'+template_name,
            os.path.expanduser("~/.local/share/VenC/themes_templates/"+template_name)
        ]
        for template_path in templates_paths:
            try:
                output = open(template_path, 'r').read().replace(".:GetEntryTitle:.", entry_name).format(**template_args)
                found_template = True
                break
            
            except KeyError as e:
                from venc3.exceptions import VenCException
                VenCException(("this_template_need_the_following_argument", template_name, str(e))).die()
            except FileNotFoundError:
                pass
                
            except PermissionError:
                from venc3.exceptions import VenCException
                os.remove(output_filename)
                VenCException(("wrong_permissions", template_path)).die()
        
        if not found_template:
            os.remove(output_filename)
            from venc3.prompt import VenCException, notify
            notify(("file_not_found", templates_paths[0]), color="RED")
            VenCException(("file_not_found", templates_paths[1])).die()
            
    stream.write(output)
    stream.close()

    try:
        if not "text_editor" in blog_configuration.keys():
            from venc3.prompt import notify
            notify(("missing_mandatory_field_in_blog_conf", "text_editor"), "YELLOW")
        
        elif type(blog_configuration["text_editor"]) != list:
            from venc3.prompt import notify
            notify(("blog_metadata_is_not_a_list", "text_editor"), "YELLOW")
            
        else:
            command = [str(arg) for arg in blog_configuration["text_editor"] if arg != '']
            command.append(output_filename)
            subprocess.call(command) 

    except FileNotFoundError:
        os.remove(output_filename)
        from venc3.prompt import die
        die(("unknown_command", blog_configuration["text_editor"]))
        
    from venc3.prompt import notify
    notify(("entry_written",))

def new_blog(blog_names):
    if len(blog_names) < 1:
        from venc3.prompt import die
        die(("missing_params", "--new-blog"))
        
    from venc3.l10n import messages
    default_configuration =	{
        "blog_name":			              messages.blog_name,
        "disable_threads":              None,
        "disable_archives":             False,
        "disable_categories":           False,
        "disable_chapters":             True,
        "disable_single_entries":       False,
        "disable_main_thread":          False,
        "disable_rss_feed":             False,
        "disable_atom_feed":            False,
        "text_editor":                  ["nano"],
        "date_format":                  "%A %d. %B %Y",
        "blog_url":			                messages.blog_url,
        "ftp_host":                     messages.ftp_host,
        "code_highlight_css_override":  False,
        "path":	{
            "ftp":                      messages.ftp_path,
            "entries_sub_folders":      "{entry_title}",
            "categories_sub_folders":   "",
            "archives_sub_folders":     "",
            "chapters_sub_folders":     "chapters",
            "index_file_name":		        "index{page_number}.html",
            "category_directory_name":	"{category}",
            "chapter_directory_name": 	"{chapter_name}",
			      "archives_directory_name":	"%Y-%m",
			      "entry_file_name":		        "index.html",
			      "rss_file_name":		          "rss.xml",
			      "atom_file_name":		        "atom.xml"
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
        "enable_jsonp":					False,
        "parallel_processing": 1
    }
    for folder_name in blog_names:
        try:
            os.mkdir(folder_name)

        except OSError:
            from venc3.prompt import die
            die(("file_already_exists", "--new-blog", os.getcwd()+'/'+folder_name))

        os.mkdir(folder_name+'/'+"blog")
        os.mkdir(folder_name+'/'+"entries")
        os.mkdir(folder_name+'/'+"theme")
        os.mkdir(folder_name+'/'+"includes")
        os.mkdir(folder_name+'/'+"extra")
        os.mkdir(folder_name+'/'+"templates")
        stream = codecs.open(folder_name+'/'+'blog_configuration.yaml', 'w',encoding="utf-8")
        default_configuration["blog_name"] = folder_name
        yaml.dump(default_configuration, stream, default_flow_style=False, allow_unicode=True)

    from venc3.prompt import notify
    notify(("blog_created" if len(blog_names) == 1 else "blogs_created",))
