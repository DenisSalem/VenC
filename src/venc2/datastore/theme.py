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

from venc2.datastore.entry import EntryWrapper
from venc2.helpers import die
from venc2.l10n import messages
from venc2.patterns.processor import PreProcessor

themes_descriptor = {
    "dummy": {"columns":1,"_themeDescription_": messages.theme_description_dummy},
    "gentle": {"columns":1,"_themeDescription_": messages.theme_description_gentle},
    "tessellation": {"columns":3,"_themeDescription_": messages.theme_description_tessellation},
}

class Theme:
    def __init__(self, theme_folder):
        try:
            self.header = PreProcessor(open(theme_folder+"chunks/header.html",'r').read())
            self.footer = PreProcessor(open(theme_folder+"chunks/footer.html",'r').read())
            self.rss_header = PreProcessor(open(theme_folder+"chunks/rssHeader.html",'r').read())
            self.rss_footer = PreProcessor(open(theme_folder+"chunks/rssFooter.html",'r').read())
            
            self.entry = EntryWrapper(open(theme_folder+"chunks/entry.html",'r').read(), "entry.html")
            self.rss_entry = EntryWrapper(open(theme_folder+"chunks/rssEntry.html",'r').read(),"rssEntry.html")

        except FileNotFoundError as e:
            die(messages.file_not_found.format(str(e.filename)))
