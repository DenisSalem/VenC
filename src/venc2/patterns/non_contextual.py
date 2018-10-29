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
from venc2 import venc_version
from venc2.l10n import messages
from venc2.helpers import PatternInvalidArgument

def get_venc_version(argv):
    return venc_version

def include_file(argv):
    try:
        filename = argv[0]
        include_string = open("includes/"+filename, 'r').read()
        return include_string
    
    except PermissionError:
        raise PatternInvalidArgument("path", filename, messages.wrong_permissions.format(argv[0]))
    
    except FileNotFoundError:
        raise PatternInvalidArgument("path", filename, messages.file_not_found.format(filename))

def video(argv):
    source = ""
    for ext in argv[1].split(','):
        # Set media once, and get complete path later.
        source += "<source src=\".:GetRelativeOrigin:.{0}.{1}\" type=\"video/{1}\">\n".format(argv[0].strip(), ext.strip())
        
    f = {
        "source" : source,
        "poster" : argv[2].strip()
    }

    template = open('theme/chunks/video.html','r').read()
    try:
        return template.format(**f)

    except Exception as e:
        print(e, template)
        return template

non_contextual_pattern_names = {
    "GetVenCVersion" : get_venc_version,
    "IncludeFile" : include_file,
    "video" : video
}


