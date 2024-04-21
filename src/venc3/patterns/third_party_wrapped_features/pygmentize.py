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

class CodeHighlight:
    def __init__(self):
        from venc3.datastore import datastore
        self._override = datastore.blog_configuration["code_highlight_css_override"]
        try:
            self._style = datastore.blog_configuration["pygmentize_style"]
            
        except KeyError:
            self._style = "default"
          
        self.includes = dict()

    def export_style_sheets(self):
        extra = os.listdir(os.getcwd()+"/extra/")
        for key in self.includes:
            if key not in extra or self._override:    
                stream = open(os.getcwd()+"/extra/"+key,'w')
                stream.write(self.includes[key])

def get_style_sheets(pattern):
    output = str()
    for filename in code_highlight.includes.keys():
        output += "<link rel=\"stylesheet\" href=\"\x1a/"+filename+"\" type=\"text/css\" >\n"

    return output
        
def highlight_include(pattern, langage, display_line_numbers, filename):
    from venc3.patterns.non_contextual import include_file
    string = include_file(pattern, filename, [])
    return highlight(pattern, langage, display_line_numbers, string)
    
def highlight(pattern, langage, display_line_numbers, input_code):
    try:
        import pygments.lexers
        import pygments.formatters
    
    except:
        from venc3.exceptions import VenCException
        raise VenCException(("module_not_found", "pygments"), pattern)

    try:
        name = "venc_source_"+langage.replace('+','Plus')

        lexer = pygments.lexers.get_lexer_by_name(langage, stripall=False)
        formatter = pygments.formatters.HtmlFormatter(style=code_highlight._style, linenos=(True if display_line_numbers=="True" else False), cssclass=name)
        
        result = "<div class=\"__VENC_PYGMENTIZE_WRAPPER__\">"+pygments.highlight(input_code.replace("\:",":"), lexer, formatter).replace(".:","&period;:").replace(":.",":&period;")+"</div>"
        if pattern.root == pattern.parent and pattern.root.has_markup_language:
            result = "</p>"+result+"<p>"
        css  = formatter.get_style_defs()

        if not name+".css" in code_highlight.includes.keys():
            code_highlight.includes[name+".css"] = css

        return result

    except pygments.util.ClassNotFound:
        from venc3.exceptions import VenCException
        raise VenCException(("unknown_language", langage), pattern)

code_highlight = None

def init_code_highlight():
    global code_highlight
    code_highlight = CodeHighlight()
