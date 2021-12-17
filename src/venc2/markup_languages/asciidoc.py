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

import importlib
import io

from venc2.markup_languages import handle_markup_language_error

def VenCAsciiDoc(source, attributes):
    try:
        ms = importlib.util.find_spec('asciidoc3.asciidoc3api')
        import asciidoc3.asciidoc3api as AsciiDoc3API
        from asciidoc3.asciidoc3api import AsciiDoc3Error
        ad = AsciiDoc3API.AsciiDoc3API(ms.origin)
    
    except ModuleNotFoundError:
        from venc2.prompt import die
        die(messages.module_not_found.format('asciidoc3'))
    
    infile = io.StringIO(source.string)
    outfile = io.StringIO()
    
    ad.options('--no-header-footer')
    
    for key in attributes.keys():
        ad.attributes[key] = attributes.keys()
        
    try:    
        ad.execute(infile, outfile, backend='html4')
        return outfile.getvalue()
    
    except Exception as e:
            handle_markup_language_error(source.ressource+": "+str(e))
