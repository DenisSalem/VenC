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

import ftplib
import socket

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.helpers import Die

def RemoteCopy(argv=list()):
    blogConfiguration = GetBlogConfiguration()
    try:
        ftp = ftplib.FTP(blogConfiguration["ftp_host"])

    except socket.gaierror as e:
        Die(str(e))

    username = input("VenC: "+Messages.username)
    userPasswd = getpass.getpass(prompt="VenC: "+Messages.userPasswd)
    
    try:
        ftp.login(user=username,passwd=userPasswd)
        ftp.cwd(VenC.core.blogConfiguration["path"]["ftp"])
        Notify(VenC.core.Messages.cleanFtpDirectory)
        ftpCleanDestination(ftp)
        Notify(Messages.copyToFtpDirectory)
        ftpExportRecursively(os.getcwd()+"/blog", ftp)
    
    except ftplib.error_perm as e:
        Die(str(e))

def ftpExportRecursively(origin, ftp):
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    ftp.mkd(item)
                    ftp.cwd(ftp.pwd()+"/"+item)
                    ftpExportRecursively(origin+"/"+item, ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])

                except:
                    try:
                        ftp.cwd(ftp.pwd()+"/"+item)
                        ftpExportRecursively(origin+"/"+item, ftp)
                        ftp.cwd(ftp.pwd()[:-len("/"+item)])

                    except:
                        raise

            else:
                ftp.storbinary("STOR "+ftp.pwd()+"/"+item, open(origin+"/"+item, 'rb'))

def ftpCleanDestination(ftp):
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
                    ftpCleanDestination(ftp)
                    ftp.cwd(ftp.pwd()[:-len("/"+item)])
