#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
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

# Sometimes format fail with {something} not found in given dict.
class SafeFormatDict(dict):
    def __missing__(self, key):
        return '{'+key+'}'

def export_extra_data(origin, destination=""):
    import os
    import shutil

    try:
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    os.mkdir(os.getcwd()+"/blog/"+destination+item)
                    export_extra_data(origin+'/'+item, item+'/')
                except Exception as e:
                    #TODO : VenCException pleaaaaaase
                    raise e
            else:
                shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)
    except:
        raise

def quirk_encoding(string):
    import unidecode
    return unidecode.unidecode(
        string.replace(
            '\'',
            '-'
        ).replace(
            ' ',
            '-'
        ).replace(
            '%',
            '-'
        ).replace(
            ':',
            '-'
        )
    )

def rm_tree_error_handler(function, path, excinfo):
    from venc3.prompt import notify
    
    if path == "blog" and excinfo[0] == FileNotFoundError:
        notify(("blog_folder_doesnt_exists"),"YELLOW")
        return

    notify(("exception_place_holder", str(function)),"RED")
    notify(("exception_place_holder", str(path)),"RED")
    notify(("exception_place_holder", str(excinfo[0])),"RED")
    exit()
