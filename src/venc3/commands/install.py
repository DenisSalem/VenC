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

import os
import shutil

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
                description = config["info"]["description"]
                                        
            except KeyError:
                from venc3.l10n import messages
                description = messages.theme_has_no_description
                
            except TypeError:
                from venc3.l10n import messages
                description = messages.theme_has_no_description

        else:
            from venc3.l10n import messages
            description = messages.theme_has_no_description

        from venc3.prompt import msg_format
        print("- "+msg_format["GREEN"]+theme+msg_format["END"]+":", description)

def install_theme(theme):
    from venc3.datastore.configuration import get_blog_configuration
    from venc3.prompt import notify

    blog_configuration = get_blog_configuration() # will fail nicely if no configuration available

    import datetime
    new_folder_name = "theme "+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", new_folder_name)
    
    except:
        pass

    try:
        shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes/"+theme, "theme")
        
        notify(("theme_installed",))
       
    except FileNotFoundError as e:
        notify(("theme_doesnt_exists", "'"+theme+"'"),color='RED')
        ''' Restore previous states '''
        try:
            shutil.move(new_folder_name, "theme")

        except Exception as e:
            die(("exception_place_holder", str(e)))

