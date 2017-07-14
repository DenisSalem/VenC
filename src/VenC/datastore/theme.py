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

from VenC.datastore.entry import EntryWrapper
from VenC.helpers import Die
from VenC.l10n import Messages
from VenC.pattern.processor import PreProcessor

ThemesDescriptor = {
    "dummy": {"columns":1,"_themeDescription_": Messages.themeDescriptionDummy},
    "gentle": {"columns":1,"_themeDescription_": Messages.themeDescriptionGentle},
    "tessellation": {"columns":3,"_themeDescription_": Messages.themeDescriptionTessellation},
}

class Theme:
    def __init__(self, themeFolder):
        try:
            self.header = PreProcessor(open(themeFolder+"chunks/header.html",'r').read())
            self.footer = PreProcessor(open(themeFolder+"chunks/footer.html",'r').read())
            self.rssHeader = PreProcessor(open(themeFolder+"chunks/rssHeader.html",'r').read())
            self.rssFooter = PreProcessor(open(themeFolder+"chunks/rssFooter.html",'r').read())
            
            self.entry = EntryWrapper(open(themeFolder+"chunks/entry.html",'r').read())
            self.rssEntry = EntryWrapper(open(themeFolder+"chunks/rssEntry.html",'r').read())

        except FileNotFoundError as e:
            Die(Messages.fileNotFound.format(str(e.filename)))
