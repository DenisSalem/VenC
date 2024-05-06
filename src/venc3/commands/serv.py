#! /usr/bin/env python3

#    Copyright 2016, 2024 Denis Salem
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
import http.server
from multiprocessing import Process
import shutil
import time
import urllib.parse 

from venc3.commands.export import export_blog
from venc3.datastore.configuration import get_blog_configuration
from venc3.helpers import copy_recursively
from venc3.prompt import notify

blog_configuration = get_blog_configuration() # TODO: Load only in time.

WATCHED_FILES = {}
LAST_WATCH_PASS = time.time()

def get_files(folder=".."):
    files = []
    for item in os.listdir(folder):
        if item in ["extra", "includes", "entries", "theme", "blog_configuration.yaml"] or (folder != ".."):
            if item[0] != '.':
                files += [folder+"/"+item]
                if os.path.isdir(folder+"/"+item):
                    files += get_files(folder+"/"+item)
    return files

def watch_files():
    global LAST_WATCH_PASS
    global WATCHED_FILES
    refresh_extra = False
    refresh_assets = False
    refresh_all = False
    
    files = get_files()
    for path in files:
        WATCHED_FILES[path] = os.path.getmtime(path)
        if WATCHED_FILES[path] > LAST_WATCH_PASS and not os.path.isdir(path):
            if path[:len("../extra")] == "../extra" :
                refresh_extra |= True

            elif path[:len("../theme/assets")] == "../theme/assets":
                refresh_assets |= True
                                
            else:
              refresh_all |= True
              break
    
    keys = tuple(WATCHED_FILES.keys())
    
    for filename in keys:
      if not filename in files:
          WATCHED_FILES.pop(filename)
          to_delete = None
          if filename[:len("../extra")] == "../extra" and filename != "../extra":
              to_delete = "blog"+filename[len("../extra"):]
              
          elif filename[:len("../theme/assets")] == "../theme/assets" and filename != "../theme/assets":
              to_delete = "blog"+ filename[len("../theme/assets"):]
              
          else:
              refresh_all |= True
              break
          
          if to_delete != None:
              notify(("deleting_file", to_delete))
              try:
                  if os.path.isdir("../"+to_delete):
                      shutil.rmtree("../"+to_delete)
                      
                  else:
                          os.unlink("../"+to_delete)         
              except FileNotFoundError:
                  pass
                      
    LAST_WATCH_PASS = time.time()
    
    if refresh_all:
        return True
        
    else:
        if refresh_extra or refresh_assets:
            notify(("copy_assets_and_extra_files",))
            
        if refresh_extra:
            copy_recursively("../extra/", "./")
    
        if refresh_assets:
            copy_recursively("../theme/assets/", "./")
            
        return False
    
def export_blog_wrapper(params):
    os.chdir('..')

    from venc3.datastore import configuration
    configuration.BLOG_CONFIGURATION = None
    get_blog_configuration()
    
    export_blog(params)
    
class VenCServer(http.server.CGIHTTPRequestHandler):    
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def do_GET(self):
        if watch_files(): # will trigger partial refresh of extra and assets
            sub_process = Process(target=export_blog_wrapper,args=([],))
            sub_process.start()
            sub_process.join()
        
        self.path = urllib.parse.unquote(self.path, encoding=blog_configuration["path_encoding"])
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        from venc3.datastore.hardcoded_assets import default_error_page
        self.error_message_format = default_error_page
        super().send_error(code, message, explain)
            
def serv(params):            
    port = params[0] if len(params) else blog_configuration["server_port"]
        
    try:
        os.chdir("blog/")
        server_address = ("", port)
        notify(("do_not_use_in_production",), color="YELLOW")        
        notify(("serving_blog", port))
        httpd = http.server.HTTPServer(server_address, VenCServer)
        watch_files()
        httpd.serve_forever()

    except OSError as e:
        from venc3.prompt import die
        die(("exception_place_holder", e.strerror))
        
    except KeyboardInterrupt:
        httpd.server_close()
            
    except FileNotFoundError:
        from venc3.prompt import die
        die(("nothing_to_serv",))
