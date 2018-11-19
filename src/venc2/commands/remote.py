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

import os
import ftplib
import socket
import getpass

from venc2.datastore.configuration import get_blog_configuration
from venc2.helpers import die
from venc2.helpers import notify
from venc2.l10n import messages

def remote_copy(argv=list()):
    blog_configuration = get_blog_configuration()
    try:
        ftp = ftplib.FTP(blog_configuration["ftp_host"])

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
    
    except ftplib.error_perm as e:
        die(str(e))

    except TimeoutError as e:
        die(str(e))

def ftp_export_recursively(origin, ftp):
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    ftp.mkd(item)
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftp_export_recursively(origin+"/"+item, ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])

                except:
                    try:
                        ftp.cwd(ftp.pwd()+"/"+item)
                        ftp_export_recursively(origin+"/"+item, ftp)
                        ftp.cwd(ftp.pwd()[:-len("/"+item)])

                    except:
                        raise

            else:
                ftp.storbinary("STOR "+ftp.pwd()+"/"+item, open(origin+"/"+item, 'rb'))

def ftp_clean_destination(ftp):
    listing = list()
    listing = ftp.nlst()
    for item in listing:
        if item not in ['.','..']:
            try:
                ftp.delete(item)

            except Exception:
                try:
                    ftp.rmd(item)

                except:
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftp_clean_destination(ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])
