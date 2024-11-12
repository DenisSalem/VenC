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

class EntriesThreadPatterns:
    def get_last_entry_timestamp(self, pattern, time_format):
        from venc3.exceptions import VenCException
        raise VenCException(
            ("you_cannot_use_this_pattern_here", "GetLastEntryTimestamp", pattern.root.context),
            pattern
        )
        
    def if_in_first_page(self, node, string1, string2=''):
        return string2.strip()

    def if_in_last_page(self, node, string1, string2=''):
        return string2.strip()
    
    def if_in_entry_id(self, node, entry_id, string1, string2=''):
        try:
            if entry_id == str(self.current_entry.id):
                return string1.strip()
                
        except AttributeError:
            pass
            
        return string2.strip()

    def for_pages(self, node, length, string, separator):
        output = ""
        params = {
            "entry_id":str(self.current_entry.id),
            "entry_title":str(self.current_entry.title),
            "page_number":'',
            "path": self.current_entry.path
        }
        
        try:
            length = int(length)

        except:
            from venc3.exceptions import VenCException
            raise VenCException(("arg_must_be_an_integer","length"), node)        
        
        try:
            output += string.format(**params) + separator
            
        except KeyError as e:
            from venc3.exceptions import VenCException
            raise VenCException(("unknown_contextual",str(e)[1:-1]), node)
            
        for i in range(0, length):
            next_entry =  None if self.current_entry_index >=  len(self.entries) - 2 else self.entries[self.current_entry_index+1]
            previous_entry = None  if self.current_entry_index == 0 else self.entries[self.current_entry_index-1]
        
            if next_entry != None:
                params["entry_id"] = next_entry.id
                params["entry_title"] = next_entry.title
                params["path"] = next_entry.path
                output += string.format(**params) + separator
                next_entry = next_entry.next_entry
            
            if previous_entry != None:
                params["entry_id"] = previous_entry.id
                params["entry_title"] = previous_entry.title
                params["path"] = previous_entry.path
                output = string.format(**params) + separator + output
                previous_entry = previous_entry.previous_entry

        return output[:-len(separator)]
