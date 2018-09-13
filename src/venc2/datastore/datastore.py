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

def merge(iterable, argv):
    return argv[1].join(
        [
            argv[0].format(something) for something in iterable
        ]
    )

def perform_recursion(open_string, content, separator, close_string, nodes):
    output_string = open_string
    for node in sorted(nodes, key = lambda x : x.value):
        variables = {
            "value" : node.value,
            "count" : node.count,
            "weight" : node.weight,
            "path" : node.path
        }

        if len(node.childs) == 0:
            output_string += content.format(variables) + separator

        else:
            output_string += content.format(variables) + perform_recursion(
                open_string,
                content,
                separator,
                close_string,
                node.childs
            )

    return output_string + close_string

class DataStore:
    def __init__(self):
        self.blog_configuration = get_blog_configuration()
        self.entries = list()
        self.entries_per_dates = list()
        self.entries_per_categories = list()
        self.requested_entry_index = 0
        self.code_highlight = CodeHighlight()
        
        ''' Entry index is different from entry id '''
        entry_index = 0
        for filename in yield_entries_content():
            self.entries.append(Entry(filename))

            ''' Update entriesPerDates '''
            if self.blog_configuration["path"]["datesDirectoryName"] != '':
                formatted_date = self.entries[-1].date.strftime(self.blog_configuration["path"]["datesDirectoryName"])
                entries_index = self.get_entries_index_for_given_date(formatted_date)
                if entries_index != None:
                    self.entries_per_dates[entries_index].count +=1
                    self.entries_per_dates[entries_index].related_to.append(entry_index)
                else:
                    self.entries_per_dates.append(MetadataNode(formatted_date, entry_index))


            ''' Update entriesPerCategories '''

            for category in self.entries[-1].raw_categories:
                branch = category.split(' > ')
                path = ".:GetRelativeOrigin:."
                root = self.entries_per_categories
                for node_name in branch:
                    if node_name == '':
                        continue

                    path += node_name+'/'

                    if not node_name in [metadata.value for metadata in root]:
                        root.append(MetadataNode(node_name, entry_index))
                        root[-1].path = path
                        root = root[-1].childs

                    else:
                        for node in root:
                            if node.value == node_name:
                                node.count +=1
                                node.related_to.append(entry_index)
                                root = node.childs

            entry_index += 1
    
        ''' Setup BlogDates Data '''
        self.blog_dates = list()
        for node in self.entries_per_dates:
            self.blog_dates.append({
                "date":node.value,
                "dateUrl": ".:GetRelativeOrigin:."+node.value,
                "count": node.count,
                "weight": node.weight
            })

    def get_blog_metadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return self.blog_configuration[argv[0]]
    
    def get_blog_metadata_if_exists(self, argv):
        try:
            return self.blog_configuration[argv[0]]
            
        except KeyError:
            return str()

    def get_entry_metadata(self, argv):
        # if exception is raised it will be automatically be catch by processor.
        return str( getattr(self.entries[self.requested_entry_index], argv[0]))
    
    def get_entry_metadata_if_exists(self, argv):
        try:
            return str( getattr(self.entries[self.requested_entry_index], argv[0]))

        except AttributeError:
            return str()

    def get_entries_index_for_given_date(self, value):
        index = 0
        for metadata in self.entries_per_dates:
            if value == metadata.value:
                return index

            index += 1


    def get_entries_for_given_date(self, value, reverse):
        index = 0
        for metadata in self.entries_per_dates:
            if value == metadata.value:
                break
            index += 1

        for entry in (self.entries_per_dates[index].related_to[::-1] if reverse else self.entries_per_dates[index].related_to):
            self.requested_entry_index = entry
            yield self.entries[entry]
            
    def get_entries(self, reverse=False):
        self.requested_entry_index = 0 if not reverse else len(self.entries) - 1

        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry

            if not reverse:
                self.requested_entry_index += 1

            else:
                self.requested_entry_index -= 1
    
    def get_entry_title(self, argv=list()):
        title = self.entries[self.requested_entry_index].title
        return title if title != None else str()
    
    def get_entry_id(self, argv=list()):
        return self.entries[self.requested_entry_index].id

    def get_entry_year(self, argv=list()):
        return self.entries[self.requested_entry_index].date.year
        
    def get_entry_month(self, argv=list()):
        return self.entries[self.requested_entry_index].date.month
        
    def get_entry_day(self, argv=list()):
        return self.entries[self.requested_entry_index].date.day

    def get_entry_hour(self, argv=list()):
        return self.entries[self.requested_entry_index].date.hour
    
    def get_entry_minute(self, argv=list()):
        return self.entries[self.requested_entry_index].date.minute

    def get_entry_date(self, argv=list()):
        return self.entries[self.requested_entry_index].date.strftime(self.blog_configuration["dateFormat"])

    def get_entry_date_url(self, argv=list()):
        return self.entries[self.requested_entry_index].date.strftime(self.blog_configuration["path"]["datesDirectoryName"])

    def get_entry_url(self, argv=list()):
        return self.blog_configuration["path"]["entryFileName"].format({
            "entryId" : self.entries[self.requested_entry_index].id
        })

    def get_author_name(self, argv=list()):
        return self.blog_configuration["authorName"]

    def get_blog_name(self, argv=list()):
        return self.blogConfiguration["blogName"]
        
    def get_blog_description(self, argv=list()):
        return self.blog_configuration["blogDescription"]
        
    def get_blog_keywords(self, argv=list()):
        return self.blog_configuration["blogKeywords"]

    def get_author_description(self, argv=list()):
        return self.blog_configuration["authorDescription"]
        
    def get_blog_license(self, argv=list()):
        return self.blog_configuration["license"]
    
    def get_blog_url(self, argv=list()):
        return self.blog_configuration["blogUrl"]
    
    def get_blog_language(self, argv=list()):
        return self.blog_configuration["blogLanguage"]
    
    def get_author_email(self, argv=list()):
        return self.blog_configuration["authorEmail"]

    def for_blog_dates(self, argv):
        return For(self.blog_dates, argv)

    def for_entry_tags(self, argv):
        return merge(self.entries[self.requested_entry_index].tags, argv)
    
    def for_entry_authors(self, argv):
        return merge(self.entries[self.requested_entry_index].authors, argv)

    def for_blog_categories(self, argv):
        output_string = str()
        output_string += perform_recursion(
            argv[0],
            argv[1],
            argv[2],
            argv[3],
            self.entries_per_categories
        )
        return output_string

        
        
        

        
