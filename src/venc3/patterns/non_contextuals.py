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

import json
import shutil
from venc3 import venc_version
from venc3.helpers import SafeFormatDict

theme_includes_dependencies = []

def disable_markup(pattern, *content):
    return '::'.join(content)
    
def html(pattern, *content):
    return "</p>"+('::'.join(content))+"<p>" if pattern.root.has_markup_language else '::'.join(content)
    
def get_venc_version(pattern):
    return venc_version

def set_background_color(pattern, color, string):        
    return "<span class=\"__VENC_TEXT_COLOR__\" style=\"background-color: "+color+";\">"+string+"</span>"
        
def set_color(pattern, color, string):        
    return "<span class=\"__VENC_TEXT_COLOR__\" style=\"color: "+color+";\">"+string+"</span>"

def set_style(pattern, tag_id, tag_class, *string):
    return "<span id=\""+tag_id.strip()+"\" class=\""+tag_class.strip()+"\">"+('::'.join(string).strip())+"</span>"

def include_file(pattern, filename, *argv, raise_error=True):
    '''venc_arg_1,venc_arg_2,venc_arg_n,...'''
    if filename == '':
        if not raise_error:
            return ""

        from venc3.exceptions import VenCException
        raise VenCException(("wrong_pattern_argument", "path", filename, "include_file"), pattern, pattern.root.string)
    
    include_string = None
    filename = filename.strip()
    paths = ("includes/"+filename,)
    for path in paths:
        if shutil.os.path.exists(path):
            try:
                include_string = open(path, 'r').read()
                break
                
            except PermissionError:
                if not raise_error:
                    return ""
                    
                from venc3.exceptions import VenCException
                raise VenCException(("wrong_permissions", path), pattern, pattern.root.string)
                
    if include_string == None:
        if not raise_error:
            return ""

        from venc3.exceptions import VenCException
        from venc3.l10n import messages
        raise VenCException(
            (
                "exception_place_holder", 
                ".:"+("::".join(pattern.payload))+":.\n" + '\n'.join(
                    (messages.file_not_found.format(path) for path in paths)
                )
            ),
            pattern,
            pattern.root.string
        )
                
    if len(argv) > 1:            
        return include_string.format_map(SafeFormatDict(**{
            "venc_arg_"+str(index) : argv[index] for index in range(1, len(argv)) 
        }))
            
    else:
        return include_string

def include_file_if_exists(pattern, filename, *argv):
    '''venc_arg_1,venc_arg_2,venc_arg_n,...'''
    return include_file(pattern, filename, *argv, raise_error=False)

def table(pattern, *argv):
    output = "<div class=\"__VENC_TABLE__\"><table>"
    tr = [[]]
    append_td = tr[-1].append
    append_tr = tr.append
    for cell in argv:
        cell_stripped = cell.strip()
        if cell_stripped == 'NewLine':
            append_tr([])
            append_td = tr[-1].append

        else:
            append_td("<td>"+cell_stripped+"</td>")
    
    join = ''.join
    for row in tr:
        output += "<tr>"+join(row)+"</tr>"
    
    output = output + "</table></div>"
    return "</p>"+output+"<p>" if pattern.root.has_markup_language else output

def escape_walk(root, node):
    for pattern in node.sub_patterns[::-1]:
        escape_walk(root, pattern)
        node.payload[pattern.payload_index] = node.payload[pattern.payload_index][:pattern.o] +".:"+("::".join(pattern.payload))+":."+ node.payload[pattern.payload_index][pattern.c:]
            
    if root == node:
        node.sub_patterns = []
        return "::".join(node.payload[1:])
    
def escape(pattern, *content):
    return escape_walk(pattern, pattern)
