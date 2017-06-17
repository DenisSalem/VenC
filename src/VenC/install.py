#! /usr/bin/python3

import datetime
import os
import shutil

from VenC.configuration import BlogConfiguration
from VenC.helpers import Notify
from VenC.l10n import Messages

def InstallTheme(argv):
    if BlogConfiguration == None:
        Notify(Messages.noBlogConfiguration)
        return

    newFolderName = "theme "+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", newFolderName)
    
    except FileNotFoundError:
        Notify(Messages.fileNotFound.format("'theme'"))

    try:
        shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0], "theme")
    
    except FileNotFoundError as e:
        Notify(Messages.themeDoesntExists.format("'"+argv[0]+"'"))
    
        ''' Restore previous states '''
        try:
            shutil.move(newFolderName, "theme")

        except Exception as e:
            Notify(str(e))
