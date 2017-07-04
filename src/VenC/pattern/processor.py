#! /usr/bin/python3

import cgi
import VenC.l10n
import VenC.helpers

from VenC.helpers import GetFormattedMessage
from VenC.helpers import HighlightValue
from VenC.l10n import Messages
from VenC.pattern.for import For
from VenC.pattern.for import RecursiveFor

class Processor():
    def __init__(self, openSymbol, closeSymbol, separator):
        self.closeSymbol	= closeSymbol
        self.openSymbol		= openSymbol
        self.separator		= separator
        self.dictionnary        = dict()
        self.functions		= dict()
        self.functions["Get"] = self.Get
        self.functions["For"] = For
        self.functions["RecursiveFor"] = RecursiveFor
        self.strict             = True
        self.currentStrings     = dict()
        self.currentString      = str()
        self.ressource          = str()
        self.preProcessedStrings = dict()
        self.patternsIndex      = dict()
        self.errors             = list()

    def handleError(self, error, default,enable=False,value=""):
        if self.strict or enable:
            err = GetFormattedMessage(error, "RED")+"\n"
            
            if self.ressource != str():
            	err += GetFormattedMessage(Messages.inRessource.format(self.ressource)+"\n", "RED")
                
            if not err in VenC.helpers.errors:
                VenC.helpers.errors.append(err)
                err += HighlightValue(self.currentString, value)
                print(err)
        
        return default

    def SetFunction(self, key, function):
        self.functions[key] = function

    def DelFunction(self, key):
        try:
            del self.functions[key]

        except:
            pass

    def DelValue(self, key):
        try:
            del self.dictionnary[key]
        except:
            pass

    def SetWholeDictionnary(self, dictionnary):
        for key in dictionnary:
            self.dictionnary[key] = dictionnary[key]

    def Set(self, symbol, value):
       self.dictionnary[symbol] = value

    def Get(self, symbol):
        try:
            return self.dictionnary[symbol[0]]

        except KeyError as e:
            return self.handleError(
                Messages.getUnknownValue.format(e),
                "~§"+"Get§§"+"$$".join(symbol)+"§~",
                value=str(e)[1:-1]
            )

        except IndexError as e:
            return self.handleError(
                "Get: "+Messages.notEnoughArgs.format(e),
                "~§"+"Get§§"+"$$".join(symbol)+"§~",
                True
            )

    def preProcess(self, inputIndex, string):
        self.currentStrings[inputIndex] = str(string)
        self.preProcessedStrings[inputIndex] = list()
        self.patternsIndex[inputIndex] = list()
        closeSymbolPos	= list()
        openSymbolPos	= list()
        i		= int()
        
        while i < len(string):
            if i + len(self.openSymbol) <= len(string) and string[i:i+len(self.openSymbol)] == self.openSymbol:
                openSymbolPos.append(i)

            elif i + len(self.closeSymbol) <= len(string) and string[i:i+len(self.closeSymbol)] == self.closeSymbol:
                closeSymbolPos.append(i)

            if len(closeSymbolPos) == len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                self.preProcessedStrings[inputIndex].append(string[i-closeSymbolPos[-1]:openSymbolPos[0]])
                self.preProcessedStrings[inputIndex].append(string[openSymbolPos[0]:closeSymbolPos[-1]+len(self.closeSymbol)])
                self.patternsIndex[inputIndex].append(len(self.preProcessedStrings[inputIndex])-1)
                
                string = string[closeSymbolPos[-1]+len(self.closeSymbol):]
                openSymbolPos = list()
                closeSymbolPos = list()
                i=0
            else:
                i+=1

        self.preProcessedStrings[inputIndex].append(string)

    def parse(self, inputIndex, escape=False):
        if len(self.patternsIndex) == 0:
            return self.currentStrings[inputIndex]
        
        output = str()

        self.currentString = self.currentStrings[inputIndex]
        for index in range(0,len(self.preProcessedStrings[inputIndex])):
            if index in self.patternsIndex[inputIndex]:
                output += self._process(self.preProcessedStrings[inputIndex][index], escape)
            else:
                output += self.preProcessedStrings[inputIndex][index]

        return output

    def _process(self, string, escape):
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

            if len(closeSymbolPos) <= len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                if openSymbolPos[-1] < closeSymbolPos[0]:
                    fields = [field for field in string[openSymbolPos[-1]+len(self.openSymbol):closeSymbolPos[0]].split(self.separator) if field != '']
                    if fields[0] in self.functions.keys():
                        output = self.functions[fields[0]](fields[1:])
                    else:
                        output =  self.handleError(
                            Messages.unknownPattern.format(fields[0]),
                            "~§"+"§§".join(fields)+"§~"
                        )
                    
                    if escape:
                        return self._process(
                            string[
                                :openSymbolPos[-1]]+
                                cgi.escape(output).encode(
                                    'ascii', 
                                    'xmlcharrefreplace'
                                ).decode(
                                    encoding='ascii'
                                )+
                                string[closeSymbolPos[0]+
                                len(self.closeSymbol):
                            ],
                            escape=True)
                    else:
                        return self._process(
                            string[
                                :openSymbolPos[-1]]+
                                str(output)+
                                string[closeSymbolPos[0]+2:
                            ],
                            escape=False
                        )

            i+=1
    
        return string
