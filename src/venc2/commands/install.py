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

import datetime
import os
import shutil

from venc2.datastore.configuration import get_blog_configuration
from venc2.helpers import notify
from venc2.helpers import die
from venc2.l10n import messages

def install_theme(argv):
    blog_configuration = get_blog_configuration()
    if blog_configuration == None:
        notify(messages.no_blog_configuration)
        return

    new_folder_name = "theme "+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", new_folder_name)
    
    except FileNotFoundError:
        die(messages.file_not_found.format("'theme'"))

    try:
        shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0], "theme")
    
    except FileNotFoundError as e:
        ''' Restore previous states '''
        try:
            shutil.move(new_folder_name, "theme")
            die(messages.theme_doesnt_exists.format("'"+argv[0]+"'"))

        except Exception as e:
            die(str(e))

    notify(messages.theme_installed)
