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

from venc3.helpers import quirk_encoding
from venc3.threads import Thread

class ArchivesThread(Thread):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_archives)
        self.filename = self.datastore.blog_configuration["paths"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["paths"]["archives_sub_folders"]
        if len(self.sub_folders) and self.sub_folders[-1] != '/':
            self.sub_folders += '/'
            
        self.relative_origin = str(".."+'/'.join([ "/.." for p in self.sub_folders.split('/') if p != ''])).replace("//",'/')
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

        from venc3.prompt import notify
        notify(("exception_place_holder", archive.value+"..."), prepend="│\t "+tree_special_char+"─ ")
        self.export_path = str("blog/"+self.sub_folders+'/'+quirk_encoding(archive.value)+'/')
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
