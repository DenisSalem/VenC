#! /usr/bin/env python3

#    Copyright 2016, 2018 Denis Salem
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

import markdown2 as markdown

from copy import deepcopy
from docutils.core import publish_parts
from docutils.utils import SystemMessage

from venc2.prompt import get_formatted_message
from venc2.prompt import highlight_value
from venc2.prompt import notify
from venc2.prompt import die
from venc2.helpers import remove_by_value
from venc2.l10n import messages
from venc2.patterns.exceptions import IllegalUseOfEscape
from venc2.patterns.exceptions import MalformedPatterns
from venc2.patterns.exceptions import UnknownContextual
from venc2.patterns.exceptions import PatternMissingArguments
from venc2.patterns.exceptions import PatternInvalidArgument
from venc2.helpers import GenericMessage

markup_language_errors = []

def get_markers_indexes(string, begin=".:", end=":."):
    op, cp = [], []
    op_append, cp_append = op.append, cp.append
    string_find = string.find
    strip_begin, strip_end = [], []
    strip_begin_append, strip_end_append = strip_begin.append, strip_end.append
    i = 0
    l = len(string)
    offset=0
    begin_eq_escape = begin == ".:Escape::"
    while i < l:
        i = string_find(begin, i)
        if i == -1:
            i=0
            break
            
        if begin_eq_escape:
            j = 0
            while string[i+10+j] in [' ','\t','\n']:
                j+=1
                
            strip_begin_append(j)

        op_append(i)
        i+=2
    
    while i < l:
        i = string_find(end, i)
        if i == -1:
            i=0
            break
            
        if begin_eq_escape:
            j = 0
            while string[i-j-1] in [' ','\t','\n']:
                j+=1
            strip_end_append(j)

        cp_append(i)
            
        i+=2

    if begin_eq_escape:
        a = [ (op[i], strip_begin[i]) for i in range(0,len(op)) ]
        b = [ (cp[i], strip_end[i])   for i in range(0,len(cp)) ]
        return (a, b)
        
    return (op, cp)

def handle_markup_language_error(message, line=None, string=None):
    if not message in markup_language_errors:
        notify(message, "RED")
        markup_language_errors.append(message)
        if line != None and string != None:
            lines = string.split('\n')
            for lineno in range(0,len(lines)):
                if line - 1 == lineno:
                    print('\033[91m'+lines[lineno]+'\033[0m')
                else:
                    print(lines[lineno])

def parse_markup_language(string, markup_language, ressource):
    if markup_language == "Markdown":
        string = markdown.markdown(string)
        
    elif markup_language == "reStructuredText":
        string = publish_parts(string, writer_name='html', settings_overrides={'doctitle_xform':False, 'halt_level': 2, 'traceback': True, "warning_stream":"/dev/null"})['html_body']

    elif markup_language != "none":
            err = messages.unknown_markup_language.format(markup_language, ressource)
            handle_markup_language_error(err)

    return string

def index_not_in_range(index, ranges, process_escapes):
    for o, c in ranges:
        if index >= o[0] and index <= (c[0] if process_escapes else c[0]+13):
            return False

    return True

class ProcessedString():
    def __init__(self, string, ressource, process_escapes=False):
        self.open_pattern_pos, self.close_pattern_pos = get_markers_indexes(string)
        
        #Process escape
        self.escapes_o, self.escapes_c = get_markers_indexes(string, begin=".:Escape::", end="::EndEscape:.")
        leo, lec = len(self.escapes_o), len(self.escapes_c)

        if leo != lec:
            raise MalformedPatterns(leo > lec, True, ressource)
        
        escapes = []
        
        # Get ranges
        while len(self.escapes_o):
            if len(self.escapes_o) > 1:
                for i in range(1, len(self.escapes_o)):
                    if self.escapes_o[i][0] > self.escapes_c[i-1][0]:
                        o = self.escapes_o[0]
                        c = self.escapes_c[i-1]

                        escapes.append((o,c))
                        self.escapes_o = self.escapes_o[i:]
                        self.escapes_c = self.escapes_c[i:]
                        break
                        
                    else:
                        raise IllegalUseOfEscape(ressource)
                    
            else:
                escapes.append((
                    self.escapes_o[0],
                    self.escapes_c[0]
                ))
                break

        if len(escapes) and process_escapes:
            # First removes open and closes indexes which
            # are actually referencing escapes indexes.
            for e in escapes:
                self.open_pattern_pos.remove(e[0][0])
                self.close_pattern_pos.remove(e[1][0]+11)
            
            # Remove Escape and EndEscapes, update indexes
            for i in range(0, len(escapes)):
                o,c = escapes[i]
                #bs and es are for begin strip and end strip
                o, bs = o
                c, es = c
                string = string[:o]+string[o+10+bs:]
                string = string[:c-10-bs-es]+string[c+3-bs:]

                # -1 to set close escape at the end of the escaped string
                escapes[i] = ((o, bs), (c-10-bs-es-1, es)) 
                
                # adjust pattern indexes
                self.open_pattern_pos = [(v-10-bs if v > o and v < c else (v-23-bs-es if v > c+13 else v)) for v in self.open_pattern_pos]
                self.close_pattern_pos = [(v-10-bs if v > o and v < c else (v-23-bs-es if v > c+13 else v)) for v in self.close_pattern_pos]
                
                escapes = escapes[:i+1]+[ ( (p[0][0]-23-bs-es, p[0][1]), (p[1][0]-23-bs-es, p[1][1])) for p in escapes[i+1:] ]
                
        # remove escaped patterns indexes
        if len(escapes):
            self.open_pattern_pos = [v for v in self.open_pattern_pos if index_not_in_range(v, escapes, process_escapes)]
            self.close_pattern_pos = [v for v in self.close_pattern_pos if index_not_in_range(v, escapes, process_escapes)]

        self.len_open_pattern_pos = len(self.open_pattern_pos)
        self.len_close_pattern_pos = len(self.close_pattern_pos)
            
        if self.len_open_pattern_pos != self.len_close_pattern_pos:
            raise MalformedPatterns(self.len_open_pattern_pos > self.len_close_pattern_pos, False, ressource)

        self.string = string
        self.ressource = ressource
        self.process_escapes = process_escapes
        self.keep_appart_from_markup_indexes = list()
        self.keep_appart_from_markup_inc = 0
        self.bop, self.bcp = [], []
        self.backup = None
            
    def restore(self):
        self.open_pattern_pos, self.close_pattern_pos, self.len_open_pattern_pos, self.len_close_pattern_pos, self.string = self.backup
        self.backup = None

    def keep_appart_from_markup_indexes_append(self, paragraphe, new_chunk):
        self.keep_appart_from_markup_indexes.append((self.keep_appart_from_markup_inc, paragraphe, new_chunk))
        output = "---VENC-TEMPORARY-REPLACEMENT-"+str(self.keep_appart_from_markup_inc)+'---'
        self.keep_appart_from_markup_inc +=1
        return output

    def process_markup_language(self, markup_language):
        try:
            self.string = parse_markup_language(self.string, markup_language, self.ressource)
        
        # catch error from reStructuredText
        except SystemMessage as e:
            try:
                line = int(str(e).split(':')[1])
                msg = str(e).split(':')[2].strip()
                handle_markup_language_error(self.ressource+": "+msg, line=line, string=string)

            except Exception as ee: 
                handle_markup_language_error(self.ressource+", "+str(e))
        
        # Last round is about replacing needles and fix one last time indexes
        while "Missings triplet is not empty":                
            missings = []

            for triplet in self.keep_appart_from_markup_indexes:
                identifier, paragraphe, new_chunk = triplet
                string = self.string
                target = "---VENC-TEMPORARY-REPLACEMENT-"+str(identifier)+"---"
                try:
                    index = string.index(target)
                
                # In some case needle may be hidden in another needle.
                except:
                    
                    missings.append(triplet)
                    continue
                
                if paragraphe:
                    if string[index-3:index] == "<p>":
                        string = string[:index-3]+string[index:]
                        index -=3

                    if string[index+len(target):index+len(target)+4] == "</p>":
                        string = string[:index+len(target)]+string[index+len(target)+4:]
            
                self.string = string[:index]+new_chunk.strip().replace("\x1B\x1B","::")+string[index+len(target):]
                
            if not len(missings):
                break
                
            self.keep_appart_from_markup_indexes = missings
            
        # After markup langage processing done, indexes are messed up.
        # This is the last time entry content is preprocessed, so it must
        # handle escapes pattern now. Also, escaped markup string may hold some VenC patterns. 
        self.__init__(self.string, self.ressource, True)

class Processor():
    def __init__(self):
        self.debug = False
        self.functions		    = {}
        self.current_input_string   = ''
        self.ressource              = ''
        self.blacklist = []
        self.keep_appart_from_markup = []
        self.include_file_called = False
        self.ignore_patterns = False

    # Run any pattern and catch exception nicely
    def run_pattern(self, pattern, argv):
        try: # TODO: Should be refactored, Create a base PatternException
            include_file = pattern == "IncludeFile"
            output = self.functions[pattern](argv[include_file:])
            if include_file:
                self.include_file_called = True 
                self.ignore_patterns = argv[0].lower() == "true"

        except KeyError as e:
            output = self.handle_error(
                e,
                messages.unknown_pattern.format(pattern),
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [self.current_input_string[self.vop:self.vcp]]
            )

        except UnknownContextual as e:
                output = self.handle_error(
                    e,
                    messages.unknown_contextual.format(e),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = "{0["+str(e)[1:-1]+']}'
                )
        
        except PatternMissingArguments as e:
            output = self.handle_error(
                e,
                pattern+": "+e.info,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [self.current_input_string[self.vop:self.vcp]]
            )

        except PatternInvalidArgument as e:
            output = self.handle_error(
                e,
                messages.wrong_pattern_argument.format(e.name, e.value, pattern)+' '+e.message,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [self.current_input_string[self.vop:self.vcp]]
            )

        except GenericMessage as e: 
            output = self.handle_error(
                e,
                e.message,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [self.current_input_string[self.vop:self.vcp]]
            )

        # might be removed
        except FileNotFoundError as e:
            output = self.handle_error(
                e,
                messages.file_not_found.format(e.filename),
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [e.filename ]
            )

        return str(output)

    # Print out notification to user and replace erroneous pattern
    def handle_error(self, exception, error, default_output, error_origin = list()):
        extra= ""
        if self.debug:
            raise exception

        err = get_formatted_message(error, "RED")+"\n"
        if self.ressource != str():
            err = messages.in_ressource.format(self.ressource)+'\n'+err
        
        if len(error_origin):
            extra+=(''.join(self.current_input_string))
            for origin in error_origin:
                extra = highlight_value(extra, origin)
        die(err, "RED", extra)

    def set_function(self, key, function):
        self.functions[key] = function

    def del_function(self, key):
        try:
            del self.functions[key]

        except:
            pass

    def del_value(self, key):
        try:
            del self.dictionary[key]

        except:
            pass

    def set_dictionary(self, dictionary):
        for key in dictionary:
            self.dictionary[key] = dictionary[key]

    def set(self, symbol, value):
       self.dictionary[symbol] = value

    def process(self, pre_processed, safe_process=False):
        extra_processing_required = []
        op, cp, lo, lc, string = pre_processed.open_pattern_pos, pre_processed.close_pattern_pos, pre_processed.len_open_pattern_pos, pre_processed.len_close_pattern_pos, pre_processed.string
        if safe_process and pre_processed.backup == None:
            pre_processed.backup = (list(op), list(cp), lo, lc, str(pre_processed.string))

        if lo == 0 and lc == 0:
            bop = pre_processed.bop
            bcp = pre_processed.bcp
            for i in range(0, len(pre_processed.bop)):
                print(">>>",(string[bop[i]:bcp[i]].replace("\x1B\x1B","::")))
                string = string[:bop[i]]+(string[bop[i]:bcp[i]].replace("\x1B\x1B","::"))+string[bcp[i]:]
            
            op, cp = sorted(op+pre_processed.bop), sorted(cp+pre_processed.bcp)
            pre_processed.bop, pre_processed.bcp = [], []
            pre_processed.len_open_pattern_pos, pre_processed.len_close_pattern_pos, pre_processed.open_pattern_pos, pre_processed.close_pattern_pos, pre_processed.string = len(op), len(cp), op, cp, string
            return
        
        self.current_input_string = string
        self.ressource = pre_processed.ressource
        while lo:
            diff = 18446744073709551616
            i = 0
            j = 0
            for io in range(0, lo):
                for ic in range(0, lc):
                    d = cp[ic] - op[io]
                    if d > 0 and d < diff:
                        diff = d
                        i = io
                        j = ic

            self.vop, self.vcp = op[i], cp[j]
            vop, vcp = self.vop, self.vcp

            fields = [field.strip() for field in string[vop+2:vcp].split("::") if field != '']
            current_pattern = fields.pop(0)
            
            if (not current_pattern == "Escape") and (not current_pattern in self.blacklist):
                if current_pattern in self.keep_appart_from_markup:
                    new_chunk = pre_processed.keep_appart_from_markup_indexes_append(
                        True,
                        self.run_pattern(current_pattern, fields)
                    )
                    if self.include_file_called:
                        extra_processing_required.append(
                            pre_processed.keep_appart_from_markup_indexes[-1]+
                            (self.ignore_patterns,)
                        )
                        self.ignore_patterns = False
                        self.include_file_called = False
            
                elif current_pattern == "SetColor":
                    new_chunk = pre_processed.keep_appart_from_markup_indexes_append(
                        False,
                        self.run_pattern(current_pattern, fields)
                    )
                
                else:
                    new_chunk = self.run_pattern(current_pattern, fields)
                
                
                string = string[0:vop] + new_chunk + string[vcp+2:]
                self.current_input_string = string
                        
                offset = len(new_chunk) - (vcp + 2 - vop)
                op = [ (v+offset if v > vop else v) for v in op]
                cp = [ (v+offset if v > vcp else v) for v in cp]
                pre_processed.bop = [ (v+offset if v > vop else v) for v in pre_processed.bop]
                pre_processed.bcp = [ (v+offset if v > vcp else v) for v in pre_processed.bcp]

                op.pop(i)
                cp.pop(j)

            elif current_pattern == "Escape":
                op.pop(i)
                cp.pop(j)

            else:
                string = string[:op[i]]+(string[op[i]:cp[j]].replace("::","\x1B\x1B"))+string[cp[j]:]
                pre_processed.bop.append( op.pop(i) )
                pre_processed.bcp.append( cp.pop(j) )

            lo -= 1
            lc -= 1

        pre_processed.len_open_pattern_pos, pre_processed.len_close_pattern_pos, pre_processed.open_pattern_pos, pre_processed.close_pattern_pos = lo, lc, op, cp
        pre_processed.string = string

        self.process(pre_processed, safe_process)
        
        for extra in extra_processing_required:
            index, paragraphe, new_chunk, ignore_patterns = extra
            if not ignore_patterns:
                extra_pre_processed = ProcessedString(new_chunk, pre_processed.ressource, True)
                self.process(extra_pre_processed, safe_process)
                
            pre_processed.keep_appart_from_markup_indexes[index] = (index, paragraphe, extra_pre_processed.string if not ignore_patterns else new_chunk)
