#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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

from venc3.datastore.configuration import get_blog_configuration
from venc3.prompt import msg_format
from venc3.prompt import notify
from venc3.prompt import die
from venc3.l10n import messages

def print_themes():
    import os
    import yaml

    themes_folder = os.path.expanduser('~')+"/.local/share/VenC/themes/"
    for theme in os.listdir(themes_folder):
        if "config.yaml" in os.listdir(themes_folder+theme) and not os.path.isdir(themes_folder+theme+"/config.yaml"):
            config = yaml.load(
                open(themes_folder+theme+"/config.yaml",'r').read(),
                Loader=yaml.FullLoader
            )
            try:
                description = getattr(messages, config["info"]["description"])
                        
            except AttributeError:
                description = config["info"]["description"]
                
            except KeyError:
                description = messages.theme_has_no_description
                
            except TypeError:
                description = messages.theme_has_no_description

        else:
            description = messages.theme_has_no_description

        print("- "+msg_format["GREEN"]+theme+msg_format["END"]+":", description)

def install_theme(theme):        
    blog_configuration = get_blog_configuration()
    if blog_configuration == None:
        notify(messages.no_blog_configuration)
        return

    new_folder_name = "theme "+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", new_folder_name)
    
    except:
        pass

    try:
        shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes/"+theme, "theme")
        notify(messages.theme_installed)
       
    except FileNotFoundError as e:
        notify(messages.theme_doesnt_exists.format("'"+theme+"'"),color='RED')
        ''' Restore previous states '''
        try:
            shutil.move(new_folder_name, "theme")

        except Exception as e:
            die(str(e))

