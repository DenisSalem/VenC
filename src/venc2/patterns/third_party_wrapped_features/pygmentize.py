#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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
from venc2.patterns.non_contextual import include_file

class CodeHighlight:
    def __init__(self, override):
        self._override = override
        self.includes = dict()

    def export_style_sheets(self):
        extra = os.listdir(os.getcwd()+"/extra/")
        for key in self.includes:
            if key not in extra or self._override:    
                stream = open(os.getcwd()+"/extra/"+key,'w')
                stream.write(self.includes[key])

def get_style_sheets():
    output = str()
    for filename in code_highlight.includes.keys():
        output += "<link rel=\"stylesheet\" href=\"\x1a"+filename+"\" type=\"text/css\" />\n"

    return output
        
def highlight_include(node, langage, display_line_numbers, filename):
    string = include_file(filename)
    return code_highlight.highlight(langage, display_line_numbers, filename, string, included_file=True)
    
def highlight(node, *pattern_args, included_file=False):
    langage, display_line_numbers = pattern_args[2:]
    input_code =  "::".join(pattern_args[:2]) if not included_file else pattern_args[:2]

    try:
        import pygments.lexers
        import pygments.formatters
    
    except:
        from venc2.exceptions import VenCException
        from venc2.l10n import messages
        raise VencException(messages.module_not_found.format('pygments'))

    try:
        name = "venc_source_"+langage.replace('+','Plus')

        lexer = pygments.lexers.get_lexer_by_name(langage, stripall=False)
        formatter = pygments.formatters.HtmlFormatter(linenos=(True if display_line_numbers=="True" else False), cssclass=name)
                            
        result = "<div class=\"__VENC_PYGMENTIZE_WRAPPER__\">"+pygments.highlight(code.replace("\:",":"), lexer, formatter).replace(".:","&period;:").replace(":.",":&period;")+"</div>"
        css  = formatter.get_style_defs()

        if not name+".css" in code_highlight.includes.keys():
            code_highlight.includes[name+".css"] = css

        return result

    except pygments.util.ClassNotFound:
        from venc2.exceptions import VenCException
        from venc2.l10n import messages
        raise VencException(messages.unknown_language.format(langage))

code_highlight = None

def init_code_highlight(override):
    global code_highlight
    code_highlight = CodeHighlight(override)

