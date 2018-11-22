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

from venc2.threads import Thread

class FeedThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns, forbidden, feed_type):
        super().__init__(prompt, datastore, theme, patterns, forbidden)
        self.footer = getattr(self.theme, feed_type+"_footer")
        self.header = getattr(self.theme, feed_type+"_header")
        self.entry = getattr(self.theme, feed_type+"_entry")
        self.context_header = feed_type+"Header.xml"
        self.context_footer = feed_type+"Footer.xml"
        self.column_opening =''
        self.column_closing =''
        
        self.filename = self.datastore.blog_configuration["path"][feed_type+"_file_name"]
        self.entries_per_page = self.datastore.blog_configuration["feed_lenght"]
        self.export_path = "blog/"
        self.relative_origin = ""
        self.in_thread = True
        self.content_type = feed_type

    def do(self):
        self.organize_entries([entry for entry in self.datastore.get_entries(True)][0:self.entries_per_page])
        super().do()
 
