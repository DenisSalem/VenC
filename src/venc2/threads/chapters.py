#! /usr/bin/env python3

#    Copyright 2016, 2019 Denis Salem
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

from venc2.prompt import notify
from venc2.threads import Thread

class ChaptersThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns_map):
        super().__init__(prompt, datastore, theme, patterns_map)
        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.entries_per_page = self.datastore.blog_configuration["entries_per_pages"]
        self.organize_entries([
            entry for entry in datastore.get_entries(
                False
            )
        ])

        self.folder_name = self.datastore.blog_configuration["path"]["chapter_directory_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["chapters_sub_folders"]
        self.relative_origin = str(''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = True
        
    def if_in_first_page(self, argv):
        return argv[1].strip() if len(argv) >= 2 else ''
    
    def if_in_last_page(self, argv):
        return argv[1].strip() if len(argv) >= 2 else ''
        
    def setup_chapters_context(self, i, top, len_top):
        node = top[i]
            
        if i == len_top-1:
            tree_special_char = '└'
                
        else:
            tree_special_char = '├'
                
        notify(self.indentation_level+tree_special_char+"─ "+node.index+' '+node.entry.title+"...")
        
        self.export_path = "blog/"+self.sub_folders+'/'+self.folder_name
        self.export_path = self.export_path.format(**{
            "chapter_name" : node.entry.title,
            "chapter_index": node.index
        })
        self.export_path = self.path_encode(self.export_path)
        self.relative_origin = ''.join([ '../' for f in self.export_path.split("/")[1:] if f != '' ]).replace("//",'/')

        try:
            os.makedirs(self.export_path)

        except FileExistsError:
            pass
            
        return (node)
    
    def extract_sub_chapters(self, sub_chapters):
        output = []
        output_append = output.append
        for c in sub_chapters:
            output_append(c.entry)
            if len(c.sub_chapters):
                for sc_entries in self.extract_sub_chapters(c.sub_chapters):
                    output_append(sc_entries)
            
        return output
        
        
    def do(self, top=None):
        if top == None:
            top = self.datastore.chapters_index
            
        for chapter_index in range(0, len(top)):
            chapter = top[chapter_index]
            self.organize_entries([ chapter.entry ] + self.extract_sub_chapters(chapter.sub_chapters))
            self.setup_chapters_context(chapter_index, top, len(top))
            super().do()
        
            if len(chapter.sub_chapters) > 0:
                self.indentation_level += "   " if len(top) - 1 == chapter_index else "│  "
                self.do(chapter.sub_chapters)
        
                # Restore states
                self.indentation_level = self.indentation_level[:-3]
                
    def GetJSONLD(self, argv):
        if self.current_page == 0:
            return '<script type="application/ld+json" src="chapters.jsonld"></script>'
        
        return ''
