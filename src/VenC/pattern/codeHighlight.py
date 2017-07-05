#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
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
import pygments.lexers
import pygments.formatters

from VenC.helpers import Notify

class CodeHighlight:
    def __init__(self):
        self.includes = dict()

    def GetStyleSheets(self, argv=list()):
        output = str()
        for filename in self.includes.keys():
            output += "<link rel=\"stylesheet\" href=\".:GetRelativeOrigin:."+filename+" type=\"text/css\" />\n"

        return output

    def ExportStyleSheets(self):
        for key in self.includes:
            stream = open(os.getcwd()+"/extra/"+key,'w')
            stream.write(self.includes[key])

    def Highlight(self, argv):
        try:
            name = "venc_source_"+argv[0].replace('+','Plus')

            lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)

            formatter = pygments.formatters.HtmlFormatter(linenos=("inline" if argv[1]=="True" else False),cssclass=name)
            code = base64.b64decode(bytes(argv[2],encoding='utf-8'))
            result = pygments.highlight(code.decode("utf-8").replace("\:",":"), lexer, formatter)
            css  = formatter.get_style_defs(name)

            if not name+".css" in self.includes.keys():
                self.includes[name+".css"] = css

            return result
    
        except Exception as e:
            raise
            Notify(str(e), "YELLOW")
            return str()
