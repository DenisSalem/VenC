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
        try:
            import traceback
            self._traceback = "\n"+''.join(traceback.format_stack())

        except:
            self._traceback = None
            
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
        if self._traceback != None:
            notify(("exception_place_holder", self._traceback), "YELLOW")

        if self.context != None:
            from venc3.patterns.processor import Pattern

            if type(self.context) == Pattern:
                context_name = self.context.root.context
                self.extra = self.context.root.string
                self.flatten(highlight=self.context)
                
            elif type(self.context) == str:
                context_name = self.context
                
            else:
                context_name = self.context.context
                self.flatten(highlight=self.context)
                
            notify(("in_", context_name), color="RED")
        
        die(("exception_place_holder", self.message), extra=self.extra)
        
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
            from venc3.patterns.non_contextual import escape
            faulty_pattern =  ".:"+highlight.payload[0]+("::" if len(highlight.payload[1:]) else "")+escape(highlight)+":."
                
            self.extra = self.extra.replace(faulty_pattern, '\033[91m' + faulty_pattern + '\033[0m')
            
    def __apply_flatten(self, pattern):
        if self.extra.find(pattern.ID) > 0:
            self.extra = self.extra.replace(pattern.ID, ".:"+("::".join(pattern.payload))+":.")
            return True
            
        return False

class PatternsCannotBeUsedHere(VenCException):
    def __init__(self, patterns):
        from venc3.l10n import messages
        message = messages.in_.format(patterns[0].root.context) + "\n"
        for pattern in patterns:
            message = message + messages.you_cannot_use_this_pattern_here.format(pattern.payload[0], pattern.root.context) + "\n"
            
        super().__init__(("exception_place_holder", message))
        self.extra = patterns[0].root.string
        self.flatten()
        for pattern in patterns:
            faulty_pattern =  ".:"+("::".join(pattern.payload))+":."
            self.extra = self.extra.replace(faulty_pattern, '\033[91m' + faulty_pattern + '\033[0m')
            
class MalformedPatterns(VenCException):
    def __init__(self, string_under_processing, op, cp):
        len_op = len(op)
        len_cp = len(cp)
        too_many_opening_symbols = len_op > len_cp
        
        from venc3.l10n import messages

        if too_many_opening_symbols:
            m = ("malformed_patterns_missing_closing_symbols", string_under_processing.context, len_op - len_cp)
        else:
            m = ("malformed_patterns_missing_opening_symbols", string_under_processing.context, len_cp - len_op)
            
        leftovers = op if too_many_opening_symbols else cp
        s = string_under_processing.string
        for leftover in leftovers:
            s = s[:leftover.index]+"\x00\x00"+s[leftover.index+2:]
        
        s = s.replace("\x00\x00", '\033[91m'+( ".:" if too_many_opening_symbols else ":.") +'\033[0m')
        
        super().__init__(m, string_under_processing)
        self.too_many_opening_symbols = too_many_opening_symbols
        self.extra = s

class MissingTemplateArguments(VenCException):
    def __init__(self, template_name, key_error):
      self.key_error = key_error
      super().__init__(("this_template_need_the_following_argument", template_name, str(key_error)))
      
class VenCSyntaxError(VenCException):  
    def __init__(self, string_under_processing, o, c):
        super().__init__(("syntax_error"), string_under_processing)
        self.extra = string_under_processing.string
        self.extra = self.extra[:o]+'\033[91m'+self.extra[o:c]+'\033[0m'+self.extra[c:]
                    
class UnknownPattern(VenCException):
    def __init__(self, pattern, string_under_processing):
        super().__init__(("unknown_pattern", pattern.payload[0]), pattern)
        self.extra = string_under_processing.string

class WrongPatternArgumentsNumber(VenCException):
      def __init__(self, pattern, string_under_processing, function, args):
        from inspect import signature
        sig = signature(function)
        mandatory_count = 0
        for p in sig.parameters.keys():
            if str(p) != 'pattern' and not '=' in str(sig.parameters[p]):
                mandatory_count += 1
                
        super().__init__(
            ("wrong_args_number", mandatory_count, len(args)),
            pattern,
        )
        
        self.extra = string_under_processing.string
