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

from venc3.prompt import notify
from venc3.threads import Thread

class CategoriesThread(Thread):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_categories)
        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["categories_sub_folders"]
        if len(self.sub_folders) and self.sub_folders[-1] != '/':
            self.sub_folders += '/'
        self.export_path = "blog/"+self.sub_folders
        self.category_value = ""
        self.relative_origin = ""
        self.in_thread = True
        self.thread_has_feeds = True

        self.disable_rss_feed = self.datastore.blog_configuration["disable_rss_feed"]
        self.disable_atom_feed = self.datastore.blog_configuration["disable_atom_feed"]
 
    def if_in_categories(self, node, string1, string2=''):
        return string1.strip()

    def do_feeds(self, entries, node, indentation_type):
        entries = sorted(entries, key = lambda entry : entry.id, reverse=True)[0:self.datastore.blog_configuration["feed_lenght"]]

        if (not self.disable_rss_feed) or (not self.disable_atom_feed):
            from venc3.threads.feed import FeedThread
              
        if not self.disable_rss_feed:
            FeedThread("rss", '├' if not self.disable_atom_feed or self.enable_jsonld or len(node.childs) else '└', self.indentation_level+indentation_type).do(entries, self.export_path, self.relative_origin)
    
        if not self.disable_atom_feed:
            FeedThread("atom", '├' if len(node.childs) or self.enable_jsonld else '└', self.indentation_level+indentation_type).do(entries, self.export_path, self.relative_origin)
            
    def do_jsonld(self, node, indentation_type):
        from venc3.l10n import messages
        import json
        blog_url = self.datastore.blog_configuration["blog_url"]
        category_as_jsonld = self.datastore.categories_as_jsonld[node.path]
        position = 2
        category_breadcrumb_path = ''
        for sub_category in self.category_value.split('/'):
            category_breadcrumb_path += sub_category+'/'
            category_as_jsonld["breadcrumb"]["itemListElement"].append({
                "@type": "ListItem",
                "position": position,
                "item": {
                    "@id": blog_url+'/'+self.sub_folders+category_breadcrumb_path+"categories.jsonld",
                    "url": blog_url+'/'+self.sub_folders+category_breadcrumb_path,
                    "name": self.datastore.blog_configuration["blog_name"] +' | '+ sub_category
                }
            })
            position += 1
        category_as_jsonld["@id"] = blog_url+'/'+self.sub_folders+self.category_value+"categories.jsonld"
        category_as_jsonld["url"] = blog_url+'/'+self.sub_folders+self.category_value
        dump = json.dumps(category_as_jsonld)
        if self.datastore.enable_jsonld:
            notify(self.indentation_level+indentation_type+ ('├─ ' if len(node.childs) or self.datastore.enable_jsonp else '└─ ')+messages.generating_jsonld_doc)
            f = open(self.export_path+"categories.jsonld", 'w')
            f.write(dump)

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
        
        notify(self.indentation_level+tree_special_char+"─ "+node.value+"...")

        export_path = self.export_path
        category_value = self.category_value
        self.category_value += node.value+'/'
        self.export_path += self.path_encode(node.value)+'/'
        self.relative_origin = ''.join([ '../' for f in self.export_path.split("/")[1:] if f != '' ]).replace("//",'/')

        try:
            os.makedirs(self.export_path)

        except FileExistsError:
            pass
            
        return (node, export_path, category_value)
            
    def do(self, root=None):
        if root == None:
            root = self.datastore.entries_per_categories
        
        len_root = len(root)
        for i in range(0, len_root):
            node, export_path, category_value = self.setup_category_context(i, root, len_root)
            if node == None:
                continue
            
            # do actual context
            entries = [self.datastore.entries[entry_index] for entry_index in node.related_to]
            self.organize_entries( entries[::-1] if self.datastore.blog_configuration["reverse_thread_order"] else entries )
            super().do()
            indentation_type = "   " if len_root - 1  == i else "│  "
            self.do_feeds(entries, node, indentation_type)
            if self.datastore.enable_jsonld or self.datastore.enable_jsonp:
                self.do_jsonld(node, indentation_type)
            
            # jump to branchs
            self.indentation_level += indentation_type
            self.do(root=node.childs)
            
            # Restore states
            self.indentation_level = self.indentation_level[:-3]
            self.export_path = export_path
            self.category_value = category_value

    def get_JSONLD(self, node):
        if self.current_page == 0 and self.enable_jsonld:
            return '<script type="application/ld+json" src="categories.jsonld"></script>'
        
        return ''
