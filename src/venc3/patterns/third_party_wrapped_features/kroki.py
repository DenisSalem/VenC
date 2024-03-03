#! /usr/bin/env python3

#    Copyright 2016, 2021 Denis Salem
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

def kroki_from_file(pattern, endpoint, image_format, filename, provider = "https://kroki.io/"):
    from venc3.patterns.non_contextual import include_file
    code = include_file(pattern, filename)
    return kroki(pattern, endpoint, image_format, code, provider)
    
def kroki(pattern, endpoint, image_format, code, provider = "https://kroki.io/"):
    endpoint = endpoint.strip()
    image_format = image_format.strip()
    provider = provider.strip()
    
    import hashlib
    filename = "kroki_"+hashlib.md5(code.encode('utf-8')).hexdigest()+"."+image_format
    import os
    if not filename in os.listdir(os.getcwd()+"/extra"):
        import zlib;
        import base64
        encoded_code=base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode("utf-8")
        
        if not os.path.isfile("extra/"+code+"."+image_format):
            from urllib.request import Request, urlopen

            try:
                print(encoded_code)
                request = Request(
                    provider+'/'+endpoint+'/'+image_format+'/'+encoded_code,
                    headers={'User-Agent': 'VenC'}
                ) 
                stream = urlopen(request)
                content = stream.read()
                
                if stream.getcode() != 200:
                    from venc3.exceptions import VenCException
                    raise VenCException(("exception_place_holder", "API Error: {0}".format(stream.getcode())), pattern)
                    
                with open("extra/"+filename,"wb") as f:
                    f.write(content)
                        
            except Exception as e:
                from venc3.exceptions import VenCException
                raise VenCException(("exception_place_holder", str(e)), pattern)
              
    return "<img class=\"__VENC_KROKI__\" src=\"\x1a/"+filename+"\">"
