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

from math import ceil

from venc2.helpers import notify
from venc2.helpers import die
from venc2.l10n import messages
from venc2.patterns.processor import Processor

class Thread:
    def __init__(self, prompt, datastore, theme, patterns, forbidden):
        # Notify wich thread is processed
        if prompt != "":
            notify(prompt)
        self.forbidden = forbidden
        self.entries_per_page = int(datastore.blog_configuration["entries_per_pages"])
        self.disable_threads = datastore.disable_threads

        # Setup useful data
        self.theme = theme
        self.current_page = 0
        self.datastore = datastore
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
    def get_relative_location():
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
    def get_relative_origin(self, argv=list()):
        return self.relative_origin

    # Must be called in child class
    def get_next_page(self,argv=list()):
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
    def get_previous_page(self, argv=list()):
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
            if (not page_number < self.current_page - self.pages_count) and (not page_number > self.current_page + self.pages_count):
                output += string.format(
                    **{
                        "page_number":str(page_number),
                        "page_url": self.filename.format(**{"page_number": (str() if page_number == 0 else page_number) })
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
        self.output = ''.join(self.processor.batch_process(self.theme.header, "header.html").sub_strings)
        self.processor.forbidden = []

        self.columns_number = self.datastore.blog_configuration["columns"]
        self.columns_counter = 0
        self.columns = [ '' for i in range(0, self.columns_number) ]
    
    def post_iteration(self):
        self.columns_counter = 0
        for column in self.columns:
            self.output += '<div id="__VENC_COLUMN_'+str(self.columns_counter)+'__" class="__VENC_COLUMN__">'+column+'</div>'
            
        self.processor.forbidden = self.forbidden
        self.output += ''.join(self.processor.batch_process(self.theme.footer, "footer.html").sub_strings)
        
        self.write_file(self.output, self.page_number)

        self.page_number += 1
        self.current_page = self.page_number

    def do_iteration(self, entry):
        self.columns[self.columns_counter] += ''.join(self.processor.batch_process(entry.html_wrapper.above, entry.filename).sub_strings)
        if entry.html_wrapper.required_content_pattern == ".:GetEntryPreview:.":
            self.columns[self.columns_counter] += ''.join(self.processor.batch_process(entry.preview, entry.filename,).sub_strings)
                
        elif entry.html_wrapper.required_content_pattern == ".:PreviewIfInThreadElseContent:." and self.in_thread:
            self.columns[self.columns_counter] += ''.join(self.processor.batch_process(entry.preview, entry.filename,).sub_strings)
                
        else: 
            self.columns[self.columns_counter] += ''.join(self.processor.batch_process(entry.content, entry.filename,).sub_strings)

        self.columns[self.columns_counter] += ''.join(self.processor.batch_process(entry.html_wrapper.below, entry.filename).sub_strings)

        self.columns_counter +=1
        if self.columns_counter >= self.columns_number:
            self.columns_counter = 0

    # Must be called in child class
    def do(self):
        self.page_number = 0
        if self.pages_count == 0:
            output = ''.join(self.processor.batch_process(self.theme.header, "header.html").sub_strings)
            output += ''.join(self.processor.batch_process(self.theme.footer, "footer.html").sub_strings)
            stream = codecs.open(
                self.export_path +'/'+ self.format_filename(0),
                'w',
                encoding="utf-8"
            )
            stream.write(output)
            stream.close()
            
        else:
            for page in self.pages:
                self.pre_iteration()
                for entry in page:
                    self.setup_context(entry)
                    self.do_iteration(entry)

                self.post_iteration()
