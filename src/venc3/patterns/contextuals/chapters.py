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

class ChaptersThreadPatterns:
    def get_next_page(self, pattern, string): #TODO : Any chance to factorize this in parent class ?
        '''page_number,entry_id,entry_title,path,chapter'''
        index = self.chapters_list.index(self.pages[self.current_page][-1].chapter.index) + 1
        if index  < len(self.chapters_list):
            entry = self.datastore.raw_chapters[self.chapters_list[index]]
            params = {
                "page_number" : '', #TODO: not implemented yet
                "entry_id" : entry.id,
                "entry_title": entry.title,
                "path" : entry.chapter.path,
                "chapter" : entry.chapter.index
            }

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
            
    def get_previous_page(self, pattern, string): #TODO : Any chance to factorize this in parent class ?
        '''page_number,entry_id,entry_title,path,chapter'''
        index = self.chapters_list.index(self.pages[self.current_page][0].chapter.index) - 1
        if index >= 0:
            entry = self.datastore.raw_chapters[self.chapters_list[index]]
            params = {
                "page_number" : '', #TODO: not implemented yet
                "entry_id" : entry.id,
                "entry_title": entry.title,
                "path" : entry.chapter.path,
                "chapter" : entry.chapter.index
            }
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

    def if_in_first_page(self, node, string1, string2=''):
        return string2.strip()
    
    def if_in_last_page(self, node, string1, string2=''):
        return string2.strip()
