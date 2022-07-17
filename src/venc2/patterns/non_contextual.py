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

import hashlib
import json
import requests
import shutil
from venc2 import venc_version
from venc2.helpers import SafeFormatDict
from venc2.l10n import messages
from venc2.exceptions import VenCException # TODO: include when needed only
from venc2.prompt import notify
from urllib.parse import urlparse

theme_includes_dependencies = []

def disable_markup(node, *argv):
    return '::'.join(*argv)


def get_embed_content(providers, url):        
    try:
        key = [ key for key in providers["oembed"].keys() if url.netloc in key][0]

    except IndexError:
        raise VenCException(messages.unknown_provider.format(url.netloc))
    
    try:
        r = requests.get(providers["oembed"][key][0], params={
            "url": url.geturl(),
            "format":"json"
        })

    except requests.exceptions.ConnectionError as e:
        raise VenCException(messages.connectivity_issue+'\n'+str(e))

    if r.status_code != 200:
        raise VenCException(messages.ressource_unavailable.format(url.geturl()))

    try:
        html = json.loads(r.text)["html"]
        
    except Exception as e:
        raise VenCException(messages.response_is_not_json.format(url.geturl()))
        
    try:
        cache_filename = hashlib.md5(url.geturl().encode('utf-8')).hexdigest()
        shutil.os.makedirs("caches/embed", exist_ok=True)
        f = open("caches/embed/"+cache_filename, "w")
        f.write(html)
        f.close()

    except PermissionError:
        notify(messages.wrong_permissions.format("caches/embed/"+cache_filename), color="YELLOW")

    return html


def get_venc_version(node):
    return venc_version
    
# TODO : pattern args order is wrong, color should be first so string can be tuple cf set_style
def set_color(node, string, color):        
    return "<span class=\"__VENC_TEXT_COLOR__\" style=\"color: "+color+";\">"+string+"</span>"

def set_style(node, ID, CLASS, *string):
  
    return "<span "+ID.strip()+' '+CLASS.strip()+">"+('::'.join(string).strip() )+"</span>"


# TODO: Must fix dirty try/except structure.
# TODO: Add explicit message about exception. 

def include_file(node, filename, *argv, raise_error=True):       
    if filename == '':
        if not raise_error:
            return ""
            
        raise VenCException(messages.wrong_pattern_argument.format("path", filename, "include_file"))
    
    include_string = None
    paths = ("includes/"+filename, shutil.os.path.expanduser("~/.local/share/VenC/themes_includes/"+filename))
    for path in paths:
        if shutil.os.path.exists(path):
            try:
                include_string = open(path, 'r').read()
                break
                
            except PermissionError:
                if not raise_error:
                    return ""
                    
                raise VenCException(messages.wrong_permissions.format(path))
                
    if include_string == None:
        if not raise_error:
            return ""
            
        raise VenCException(
            '\n' + '\n'.join(
                (messages.file_not_found.format(path) for path in paths)
            )
        )
                
    if len(argv) > 1:            
        return include_string.format_map(SafeFormatDict(**{
            "venc_arg_"+str(index) : argv[index] for index in range(1, len(argv)) 
        }))
            
    else:
        return include_string

# TODO : Not document in pattern cheat sheet
def include_file_if_exists(node, filename, *argv):
    return include_file(node, filename, *argv, raise_error=False)

def table(node, *argv):
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
        
    return output + "</table></div>"

def escape(node, string, legacy_end_escape='', root_call=True):
    # TODO: when too much args are given
        
    while len(node.sub_strings):
        sub_node = node.sub_strings.pop()
        if len(sub_node.sub_strings) == 0:
            node.update_child(".:"+sub_node.name+"::"+("::".join(sub_node.args))+":.", sub_node, apply_offset=False)
        else:
            node.update_child(escape(sub_node, string, root_call=False), sub_node, apply_offset=False)

    # LEGACY TO DROP in 3.x.x
    return ( str(node)[10:-13] if len(legacy_end_escape) else str(node)[10:-2]) if root_call else str(node)
