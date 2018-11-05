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

import os

from venc2.helpers import notify
from venc2.threads import Thread

class EntriesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns, forbidden):
        super().__init__(prompt, datastore, theme, patterns, forbidden)
        self.entries_per_page = 1 #override value
        self.organize_entries([
            entry for entry in datastore.get_entries(
                False
            )
        ])

        self.filename = self.datastore.blog_configuration["path"]["entry_file_name"]
        self.relative_origin = str()
        self.export_path = "blog/"
        self.in_thread = False
    
    def if_in_first_page(self, argv):
        return argv[1]
    
    def if_in_last_page(self, argv):
        return argv[1]
    
    def if_in_entry_id(self, argv):
        try:
            if argv[0] == str(self.current_entry.id):
                return argv[1]
        
            else:
                return argv[2]

        except AttributeError:
            return argv[2]

    def do(self):
        if len(self.pages):
            super().do()


