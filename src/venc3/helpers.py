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

import math
import base64
import datetime
import os
import shutil

import pygments

from venc3.l10n import messages
from venc3.prompt import die
from venc3.prompt import notify

# Sometimes format fail with {something} not found in given dict.
class SafeFormatDict(dict):
    def __missing__(self, key):
        return '{'+key+'}'

# hold error messages
errors=list()

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

def quirk_encoding(string):
    return string.replace(
        '\'',
        '-'
    ).replace(
        ' ',
        '-'
    ).replace(
        '%',
        '-'
    )
    
def setup_categories_tree_base_sub_folder(categories_sub_folders):
    sub_folders = "\x1a"+categories_sub_folders

    try:
        if self.path_encoding == '':
            sub_folders = quirk_encoding(unidecode.unidecode(sub_folders))
        else:
            sub_folders = urllib_parse_quote(sub_folders, encoding=self.path_encoding)

    except UnicodeEncodeError as e:
        from venc3.exceptions import VenCException
        from venc3.l10n import messages
        raise VenCException(messages.encoding_error_in_categories_sub_folder_path)
                    
    self.categories_tree_base_sub_folders = (sub_folders if sub_folders[-1] == '/' else sub_folders+'/' )if sub_folders != '/' else ''
    return self.categories_tree_base_sub_folders
