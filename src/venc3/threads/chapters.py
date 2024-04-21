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

import os

from venc3.threads import Thread

class ChaptersThread(Thread):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_chapters)
        self.filename = self.datastore.blog_configuration["paths"]["index_file_name"]
        self.entries_per_page = self.datastore.blog_configuration["entries_per_pages"]
        self.folder_name = self.datastore.blog_configuration["paths"]["chapter_directory_name"]
        self.sub_folders = self.datastore.blog_configuration["paths"]["chapters_sub_folders"]
        self.relative_origin = str(''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = True
        self.thread_has_feeds = False
        self.chapters_list = [ [int(v) for v in key.split('.')] for key in self.datastore.raw_chapters.keys() ]
        self.chapters_list.sort()
        self.chapters_list = ['.'.join([str(v) for v in l]) for l in self.chapters_list]

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
        
    def setup_chapters_context(self, i, top, len_top):
        from venc3.helpers import quirk_encoding
        from venc3.prompt import notify
        node = top[i]
            
        if i == len_top-1:
            tree_special_char = '└'
                
        else:
            tree_special_char = '├'
        entry = self.datastore.entries[node.entry_index]
        notify(("exception_place_holder", node.index+' '+entry.title+"..."), prepend=self.indentation_level+tree_special_char+"─ ")
        self.thread_name = entry.title
        folder_name = quirk_encoding(
            self.folder_name.format(**{
              "chapter_name" : entry.title,
              "chapter_index": node.index
          })
        )
        self.export_path = "blog/"+self.sub_folders+'/'+folder_name
        self.relative_origin = '/'.join([ '..' for f in self.export_path.split("/")[1:] if f != '' ]).replace('//','/')

        try:
            os.makedirs(self.export_path)

        except FileExistsError:
            pass
            
        return (node)
    
    def extract_sub_chapters(self, sub_chapters): # TODO : Investigate yielding usage here for better efficiency
        output = []
        output_append = output.append
        for c in sub_chapters:
            output_append(self.datastore.entries[c.entry_index])
            if len(c.sub_chapters):
                for sc_entries in self.extract_sub_chapters(c.sub_chapters):
                    output_append(sc_entries)
        
        return output
            
    def do(self, top=None):          
        if top == None:
            top = self.datastore.chapters_index
            
        for chapter_index in range(0, len(top)):
            chapter = top[chapter_index]
            entry = self.datastore.entries[chapter.entry_index]
            self.organize_entries([ entry ] + self.extract_sub_chapters(chapter.sub_chapters))
            self.setup_chapters_context(chapter_index, top, len(top))
            super().do()
        
            if len(chapter.sub_chapters) > 0:
                self.indentation_level += "   " if len(top) - 1 == chapter_index else "│  "
                self.do(chapter.sub_chapters)
        
                # Restore states
                self.indentation_level = self.indentation_level[:-3]
