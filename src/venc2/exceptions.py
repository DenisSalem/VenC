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

from venc2.l10n import messages

class VenCException(Exception):
    def __init__(self, message, context=None):
        self.message = message
        self.extra = ""
        self.context = context
    
    def __str__(self):
        return self.message
        
    def __repr__(self):
        return (type(self).__name__, message, value, context)

    def die(self):
        from venc2.prompt import die, notify
        if self.context != None:
            # TODO rename context to context_name
            notify(messages.in_.format(self.context.context), color="RED")
        die(self.message, extra=self.extra)
        
class MalformedPatterns(VenCException):
    def __init__(self, string_under_processing):
        len_op = len(string_under_processing.op)
        len_cp = len(string_under_processing.cp)
        too_many_opening_symbols = len_op > len_cp
        if too_many_opening_symbols:
            m = messages.malformed_patterns_missing_closing_symbols.format(string_under_processing.context, len_op - len_cp)
        else:
            m = messages.malformed_patterns_missing_opening_symbols.format(string_under_processing.context, len_cp - len_op)
            
        leftovers = string_under_processing.op if too_many_opening_symbols else string_under_processing.cp
        s = str(string_under_processing)
        for leftover in leftovers:
            s = s[:leftover]+"\x00\x00"+s[leftover+2:]
        
        s = s.replace("\x00\x00", '\033[91m'+( ".:" if too_many_opening_symbols else ":.") +'\033[0m')
        
        super().__init__(m, string_under_processing.context)
        self.too_many_opening_symbols = too_many_opening_symbols
        self.extra = s

class UnknownPattern(VenCException):
    def __init__(self, pattern, string_under_processing):
        super().__init__(messages.unknown_pattern.format(pattern.name), string_under_processing)

