#! /usr/bin/env python3

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

from venc2.prompt import die
from venc2.prompt import notify
from venc2.l10n import messages

""" Need to handle missing args in case of unknown number of args """
class CodeHighlight:
    def __init__(self, override):
        self._override = override
        self._includes = dict()

    def get_style_sheets(self, argv=list()):
        output = str()
        for filename in self._includes.keys():
            output += "<link rel=\"stylesheet\" href=\".:GetRelativeOrigin:."+filename+"\" type=\"text/css\" />\n"

        return output

    def export_style_sheets(self):
        extra = os.listdir(os.getcwd()+"/extra/")
        for key in self._includes:
            if key not in extra or self._override:    
                stream = open(os.getcwd()+"/extra/"+key,'w')
                stream.write(self._includes[key])

    def highlight(self, argv):
        try:
            name = "venc_source_"+argv[0].replace('+','Plus')

            lexer = pygments.lexers.get_lexer_by_name(argv[0], stripall=True)

            formatter = pygments.formatters.HtmlFormatter(linenos=("table" if argv[1]=="True" else False), cssclass=name)
            code = argv[2]
            result = pygments.highlight(code.replace("\:",":"), lexer, formatter).replace(".:","&period;:")
            css  = formatter.get_style_defs()
            css += "\n."+name+"table {width: 100%; display: block;}"
            css += "\n."+name+"table tr {width: 100%; display: block;}"
            css += "\n."+name+"table tbody {width: 100%; display: block;}"
            css += "\n."+name+"table .linenos {width: 4%; display: inline-block;vertical-align: top;}"
            css += "\n."+name+"table .code {width: 95%; display: inline-block;vertical-align: top;}"
            css += "\n."+name+"table td pre {vertical-align: top; overflow: hidden; overflow-x: scroll;}"
            css += "\n."+name+" pre {overflow: hidden; overflow-x: scroll;}"

            if not name+".css" in self._includes.keys():
                self._includes[name+".css"] = css

            return result
    
        except pygments.util.ClassNotFound:
            die(messages.unknown_language.format(argv[0]))

        except Exception as e:
            print(e)
