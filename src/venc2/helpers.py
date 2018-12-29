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

import math
import base64
import datetime
import os
import pygments
import shutil

from venc2.l10n import messages


class GenericMessage(Exception):
    def __init__(self, message):
        self.message = message

msg_format = {
    "END" : '\033[0m',
    "GREEN" : '\033[92m',
    "RED" : '\033[91m',
    "YELLOW" : '\033[33m'
}

# hold error messages
errors=list()

def handle_malformed_patterns(e):
    if e.escape:
        if e.too_many_openings_symbols:
            die(messages.malformed_escape_patterns_missing_closing_symbols.format(e.ressource))
        die(messages.malformed_escape_patterns_missing_opening_symbols.format(e.ressource))
    
    if e.too_many_openings_symbols:
        die(messages.malformed_patterns_missing_closing_symbols.format(e.ressource))
    die(messages.malformed_patterns_missing_opening_symbols.format(e.ressource))

# Some data printed out may exceed few lines so
# it's nicer to highlight specific part of the output
def highlight_value(text, value, color="RED"):
    return text.replace(
        value,
        msg_format[color]+value+msg_format["END"]
    )

# Terminate nicely with notification
def die(msg, color="RED", extra=""):
    notify(msg, color)
    if extra != "":
        print(extra)
    exit()

# Being verborse is nice, with colours it's better
def notify(msg, color="GREEN"):
    print(get_formatted_message(msg, color))

# Take care of setting up colours in printed out message
def get_formatted_message(msg, color="GREEN", prompt="VenC: "):
    return msg_format[color]+"\033[1m"+prompt+"\033[0m"+msg_format[color]+msg+msg_format["END"]

def orderable_str_to_int(string):
    try:
        return int(string)

    except:
        return -1

def merge_dictionnaries(current, public):
    d = current.copy()
    d.update(public)
    return d 

def get_list_of_pages(entries_per_page, entries_count):
    list_of_pages = list()
    pages_count = math.ceil(entries_count/entries_per_page)
    for page_number in range(0,pages_count):
        list_of_pages.append(
            {
                "pageNumber": page_number,
                "pageUrl": "index"+str(page_number)+".html" if page_number != 0 else "index.html" 
            }
        )
    return list_of_pages

def rm_tree_error_handler(function, path, excinfo):
    if path == "blog" and excinfo[0] == FileNotFoundError:
        notify(messages.blog_folder_doesnt_exists,"YELLOW")
        return

    notify(str(function),"RED")
    notify(str(path),"RED")
    notify(str(excinfo[0]),"RED")
    exit()

def get_filename(index_filename, page_counter):
    return index_filename.format(page_number=(str(page_counter) if page_counter != 0 else str()))

def export_extra_data(origin, destination=""):
    try:
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    os.mkdir(os.getcwd()+"/blog/"+destination+item)
                    export_extra_data(origin+'/'+item, item+'/')
                except:
                    raise
            else:
                shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)
    except:
        raise

def remove_by_value(l, v):
    return [x for x in filter(lambda x : x != v, l)]
