#! /usr/bin/python3

import cgi
import VenC.core

class processor():
    def __init__(self, openSymbol, closeSymbol, separator):
        self.closeSymbol	= closeSymbol
        self.openSymbol		= openSymbol
        self.separator		= separator
        self.dictionnary        = dict()
        self.functions		= dict()
        self.functions["Get"] = self.Get
        self.functions["For"] = self.For
        self.functions["RecursiveFor"] = self.RecursiveFor
        self.strict             = True
        self.currentString      = str()
        self.ressource          = str()
        self.errors             = list()

    def handleError(self,error, default,enable=False):
        if self.strict or enable:
            err = VenC.core.OutputColors.FAIL+"VenC: "+error+"\n"
            
            if self.ressource != str():
            	err +="VenC: "+VenC.core.Messages.inRessource.format(self.ressource)+"\n"
                
            if not err in VenC.core.errors:
                VenC.core.errors.append(err)
                err += self.currentString+VenC.core.OutputColors.END+"\n\n"
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
            return self.handleError(VenC.core.Messages.getUnknownValue.format(e), "~§"+"Get§§"+"$$".join(symbol)+"§~",True)

        except IndexError as e:
            return self.handleError(VenC.core.Messages.getNotEnoughArgs.format(e), "~§"+"Get§§"+"$$".join(symbol)+"§~",True)

    def For(self, argv):
        outputString = str()
        try:
            for Item in self.dictionnary[argv[0]]:
                outputString += argv[1].format(Item) + argv[2]

            return outputString[:-len(argv[2])]
        except KeyError as e:
            return self.handleError(VenC.core.Messages.forUnknownValue.format(e),"~§For§§"+"§§".join(argv)+"§~",True)
        
        except IndexError as e:
            return self.handleError(VenC.core.Messages.forNotEnoughArgs,"~§For§§"+"§§".join(argv)+"§~",True)

    def _RecursiveFor(self, openString, content, separator,closeString, nodes):
        outputString = openString
        try:
            for Key in sorted(nodes.keys()):
                variables = dict()
                for key in nodes[Key]:
                    if key[:2] == '__':
                        variables[key[2:]] = nodes[Key][key]
                variables["item"] = Key
                if Key != "_nodes":
                    if not "_nodes" in nodes[Key].keys():
                        outputString += content.format(variables) + separator
                    else:
                        outputString += content.format(variables) + self._RecursiveFor(openString, content, separator, closeString, nodes[Key]["_nodes"])
        except KeyError as e:
            return self.handleError(VenC.core.Messages.forUnknownValue.format(e),"<!-- Recursive For KeyError exception, shouldn't happen -->",True)

        return outputString + closeString

    def RecursiveFor(self, argv):
        outputString = str()
        try:
            outputString += self._RecursiveFor(
                argv[1],
                argv[2],
                argv[3],
                argv[4],
                self.dictionnary[argv[0]]
            )
            return outputString
        except IndexError as e:
            return self.handleError(VenC.core.Messages.recursiveForNotEnoughArgs,"~§RecursiveFor§§"+"§§".join(argv)+"§~",True)
        except KeyError as e:
            return self.handleError(VenC.core.Messages.recursiveForUnknownValue.format(e),"~§RecursiveFor§§"+"§§".join(argv)+"§~",True)

    def parse(self, string,escape=False):
        self.currentString = string
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
                    fields = [field for field in string[openSymbolPos[-1]+2:closeSymbolPos[0]].split(self.separator) if field != '']
                    if fields[0] in self.functions.keys():
                        output = self.functions[fields[0]](fields[1:])
                    else:
                        output =  self.handleError(VenC.core.Messages.unknownPattern.format(fields[0]),"~§"+"§§".join(fields)+"§~")
                    
                    if escape:
                        return self.parse(string[:openSymbolPos[-1]]+cgi.escape(output).encode('ascii', 'xmlcharrefreplace').decode(encoding='ascii')+string[closeSymbolPos[0]+2:],escape=True)
                    else:
                        return self.parse(string[:openSymbolPos[-1]]+str(output)+string[closeSymbolPos[0]+2:])

            i+=1
    
        return string
