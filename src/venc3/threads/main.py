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

from venc3.threads import Thread

class MainThread(Thread):
    def __init__(self):
        from venc3.l10n import messages
        super().__init__(messages.export_main_thread)
        from venc3.datastore import datastore
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
        self.thread_has_feeds = True

            
    def get_feed_entries(self):
        entries = []
        i = 0
        for entry in self.datastore.get_entries(True):
            entries.append(entry)
            i+=1
            if i == self.datastore.blog_configuration["feed_lenght"]:
                return entries
                
        return entries
    
    def do_feeds(self):
        disable_rss_feed = self.datastore.blog_configuration["disable_rss_feed"]
        disable_atom_feed = self.datastore.blog_configuration["disable_atom_feed"]
        entries = [] 
        if (not disable_rss_feed) or (not disable_atom_feed):
            entries += self.get_feed_entries()
            from venc3.threads.feed import FeedThread
        
        if not disable_atom_feed:
            FeedThread("atom", '└' if disable_rss_feed and not self.enable_jsonld else '├', "│  ").do(entries, self.export_path, self.relative_origin )
            
        if not disable_rss_feed:
            FeedThread("rss", '└' if not self.enable_jsonld else '├', "│  ").do(entries, self.export_path, self.relative_origin)
 
    def do_jsonld(self):
        if self.datastore.enable_jsonld or self.datastore.enable_jsonp:
            from venc3.prompt import notify
            import json
            dump = json.dumps(self.datastore.root_as_jsonld)
        
        if self.datastore.enable_jsonld:
            notify(("generating_jsonld_doc",), prepend=self.indentation_level+('└─ ' if not self.datastore.enable_jsonp else '├─ '))
            f = open("blog/root.jsonld", 'w')
            f.write(dump)
        
        if self.datastore.enable_jsonp:
            notify(("generating_jsonp_doc",), prepend=self.indentation_level+'└─ ')
            import hashlib
            url_digest = hashlib.sha512(self.datastore.blog_url.encode('utf-8'))
            f = open("blog/root.jsonp", 'w')
            f.write("function _"+url_digest.hexdigest()+"() {return "+dump+";}")
            
    def do(self):
        super().do()
        self.do_feeds()
        self.do_jsonld()

    def get_JSONLD(self, node):
        if self.current_page == 0 and self.datastore.enable_jsonld:
            return '<script type="application/ld+json" src="root.jsonld"></script>'
        
        return ''
                
    def if_in_main_thread(self, node, string1, string2=''):
        return string1.strip()
