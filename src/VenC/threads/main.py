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

from VenC.threads.thread import Thread
from VenC.pattern.processor import UnknownContextual
from VenC.pattern.processor import MergeBatches

class Main(Thread):
    def __init__(self, prompt, datastore):
        super().__init__(prompt, datastore)
        self.OrganizeEntries([
            entry for entry in datastore.GetEntries(
                datastore.blogConfiguration["reverseThreadOrder"]
            )
        ])

        self.currentPage = 0
        self.indexFileName = self.datastore.blogConfiguration["path"]["indexFileName"]
        self.entryName = str()
        self.relativeOrigin = str()
        self.exportPath = str()

    def Do(self):
        for page in self.pages:
            output = str()
            for entry in page:
                
                output += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.above))
                output += MergeBatches(self.processor.BatchProcess(entry.content))
                output += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.below))
                
                


