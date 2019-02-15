#! /usr/bin/python3

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

from venc2.threads import Thread

class MainThread(Thread):
    def __init__(self, prompt, datastore, theme, patterns, forbidden):
        if datastore.blog_configuration["disable_main_thread"]:
            prompt = ""

        super().__init__(prompt, datastore, theme, patterns, forbidden)
        
        if datastore.blog_configuration["disable_main_thread"]:
            self.pages_count = 0

        else:
            self.organize_entries([
                entry for entry in datastore.get_entries(
                    datastore.blog_configuration["reverse_thread_order"]
                )
            ])

        self.filename = self.datastore.blog_configuration["path"]["index_file_name"]
        self.relative_origin = str()
        self.export_path = "blog/"
        self.in_thread = True
        disable_rss_feed = self.datastore.blog_configuration["disable_rss_feed"]
        disable_atom_feed = self.datastore.blog_configuration["disable_atom_feed"]
        entries = [] 
        if (not disable_rss_feed) or (not disable_atom_feed):
            entries += self.get_feed_entries()
            from venc2.threads.feed import FeedThread
        
        if not disable_atom_feed:
            FeedThread(datastore, theme, patterns, forbidden, "atom").do(entries, self.export_path, self.relative_origin)
            
        if not disable_rss_feed:
            FeedThread(datastore, theme, patterns, forbidden, "rss").do(entries, self.export_path, self.relative_origin)
            
    def get_feed_entries(self):
        entries = []
        i = 0
        for entry in self.datastore.get_entries(True):
            entries.append(entry)
            i+=1
            if i == self.datastore.blog_configuration["feed_lenght"]:
                return entries
                    
    def do(self):
        super().do()
        if self.datastore.enable_jsonld: 
            import json
            dump = json.dumps(self.datastore.root_as_jsonld)
            f = open("blog/root.jsonld", 'w')
            f.write(dump)
            
    def JSONLD(self, argv):
        if self.current_page == 0:
            return '<script type="application/ld+json" src="root.jsonld"></script>'
        
        return ''
                
                


