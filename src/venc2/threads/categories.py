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
import urllib.parse

from venc2.prompt import notify
from venc2.threads import Thread

class CategoriesThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns_map):
        super().__init__(prompt, datastore, theme, patterns_map)
        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.sub_folders = self.datastore.blog_configuration["path"]["categories_sub_folders"]
        if len(self.sub_folders) and self.sub_folders[-1] != '/':
            self.sub_folders += '/'
        self.export_path = "blog/"+self.sub_folders
        self.category_value = ""
        self.relative_origin = ""
        self.in_thread = True
        self.disable_rss_feed = self.datastore.blog_configuration["disable_rss_feed"]
        self.disable_atom_feed = self.datastore.blog_configuration["disable_atom_feed"]
        
        if (not self.disable_rss_feed) or (not self.disable_atom_feed):
            from venc2.threads.feed import FeedThread
        
        if not self.disable_rss_feed:
            self.rss_feed = FeedThread(datastore, theme, self.patterns_map, "rss")
        
        if not self.disable_atom_feed:
            self.atom_feed = FeedThread(datastore, theme, self.patterns_map, "atom")
 
    def if_in_categories(self, argv):
        return argv[0].strip()

    def do(self, root=None):
        if root == None:
            root = self.datastore.entries_per_categories
        
        len_root = len(root)
        for i in range(0, len_root):
            node = root[i]
            if node.value in self.disable_threads:
                continue
            
            if i == len_root-1:
                tree_special_char = '└'
                
            else:
                tree_special_char = '├'
                
            notify(self.indentation_level+tree_special_char+"─ "+node.value+"...")

            export_path = self.export_path
            category_value = self.category_value
            self.category_value += node.value+'/'
            self.export_path += str(node.value+'/').replace(' ','-')
            self.relative_origin = ''.join([ '../' for f in self.export_path.split("/")[1:] if f != '' ]).replace("//",'/')

            try:
                os.makedirs(self.export_path)

            except FileExistsError:
                pass

            # Get entries
            entries = [self.datastore.entries[entry_index] for entry_index in node.related_to]
            self.organize_entries( entries[::-1] if self.datastore.blog_configuration["reverse_thread_order"] else entries )
            super().do()
            entries = sorted(entries, key = lambda entry : entry.id, reverse=True)[0:self.datastore.blog_configuration["feed_lenght"]]
            if i == len_root-1:
                tree_special_char = ' '
                
            else:
                tree_special_char = '│'
                
            if not self.disable_rss_feed:
                self.rss_feed.do(entries, self.export_path, self.relative_origin,self.indentation_level+tree_special_char+' ', ' ├' if not self.disable_atom_feed or self.datastore.enable_jsonld or len(node.childs) else ' └')
    
            if not self.disable_atom_feed:
                self.atom_feed.do(entries, self.export_path, self.relative_origin,self.indentation_level+tree_special_char+' ', ' ├' if len(node.childs) or self.datastore.enable_jsonld else ' └')
            
            if self.datastore.enable_jsonld:
                from venc2.l10n import messages
                notify(self.indentation_level+tree_special_char+' '+ (' ├─ ' if len(node.childs) else ' └─ ')+messages.generating_jsonld_doc)
                import json
                blog_url = self.datastore.blog_configuration["blog_url"]
                category_as_jsonld = self.datastore.categories_as_jsonld[self.category_value]
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
                f = open(("blog/"+self.sub_folders+self.category_value+"categories.jsonld").replace(' ','-'), 'w')
                f.write(dump)
            
            if len_root - 1 == i:
                self.indentation_level += "   "
            else:
                self.indentation_level += "│  "
            
            self.do(root=node.childs)
            self.indentation_level = self.indentation_level[:-3]
            
            # Restore path
            self.export_path = export_path
            self.category_value = category_value


    def JSONLD(self, argv):
        if self.current_page == 0:
            return '<script type="application/ld+json" src="categories.jsonld"></script>'
        
        return ''





                
                


