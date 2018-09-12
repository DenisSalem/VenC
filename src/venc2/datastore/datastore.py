#! /usr/bin/python

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

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.entry import yield_entries_content
from venc2.datastore.entry import Entry
from venc2.datastore.metadata import MetadataNode
from venc2.pattern.codeHighlight import CodeHighlight

# Generic method used to iterate
def For(iterable, argv):
    return argv[1].join(
        [
            argv[0].format(something) for something in iterable
        ]
    )

def PerformRecursion(openString, content, separator, closeString, nodes):
    outputString = openString
    for node in sorted(nodes, key = lambda x : x.value):
        variables = {
            "value" : node.value,
            "count" : node.count,
            "weight" : node.weight,
            "path" : node.path
        }

        if len(node.childs) == 0:
            outputString += content.format(variables) + separator

        else:
            outputString += content.format(variables) + PerformRecursion(
                openString,
                content,
                separator,
                closeString,
                node.childs
            )

    return outputString + closeString

class DataStore:
    def __init__(self):
        self.blogConfiguration = GetBlogConfiguration()
        self.entries = list()
        self.entriesPerDates = list()
        self.entriesPerCategories = list()
        self.requestedEntryIndex = 0
        self.codeHighlight = CodeHighlight()
        
        ''' Entry index is different from entry id '''
        entryIndex = 0
        for filename in YieldEntriesContent():
            self.entries.append(Entry(filename))

            ''' Update entriesPerDates '''
            if self.blogConfiguration["path"]["datesDirectoryName"] != '':
                formattedDate = self.entries[-1].date.strftime(self.blogConfiguration["path"]["datesDirectoryName"])
                entriesIndex = self.GetEntriesIndexForGivenDate(formattedDate)
                if entriesIndex != None:
                    self.entriesPerDates[entriesIndex].count +=1
                    self.entriesPerDates[entriesIndex].relatedTo.append(entryIndex)
                else:
                    self.entriesPerDates.append(MetadataNode(formattedDate, entryIndex))


            ''' Update entriesPerCategories '''

            for category in self.entries[-1].rawCategories:
                branch = category.split(' > ')
                path = ".:GetRelativeOrigin:."
                root = self.entriesPerCategories
                for nodeName in branch:
                    if nodeName == '':
                        continue

                    path += nodeName+'/'

                    if not nodeName in [metadata.value for metadata in root]:
                        root.append(MetadataNode(nodeName, entryIndex))
                        root[-1].path = path
                        root = root[-1].childs

                    else:
                        for node in root:
                            if node.value == nodeName:
                                node.count +=1
                                node.relatedTo.append(entryIndex)
                                root = node.childs

            entryIndex += 1
    
        ''' Setup BlogDates Data '''
        self.BlogDates = list()
        for node in self.entriesPerDates:
            self.BlogDates.append({
                "date":node.value,
                "dateUrl": ".:GetRelativeOrigin:."+node.value,
                "count": node.count,
                "weight": node.weight
            })

    def GetBlogMetadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return self.blogConfiguration[argv[0]]
    
    def GetBlogMetadataIfExists(self, argv):
        try:
            return self.blogConfiguration[argv[0]]
            
        except KeyError:
            return str()

    def GetEntryMetadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return str( getattr(self.entries[self.requestedEntryIndex], argv[0]))
    
    def GetEntryMetadataIfExists(self, argv):
        try:
            return str( getattr(self.entries[self.requestedEntryIndex], argv[0]))

        except AttributeError:
            return str()

    def GetEntriesIndexForGivenDate(self, value):
        index = 0
        for metadata in self.entriesPerDates:
            if value == metadata.value:
                return index

            index += 1


    def GetEntriesForGivenDate(self, value, reverse):
        index = 0
        for metadata in self.entriesPerDates:
            if value == metadata.value:
                break
            index += 1

        for entry in (self.entriesPerDates[index].relatedTo[::-1] if reverse else self.entriesPerDates[index].relatedTo):
            self.requestedEntryIndex = entry
            yield self.entries[entry]
            
    def GetEntries(self, reverse=False):
        self.requestedEntryIndex = 0 if not reverse else len(self.entries) - 1

        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry

            if not reverse:
                self.requestedEntryIndex += 1

            else:
                self.requestedEntryIndex -= 1
    
    def GetEntryTitle(self, argv=list()):
        title = self.entries[self.requestedEntryIndex].title
        return title if title != None else str()
    
    def GetEntryID(self, argv=list()):
        return self.entries[self.requestedEntryIndex].id

    def GetEntryYear(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.year
        
    def GetEntryMonth(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.month
        
    def GetEntryDay(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.day

    def GetEntryHour(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.hour
    
    def GetEntryMinute(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.minute

    def GetEntryDate(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.strftime(self.blogConfiguration["dateFormat"])

    def GetEntryDateURL(self, argv=list()):
        return self.entries[self.requestedEntryIndex].date.strftime(self.blogConfiguration["path"]["datesDirectoryName"])

    def GetEntryURL(self, argv=list()):
        return self.blogConfiguration["path"]["entryFileName"].format({
            "entryId" : self.entries[self.requestedEntryIndex].id
        })

    def GetAuthorName(self, argv=list()):
        return self.blogConfiguration["authorName"]

    def GetBlogName(self, argv=list()):
        return self.blogConfiguration["blogName"]
        
    def GetBlogDescription(self, argv=list()):
        return self.blogConfiguration["blogDescription"]
        
    def GetBlogKeywords(self, argv=list()):
        return self.blogConfiguration["blogKeywords"]

    def GetAuthorDescription(self, argv=list()):
        return self.blogConfiguration["authorDescription"]
        
    def GetBlogLicense(self, argv=list()):
        return self.blogConfiguration["license"]
    
    def GetBlogURL(self, argv=list()):
        return self.blogConfiguration["blogUrl"]
    
    def GetBlogLanguage(self, argv=list()):
        return self.blogConfiguration["blogLanguage"]
    
    def GetAuthorEmail(self, argv=list()):
        return self.blogConfiguration["authorEmail"]

    def ForBlogDates(self, argv):
        return For(self.BlogDates, argv)

    def ForEntryTags(self, argv):
        return For(self.entries[self.requestedEntryIndex].tags, argv)
    
    def ForEntryAuthors(self, argv):
        return For(self.entries[self.requestedEntryIndex].authors, argv)

    def ForBlogCategories(self, argv):
        outputString = str()
        outputString += PerformRecursion(
            argv[0],
            argv[1],
            argv[2],
            argv[3],
            self.entriesPerCategories
        )
        return outputString

        
        
        

        
