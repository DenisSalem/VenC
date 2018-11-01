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

class MainThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns):
        super().__init__(prompt, datastore, theme, patterns)
        
        self.organize_entries([
            entry for entry in datastore.get_entries(
                datastore.blog_configuration["reverse_thread_order"]
            )
        ])

        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.relative_origin = str()
        self.export_path = "blog/"
        self.in_thread = True




                
                


