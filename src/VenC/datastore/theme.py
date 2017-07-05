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

from VenC.helpers import Die
from VenC.l10n import Messages

ThemesDescriptor = {
    "dummy": {"columns":1,"_themeDescription_": Messages.themeDescriptionDummy},
    "gentle": {"columns":1,"_themeDescription_": Messages.themeDescriptionGentle},
    "tessellation": {"columns":3,"_themeDescription_": Messages.themeDescriptionTessellation},
}

class Theme:
    def __init__(self, themeFolder):
        self.header = str()
        self.footer = str()
        self.entry = str()
        self.rssHeader = str()
        self.rssFooter = str()
        self.rssEntry = str()

        try:
            self.header = open(themeFolder+"chunks/header.html",'r').read()
            self.footer = open(themeFolder+"chunks/footer.html",'r').read()
            self.entry = open(themeFolder+"chunks/entry.html",'r').read()
            self.rssHeader = open(themeFolder+"chunks/rssHeader.html",'r').read()
            self.rssFooter = open(themeFolder+"chunks/rssFooter.html",'r').read()
            self.rssEntry = open(themeFolder+"chunks/rssEntry.html",'r').read()

        except FileNotFoundError as e:
            Die(Messages.fileNotFound.format(str(e.filename)))
