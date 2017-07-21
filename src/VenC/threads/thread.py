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

from math import ceil

from VenC.helpers import Notify
from VenC.pattern.processor import Processor

class Thread:
    def __init__(self, prompt, datastore, theme):
        # Notify wich thread is processed
        Notify(prompt)
        
        # Setup useful data
        self.theme = theme
        self.processor = Processor()
        self.processor.SetFunction("GetRelativeOrigin", self.GetRelativeOrigin)
        self.processor.SetFunction("GetNextPage", self.GetNextPage)
        self.processor.SetFunction("GetPreviousPage", self.GetPreviousPage)
        self.datastore = datastore
        self.currentPage = 0

    def ReturnPageAround(self, string, destinationPageNumber, indexFileName):
        try:
            return string.format({
                "destinationPage":destinationPageNumber,
                "destinationPageUrl":indexFileName,
                "entryName" : self.entryName
            })

        except KeyError:
            raise UnknownContextual(str(e)[1:-1])



    # Must be called in child class
    def OrganizeEntries(self, entries):
        self.pages = list()
        entriesPerPage = int(self.datastore.blogConfiguration["entriesPerPages"])
        for i in range(0, ceil(len(entries)/entriesPerPage)):
            self.pages.append(
                entries[i*entriesPerPage:(i+1)*entriesPerPage]
            )

        self.pagesCount = len(self.pages)

    # Must be called in child class
    def WritePage(self, folderDestination, filename, content):
        try:
            os.chdir("blog/")
            os.makedirs(folderDestination)
            os.chdir("../")

        # a little bit dirty...
        except:
            os.chdir("../")

        stream = codecs.open(
            "blog/"+folderDestination+filename,
            'w',
            encoding="utf-8"
        )
        stream.write(self.outputPage)
        stream.close()

    # Must be called in child class
    def GetRelativeOrigin(self, argv=list()):
        return self.relativeOrigin

    # Must be called in child class
    def GetNextPage(self,argv=list()):
        if self.currentPage < len(self.pages) - 1:
            destinationPageNumber = str(self.currentPage + 1)
            ''' Must catch KeyError exception '''
            indexFileName = self.indexFileName.format({"pageNumber":destinationPageNumber})
            return self.ReturnPageAround(argv[0], destinationPageNumber, indexFileName)

        else:
            return str()

    def GetPreviousPage(self, argv=list()):
        if self.currentPage > 0:
            destinationPageNumber = str(self.currentPage - 1)
            if self.currentPage == 1:
                ''' Must catch KeyError exception '''
                indexFileName = self.indexFileName.format(page_number="")

            else:
                ''' Must catch KeyError exception '''
                indexFileName = self.indexFileName.format(page_number=destinationPageNumber)
            
            return self.ReturnPageAround(argv[0], destinationPageNumber, indexFileName)
        
        else:
            return str()
