#! /usr/bin/env python3

#    Copyright 2016, 2019 Denis Salem
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
import socket
import getpass

from venc2.datastore.configuration import get_blog_configuration
from venc2.prompt import die
from venc2.prompt import notify
from venc2.l10n import messages

#TODO : Initiate multiple, threaded, connection to speed up FTP transfert

def remote_copy(argv=list()):
    blog_configuration = get_blog_configuration()
    try:
        ftp = ftplib.FTP(blog_configuration["ftp_host"])
        ftp.encoding='latin-1'

    except socket.gaierror as e:
        die(str(e))

    username = input("VenC: "+messages.username)
    user_passwd = getpass.getpass(prompt="VenC: "+messages.user_passwd)
    
    try:
        ftp.login(user=username,passwd=user_passwd)
        ftp.cwd(blog_configuration["path"]["ftp"])
        notify(messages.clean_ftp_directory)
        ftp_clean_destination(ftp)
        notify(messages.copy_to_ftp_directory)
        ftp_export_recursively(os.getcwd()+"/blog", ftp)
    
    except TimeoutError as e:
        die(str(e))
    
    except ftplib.error_perm as e:
        die(str(e), color="YELLOW")

def ftp_export_recursively(origin, ftp):
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    try:
                        ftp.mkd(item)

                    except ftplib.error_perm as e:
                        if not ": File exists" in str(e.args):
                            raise
                    
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftp_export_recursively(origin+"/"+item, ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])

                except Exception as e:
                    notify(item+": "+str(e), color="YELLOW")

            else:
                notify(messages.item_uploaded_to_server+ftp.pwd()+"/"+item)
                ftp.storbinary("STOR "+ftp.pwd()+"/"+item, open(origin+"/"+item, 'rb'))

def ftp_clean_destination(ftp):
    listing = list()
    listing = ftp.nlst()

    for item in listing:
        if item not in ['.','..']:
            try:
                ftp.delete(item)
                notify(messages.item_deleted_from_server+ftp.pwd()+"/"+item)


            except Exception:
                try:
                    ftp.rmd(item)
                    notify(messages.item_deleted_from_server+ftp.pwd()+"/"+item)

                except:
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftp_clean_destination(ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])
