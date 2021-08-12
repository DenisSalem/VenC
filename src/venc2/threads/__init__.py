#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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
import unidecode

from venc2.helpers import quirk_encoding
from venc2.prompt import notify
from venc2.l10n import messages
from venc2.patterns.exceptions import PatternInvalidArgument
from venc2.patterns.exceptions import PatternMissingArguments
from venc2.patterns.exceptions import UnknownContextual
from venc2.patterns.processor import Processor

current_source = None

def undefined_variable(match):
    from venc2.prompt import die
    die(
        messages.undefined_variable.format(
            match,
            current_source.ressource
        ), 
        extra=current_source.string.replace(
            match[1:-1], 
            '\033[91m'+match[1:-1]+'\033[0m'
        )
    )

class Thread:
    def __init__(self, prompt, datastore, theme, patterns_map):
        self.indentation_level = "│  "
        self.patterns_map = patterns_map
        self.datastore = datastore
        self.enable_jsonld = datastore.blog_configuration["enable_jsonld"]
        self.path_encoding = datastore.blog_configuration["path_encoding"]
        # Notify wich thread is processed
        if prompt != "":
            notify("├─ "+prompt)

        self.forbidden = patterns_map.non_contextual_entries_keys
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
        self.thread_name = ""
        self.rss_feed = None
        self.atom_feed = None
        # Setup pattern processor
        self.processor = Processor()
        for pattern_name in patterns_map.contextual["functions"].keys():
            self.processor.set_function(pattern_name, patterns_map.contextual["functions"][pattern_name])
                
        for pattern_name in patterns_map.contextual["names"].keys():
            self.processor.set_function(pattern_name, getattr(self, patterns_map.contextual["names"][pattern_name]))

    def path_encode(self, path):
        if self.path_encoding in ["utf-8",'']:
            return quirk_encoding(unidecode.unidecode(path))
            
        else:
            return path

    def return_page_around(self, string, params):
        try:
            return string.format(**params)
            
        except KeyError as e:
            raise UnknownContextual(str(e)[1:-1])
            
    # Must be called in child class
    def get_relative_location(self, argv):
        return self.export_path[5:]
        
    def get_relative_origin(self, argv):
        return self.relative_origin

    def get_thread_name(self, argv):
        if len(self.thread_name):
            try:
                return argv[0].format(**{"value":self.thread_name})
            except IndexError:
                return self.thread_name
        
        else:
            try:
                return argv[1]
                
            except IndexError:
                return ""
            
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
                    
            try:
                return argv[0].format(**params)
                
            except KeyError as e:
                raise UnknownContextual(str(e)[1:-1])

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

            try:
                return argv[0].format(**params)
                
            except KeyError as e:
                raise UnknownContextual(str(e)[1:-1])
                
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
                try:
                    output += string.format(
                        **{
                            "entry_id":'',
                            "entry_title":'',
                            "page_number":str(page_number),
                            "path": self.format_filename(page_number)
                        }
                    ) + separator
                    
                except KeyError as e:
                    raise UnknownContextual(str(e)[1:-1])

            page_number +=1
        
        return output[:-len(separator)]

    def JSONLD(self, argv):
        return ''

    def if_pages(self, argv):
        if self.pages_count > 1:
            return argv[0].strip()
            
        elif len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
                    
    def if_in_first_page(self, argv):
        if self.current_page == 0:
            return argv[0].strip()
        
        elif len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return  ''

    def if_in_last_page(self, argv):
        if self.current_page == len(self.pages) -1:
            return argv[0].strip()
        
        elif len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''

    def if_in_entry_id(self, argv):
        if len(argv) >= 3:
            return argv[2].strip()
            
        else:
            return ''

    def if_in_main_thread(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
            
    def if_in_categories(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
            
    def if_in_archives(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
        
    def if_in_thread(self, argv):
        if self.in_thread:
            return argv[0].strip()

        elif len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''


    def if_in_feed(self, argv):
        if len(argv) >= 2:
            return argv[1].strip()
            
        else:
            return ''
                    
    def if_in_thread_and_has_feeds(self, argv):
        return argv[0] if self.thread_has_feeds else ("" if len(argv) <= 1 else argv[1])

    def format_filename(self, value):
        try:
            if value == 0:
                return self.path_encode(
                    self.filename.format(**{
                        'page_number':''
                    })
                )
        
            else:
                return self.path_encode(
                    self.filename.format(**{
                        'page_number':value
                    })
                )

        except KeyError as e:
            from venc2.prompt import die
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
        stream.write(output.replace("\x1a", self.relative_origin))
        stream.close()

    def pre_iteration(self):
        global current_source
        self.processor.blacklist = self.forbidden
        current_source = self.header
        self.processor.process(current_source, safe_process = True)
        self.output = current_source.string
        current_source.restore()
        self.processor.blacklist = []
        self.columns_counter = 0
        self.columns = [ '' for i in range(0, self.columns_number) ]
    
    def post_iteration(self):
        global current_source
        self.columns_counter = 0
        for column in self.columns:
            self.output += self.column_opening.format(self.columns_counter)+column+self.column_closing
            
        self.processor.blacklist = self.forbidden
        
        current_source = self.footer
        self.processor.process(current_source, safe_process = True)
        self.output += current_source.string
        self.footer.restore()
        
        self.write_file(self.output.replace("\x1a",self.relative_origin), self.page_number)

        self.page_number += 1
        self.current_page = self.page_number

    def do_iteration(self, entry):
        global current_source
        
        entry_wrapper = getattr(entry, self.content_type+"_wrapper")
        
        preprocessed_wrapper = getattr(entry, self.content_type+"_wrapper").processed_string
        self.processor.process(preprocessed_wrapper, safe_process = True)
        
        output=preprocessed_wrapper.string
        
        if entry_wrapper.process_get_entry_content:
            self.processor.process(entry.content, safe_process = True)
            output=output.replace(
                "---VENC-GET-ENTRY-CONTENT---",
                entry.content.string
            )

        if entry_wrapper.process_get_entry_preview:
            self.processor.process(entry.preview, safe_process = True)
            output=output.replace(
                "---VENC-GET-ENTRY-PREVIEW---",
                entry.preview.string
            )
        
        output=output.replace(
            "---VENC-PREVIEW-IF-IN-THREAD-ELSE-CONTENT---",
            entry.preview.string if self.in_thread else entry.content.string
        )
            
        self.columns[self.columns_counter] += output
        preprocessed_wrapper.restore()
        if entry_wrapper.process_get_entry_content:
            entry.content.restore()
        if entry_wrapper.process_get_entry_preview:
            entry.preview.restore()
        
        self.columns_counter +=1
        if self.columns_counter >= self.columns_number:
            self.columns_counter = 0

    def iterate_through_pages(self):
        for page in self.pages:
            self.pre_iteration()
            for entry in page:
                self.setup_context(entry)
                self.do_iteration(entry)

            self.post_iteration()
    
    # Must be called in child class           
    def do(self):
        global current_source
        self.current_page = 0
        self.page_number = 0
        if self.pages_count == 0:
            current_source = self.header
            self.processor.process(current_source)
            output = current_source.string

            current_source = self.footer
            self.processor.process(current_source)
            output += current_source.string
            stream = codecs.open(
                self.export_path +'/'+ self.format_filename(0),
                'w',
                encoding="utf-8"
            )
            stream.write(output.replace("\x1a", self.relative_origin))
            stream.close()
            
        else:
            self.iterate_through_pages()

