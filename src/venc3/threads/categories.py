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

from venc3.helpers import quirk_encoding
from venc3.threads import Thread

class CategoriesThread(Thread):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_categories)
        self.filename = self.datastore.blog_configuration["paths"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["paths"]["categories_sub_folders"]
        self.export_path = "blog/"+self.sub_folders+'/'
        self.category_value = ""
        self.relative_origin = ""
        self.in_thread = True
        self.thread_has_feeds = True

        self.disable_rss_feed = self.datastore.blog_configuration["disable_rss_feed"]
        self.disable_atom_feed = self.datastore.blog_configuration["disable_atom_feed"]
 
    def if_in_categories(self, node, string1, string2=''):
        return string1.strip()

    def do_feeds(self, entries, node, indentation_type):
        entries = sorted(entries, key = lambda entry : entry.id, reverse=True)[0:self.datastore.blog_configuration["feed_length"]]

        if (not self.disable_rss_feed) or (not self.disable_atom_feed):
            from venc3.threads.feed import FeedThread
              
        if not self.disable_rss_feed:
            FeedThread("rss", '├' if not self.disable_atom_feed or len(node.childs) else '└', self.indentation_level+indentation_type).do(entries, self.export_path, self.relative_origin)
    
        if not self.disable_atom_feed:
            FeedThread("atom", '├' if len(node.childs) else '└', self.indentation_level+indentation_type).do(entries, self.export_path, self.relative_origin)

    def setup_category_context(self, i, root, len_root):
        node = root[i]
        if node.value in self.disable_threads:
            return (None, None, None)
            
        self.thread_name = node.value
        if self.rss_feed:
            self.rss_feed.thread_name = node.value
        
        if self.atom_feed:
            self.atom_feed.thread_name = node.value

        if i == len_root-1:
            tree_special_char = '└'
                
        else:
            tree_special_char = '├'
            
        from venc3.prompt import notify
        notify(("exception_place_holder", node.value+"..."), prepend=self.indentation_level+tree_special_char+"─ ")

        export_path = self.export_path
        category_value = self.category_value
        self.category_value += node.value+'/'
        self.export_path += quirk_encoding(node.value)+'/'
        self.relative_origin = '/'.join([ '..' for f in self.export_path.split("/")[1:] if f != '' ]).replace("//",'/')

        try:
            os.makedirs(self.export_path)

        except FileExistsError:
            pass
            
        return (node, export_path, category_value)
            
    def do(self, root=None):
        if self.datastore.entries_per_categories == None:
            return
            
        if root == None:
            root = self.datastore.entries_per_categories
        
        len_root = len(root)
        for i in range(0, len_root):
            node, export_path, category_value = self.setup_category_context(i, root, len_root)
            if node == None:
                continue
            
            # do actual context
            entries = [entry for entry in self.datastore.entries if entry.id in node.related_to]
            self.organize_entries( entries[::-1] if self.datastore.blog_configuration["reverse_thread_order"] else entries )
            super().do()
            indentation_type = "   " if len_root - 1  == i else "│  "
            self.do_feeds(entries, node, indentation_type)
            
            # jump to branchs
            self.indentation_level += indentation_type
            self.do(root=node.childs)
            
            # Restore states
            self.indentation_level = self.indentation_level[:-3]
            self.export_path = export_path
            self.category_value = category_value
