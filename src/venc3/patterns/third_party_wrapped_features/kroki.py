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

def kroki_from_file(pattern, endpoint, filename, provider = "https://kroki.io/"):
    from venc3.patterns.non_contextual import include_file
    code = include_file(pattern, filename)
    return kroki(pattern, endpoint, code, provider)
    
def kroki(pattern, endpoint, code, provider = "https://kroki.io/"): 
    import hashlib
    filename = "kroki_"+hashlib.md5(code.encode('utf-8')).hexdigest()+".svg"
    import os
    if not filename in os.listdir(os.getcwd()+"/includes"):
        import zlib;
        import base64
        encoded_code=base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode("utf-8")
        
        if not os.path.isfile("extra/"+code+".svg"):
            try:
                import requests
                
            except:
                from venc3.exceptions import VenCException
                raise VenCException(("module_not_found", "requests"), pattern)

            from venc3.exceptions import VenCException
            try:
                r = requests.get(provider+'/'+endpoint+'/svg/'+encoded_code)
                if r.status_code != 200:
                    raise VenCException(("exception_place_holder", "API Error: {0}".format(r.status_code)), pattern)
                    
                with open("extra/"+filename,"w") as f:
                    f.write(r.text)
                    
            except Exception as e:
                raise VenCException(("exception_place_holder", str(e)), pattern)
              
    return "<img class=\"__VENC_KROKI__\" src=\"\x1a"+filename+"\">"
