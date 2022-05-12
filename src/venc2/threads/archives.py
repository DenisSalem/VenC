#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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
    def __init__(self, prompt, datastore, theme, patterns_map):
        super().__init__(prompt, datastore, theme, patterns_map)
        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["archives_sub_folders"]
        if len(self.sub_folders) and self.sub_folders[-1] != '/':
            self.sub_folders += '/'
            
        self.relative_origin = str("../"+''.join([ "../" for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
        self.in_thread = True
        self.thread_has_feeds = False

    def if_in_archives(self, node, string1, string2=''):
        return string1.strip()

    def setup_archive_context(self, i, len_archives):
        archive = self.datastore.entries_per_archives[i]
        if archive.value in self.disable_threads:
            return None

        self.thread_name = archive.value
        
        tree_special_char = '└' if i == len_archives-1 else '├'

                
        notify("│\t "+tree_special_char+"─ "+archive.value+"...")
        self.export_path = str("blog/"+self.sub_folders+'/'+archive.value+'/')
        self.export_path = self.path_encode(self.export_path)            
        os.makedirs(self.export_path)
        self.organize_entries([
            entry for entry in self.datastore.get_entries_for_given_date(
                archive.value,
                self.datastore.blog_configuration["reverse_thread_order"]
            )
        ])
        return archive
        
    def do(self):
        len_archives = len(self.datastore.entries_per_archives)
        for i in range(0, len_archives):
            archive = self.setup_archive_context(i, len_archives)
            if archive == None:
                continue
                
            super().do()
            if self.datastore.enable_jsonld or self.datastore.enable_jsonp:
                from venc2.l10n import messages
                notify("│\t "+('│' if i != len_archives-1 else ' ')+"  └─ "+messages.generating_jsonld_doc)
                
                blog_url = self.datastore.blog_configuration["blog_url"]
                archive_as_jsonld = self.datastore.archives_as_jsonld[archive.value]
                archive_as_jsonld["breadcrumb"]["itemListElement"].append({
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": blog_url+'/'+self.sub_folders+archive.value+"/archives.jsonld",
                        "url": blog_url+'/'+self.sub_folders+archive.value,
                        "name": self.datastore.blog_configuration["blog_name"] +' | '+archive.value
                    }
                })
                archive_as_jsonld["@id"] = blog_url+'/'+self.sub_folders+archive.value+"/archives.jsonld"
                archive_as_jsonld["url"] = blog_url+'/'+self.sub_folders+archive.value
                dump = json.dumps(archive_as_jsonld)
                f = open("blog/"+self.sub_folders+'/'+archive.value+"/archives.jsonld", 'w')
                f.write(dump)

    def get_JSONLD(self, node):
        if self.current_page == 0 and self.enable_jsonld:
            return '<script type="application/ld+json" src="archives.jsonld"></script>'
        
        return ''
