#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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

from venc2.threads import Thread
from venc2.prompt import notify
from venc2.l10n import messages

class FeedThread(Thread):
    def __init__(self, feed_type):
        super().__init__('FEED_THREAD_PLACE_HOLDER')
        self.footer = getattr(self.theme, feed_type+"_footer")
        self.header = getattr(self.theme, feed_type+"_header")
        self.entry = getattr(self.theme, feed_type+"_entry")
        self.context_header = feed_type+"Header.xml"
        self.context_footer = feed_type+"Footer.xml"
        self.column_opening = ''
        self.column_closing = ''
        self.columns_number = 1
        
        self.filename = self.datastore.blog_configuration["path"][feed_type+"_file_name"]
        self.entries_per_page = self.datastore.blog_configuration["feed_lenght"]
        self.in_thread = True
        self.content_type = feed_type

    def do(self, entries, export_path, relative_origin, indentation_level, tree_special_char):
        notify(indentation_level+tree_special_char+"─ "+getattr(messages, "generating_"+self.content_type))
        self.export_path = export_path
        self.relative_origin = relative_origin
        self.organize_entries(entries)
        super().do()
    
    def get_JSONLD(self, node):
        from venc2.exceptions import VenCException
        raise VenCException(messages.unknown_pattern.format("GetJSONLD"))

    def if_in_feed(self, node, string1, string2=''):
        return string1.strip()
            

