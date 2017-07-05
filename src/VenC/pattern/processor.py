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

import cgi
import VenC.l10n
import VenC.helpers

from VenC.helpers import GetFormattedMessage
from VenC.helpers import HighlightValue
from VenC.l10n import Messages
from VenC.pattern.iterate import For
from VenC.pattern.iterate import RecursiveFor

OPEN_SYMBOL = ".:"
SEPARATOR = "::"
CLOSE_SYMBOL = ":."

# Some patterns are contextual while others are constant in time.
# To save time we wan't to perform two-pass analysis. In the first one
# we're ignoring some given patterns which usualy are contextual. Once
# non-contextual pattern are parsed the second pass occurs each time we
# require the given string in every needed context
BlackList = list()

# Because parsing is recursive we want to avoid useless computation
# by splitting a given string and mark where exactly are the patterns 
# we want to process.

class PreProcessor():
    def __init__(self, string):
        self.blacklist = list()
        self.SubStrings = list()
        self.patternsIndex = list()
        closeSymbolPos	= list()
        openSymbolPos	= list()
        i		= int()
        
        while i < len(string):
            if string[i:i+2] == OPEN_SYMBOL:
                openSymbolPos.append(i)

            elif string[i:i+2] == CLOSE_SYMBOL:
                closeSymbolPos.append(i)

            # At some point, when we get the same opening and closing symbols, it means that we just reach the end of a pattern
            # so we can do the real job.
            if len(closeSymbolPos) == len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                # Append non pattern substring
                self.SubStrings.append(string[i-closeSymbolPos[-1]:openSymbolPos[0]])

                # Append pattern substring
                self.SubStrings.append(string[openSymbolPos[0]:closeSymbolPos[-1]+2])

                # Push pattern substring index in queue
                self.patternsIndex.append(len(self.SubStrings)-1)
                string = string[closeSymbolPos[-1]+2:]
                openSymbolPos = list()
                closeSymbolPos = list()
                i=0
            
            else:
                i+=1

        # append last substring
        self.SubStrings.append(string)

def MergeBatches(batches):
    merged = batches[0]
    for batch in batches[1:]:
        pass

def GetFinalString(processed):
    output = str()
    for chunk in processed.SubStrings:
        output += chunk

    return output

class Processor():
    def __init__(self):
        self.dictionary         = dict()
        self.functions		 = dict()
        self.functions["Get"]    = self.Get
        self.currentString       = str()
        self.ressource           = str()
        self.errors              = list()

    # Print out notification to user and replace erroneous
    def handleError(self, error, defaultOutput, errorOrigin = ""):
        err = GetFormattedMessage(error, "RED")+"\n"
            
        if self.ressource != str():
            err += GetFormattedMessage(Messages.inRessource.format(self.ressource)+"\n", "RED")
                
        if not err in VenC.helpers.errors:
            VenC.helpers.errors.append(err)
            if errorOrigin != "":
                err += HighlightValue(''.join(self.currentString), errorOrigin)
            
            print(err)
        
        return defaultOutput

    def SetFunction(self, key, function):
        self.functions[key] = function

    def DelFunction(self, key):
        try:
            del self.functions[key]

        except:
            pass

    def DelValue(self, key):
        try:
            del self.dictionary[key]

        except:
            pass

    def SetDictionary(self, dictionary):
        for key in dictionary:
            self.dictionary[key] = dictionary[key]

    def Set(self, symbol, value):
       self.dictionary[symbol] = value

    def Get(self, symbol):
        try:
            return self.dictionary[symbol[0]]

        except KeyError as e:
            return self.handleError(
                Messages.getUnknownValue.format(e),
                "~§"+"Get§§"+"$$".join(symbol)+"§~",
                errorOrigin=str(e)[1:-1]
            )

        except IndexError as e:
            return self.handleError(
                "Get: "+Messages.notEnoughArgs.format(e),
                "~§"+"Get§§"+"$$".join(symbol)+"§~",
            )

    # Process queue
    def BatchProcess(self, preProcessed, escape=False):
        global BlackList

        if len(preProcessed.patternsIndex) == 0:
            return preProcessed
        
        self.currentString = preProcessed.SubStrings
        toRemove = list()
        for index in preProcessed.patternsIndex:
            if not preProcessed.SubStrings[index][2:-2].split('::')[0] in BlackList:
                preProcessed.SubStrings[index] = self.Process(preProcessed.SubStrings[index], escape)
                toRemove.append(index)

        for index in toRemove:
            preProcessed.patternsIndex = RemoveByValue(preProcessed.patternsIndex, index)

        return preProcessed

    def Process(self, string, escape):
        closeSymbolPos	= list()
        openSymbolPos	= list()
        output		= str()
        fields		= list()
        i		= int()

        while i < len(string):
            if string[i:i+2] == OPEN_SYMBOL:
                openSymbolPos.append(i)

            elif string[i:i+2] == CLOSE_SYMBOL:
                closeSymbolPos.append(i)

            if len(closeSymbolPos) <= len(openSymbolPos) and len(closeSymbolPos) != 0 and len(openSymbolPos) != 0:
                if openSymbolPos[-1] < closeSymbolPos[0]:
                    fields = [field for field in string[openSymbolPos[-1]+2:closeSymbolPos[0]].split(SEPARATOR) if field != '']
                    if fields[0] in self.functions.keys():
                        output = str(self.functions[fields[0]](fields[1:]))

                    else:
                        output =  self.handleError(
                            Messages.unknownPattern.format(fields[0]),
                            "~§"+"§§".join(fields)+"§~",
                            errorOrigin = fields[0]
                        )
                    
                    if escape:
                        return self.Process(
                            string[:openSymbolPos[-1]]+
                            
                            cgi.escape(output).encode(
                                'ascii', 
                                'xmlcharrefreplace'
                            ).decode(
                                encoding='ascii'
                            )+
                            
                            string[closeSymbolPos[0]+2:],
                            escape=True
                        )
                    else:
                        return self.Process(
                            string[
                                :openSymbolPos[-1]]+
                                str(output)+
                                string[closeSymbolPos[0]+2:
                            ],
                            escape=False
                        )

            i+=1
    
        return string
