#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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

from venc3.datastore.theme import theme

def get_media(media_type, target, extensions, poster=''):
    source = ""
    for ext in extensions.split(','):
        # Set media once, and get complete path later.
        source += str("<source src=\"{0}.{1}\" type=\""+media_type+"/{1}\">").format(target.strip(), ext.strip())
    
    f = {}
    f["source"] = source
    f["poster"] = ""
    
    if media_type == "video":
        f["poster"] = poster.strip().format(**{"relative_origin" : "\x1a/"})

    return getattr(theme, media_type).format(**f)

def get_audio(pattern, source, extensions):
    '''source'''
    return get_media("audio", source, extensions)

def get_video(pattern, source, extensions, poster=''):
    '''source,poster'''
    return get_media("video", source, extensions, poster)
