#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
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
