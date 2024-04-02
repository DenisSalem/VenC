#! /usr/bin/env python3

#    Copyright 2016, 2024 Denis Salem
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
import ftplib

from venc3.prompt import notify

def get_remote_files(ftp):
    items = list()
    for item in ftp.mlsd():
        filename, info = item
        if not filename in [".", ".."]:
            if info["type"] == "dir":
                cwd = ftp.pwd()
                ftp.cwd(ftp.pwd()+"/"+filename)
                items.append((ftp.pwd(), info))
                items += get_remote_files(ftp)
                ftp.cwd(cwd)
                
            else:
                items.append((ftp.pwd()+"/"+filename, info))
            
    return items
    
def get_local_files(directory):
    items = list()
    for item in os.listdir(directory):
        items.append(
            (
                directory+"/"+item,
                {
                    "type": "dir" if os.path.isdir(directory+"/"+item) else "file",
                    "modify": os.path.getmtime(directory+"/"+item),
                    "size": os.path.getsize(directory+"/"+item)
                }
            )
        )
        
        if items[-1][1]["type"] == "dir":
            items += get_local_files(directory+"/"+item)
            
    return items
          
def remote_copy(params):
    import getpass

    from venc3.datastore.configuration import get_blog_configuration
    from venc3.l10n import messages
    
    blog_configuration = get_blog_configuration()
    
    if not "ftp_host" in blog_configuration.keys():
        from venc3.prompt import die
        die(("undefined_variable", "ftp_host", "blog_configuration.yml"))

    if not "ftp_port" in blog_configuration.keys():
        blog_configuration["ftp_port"] = 21
        
    if len(blog_configuration["ftp_host"]) == 0:
        from venc3.prompt import die
        die(("invalid_value_in_setting", blog_configuration["ftp_host"], "ftp_host"))
    
    try:
        ftp = ftplib.FTP()
        ftp.encoding='latin-1' # TODO: is this necessary ?
        ftp.connect(blog_configuration["ftp_host"], blog_configuration["ftp_port"], timeout=10)
        
        username = input("VenC: "+messages.username)
        user_passwd = getpass.getpass(prompt="VenC: "+messages.user_passwd)
    
        if not "ftp" in blog_configuration["paths"].keys():
            from venc3.prompt import die
            die(("undefined_variable", "ftp", "blog_configuration.yml"))
            
        if len(blog_configuration["paths"]["ftp"]) == 0:
            from venc3.prompt import die
            die(("invalid_value_in_setting", blog_configuration["ftp"], "ftp"))
          
        ftp.login(user=username,passwd=user_passwd)
        ftp.cwd(blog_configuration["paths"]["ftp"])
        
        notify(("sync_ftp_directory",))
        local_files = { item[0][len(os.getcwd()+"/blog/"):] : item for item in get_local_files(os.getcwd()+"/blog") }
        remote_files = { item[0][len('/'+blog_configuration["paths"]["ftp"]+'/'):] : item for item in get_remote_files(ftp) }        
        
        to_delete = {}
        to_update = {}
        to_create = {}
        for item in local_files.keys():
            if not item in remote_files.keys():
                to_create[item] = local_files[item]
            elif local_files[item]["size"] != remote_files[item]["size"]:
                to_update[item] = local_files[item]
                
        for item in remote_files.keys():
            if not item in loca_files.keys():
                to_delete[item] = remote_files[item]
    
        from venc3.prompt import get_formatted_message
        for item in to_create.keys():
            print(get_formatted_message(item[0], color="GREEN", prompt=""))
            
        for item in to_update.keys():
            print(get_formatted_message(item[0], color="YELLOW", prompt=""))
            
        for item in to_delete.keys():
            print(get_formatted_message(item[0], color="RED", prompt=""))
          
    except Exception as e:
        from venc3.prompt import die
        die(("exception_place_holder", str(e)))
