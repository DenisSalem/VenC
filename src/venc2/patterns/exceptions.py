#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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

from venc2.l10n import messages

# Special case of KeyError
class UnknownContextual(KeyError):
    pass

class IllegalUseOfEscape(Exception):
    def __init__(self, ressource):
        self.ressource = ressource
        pass
               
class MalformedPatterns(Exception):
    def __init__(self, too_many_opening_symbols, escape, ressource):
        self.too_many_opening_symbols = too_many_opening_symbols
        self.escape = escape
        self.ressource = ressource

class PatternInvalidArgument(Exception):
    def __init__(self, name, value, message=''):
        self.name = name
        self.value = value
        self.message = message

class PatternMissingArguments(Exception):
    def __init__(self, e=messages.not_enough_args, expected=1, got=0):
        if type(e) != str:
            v = e.args[0].replace(',',' ').replace(')',' ').split()
            self.expected, self.got = tuple([int(s) for s in v if s.isdigit()])
            self.info = messages.not_enough_args.format(self.expected, self.got)

        else:
            self.expected = expected
            self.got = got
            self.info = e.format(expected,got)
