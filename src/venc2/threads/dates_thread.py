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
from venc2.threads.thread import Thread
from venc2.patterns.processor import UnknownContextual

class DatesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns):
        super().__init__(prompt, datastore, theme, patterns)
        
        self.filename = self.datastore.blog_configuration["path"]["indexFileName"]
        self.entry_name = str()
        self.relative_origin = "../"
        self.in_thread = True

    def do(self):
        for thread in self.datastore.entries_per_dates:
            notify("\t"+thread.value+"...")
            self.export_path = "blog/"+thread.value+'/'
            os.makedirs(self.export_path)
            self.organize_entries([
                entry for entry in self.datastore.get_entries_for_given_date(
                    thread.value,
                    self.datastore.blog_configuration["reverseThreadOrder"]
                )
            ])

            super().do()




                
                


