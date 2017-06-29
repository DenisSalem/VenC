#! /usr/bin/python3

import datetime
import os
import shutil

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.helpers import Notify
from VenC.helpers import Die
from VenC.l10n import Messages

def InstallTheme(argv):
    blogConfiguration = GetBlogConfiguration()
    if blogConfiguration == None:
        Notify(Messages.noBlogConfiguration)
        return

    newFolderName = "theme "+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", newFolderName)
    
    except FileNotFoundError:
        Die(Messages.fileNotFound.format("'theme'"))

    try:
        shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0], "theme")
    
    except FileNotFoundError as e:
        ''' Restore previous states '''
        try:
            shutil.move(newFolderName, "theme")
            Die(Messages.themeDoesntExists.format("'"+argv[0]+"'"))

        except Exception as e:
            Die(str(e))

    Notify(Messages.themeInstalled)
