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

from VenC.datastore.theme import ThemesDescriptor
from VenC.helpers import MsgFormat
from VenC.l10n import Messages;

def PrintVersion(argv):
    print("VenC 2.0.0")

def PrintHelp(argv=None):
    print("-v\t--version")
    print("-nb\t--new-blog <\""+Messages.argBlogName.format("1")+"\"> [\""+Messages.argBlogName.format("2")+"\" ... ]")
    print("-ne\t--new-entry <\""+Messages.argEntryName+"\"> [\""+Messages.argTemplateName+"\"]")
    print("-xb\t--export-blog ["+Messages.themeName+"]")
    print("-ex\t--edit-and-xport <\""+Messages.argInputFilename+"\">")
    print("-xftp\t--export-via-ftp")
    print("-rc\t--remote-copy")
    print("-h\t--help")
    print("-t\t--themes")
    print("-it\t--install-themes <"+Messages.themeName+">")

def PrintThemes(argv=None):
    for theme in ThemesDescriptor.keys():
        print ("- "+MsgFormat["GREEN"]+theme+MsgFormat["END"]+":", ThemesDescriptor[theme]["_themeDescription_"])
