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

from copy import deepcopy
from math import ceil

from venc2.helpers import notify
from venc2.helpers import die
from venc2.l10n import messages
from venc2.patterns.processor import Processor

class Thread:
    def __init__(self, prompt, datastore, theme, patterns, forbidden):
        self.datastore = datastore
        # Notify wich thread is processed
        if prompt != "":
            notify(prompt)

        self.forbidden = forbidden
        self.entries_per_page = int(datastore.blog_configuration["entries_per_pages"])
        self.disable_threads = datastore.disable_threads

        # Setup useful data
        self.theme = theme
        self.footer = deepcopy(self.theme.footer)
        self.header = deepcopy(self.theme.header)
        self.entry = deepcopy(self.theme.entry)
        self.context_header = "header.html"
        self.context_footer = "footer.html"
        self.content_type = "html"
        self.column_opening = '<div id="__VENC_COLUMN_{0}__" class="__VENC_COLUMN__">'
        self.column_closing = "</div>"
        self.columns_number = self.datastore.blog_configuration["columns"]
        
        self.current_page = 0
        # Setup pattern processor
        self.processor = Processor()
        for pattern_name in patterns.keys():
            try:
                self.processor.set_function(pattern_name, getattr(self, patterns[pattern_name]))

            except TypeError: # if value isn't string but function reference
                self.processor.set_function(pattern_name, patterns[pattern_name])

    def return_page_around(self, string, params):
        return string.format(**params)


    # Must be called in child class
    def get_relative_location(self, argv):
        return self.export_path[5:]

    # Must be called in child class
    def organize_entries(self, entries):
        self.pages = list()
        for i in range(0, ceil(len(entries)/self.entries_per_page)):
            self.pages.append(
                entries[i*self.entries_per_page:(i+1)*self.entries_per_page]
            )

        self.pages_count = len(self.pages)

    # Must be called in child class
    def get_next_page(self, argv):
        if self.current_page < self.pages_count - 1:
            params = {
                "page_number" : str(self.current_page + 1),
                "entry_id" : '',
                "entry_title": '',
                "path" : ''
            }

            if self.in_thread:
                params["path"] = self.filename.format(**params)

            else:
                try:
                    params["path"] = self.current_entry.next_entry.url
                    params["entry_id"] = self.current_entry.next_entry.id
                    params["entry_title"] = self.current_entry.next_entry.title

                except AttributeError:
                    pass

            return argv[0].format(**params)

        else:
            return str()

    # Must be called in child class
    def get_previous_page(self, argv):
        if self.current_page > 0:
            params = {
                "page_number" : str(self.current_page - 1) if self.current_page - 1 != 0 else '',
                "entry_id" : '',
                "entry_title": '',
                "path" : ''
            }

            if self.in_thread:
                params["path"] = self.filename.format(**params)

            else:
                try:
                    params["entry_id"] = self.current_entry.previous_entry.id
                    params["entry_title"] = self.current_entry.previous_entry.title
                    params["path"] = self.current_entry.previous_entry.url
                except AttributeError:
                    pass

            return argv[0].format(**params)
        
        else:
            return str()

    # Must be called in child class
    def for_pages(self, argv):
        list_lenght = int(argv[0])
        string = argv[1]
        separator = argv[2]
            
        if self.pages_count <= 1:
            return str()

        output = str()
        page_number = 0
        for page in self.pages:
            if (not page_number < self.current_page - list_lenght) and (not page_number > self.current_page + list_lenght):
                output += string.format(
                    **{
                        "entry_id":'',
                        "entry_title":'',
                        "page_number":str(page_number),
                        "path": self.filename.format(**{"page_number": (str() if page_number == 0 else page_number) })
                    }
                ) + separator

            page_number +=1
        
        return output[:-len(separator)]

    def if_in_first_page(self, argv):
        if self.current_page == 0:
            return argv[0].strip()
        
        else:
            return argv[1].strip()

    def if_in_last_page(self, argv):
        if self.current_page == len(self.pages) -1:
            return argv[0].strip()
        
        else:
            return argv[1].strip()

    def if_in_entry_id(self, argv):
        return argv[2].strip()

    def if_in_categories(self, argv):
        return argv[1].strip()

    def if_in_archives(self, argv):
        return argv[1].strip()
        
    def if_in_thread(self, argv):
        if self.in_thread:
            return argv[0].strip()

        else:
            return argv[1].strip()

    def format_filename(self, value):
        try:
            if value == 0:
                return self.filename.format(**{
                    'page_number':''
                })
        
            else:
                return self.filename.format(**{
                    'page_number':value
                })

        except KeyError as e:
            die(messages.variable_error_in_filename.format(str(e)))

    # Overridden in child class (EntriesThread)
    def setup_context(self, entry):
        self.current_entry = entry

    def write_file(self, output, file_id):
        if self.in_thread:
            format_value = file_id

        else:
            format_value = page[0].id
                
        stream = codecs.open(
            self.export_path+'/'+self.format_filename(format_value),
            'w',
            encoding="utf-8"
        )
        stream.write(output)
        stream.close()

    def pre_iteration(self):
        self.processor.forbidden = self.forbidden
        self.processor.process(self.header, safe_process = True)
        self.output = self.header.string
        self.header.restore()
        self.processor.forbidden = []
        self.columns_counter = 0
        self.columns = [ '' for i in range(0, self.columns_number) ]
    
    def post_iteration(self):
        self.columns_counter = 0
        for column in self.columns:
            self.output += self.column_opening.format(self.columns_counter)+column+self.column_closing
            
        self.processor.forbidden = self.forbidden
        self.processor.process(self.footer, safe_process = True)
        self.output += self.footer.string
        self.footer.restore()
        
        self.write_file(self.output.replace(".:GetRelativeOrigin:.", self.relative_origin), self.page_number)

        self.page_number += 1
        self.current_page = self.page_number

    def do_iteration(self, entry):
        content_header = getattr(entry,self.content_type+"_wrapper").above
        self.processor.process(content_header, safe_process = True)
        self.columns[self.columns_counter] += content_header.string
        content_header.restore()
        
        if (entry.html_wrapper.required_content_pattern == ".:GetEntryPreview:.") or (entry.html_wrapper.required_content_pattern == ".:PreviewIfInThreadElseContent:." and self.in_thread):
            self.processor.process(entry.preview, safe_process = True)
            self.columns[self.columns_counter] += entry.preview.string
            entry.preview.restore()
                
        else: 
            self.processor.process(entry.content, safe_process = True)
            self.columns[self.columns_counter] += entry.content.string
            entry.content.restore()

        content_footer = getattr(entry,self.content_type+"_wrapper").below
        self.processor.process(content_footer, safe_process = True)
        self.columns[self.columns_counter] += content_footer.string
        content_footer.restore()

        self.columns_counter +=1
        if self.columns_counter >= self.columns_number:
            self.columns_counter = 0

    # Must be called in child class
    def do(self):
        self.page_number = 0
        if self.pages_count == 0:
            self.processor.process(self.header)
            output = self.header.string

            self.processor.process(self.footer)
            output += self.footer.string
            stream = codecs.open(
                self.export_path +'/'+ self.format_filename(0),
                'w',
                encoding="utf-8"
            )
            stream.write(output.replace(".:GetRelativeOrigin:.", self.relative_origin))
            stream.close()
            
        else:
            for page in self.pages:
                self.pre_iteration()
                for entry in page:
                    self.setup_context(entry)
                    self.do_iteration(entry)

                self.post_iteration()
