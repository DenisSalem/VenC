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
from venc2.patterns.processor import merge_batches

class Thread:
    def __init__(self, prompt, datastore, theme, patterns):
        # Notify wich thread is processed
        notify(prompt)
        
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
        return string.format({
            "destinationPage":destination_page_number,
            "destinationPageUrl":filename,
            "entryName" : self.entry_name
        })


    # Must be called in child class
    def get_relative_location():
        return self.export_path[5:]

    # Must be called in child class
    def organize_entries(self, entries):
        self.pages = list()
        entries_per_page = int(self.datastore.blog_configuration["entriesPerPages"])
        for i in range(0, ceil(len(entries)/entries_per_page)):
            self.pages.append(
                entries[i*entries_per_page:(i+1)*entries_per_page]
            )

        self.pages_count = len(self.pages)

    # Must be called in child class
    def get_relative_origin(self, argv=list()):
        return self.relative_origin

    # Must be called in child class
    def get_next_page(self,argv=list()):
        if self.current_page < len(self.pages) - 1:
            destination_page_number = str(self.current_page + 1)
            ''' Must catch KeyError exception '''
            filename = self.filename.format({"pageNumber":destination_page_number})
            return self.return_page_around(argv[0], destination_page_number, filename)

        else:
            return str()

    # Must be called in child class
    def get_previous_page(self, argv=list()):
        if self.current_page > 0:
            destination_page_number = str(self.current_page - 1)
            if self.current_page == 1:
                ''' Must catch KeyError exception '''
                filename = self.filename.format(page_number="")

            else:
                ''' Must catch KeyError exception '''
                filename = self.filename.format(page_number=destination_page_number)
            
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
                    {
                        "pageNumber":str(page_number),
                        "pageUrl": self.filename.format({"pageNumber": (str() if page_number == 0 else page_number) })
                    }
                ) + separator

            page_number +=1
        
        return output[:-len(separator)]


    def if_in_thread(self, argv):
        if self.in_thread:
            return argv[0]

        else:
            return argv[1]

    def format_filename(self, page_number):
        try:
            if page_number == 0:
                return self.filename.format({
                    'entryId':'',
                    'pageNumber':''
                })
        
            else:
                return self.filename.format({
                    'entryId':page_number,
                    'pageNumber':page_number
                })

        except KeyError as e:
            die(messages.variable_error_in_filename.format(str(e)))

    # Must be called in child class
    def do(self):
        page_number = 0
        for page in self.pages:
            output = merge_batches(self.processor.batch_process(self.theme.header, "header.html"))

            columns_number = self.datastore.blog_configuration["columns"]
            columns_counter = 0
            columns = [ '' for i in range(0, columns_number) ]
            for entry in page:
                columns[columns_counter] += merge_batches(self.processor.batch_process(entry.html_wrapper.above, entry.filename, not entry.do_not_use_markdown))
                columns[columns_counter] += merge_batches(self.processor.batch_process(entry.content, entry.filename, not entry.do_not_use_markdown))
                columns[columns_counter] += merge_batches(self.processor.batch_process(entry.html_wrapper.below, entry.filename, not entry.do_not_use_markdown))

                columns_counter +=1
                if columns_counter >= columns_number:
                    columns_counter = 0

            columns_counter = 0
            for column in columns:
                output += '<div id="__VENC_COLUMN_'+str(columns_counter)+'__" class="__VENC_COLUMN__">'+column+'</div>'
            
            output += merge_batches(self.processor.batch_process(self.theme.footer, "footer.html"))
        
            stream = codecs.open(
                self.export_path + self.format_filename(page_number),
                'w',
                encoding="utf-8"
            )
            stream.write(output)
            stream.close()

            page_number += 1
