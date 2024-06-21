#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
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


embed_content_cache = []
embed_providers = dict()

def cache_embed_exists(link):
    import hashlib
    cache_filename = hashlib.md5(link.encode('utf-8')).hexdigest()
    try:
        return open("caches/embed/"+cache_filename,"r").read()

    except FileNotFoundError:
        return ""

def get_embed_content(pattern, providers, target):  
    from urllib.parse import urlparse
    url = urlparse(target)

    try:
        key = [ key for key in providers["oembed"].keys() if url.netloc in key][0]

    except IndexError:
        from venc3.exceptions import VenCException
        raise VenCException(("unknown_provider", url.netloc), pattern)
    
    try:
        from urllib.request import Request, urlopen
        from urllib.parse import urlencode
        request = Request(
            providers["oembed"][key][0]+'?'+urlencode({
                "url": url.geturl(),
                "format":"json",
                "maxwidth": 640,
                "maxheight": 320
            })
        )
        stream = urlopen(request)
        content = stream.read()

    except Exception as e:
        from venc3.exceptions import VenCException
        raise VenCException(("connectivity_issue", str(e)), pattern)

    if stream.getcode() != 200:
        from venc3.exceptions import VenCException
        raise VenCException(("ressource_unavailable", url.geturl()), pattern)

    try:
        import json
        html = "<div class=\"__VENC_OEMBED__\">"+json.loads(content)["html"]+"</div>"
        html = "</p>"+html+"<p>" if pattern.root.has_markup_language else html
        
    except Exception as e:
        from venc3.exceptions import VenCException
        raise VenCException(("response_is_not_json", url.geturl(), content), pattern)
        
    try:
        import hashlib, shutil
        cache_filename = hashlib.md5(url.geturl().encode('utf-8')).hexdigest()
        shutil.os.makedirs("caches/embed", exist_ok=True)
        f = open("caches/embed/"+cache_filename, "w")
        f.write(html)
        f.close()

    except PermissionError:
        from venc3.prompt import notify
        notify(("wrong_permissions", "caches/embed/"+cache_filename), color="YELLOW")
        
    return html

def wrapper_embed_content(pattern, content_url):
    global embed_content_cache
    embed_content_cache = cache_embed_exists(content_url)
    if embed_content_cache != "":
        return embed_content_cache

    else:
        global embed_providers
        if embed_providers == dict():
            import os
            import json
            from venc3 import package_data_path
            
            f = open(package_data_path+"/oembed_providers.json")
            embed_providers["oembed"] = {}
            j = json.load(f)
            for p in j:
                embed_providers["oembed"][p["provider_url"]] = []
                for e in p["endpoints"]:
                    embed_providers["oembed"][p["provider_url"]].append(e["url"])
                    
    return get_embed_content(pattern, embed_providers, content_url)
