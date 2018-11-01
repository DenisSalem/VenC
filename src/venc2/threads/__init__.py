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
    def __init__(self, prompt, datastore, theme, patterns):
        # Notify wich thread is processed
        notify(prompt)
        self.entries_per_page = int(datastore.blog_configuration["entries_per_pages"])
        
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

    def return_page_around(self, string, destination_page_number, filename):
        return string.format(**{
            "destination_page":destination_page_number,
            "destination_page_url":filename,
            "entry_name" : self.current_entry.title,
            "entry_id": self.current_entry.id
        })


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
        if self.current_page < len(self.pages) - 1:
            destination_page_number = str(self.current_page + 1)
            next_entry_id = self.current_entry.next_entry.id
            filename = self.filename.format(**{"page_number":destination_page_number,"entry_id":next_entry_id})
            return self.return_page_around(argv[0], destination_page_number, filename)

        else:
            return str()

    # Must be called in child class
    def get_previous_page(self, argv=list()):
        if self.current_page > 0:
            destination_page_number = str(self.current_page - 1)
            try:
                previous_entry_id = self.current_entry.previous_entry.id
            except:
                previous_entry_id = -1

            if self.current_page == 1:
                filename = self.filename.format(**{"page_number" : "", "entry_id" : previous_entry_id})

            else:
                filename = self.filename.format(**{"page_number" : destination_page_number, "entry_id" : previous_entry_id})
            
            return self.return_page_around(argv[0], destination_page_number, filename)
        
        else:
            return str()
    # Must be called in child class
    def for_pages(self, argv):
        list_lenght = int(argv[0])
        string = argv[1]
        separator = argv[2]
            
        if self.pages_count == 1 or not self.in_thread:
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
            return argv[0]
        
        else:
            return argv[1]

    def if_in_last_page(self, argv):
        if self.current_page == len(self.pages) -1:
            return argv[0]
        
        else:
            return argv[1]

    def if_in_entry_id(self, argv):
        return argv[2]

    def if_in_categories(self, argv):
        return argv[1]

    def if_in_archives(self, argv):
        return argv[1]
        
    def if_in_thread(self, argv):
        if self.in_thread:
            return argv[0]

        else:
            return argv[1]

    def format_filename(self, value):
        try:
            if value == 0:
                return self.filename.format(**{
                    'entry_id':value,
                    'page_number':''
                })
        
            else:
                return self.filename.format(**{
                    'entry_id':value,
                    'page_number':value
                })

        except KeyError as e:
            die(messages.variable_error_in_filename.format(str(e)))

    # Must be called in child class
    def do(self):
        page_number = 0
        if len(self.pages) == 0:
            output = ''.join(self.processor.batch_process(self.theme.header, "header.html").sub_strings)
            output += ''.join(self.processor.batch_process(self.theme.footer, "footer.html").sub_strings)
            stream = codecs.open(
                self.export_path + self.format_filename(0),
                'w',
                encoding="utf-8"
            )
            stream.write(output)
            stream.close()
            
        else:
            for page in self.pages:
                output = ''.join(self.processor.batch_process(self.theme.header, "header.html").sub_strings)

                columns_number = self.datastore.blog_configuration["columns"]
                columns_counter = 0
                columns = [ '' for i in range(0, columns_number) ]
                for entry in page:
                    self.current_entry = entry
                    columns[columns_counter] += ''.join(self.processor.batch_process(entry.html_wrapper.above, entry.filename).sub_strings)
                    if entry.html_wrapper.required_content_pattern == ".:GetEntryPreview:.":
                        columns[columns_counter] += ''.join(self.processor.batch_process(entry.preview, entry.filename,).sub_strings)
                
                    elif entry.html_wrapper.required_content_pattern == ".:PreviewIfInThreadElseContent:." and self.in_thread:
                        columns[columns_counter] += ''.join(self.processor.batch_process(entry.preview, entry.filename,).sub_strings)
                
                    else: 
                        columns[columns_counter] += ''.join(self.processor.batch_process(entry.content, entry.filename,).sub_strings)

                    columns[columns_counter] += ''.join(self.processor.batch_process(entry.html_wrapper.below, entry.filename).sub_strings)

                    columns_counter +=1
                    if columns_counter >= columns_number:
                        columns_counter = 0

                columns_counter = 0
                for column in columns:
                    output += '<div id="__VENC_COLUMN_'+str(columns_counter)+'__" class="__VENC_COLUMN__">'+column+'</div>'
            
                output += ''.join(self.processor.batch_process(self.theme.footer, "footer.html").sub_strings)
        
                if self.in_thread:
                    format_value = page_number

                else:
                    format_value = page[0].id

                stream = codecs.open(
                    self.export_path + self.format_filename(format_value),
                    'w',
                    encoding="utf-8"
                )
                stream.write(output)
                stream.close()

                page_number += 1
                self.current_page = page_number
