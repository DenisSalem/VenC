#! /usr/bin/env python3

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
import http.server
import urllib.parse 

from venc3.datastore.configuration import get_blog_configuration

blog_configuration = get_blog_configuration()

class VenCServer(http.server.CGIHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
    
    def do_GET(self):
        self.path = urllib.parse.unquote(self.path, encoding=blog_configuration["path_encoding"])
        super().do_GET()

    def send_error(self, code, message=None, explain=None):
        from venc3.datastore.hardcoded_assets import default_error_page
        self.error_message_format = default_error_page
        super().send_error(code, message, explain)

def serv_blog(params):
    from venc3.prompt import notify

    try:
        PORT = params[0] if len(params) else blog_configuration["server_port"]
        PORT = int(PORT)
        
    except ValueError:
        from venc3.prompt import die
        die(("server_port_is_invalid", str(PORT)))
        
    try:
        os.chdir("blog/")
        server_address = ("", PORT)
        notify(("do_not_use_in_production",), color="YELLOW")        
        notify(("serving_blog", PORT))
        httpd = http.server.HTTPServer(server_address, VenCServer)
        httpd.serve_forever()

    except OSError as e:
        from venc3.prompt import die
        die(("exception_place_holder", e.strerror))
        
    except KeyboardInterrupt:
        httpd.server_close()

    except FileNotFoundError:
        from venc3.prompt import die
        die(("nothing_to_serv",))
