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

from venc2.datastore.configuration import get_blog_configuration
from venc2.prompt import die
from venc2.prompt import notify
from venc2.l10n import messages

blog_configuration = get_blog_configuration()

class VenCServer(http.server.CGIHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        
    def do_GET(self):
        self.path = urllib.parse.unquote(self.path, encoding=blog_configuration["path_encoding"])
        super().do_GET()

def serv_blog(argv=list()):
    try:
        os.chdir("blog/")
        PORT = int(argv[0]) if len(argv) else int(blog_configuration["server_port"])
        server_address = ("", PORT)
        notify(messages.serving_blog.format(PORT))
        httpd = http.server.HTTPServer(server_address, VenCServer)
        httpd.serve_forever()

    except OSError as e:
        die(e.strerror)
        
    except ValueError:
        die(messages.server_port_is_invalid.format(blog_configuration["server_port"]))

    except KeyboardInterrupt:
        httpd.server_close()

    except FileNotFoundError:
        die(messages.nothing_to_serv)
