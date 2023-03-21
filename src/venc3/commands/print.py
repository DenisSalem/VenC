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

from venc3.l10n import messages;

USAGE = \
    "\033[92m"+messages.full_documentation_there.format("https://venc.software")+"\033[0m\n" +\
    "-v\t--version\n" +\
    "-nb\t--new-blog <\""+messages.arg_blog_name.format("1")+"\"> [\""+messages.arg_blog_name.format("2")+"\" ... ]\n" +\
    "-ne\t--new-entry <\""+messages.arg_entry_name+"\"> [\""+messages.arg_template_name+"\"]\n" +\
    "-xb\t--export-blog ["+messages.theme_name+"]\n" +\
    "-ex\t--edit-and-xport <\""+messages.arg_input_filename+"\"> ["+messages.theme_name+"]\n" +\
    "-s\t--serv\n" +\
    "-xftp\t--export-via-ftp\n" +\
    "-rc\t--remote-copy\n" +\
    "-h\t--help\n" +\
    "-it\t--install-theme <"+messages.theme_name+">"
    
def version(params):
    from venc3 import venc_version
    print("VenC", venc_version)
    import platform
    print("Python", platform.python_version())


# Will be removed and replaced by argparse
def help(params):
    from venc3.prompt import notify
    from venc3.l10n import messages;
    print(USAGE)

