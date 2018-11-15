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

import codecs
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
        self.sub_folders = self.datastore.blog_configuration["path"]["entries_sub_folders"]
        self.export_path = "blog/"+self.sub_folders
        self.relative_origin = str(''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = False
    
    def if_in_first_page(self, argv):
        return argv[1]
    
    def if_in_last_page(self, argv):
        return argv[1]
    
    def format_filename(self, value=None): #value ignored
        try:
            return self.filename.format(**{
                'entry_id': self.current_entry.id,
                'entry_title': self.current_entry.title
            })
        
        except KeyError as e:
            die(messages.variable_error_in_filename.format(str(e)))

    
    def if_in_entry_id(self, argv):
        try:
            if argv[0] == str(self.current_entry.id):
                return argv[1]
        
            else:
                return argv[2]

        except AttributeError:
            return argv[2]

    def setup_sub_folders(self):
        export_path = self.export_path.format(**{
                'entry_id': self.current_entry.id,
                'entry_title': self.current_entry.title
        })
        self.relative_origin = str(''.join([ "../" for p in export_path.split('/')[1:] if p != ''])).replace("//",'/')
        print(export_path, self.relative_origin, export_path.split('/')[1:])
        os.makedirs(export_path, exist_ok=True)

    def write_file(self, output, file_id):
        export_path = self.export_path.format(**{
            'entry_id': self.current_entry.id,
            'entry_title': self.current_entry.title
        })
        stream = codecs.open(
            export_path+'/'+self.format_filename(),
            'w',
            encoding="utf-8"
        )
        stream.write(output)
        stream.close()

    def do(self):
        if len(self.pages):
            super().do()


