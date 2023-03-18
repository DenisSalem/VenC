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

import os

def kroki(node, code, endpoint, provider = "https://kroki.io/"):   
    code=base64.urlsafe_b64encode(zlib.compress(code.encode("utf-8"), 9)).decode("utf-8")
    
    if not os.path.isfile("extra/"+code+".svg"):
        try:
            import requests
            
        except:
            from venc3.exceptions import VenCException
            raise VenCException(("module_not_found", "requests"), node)
        import zlib;
        import base64
        with open("extra/"+code+".svg","w") as f:
            try:
                f.write(requests.get(provider+'/'+endpoint+'/svg/'+code).text)
                
            except Exception as e:
                from venc3.exceptions import VenCException
                raise VencException(("exception_place_holder", str(e)), node)
              
    return "<img class=\"__VENC_KROKI__\" src=\".:GetRelativeOrigin:."+code+".svg"+"\" />"