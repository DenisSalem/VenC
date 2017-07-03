#! /usr/bin/python3

import os
import pygments.lexers
import pygments.formatters

from VenC.helpers import Notify

class CodeHighlight:
    def __init__(self):
        self.includes = dict()

    def GetStyleSheets(self, argv=list()):
        output = str()
        for style in self.includes:
            output += "<link rel=\"stylesheet\" href=\"../venc_source_C.css\" type=\"text/css\" />\n" 
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
