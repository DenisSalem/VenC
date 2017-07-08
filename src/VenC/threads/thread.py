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

class Thread:
    def __init__(self, prompt, datastore):
        # Notify wich thread is processed
        Notify(prompt)
        
        # Setup useful data
        self.datastore = datastore
        self.currentPage = 0

    def OrganizeEntries(self, entries):
        self.entries = list()
        entriesPerPage = int(self.datastore.blogConfiguration["entriesPerPages"])
        print(entriesPerPage)
        for i in range(0, entriesPerPage):
            self.entries.append(
                entries[i*entriesPerPage:(i+1)*entriesPerPage]
            )
            print(self.entries[-1])


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
