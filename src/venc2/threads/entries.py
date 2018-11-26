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
        return argv[1].strip()
    
    def if_in_last_page(self, argv):
        return argv[1].strip()
    
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
                return argv[1].strip()
        
            else:
                return argv[2].strip()

        except AttributeError:
            return argv[2].strip()

    def for_pages(self, argv):
        list_lenght = int(argv[0])
        string = argv[1]
        separator = argv[2]
        output = ""
        params = {
            "entry_id":str(self.current_entry.id),
            "entry_title":str(self.current_entry.title),
            "page_number":'',
            "path": self.current_entry.url
        }
        output += string.format(**params) + separator

        next_entry = self.current_entry.next_entry
        previous_entry = self.current_entry.previous_entry
        for i in range(0, list_lenght):
            if entry_next != None:
                params["entry_id"] = next_entry.id
                params["entry_title"] = next_entry.title
                params["path"] = next_entry.url
                output += string.format(**params) + separator
                next_entry = entry_next.next_entry
            
            if entry_previous != None:
                params["entry_id"] = entry_previous.id
                params["entry_title"] = entry_previous.title
                params["path"] = entry_previous.url
                output = string.format(**params) + separator + output
                entry_previous = entry_previous.previous_entry

        return output[:-len(separator)]

    def setup_context(self, entry):
        super().setup_context(entry)
        export_path = self.export_path.format(**{
                'entry_id': self.current_entry.id,
                'entry_title': self.current_entry.title
        }).replace(' ','-')
        self.relative_origin = str(''.join([ "../" for p in export_path.split('/')[1:] if p != ''])).replace("//",'/')
        os.makedirs(export_path, exist_ok=True)

    def write_file(self, output, file_id):
        export_path = self.export_path.format(**{
            'entry_id': self.current_entry.id,
            'entry_title': self.current_entry.title
        }).replace(' ','-')
        stream = codecs.open(
            export_path+'/'+self.format_filename(),
            'w',
            encoding="utf-8"
        )
        stream.write(output)
        stream.close()

    
    def do(self):
        self.page_number = 0
        if len(self.pages):
            for page in self.pages:
                for entry in page:
                    self.setup_context(entry)
                    self.pre_iteration()
                    self.do_iteration(entry)
                    self.post_iteration()


