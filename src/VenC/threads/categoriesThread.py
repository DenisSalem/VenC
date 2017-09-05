#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
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

from VenC.helpers import Notify
from VenC.threads.thread import Thread
from VenC.pattern.processor import UnknownContextual
from VenC.pattern.processor import MergeBatches

class CategoriesThread(Thread):
    def __init__(self, prompt, datastore, theme):
        super().__init__(prompt, datastore, theme)
        
        self.fileName = self.datastore.blogConfiguration["path"]["indexFileName"]
        self.entryName = str()
        self.relativeOrigin = "../"
        self.inThread = True
        self.exportPath = "blog/"

    def Do(self, root=None):

        if root == None:
            root = self.datastore.entriesPerCategories

        for node in root:
            if node.value == '':
                print(node.relatedTo)

            Notify("\t"+node.value+"...")

            exportPath = self.exportPath
            self.exportPath += node.value+'/'

            # Get entries
            try:
                os.makedirs(self.exportPath)

            except FileExistsError:
                pass

            entries = [self.datastore.entries[entryIndex] for entryIndex in node.relatedTo]
            self.OrganizeEntries( entries[::-1] if self.datastore.blogConfiguration["reverseThreadOrder"] else entries )
            
            super().Do()
            
            self.Do(root=node.childs)

            # Restore path
            self.exportPath = exportPath





                
                


