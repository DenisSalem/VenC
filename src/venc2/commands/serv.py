import os
import http.server
import urllib.parse 

from venc2.datastore.configuration import get_blog_configuration
from venc2.helpers import die
from venc2.helpers import notify
from venc2.l10n import messages

blog_configuration = get_blog_configuration()

class VenCServer(http.server.CGIHTTPRequestHandler):
    def do_GET(self):
        self.path = urllib.parse.unquote(self.path, encoding=blog_configuration["path_encoding"])        
        super().do_GET()

def serv_blog(argv=list()):
    try:
        os.chdir("blog/")
        PORT = int(blog_configuration["server_port"]) 
        server_address = ("", PORT)
        notify(messages.serving_blog.format(PORT))
        httpd = http.server.HTTPServer(server_address, VenCServer)
        httpd.serve_forever()

    except ValueError:
        die(messages.server_port_is_invalid.format(blog_configuration["server_port"]))

    except KeyboardInterrupt:
        httpd.server_close()
