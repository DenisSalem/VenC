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

from copy import deepcopy

from venc3.patterns.third_party_wrapped_features.pygmentize import get_style_sheets
from venc3.patterns.processor import Pattern

class ThreadPatterns:
    def get_random_number(self, pattern, min_value, max_value, precision):    
            import random
            try:
                v = float(min_value) + random.random() * (float(max_value) - float(min_value))
                return str(int(v)) if int(precision) == 0 else str(round(v, int(precision)))
                
            except ValueError as e:
                from venc3.exceptions import VenCException
                faulty_arg_name = {v: k for k, v in locals().items()}[e.args[0].split('\'')[1]]
                
                raise VenCException(
                    ("wrong_pattern_argument", faulty_arg_name[1:], locals()[faulty_arg_name], "GetRandomNumber", str(e)),
                    pattern
                )
                
    def get_style_sheets(self, pattern):
        return get_style_sheets(pattern).replace("\x1a", self.relative_origin if len(self.relative_origin) else ".")
          
    def get_relative_location(self, pattern):
        return self.export_path[5:]
        
    def get_relative_root(self, pattern):
        return self.relative_origin

    def get_thread_name(self, pattern, string1='', string2=''):
        '''value'''
        if len(self.thread_name):
            return string1.format(**{"value":self.thread_name})
        
        else:
            return string2
                
    def get_last_entry_timestamp(self, pattern, time_format):
        import datetime
        return datetime.datetime.strftime(self.most_recent_entry_date, time_format)
        
    def get_next_page(self, pattern, string):
        '''page_number,entry_id,entry_title,path'''
        if self.current_page < self.pages_count - 1:
            params = {
                "page_number" : str(self.current_page + 1),
                "entry_id" : '',
                "entry_title": '',
                "path" : '',
                "chapter": ''
            }

            if self.in_thread:
                params["path"] = self.filename.format(**params)

            else:
                params["path"] = self.current_entry.next_entry.path
                params["entry_id"] = self.current_entry.next_entry.id
                params["entry_title"] = self.current_entry.next_entry.metadata.title
                    
            try:
                return string.format(**params)
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(
                    ("unknown_contextual", str(e)[1:-1]),
                    pattern
                )

        else:
            return str()

    def get_previous_page(self, pattern, string):
        '''page_number,entry_id,entry_title,path'''
        if self.current_page > 0:
            params = {
                "page_number" : str(self.current_page - 1) if self.current_page - 1 != 0 else '',
                "entry_id" : '',
                "entry_title": '',
                "path" : '',
                "chapter" : ''
            }

            if self.in_thread:
                params["path"] = self.filename.format(**params)

            else:
                    params["entry_id"] = self.current_entry.previous_entry.id
                    params["entry_title"] = self.current_entry.previous_entry.metadata.title
                    params["path"] = self.current_entry.previous_entry.path

            try:
                return string.format(**params)
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(
                    ("unknown_contextual", str(e)[1:-1]),
                    pattern
                )
                
        else:
            return str()

    def for_pages(self, pattern, length, string, separator):
        '''page_number,entry_id,entry_title,path'''
        if self.pages_count <= 1:
            return str()

        try:
            length = int(length)

        except:
            from venc3.exceptions import VenCException
            raise VenCException(("arg_must_be_an_integer", "length"), pattern)
            
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
                    raise VenCException(("unknown_contextual",str(e)[1:-1]), pattern)

            page_number +=1
        
        return output[:-len(separator)]

    def get_entry_content(self, pattern):
        if not hasattr(self, "current_entry"):
            from venc3.exceptions import PatternsCannotBeUsedHere
            raise PatternsCannotBeUsedHere([pattern])
            
        content = deepcopy(self.current_entry.content)
        self.processor.process(content, Pattern.FLAG_CONTEXTUAL, id(pattern.payload[0]))
        return content.string
        
    def get_entry_preview(self, pattern):
        if not hasattr(self, "current_entry"):
            from venc3.exceptions import PatternsCannotBeUsedHere
            raise PatternsCannotBeUsedHere([pattern])
            
        preview = deepcopy(self.current_entry.preview)
        self.processor.process(preview, Pattern.FLAG_CONTEXTUAL, id(pattern.payload[0]))
        return preview.string
      
    def preview_if_in_thread_else_content(self, pattern):
        if not hasattr(self, "current_entry"):
            from venc3.exceptions import PatternsCannotBeUsedHere
            raise PatternsCannotBeUsedHere([pattern])
            
        if self.in_thread:
            preview = deepcopy(self.current_entry.preview)
            self.processor.process(preview, Pattern.FLAG_CONTEXTUAL, id(pattern.payload[0]))
            return preview.string
            
        else:
            content = deepcopy(self.current_entry.content)
            self.processor.process(content, Pattern.FLAG_CONTEXTUAL,id(pattern.payload[0]))
            return content.string            
        
    def if_entries_in_page_have_metadata(self, pattern, metadata_name, string_1, string_2=''):
        for entry in self.pages[self.current_page]:
            if hasattr(entry.metadata, metadata_name):
                return string_1
                
        return string_2

    def if_pages(self, pattern, string1, string2=''):
        if self.pages_count > 1:
            return string1.strip()
            
        else:
            return string2.strip()
                    
    def if_in_first_page(self, pattern, string1, string2=''):
        return string1.strip() if self.current_page == 0 else string2.strip()
            
    def if_in_last_page(self, pattern, string1, string2=''):
        return string1.strip() if self.current_page == len(self.pages) -1 else string2.strip()


    def if_in_entry_id(self, pattern, entry_id, string1, string2=''):
        return string2.strip()

    def if_in_main_thread(self, pattern, string1, string2=''):
        return string2.strip()
            
    def if_in_categories(self, pattern, string1, string2=''):
        return string2.strip()
            
    def if_in_archives(self, pattern, string1, string2=''):
        return string2
        
    def if_in_thread(self, pattern, string1, string2=''):
        return (string1 if self.in_thread else string2).strip()

    def if_in_thread_and_has_feeds(self, pattern, string1, string2=''):
        return (string1 if self.thread_has_feeds else string2).strip()
        
    def if_in_feed(self, pattern, string1, string2=''):
        return string2.strip() 
