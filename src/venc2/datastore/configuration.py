#! /usr/bin/python3

#   Copyright 2016, 2017 Denis Salem

#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import os
import yaml

from venc2.helpers import die
from venc2.helpers import notify
from venc2.l10n import messages

def get_blog_configuration():
    try:
        blog_configuration = yaml.load(open(os.getcwd()+"/blogConfiguration.yaml",'r').read())
        
        mandatory_fields = [
            "blogName",
            "textEditor",
            "dateFormat",
	    "authorName",
	    "blogDescription",
	    "blogKeywords",
	    "authorDescription",
	    "license",
	    "blogUrl",
            "ftpHost",
	    "blogLanguage",
	    "authorEmail",
	    "entriesPerPages",
            "columns",
	    "rssThreadLenght",
            "reverseThreadOrder"
        ]

        everything_is_okay = True
        for field in mandatory_fields:
            if not field in blog_configuration.keys():
                everything_is_okay = False
                notify(messages.missing_mandatory_field_in_blog_conf.format(field),"RED")
        
        mandatory_fields = [
            "indexFileName",
	    "categoryDirectoryName",
	    "datesDirectoryName",
	    "entryFileName",
	    "rssFileName",
            "ftp"
        ]

        for field in mandatory_fields:
            if not field in blog_configuration["path"].keys():
                everything_is_okay = False
                notify(messages.missing_mandatory_field_in_blog_conf.format(field),"RED")

        if not everything_is_okay:
            exit()

        return blog_configuration

    except FileNotFoundError:
        die(messages.no_blog_configuration)

    except PermissionError:
        die(messages.no_blog_configuration)

    except yaml.scanner.ScannerError:
        die(messages.possible_malformed_blogC_configuration)
