#! /usr/bin/python3

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
import json

from venc2.prompt import notify
from venc2.threads import Thread


class ArchivesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns, forbidden):
        super().__init__(prompt, datastore, theme, patterns, forbidden)
        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["dates_sub_folders"]
        if len(self.sub_folders) and self.sub_folders[-1] != '/':
            self.sub_folders += '/'
            
        self.relative_origin = str("../"+''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = True

    def if_in_archives(self, argv):
        return argv[0].strip()
        
    def do(self):
        len_archives = len(self.datastore.entries_per_dates)
        for i in range(0, len_archives):
            thread = self.datastore.entries_per_dates[i]
            if thread.value in self.disable_threads:
                continue

            if i == len_archives-1:
                tree_special_char = '└'
            else:
                tree_special_char = '├'
                
            notify("│\t "+tree_special_char+"─ "+thread.value+"...")
            self.export_path = str("blog/"+self.sub_folders+'/'+thread.value+'/').replace(' ','-')
            os.makedirs(self.export_path)
            self.organize_entries([
                entry for entry in self.datastore.get_entries_for_given_date(
                    thread.value,
                    self.datastore.blog_configuration["reverse_thread_order"]
                )
            ])
            super().do()
            if self.datastore.enable_jsonld:
                blog_url = self.datastore.blog_configuration["blog_url"]
                self.datastore.archives_as_jsonld[thread.value]["breadcrumb"]["itemListElement"].append({
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": blog_url+'/'+self.sub_folders+thread.value+"/archives.jsonld",
                        "url": blog_url+'/'+self.sub_folders+thread.value,
                        "name": self.datastore.blog_configuration["blog_name"] +' | '+thread.value
                    }
                })
                dump = json.dumps(self.datastore.archives_as_jsonld[thread.value])
                f = open("blog/"+self.sub_folders+'/'+thread.value+"/archives.jsonld", 'w')
                f.write(dump)

    def JSONLD(self, argv):
        if self.current_page == 0:
            return '<script type="application/ld+json" src="archives.jsonld"></script>'
        
        return ''



                
                


