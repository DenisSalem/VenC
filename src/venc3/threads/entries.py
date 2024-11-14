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

import codecs
import os

from venc3.helpers import quirk_encoding
from venc3.threads import Thread
from venc3.patterns.contextuals.entries import EntriesThreadPatterns

class EntriesThread(Thread, EntriesThreadPatterns):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_single_entries)
        self.entries_per_page = 1 #override value
        self.organize_entries(self.datastore.entries)
        self.current_entry_index=-1
        self.entries = self.datastore.entries
        self.filename = self.datastore.blog_configuration["paths"]["entry_file_name"]
        self.sub_folders = self.datastore.blog_configuration["paths"]["entries_sub_folders"]
        self.export_path = "blog/"+self.sub_folders
        self.relative_origin = str('/'.join([ ".." for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = False
        self.thread_has_feeds = False
        self.known_written_path = []

    def format_filename(self, value=None): #value ignored
        try:
            return self.filename.format(**{
                'entry_id': self.current_entry.id,
                'entry_title': self.current_entry.metadata.title
            })
        
        except KeyError as e:
            from venc3.prompt import die
            die(("variable_error_in_filename", str(e)))

    def setup_context(self, entry):
        super().setup_context(entry)
        self.current_entry_index+=1
        export_path = quirk_encoding(
            self.export_path.format(**{
                    'entry_id': self.current_entry.id,
                    'entry_title': self.current_entry.metadata.title
            })
        )
        self.thread_name = self.current_entry.metadata.title
        self.relative_origin = str('/'.join([ ".." for p in export_path.split('/')[1:] if p != ''])).replace("//",'/')
        os.makedirs(export_path, exist_ok=True)


    def write_file(self, output, file_id):
        export_path = quirk_encoding(self.export_path.format(**{
            'entry_id': self.current_entry.id,
            'entry_title': self.current_entry.metadata.title
        }))
        written_path = export_path+'/'+self.format_filename()
        stream = codecs.open(
            written_path,
            'w',
            encoding="utf-8"
        )
        stream.write(output)
        stream.close()
        self.current_export_path = export_path
        if not written_path in [t[2] for t in self.known_written_path]:
            self.known_written_path.append((
                self.current_entry.id,
                self.current_entry.metadata.title,
                written_path
            ))
            
        else:
            from venc3.l10n import messages
            from venc3.prompt import die
            die(
              ("current_entry_is_overriding_the_following",
                self.current_entry.id,
                '\n'.join(
                    ["\t- #"+str(t[0])+" "+t[1] for t in self.known_written_path if t[2] == written_path]
                )
              )
            )
            
    def do(self):           
        self.page_number = 0
        self.current_page = 0
        if len(self.pages):
            for page in self.pages:
                for entry in page:
                    self.setup_context(entry)
                    self.pre_iteration()
                    self.do_iteration(entry)
                    self.post_iteration()
