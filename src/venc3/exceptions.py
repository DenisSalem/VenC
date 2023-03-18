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

class VenCException(Exception):
    def __init__(self, message_format, context=None, extra=""):
        from venc3.l10n import messages
        if len(message_format) > 1:
            message_attr, *format_args = message_format
            self.message = getattr(messages, message_attr).format(*format_args)
        else:
            self.message = getattr(messages, message_format[0])
            
        self.context = context
        self.extra = extra
    
    def __str__(self):
        return self.message
        
    def __repr__(self):
        return (type(self).__name__, message, value, context)

    def die(self):
        from venc3.prompt import die, notify
        try:
            import traceback
            notify("\n"+''.join(traceback.format_stack()[:-1]), "YELLOW")
        except:
            pass
            
        if self.context != None:
            from venc3.patterns.processor import Pattern
            from venc3.l10n import messages

            if type(self.context) == Pattern:
                context_name = self.context.root.context
                self.extra = self.context.root.string
                self.flatten(highlight=self.context)
                
            elif type(self.context) == str:
                context_name = self.context
                
            else:
                context_name = self.context.context
                self.flatten(highlight=self.context)
                
            notify(messages.in_.format(context_name), color="RED")
        
        die(self.message, extra=self.extra)
        
    def flatten(self, highlight=None):
        # use garbage collector to rebuild original string
        import gc
        from venc3.patterns.processor import Pattern
        patterns = [ o for o in gc.get_objects() if type(o) == Pattern]
        while len(patterns):
            len_before = len(patterns)
            patterns = [pattern for pattern in patterns if not self.__apply_flatten(pattern)]
            if len(patterns) == len_before:
                break
                
            len_before = len(patterns)
            
        if type(highlight) == Pattern:
            faulty_pattern =  ".:"+("::".join(highlight.payload))+":."
            self.extra = self.extra.replace(faulty_pattern, '\033[91m' + faulty_pattern + '\033[0m')
            
    def __apply_flatten(self, pattern):
        if self.extra.find(pattern.ID) > 0:
            self.extra = self.extra.replace(pattern.ID, ".:"+("::".join(pattern.payload))+":.")
            return True
            
        return False
        
class MalformedPatterns(VenCException):
    def __init__(self, string_under_processing, op, cp):
        len_op = len(op)
        len_cp = len(cp)
        too_many_opening_symbols = len_op > len_cp
        
        from venc3.l10n import messages

        if too_many_opening_symbols:
            m = messages.malformed_patterns_missing_closing_symbols.format(string_under_processing.context, len_op - len_cp)
        else:
            m = messages.malformed_patterns_missing_opening_symbols.format(string_under_processing.context, len_cp - len_op)
            
        leftovers = op if too_many_opening_symbols else cp
        s = string_under_processing.string
        for leftover in leftovers:
            s = s[:leftover.index]+"\x00\x00"+s[leftover.index+2:]
        
        s = s.replace("\x00\x00", '\033[91m'+( ".:" if too_many_opening_symbols else ":.") +'\033[0m')
        
        super().__init__(m, string_under_processing)
        self.too_many_opening_symbols = too_many_opening_symbols
        self.extra = s

class VenCSyntaxError(VenCException):  
    def __init__(self, string_under_processing, o, c):
        from venc3.l10n import messages
        super().__init__(("syntax_error"), string_under_processing)
        self.extra = string_under_processing.string
        self.extra = self.extra[:o]+'\033[91m'+self.extra[o:c]+'\033[0m'+self.extra[c:]
                    
class UnknownPattern(VenCException):
    def __init__(self, pattern, string_under_processing):
        from venc3.l10n import messages
        super().__init__(("unknown_pattern", pattern.payload[0]), pattern)
        self.extra = string_under_processing.string

class WrongPatternArgumentsNumber(VenCException):
      def __init__(self, pattern, string_under_processing, function, args):
        from inspect import signature
        from venc3.l10n import messages
        sig = signature(function)
        super().__init__(
            ("wrong_args_number", len(sig.parameters)-1, len(args)),
            pattern
        )
        self.extra = string_under_processing.string
