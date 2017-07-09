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

from VenC.helpers import Die
from VenC.helpers import Notify
from VenC.l10n import Messages

def GetBlogConfiguration():
    try:
        blogConfiguration = yaml.load(open(os.getcwd()+"/blogConfiguration.yaml",'r').read())
        
        mandatoryFields = [
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

        everythingIsOkay = True
        for field in mandatoryFields:
            if not field in blogConfiguration.keys():
                everythingIsOkay = False
                Notify(Messages.missingMandatoryFieldInBlogConf.format(field),"RED")
        
        mandatoryFields = [
            "indexFileName",
	    "categoryDirectoryName",
	    "datesDirectoryName",
	    "entryFileName",
	    "rssFileName",
            "ftp"
        ]

        for field in mandatoryFields:
            if not field in blogConfiguration["path"].keys():
                everythingIsOkay = False
                Notify(Messages.missingMandatoryFieldInBlogConf.format(field),"RED")

        if not everythingIsOkay:
            exit()

        return blogConfiguration

    except FileNotFoundError:
        Die(Messages.noBlogConfiguration)

    except PermissionError:
        Die(Messages.noBlogConfiguration)

    except yaml.scanner.ScannerError:
        Die(Messages.possibleMalformedBlogConfiguration)
