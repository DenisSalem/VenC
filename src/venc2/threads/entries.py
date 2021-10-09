#! /usr/bin/env python3

#    Copyright 2016, 2021 Denis Salem
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

import json

from venc2.helpers import quirk_encoding
from venc2.prompt import notify
from venc2.threads import Thread
from venc2.l10n import messages

class EntriesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns_map):
        super().__init__(prompt, datastore, theme, patterns_map)
        self.entries_per_page = 1 #override value
        self.organize_entries(datastore.entries)
        self.current_entry_index=-1
        self.entries = self.datastore.entries
        self.filename = self.datastore.blog_configuration["path"]["entry_file_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["entries_sub_folders"]
        self.export_path = "blog/"+self.sub_folders
        self.relative_origin = str(''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = False
        self.thread_has_feeds = False

    def format_filename(self, value=None): #value ignored
        try:
            return self.filename.format(**{
                'entry_id': self.current_entry.id,
                'entry_title': self.current_entry.title
            })
        
        except KeyError as e:
            die(messages.variable_error_in_filename.format(str(e)))
            
    def if_in_first_page(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
            
    def if_in_last_page(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
    
    def if_in_entry_id(self, argv):
        try:
            if argv[0] == str(self.current_entry.id):
                return argv[1].strip()
        
            elif len(argv) >= 3:
                return argv[2].strip()
                
            else:
                return ''
                
        except AttributeError:
            return argv[2].strip() if len(argv) >= 3 else ''

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

        for i in range(0, list_lenght):
            next_entry =  None if self.current_entry_index >=  len(self.entries) - 2 else self.entries[self.current_entry_index+1]
            previous_entry = None  if self.current_entry_index == 0 else self.entries[self.current_entry_index-1]
        
            if next_entry != None:
                params["entry_id"] = next_entry.id
                params["entry_title"] = next_entry.title
                params["path"] = next_entry.url
                output += string.format(**params) + separator
                next_entry = next_entry.next_entry
            
            if previous_entry != None:
                params["entry_id"] = previous_entry.id
                params["entry_title"] = previous_entry.title
                params["path"] = previous_entry.url
                output = string.format(**params) + separator + output
                previous_entry = previous_entry.previous_entry

        return output[:-len(separator)]

    def setup_context(self, entry):
        super().setup_context(entry)
        self.current_entry_index+=1
        export_path = quirk_encoding(
            self.export_path.format(**{
                    'entry_id': self.current_entry.id,
                    'entry_title': self.current_entry.title
            })
        )
        self.thread_name = self.current_entry.title
        export_path = self.path_encode(export_path)
        self.relative_origin = str(''.join([ "../" for p in export_path.split('/')[1:] if p != ''])).replace("//",'/')
        os.makedirs(export_path, exist_ok=True)


    def write_file(self, output, file_id):
        export_path = self.path_encode(self.export_path.format(**{
            'entry_id': self.current_entry.id,
            'entry_title': self.current_entry.title
        }))
        stream = codecs.open(
            export_path+'/'+self.format_filename(),
            'w',
            encoding="utf-8"
        )
        stream.write(output)
        stream.close()
        self.current_export_path = export_path
    
    def do_jsonld(self, entry):
        dump = json.dumps(self.datastore.entries_as_jsonld[self.current_entry.id])
        f = open(self.current_export_path+"/entry"+str(entry.id)+".jsonld", 'w')
        f.write(dump.replace("\\u001a", self.relative_origin))
            
    def do(self):
        if self.datastore.enable_jsonld or self.datastore.enable_jsonp:
            notify(self.indentation_level+'└─ '+messages.generating_jsonld_docs)
            
        self.page_number = 0
        self.current_page = 0
        if len(self.pages):
            for page in self.pages:
                for entry in page:
                    self.setup_context(entry)
                    self.pre_iteration()
                    self.do_iteration(entry)
                    self.post_iteration()
                    if self.datastore.enable_jsonld:
                        self.do_jsonld(entry)


    def GetJSONLD(self, argv):
        if self.datastore.enable_jsonld and self.enable_jsonld:
            return '<script type="application/ld+json" src="entry'+str(self.current_entry.id)+'.jsonld"></script>'
            
        return ''

