#! /usr/bin/python
# -*- coding: utf-8 -*-

import cgi

class processor():
    def __init__(self, openSymbol, closeSymbol, separator, functions=dict()):
        self.closeSymbol	= closeSymbol
        self.openSymbol		= openSymbol
        self.separator		= separator
        self.functions		= functions

    def parse(self, string,escape=False):
        closeSymbolPos	= list()
        openSymbolPos	= list()
        output		= str()
        fields		= list()
        i		= int()
        while i < len(string):
            if i + len(self.openSymbol) <= len(string) and string[i:i+len(self.openSymbol)] == self.openSymbol:
                openSymbolPos.append(i)

            elif i + len(self.closeSymbol) <= len(string) and string[i:i+len(self.closeSymbol)] == self.closeSymbol:
                closeSymbolPos.append(i)

            if len(closeSymbolPos) == len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                if openSymbolPos[-1] < closeSymbolPos[0]:
                    fields = [field for field in string[openSymbolPos[-1]+2:closeSymbolPos[0]].split(self.separator) if field != '']
                    if fields[0] in self.functions.keys():
                        output = self.functions[fields[0]](fields[1:])

                    if escape:
                        return self.parse(string[:openSymbolPos[-1]]+cgi.escape(output).encode('ascii', 'xmlcharrefreplace').decode(encoding='ascii')+string[closeSymbolPos[0]+2:],escape=True)
                    else:
                        return self.parse(string[:openSymbolPos[-1]]+output+string[closeSymbolPos[0]+2:])

            i+=1
    
        return string
