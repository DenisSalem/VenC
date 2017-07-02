#! /usr/bin/python3

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
            "threadOrder"
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
