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

import hashlib
import json
import os
import requests
from venc2 import venc_version
from venc2.l10n import messages
from venc2.helpers import PatternInvalidArgument
from venc2.helpers import GenericMessage
from venc2.helpers import notify
from urllib.parse import urlparse

def try_oembed(providers, url):
    try:
        key = [ key for key in providers["oembed"].keys() if url.netloc in key][0]

    except IndexError:
        raise PatternInvalidArgument("url", url.geturl(), messages.unknown_provider.format(url.netloc))
    
    try:
        r = requests.get(providers["oembed"][key][0], params={
            "url": url.geturl(),
            "format":"json"
        })
    except requests.exceptions.ConnectionError as e:
        raise GenericMessage(messages.connectivity_issue+'\n'+str(e))

    if r.status_code != 200:
        raise GenericMessage(messages.ressource_unavailable.format(url.geturl()))

    try:
        html = json.loads(r.text)["html"]
    except Exception as e:
        raise GenericMessage(messages.response_is_not_json.format(url.geturl()))
        
    try:
        cache_filename = hashlib.md5(url.geturl().encode('utf-8')).hexdigest()
        os.makedirs("caches/embed", exist_ok=True)
        f = open("caches/embed/"+cache_filename, "w")
        f.write(html)
        f.close()

    except PermissionError:
        notify(messages.wrong_permissions.format("caches/embed/"+cache_filename), color="YELLOW")

    return html

def get_embed_content(providers, argv):
    url = urlparse(argv[0])
    return try_oembed(providers, url)

def get_venc_version(argv):
    return venc_version

def set_color(argv):
    return "<span style=\"color: "+('::'.join(argv[1:]))+";\">"+argv[0]+"</span>"

def include_file(argv):
    try:
        filename = argv[0]
        include_string = open("includes/"+filename, 'r').read()
        return include_string
    
    except PermissionError:
        raise PatternInvalidArgument("path", filename, messages.wrong_permissions.format(argv[0]))
    
    except FileNotFoundError:
        raise PatternInvalidArgument("path", filename, messages.file_not_found.format(filename))

non_contextual_pattern_names = {
    "GetVenCVersion" : get_venc_version,
    "IncludeFile" : include_file,
    "SetColor" : set_color
}


