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

def install_theme(params):
    import os
    import shutil
    
    if len(params):
        theme = params[0]
    else:
        from venc3.prompt import die
        die(("missing_params", "--install-theme"))
        
    from venc3.datastore.configuration import get_blog_configuration
    from venc3.prompt import notify

    blog_configuration = get_blog_configuration() # will fail nicely if no configuration available

    import datetime
    new_folder_name = "theme-"+str(datetime.datetime.now()).replace(':','-')

    try:
        shutil.move("theme", new_folder_name)
    
    except:
        pass

    try:
        from venc3 import package_data_path
        shutil.copytree(package_data_path+"/themes/"+theme, "theme")
        notify(("theme_installed",))
       
    except FileNotFoundError as e:
        notify(("theme_doesnt_exists", "'"+theme+"'"),color='RED')
        ''' Restore previous states '''
        try:
            shutil.move(new_folder_name, "theme")

        except Exception as e:
            die(("exception_place_holder", str(e)))

