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

from venc2 import venc_version
from venc2.l10n import messages
import venc2.helpers.PatternInvalidArgument

def get_venc_version(argv):
    try:
        include_string = open("includes/"+argv[0], 'r').read()
        return include_string
    
    except PermissionError:
        raise PatternInvalidArgument("path", argv[0], )
    
    except FileNotFoundError:
        raise PatternInvalidArgument("path", argv[0], )

non_contextual_pattern_name = {
    "GetVenCVersion" : get_venc_version
    "Include" : include
}


