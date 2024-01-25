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

import ftplib
import os

from venc.prompt import notify


def remote_copy(params):
    import getpass
    import socket

    from venc.datastore.configuration import get_blog_configuration
    from venc.l10n import messages

    blog_configuration = get_blog_configuration()
    try:
        ftp = ftplib.FTP(blog_configuration["ftp_host"])
        ftp.encoding = "latin-1"

    except socket.gaierror as e:
        from venc.prompt import die

        die(("exception_place_holder", str(e)))

    username = input("VenC: " + messages.username)
    user_passwd = getpass.getpass(prompt="VenC: " + messages.user_passwd)

    try:
        ftp.login(user=username, passwd=user_passwd)
        ftp.cwd(blog_configuration["path"]["ftp"])
        notify(("clean_ftp_directory",))
        ftp_clean_destination(ftp)
        notify(("copy_to_ftp_directory",))
        ftp_export_recursively(os.getcwd() + "/blog", ftp)

    except TimeoutError as e:
        from venc.prompt import die

        die(("exception_place_holder", str(e)))

    except ftplib.error_perm as e:
        from venc.prompt import die

        die(("exception_place_holder", str(e)))


def ftp_export_recursively(origin, ftp):
    folder = os.listdir(origin)
    for item in folder:
        if os.path.isdir(origin + "/" + item):
            try:
                try:
                    ftp.mkd(item)

                except ftplib.error_perm as e:
                    if not ": File exists" in str(e.args):
                        from venc.prompt import die

                        die(("exception_place_holder", str(e)))

                ftp.cwd(ftp.pwd() + "/" + item)
                ftp_export_recursively(origin + "/" + item, ftp)
                ftp.cwd(ftp.pwd()[: -len("/" + item)])

            except Exception as e:
                notify(("exception_place_holder", item + ": " + str(e)), color="YELLOW")

        else:
            notify(("item_uploaded_to_server", ftp.pwd() + "/" + item))
            ftp.storbinary(
                "STOR " + ftp.pwd() + "/" + item, open(origin + "/" + item, "rb")
            )


def ftp_clean_destination(ftp):
    listing = list()
    listing = ftp.nlst()

    for item in listing:
        if item not in [".", ".."]:
            try:
                ftp.delete(item)
                notify(("item_deleted_from_server", ftp.pwd() + "/" + item))

            except Exception:
                try:
                    ftp.rmd(item)
                    notify(("item_deleted_from_server", ftp.pwd() + "/" + item))

                except:
                    ftp.cwd(ftp.pwd() + "/" + item)
                    ftp_clean_destination(ftp)
                    ftp.cwd(ftp.pwd()[: -len("/" + item)])
