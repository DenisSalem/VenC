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
    def __init__(self, prompt, datastore, theme):
        super().__init__(prompt, datastore, theme)
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
        self.singleEntry = False

        self.processor.SetFunction("ForPages", self.ForPages)

    def ForPages(self, argv):
        listLenght = int(argv[0])
        string = argv[1]
        separator = argv[2]
            
        if self.pagesCount == 1 or self.singleEntry:
            return str()

        output = str()
        pageNumber = 0
        for page in self.pages:
            if (not pageNumber < self.currentPage - self.pagesCount) and (not pageNumber > self.currentPage + self.pagesCount):
                output += string.format(
                    {
                        "pageNumber":str(pageNumber),
                        "pageUrl": self.indexFileName.format({"pageNumber":pageNumber})
                    }
                ) + separator

            pageNumber +=1
        
        return output[:-len(separator)]

    def Do(self):
        for page in self.pages:
            output = MergeBatches(self.processor.BatchProcess(self.theme.header))

            for entry in page:
                output += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.above))
                output += MergeBatches(self.processor.BatchProcess(entry.content))
                output += MergeBatches(self.processor.BatchProcess(entry.htmlWrapper.below))
            
            output = MergeBatches(self.processor.BatchProcess(self.theme.footer))

                
                


