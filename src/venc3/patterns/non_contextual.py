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
import shutil
from venc3 import venc_version
from venc3.helpers import SafeFormatDict

theme_includes_dependencies = []

def disable_markup(node, *argv):
    return '::'.join(argv)


def get_embed_content(node, providers, target):  
    try:
        import requests

    except:
        from venc3.exceptions import VenCException
        raise VenCException(("module_not_found", "requests"), node)

    from urllib.parse import urlparse
    url = urlparse(target)

    try:
        key = [ key for key in providers["oembed"].keys() if url.netloc in key][0]

    except IndexError:
        from venc3.exceptions import VenCException
        raise VenCException(("unknown_provider", url.netloc), node)
    
    try:
        r = requests.get(providers["oembed"][key][0], params={
            "url": url.geturl(),
            "format":"json",
            "maxwidth": 640,
            "maxheight": 320
        })

    except requests.exceptions.ConnectionError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("connectivity_issue", str(e)), node)

    if r.status_code != 200:
        from venc3.exceptions import VenCException
        raise VenCException(("ressource_unavailable", url.geturl()), node)

    try:
        html = "<div class=\"__VENC_OEMBED__\">"+json.loads(r.text)["html"]+"</div>"
        html = "</p>"+html+"<p>" if node.root.has_markup_language else html
        
    except Exception as e:
        from venc3.exceptions import VenCException
        raise VenCException(("response_is_not_json", url.geturl()), node)
        
    try:
        cache_filename = hashlib.md5(url.geturl().encode('utf-8')).hexdigest()
        shutil.os.makedirs("caches/embed", exist_ok=True)
        f = open("caches/embed/"+cache_filename, "w")
        f.write(html)
        f.close()

    except PermissionError:
        from venc3.prompt import notify
        notify(("wrong_permissions", "caches/embed/"+cache_filename), color="YELLOW")
    return html

def get_venc_version(node):
    return venc_version
    
def set_color(node, color, string):        
    return "<span class=\"__VENC_TEXT_COLOR__\" style=\"color: "+color+";\">"+string+"</span>"

def set_style(node, ID, CLASS, *string):
    return "<span id=\""+ID.strip()+"\" class=\""+CLASS.strip()+"\">"+('::'.join(string).strip())+"</span>"


def include_file(node, filename, *argv, raise_error=True):
    if filename == '':
        if not raise_error:
            return ""

        from venc3.exceptions import VenCException
        raise VenCException(("wrong_pattern_argument", "path", filename, "include_file"), node, node.root.string)
    
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
                    
                from venc3.exceptions import VenCException
                raise VenCException(("wrong_permissions", path), node, node.root.string)
                
    if include_string == None:
        if not raise_error:
            return ""

        from venc3.exceptions import VenCException
        from venc3.l10n import messages
        raise VenCException(
            (
                "exception_place_holder", 
                ".:"+("::".join(node.payload))+":.\n" + '\n'.join(
                    (messages.file_not_found.format(path) for path in paths)
                )
            ),
            node,
            node.root.string
        )
                
    if len(argv) > 1:            
        return include_string.format_map(SafeFormatDict(**{
            "venc_arg_"+str(index) : argv[index] for index in range(1, len(argv)) 
        }))
            
    else:
        return include_string

# TODO : Not documented in pattern cheat sheet
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

def escape_walk(root, node):
    for pattern in node.sub_patterns[::-1]:
        escape_walk(root, pattern)
        node.payload[pattern.payload_index] = node.payload[pattern.payload_index][:pattern.o] +".:"+("::".join(pattern.payload))+":."+ node.payload[pattern.payload_index][pattern.c:]

    if root == node:
        node.sub_patterns = []
        return "::".join(node.payload[1:])
    
def escape(pattern, *string):
    return escape_walk(pattern, pattern)
