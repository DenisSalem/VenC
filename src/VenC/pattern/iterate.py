#! /usr/bin/python3

#   Copyright 2016, 2017 Denis Salem
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

def For(self, argv):
    outputString = str()
    try:
        for Item in self.dictionnary[argv[0]]:
            outputString += argv[1].format(Item) + argv[2]

        return outputString[:-len(argv[2])]

    except KeyError as e:
        return self.handleError(
            Messages.forUnknownValue.format(e),
            "~§For§§"+"§§".join(argv)+"§~",
            True
        )
        
    except IndexError as e:
        return self.handleError(
            "For: "+Messages.notEnoughArgs,
            "~§For§§"+"§§".join(argv)+"§~",
            True
        )

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
                    outputString += content.format(variables) + self._RecursiveFor(
                        openString,
                        content,
                        separator,
                        closeString,
                        nodes[Key]["_nodes"]
                    )

    except KeyError as e:
        return self.handleError(
            Messages.forUnknownValue.format(e),
            "<!-- Recursive For KeyError exception, shouldn't happen -->",
            True
        )

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
        return self.handleError(
            "RecursiveFor: "+Messages.notEnoughArgs,
            "~§RecursiveFor§§"+"§§".join(argv)+"§~",
            True
        )

    except KeyError as e:
        return self.handleError(
            VenC.l10n.Messages.recursiveForUnknownValue.format(e),
            "~§RecursiveFor§§"+"§§".join(argv)+"§~",
            True
        )
