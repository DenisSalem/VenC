#! /usr/bin/python3

#    Copyright 2016, 2018 Denis Salem
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

from venc2.helpers import die
from venc2.helpers import notify
from venc2.l10n import messages

class CodeHighlight:
    def __init__(self):
        self.includes = dict()

    def get_style_sheets(self, argv=list()):
        output = str()
        for filename in self.includes.keys():
            output += "<link rel=\"stylesheet\" href=\".:GetRelativeOrigin:."+filename+" type=\"text/css\" />\n"

        return output

    def export_style_sheets(self):
        extra = os.listdir(os.getcwd()+"/extra/")
        for key in self.includes:
            if key not in extra:    
                stream = open(os.getcwd()+"/extra/"+key,'w')
                stream.write(self.includes[key])

    def highlight(self, argv):
        try:
            name = "venc_source_"+argv[0].replace('+','Plus')

            lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)

            formatter = pygments.formatters.HtmlFormatter(linenos=("inline" if argv[1]=="True" else False),cssclass=name)
            code = argv[2]
            result = pygments.highlight(code.replace("\:",":"), lexer, formatter)
            css  = formatter.get_style_defs(name)

            if not name+".css" in self.includes.keys():
                self.includes[name+".css"] = css

            return result
    
        except pygments.util.ClassNotFound:
            die(messages.unknown_language.format(argv[0]))
