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

from venc3.threads import Thread

class FeedThread(Thread):
    def __init__(self, feed_type, prompt, indentation_type):
        from venc3.l10n import messages
        super().__init__(prompt+"─ "+getattr(messages, "generating_"+feed_type), indentation_type)
        self.footer = getattr(self.theme, feed_type+"_footer")
        self.header = getattr(self.theme, feed_type+"_header")
        self.entry = getattr(self.theme, feed_type+"_entry")
        self.context_header = feed_type+"Header.xml"
        self.context_footer = feed_type+"Footer.xml"
        self.column_opening = ''
        self.column_closing = ''
        self.columns_number = 1
        self.filename = self.datastore.blog_configuration["paths"][feed_type+"_file_name"]
        self.entries_per_page = self.datastore.blog_configuration["feed_length"]
        self.in_thread = True
        self.content_type = feed_type

    def do(self, entries, export_path, relative_origin):
        self.export_path = export_path
        self.relative_origin = relative_origin
        self.organize_entries(entries)
        super().do()

    def if_in_feed(self, node, string1, string2=''):
        return string1.strip()
