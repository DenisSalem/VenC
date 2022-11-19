#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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

from venc3.helpers import quirk_encoding
from venc3.prompt import notify
from venc3.l10n import messages
from venc3.patterns.processor import Processor, Pattern
from venc3.patterns.third_party_wrapped_features.pygmentize import get_style_sheets

def undefined_variable(match):
    from venc3.prompt import die
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
    def __init__(self, prompt):
        from venc3.patterns.contextual import get_random_number
        from venc3.datastore import datastore
        from venc3.datastore.theme import theme
        from venc3.patterns.patterns_map import patterns_map
        
        self.get_random_number = get_random_number
        
        self.workers_count = datastore.workers_count
        self.indentation_level = "│  "
        self.patterns_map = patterns_map
        self.datastore = datastore
        self.enable_jsonld = datastore.blog_configuration["enable_jsonld"]
        self.path_encoding = datastore.blog_configuration["path_encoding"]
        
        # Notify wich thread is processed
        notify("├─ "+prompt)

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
        self.processor.set_patterns(
            # TODO : Remove this ugly hack.
            # Value is None for GetEntryContent, GetEntryPreview, PreviewIfInThreadElseContent
            { key : (getattr(self, value) if value else None) for key,value, in patterns_map.CONTEXTUALS.items()}
        )

    def get_style_sheets(self, node):
        return get_style_sheets(node).replace("\x1a", self.relative_origin)
        
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
    def get_relative_location(self, node):
        return self.export_path[5:]
        
    def get_relative_origin(self, node):
        return self.relative_origin

    def get_thread_name(self, node, string1='', string2=''):
        if len(self.thread_name):
            return string1.format(**{"value":self.thread_name})
        
        else:
            return string2
                
            
    # Must be called in child class
    def organize_entries(self, entries):
        self.pages = list()
        for i in range(0, ceil(len(entries)/self.entries_per_page)):
            self.pages.append(
                entries[i*self.entries_per_page:(i+1)*self.entries_per_page]
            )

        self.pages_count = len(self.pages)

    # Must be called in child class
    def get_next_page(self, node, string):
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
                    params["path"] = self.current_entry.next_entry.url
                    params["entry_id"] = self.current_entry.next_entry.id
                    params["entry_title"] = self.current_entry.next_entry.title
                    
            try:
                return string.format(**params)
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(
                    messages.unknown_contextual.format(
                        (str(e)[1:-1])
                    )
                )

        else:
            return str()

    # Must be called in child class
    def get_previous_page(self, node, string):
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
                    params["entry_id"] = self.current_entry.previous_entry.id
                    params["entry_title"] = self.current_entry.previous_entry.title
                    params["path"] = self.current_entry.previous_entry.url

            try:
                return string.format(**params)
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(
                    messages.unknown_contextual.format(
                        (str(e)[1:-1])
                    )
                )
                
        else:
            return str()

    # Must be called in child class
    def for_pages(self, node, length, string, separator):           
        if self.pages_count <= 1:
            return str()

        try:
            length = int(length)

        except:
            from venc3.exceptions import VenCException
            raise VenCException(messages.arg_must_be_an_integer.format("length"))
            
        output = str()
        page_number = 0
        for page in self.pages:
            if (not page_number < self.current_page - length) and (not page_number > self.current_page + length):
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
                    raise VenCException(messages.unknown_contextual.format(str(e)[1:-1]))

            page_number +=1
        
        return output[:-len(separator)]

    def get_JSONLD(self, node):
        return ''

    def get_entry_content(self, node):
        content = deepcopy(self.current_entry.content)
        self.processor.process(content, Pattern.FLAG_CONTEXTUAL)
        return content.string
        
    def get_entry_preview(self, node):
        preview = deepcopy(self.current_entry.preview)
        self.processor.process(content, Pattern.FLAG_CONTEXTUAL)
        return preview.string
      
    def preview_if_in_thread_else_content(self, node):
        if self.in_thread:
            preview = deepcopy(self.current_entry.preview)
            self.processor.process(content, Pattern.FLAG_CONTEXTUAL)
            return preview.string
        else:
            content = deepcopy(self.current_entry.content)
            self.processor.process(content, Pattern.FLAG_CONTEXTUAL)
            return content.string            
        
    def if_pages(self, node, string1, string2=''):
        if self.pages_count > 1:
            return string1.strip()
            
        else:
            return string2.strip()
                    
    def if_in_first_page(self, node, string1, string2=''):
        return string1.strip() if self.current_page == 0 else string2.strip()
            
    def if_in_last_page(self, node, string1, string2=''):
        return string1.strip() if self.current_page == len(self.pages) -1 else string2.strip()

    def if_in_entry_id(self, node, entry_id, string1, string2=''):
        return string2.strip()

    def if_in_main_thread(self, node, string1, string2=''):
        return string2.strip()
            
    def if_in_categories(self, node, string1, string2=''):
        return string2.strip()
            
    def if_in_archives(self, node, string1, string2=''):
        return string2
        
    def if_in_thread(self, node, string1, string2=''):
        return (string1 if self.in_thread else string2).strip()

    def if_in_thread_and_has_feeds(self, node, string1, string2=''):
        return (string1 if self.thread_has_feeds else string2).strip()
        
    def if_in_feed(self, node, string1, string2=''):
        return string2.strip()

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
            from venc3.prompt import die
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

    # QUESTION : Why the fuck using global current_source ?
    def pre_iteration(self):
        header = deepcopy(self.header)
        self.processor.process(header, Pattern.FLAG_CONTEXTUAL)
        self.output = header.string

        self.processor.blacklist = []
        self.columns_counter = 0
        self.columns = [ '' for i in range(0, self.columns_number) ]
    
    def post_iteration(self):
        self.columns_counter = 0
        for column in self.columns:
            self.output += self.column_opening.format(self.columns_counter)+column+self.column_closing
                  
        footer = deepcopy(self.footer)
        self.processor.process(footer, Pattern.FLAG_CONTEXTUAL)
        
        self.output += footer.string
        
        self.write_file(self.output.replace("\x1a",self.relative_origin), self.page_number)

        self.page_number += 1
        self.current_page = self.page_number
    
    def do_iteration(self, entry):
        entry_wrapper = deepcopy(getattr(entry, self.content_type+"_wrapper"))

        self.processor.process(entry_wrapper, Pattern.FLAG_CONTEXTUAL)

        output = entry_wrapper.string
        
        # ~ # deprecated
        # ~ if entry_wrapper.process_get_entry_content:
            # ~ self.processor.process(content, Pattern.FLAG_CONTEXTUAL)
            # ~ output=output.replace(
                # ~ "---VENC-GET-ENTRY-CONTENT---",
                # ~ content.string
            # ~ )

        # ~ if entry_wrapper.process_get_entry_preview:
            # ~ self.processor.process(preview, Pattern.FLAG_CONTEXTUAL)
            # ~ output=output.replace(
                # ~ "---VENC-GET-ENTRY-PREVIEW---",
                # ~ preview.string
            # ~ )
        
        # ~ output=output.replace(
            # ~ "---VENC-PREVIEW-IF-IN-THREAD-ELSE-CONTENT---",
            # ~ preview.string if self.in_thread else content.string
        # ~ )
           
        self.columns[self.columns_counter] += output
        
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
        global current_source #what the fuck ???
        self.current_page = 0
        self.page_number = 0
        if self.pages_count == 0:
            current_source = self.header
            self.processor.process(current_source, Pattern.FLAG_CONTEXTUAL)
            output = current_source.string
            
            current_source = self.footer
            self.processor.process(current_source, Pattern.FLAG_CONTEXTUAL)
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
