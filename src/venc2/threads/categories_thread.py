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

import os

from venc2.helpers import notify
from venc2.threads import Thread
from venc2.patterns.processor import UnknownContextual

class CategoriesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns):
        super().__init__(prompt, datastore, theme, patterns)
        
        self.filename = self.datastore.blog_configuration["path"]["indexFileName"]
        self.entryname = str()
        self.relative_origin = "../"
        self.in_thread = True
        self.export_path = "blog/"

    def do(self, root=None):
        if root == None:
            root = self.datastore.entries_per_categories

        for node in root:
            if node.value == '':
                print(node.related_to)

            notify("\t"+node.value+"...")

            export_path = self.export_path
            self.export_path += node.value+'/'

            # Get entries
            try:
                os.makedirs(self.export_path)

            except FileExistsError:
                pass

            entries = [self.datastore.entries[entry_index] for entry_index in node.related_to]
            self.organize_entries( entries[::-1] if self.datastore.blog_configuration["reverseThreadOrder"] else entries )
            
            super().do()
            
            self.do(root=node.childs)

            # Restore path
            self.export_path = export_path





                
                


