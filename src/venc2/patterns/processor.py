#! /usr/bin/python3

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

import cgi
import markdown2 as markdown
import venc2.l10n
import venc2.helpers

from copy import deepcopy
from docutils.core import publish_parts
from docutils.utils import SystemMessage

from venc2.helpers import get_formatted_message
from venc2.helpers import highlight_value
from venc2.helpers import notify
from venc2.helpers import die
from venc2.helpers import remove_by_value
from venc2.helpers import PatternInvalidArgument
from venc2.helpers import GenericMessage
from venc2.l10n import messages

markup_language_errors = []

def cgi_escape(string):
    return cgi.escape(string).encode(
        'ascii', 
        'xmlcharrefreplace'
    ).decode(
        encoding='ascii'
    )

def get_markers_indexes(string):
    op = []
    cp = []
    i = 0
    l = len(string)
    offset=0
    while i < l:
        i = string.find(".:", i)
        if i == -1:
            i=0
            break
        op.append(i)
        i+=2
    
    while i < l:
        i = string.find(":.", i)
        if i == -1:
            i=0
            break
        cp.append(i)
        i+=2

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

# Special case of KeyError
class UnknownContextual(KeyError):
    pass

class ProcessedString():
    def __init__(self, string, ressource):
        self.open_pattern_pos, self.close_pattern_pos = get_markers_indexes(string)
        self.len_open_pattern_pos = len(self.open_pattern_pos)
        self.len_close_pattern_pos = len(self.close_pattern_pos)
        if self.len_open_pattern_pos > self.len_close_pattern_pos:
            l = self.open_pattern_pos +  self.close_pattern_pos
            mn, mx = min(l), max(l)
            die(messages.malformed_patterns_missing_closing_symbols.format(source))
            
        elif self.len_open_pattern_pos > self.len_close_pattern_pos:
            l = self.open_pattern_pos +  self.close_pattern_pos
            mn, mx = min(l), max(l)
            die(messages.malformed_patterns_missing_closing_symbols.format(source))

        self.string = string
        self.ressource = ressource
        self.keep_appart_from_markup_indexes = list()
        self.keep_appart_from_markup_inc = 0

    def keep_appart_from_markup_indexes_append(paragraphe, new_chunk, escape):
        if escape:
            new_chunk = cgi_escape(new_chunk)

        self.keep_appart_from_markup_indexes.append((self.keep_appart_from_markup_inc, paragraphe, new_chunk))
        output = "VENC_TEMPORARY_REPLACEMENT_"+str(self.keep_appart_from_markup_inc)
        self.keep_appart_from_markup_inc +=1
        return output

    def process_markup_language(self, markup_language, source):
        try:
            self.string = parse_markup_language(self.string, markup_language, source)
        
        # catch error from reStructuredText
        except SystemMessage as e:
            try:
                line = int(str(e).split(':')[1])
                msg = str(e).split(':')[2].strip()
                handle_markup_language_error(source+": "+msg, line=line, string=string)

            except Exception as ee: 
                print(ee, len(string.split('\n')))
                handle_markup_language_error(source+", "+str(e))
        
        for triplet in self.keep_appart_from_markup_indexes:
            index, paragraphe, new_chunk = triplet
            if paragraphe:
                self.string = self.string.replace(
                    "<p>VENC_TEMPORARY_REPLACEMENT_"+str(index)+"</p>",
                    new_chunk
                )
            else:
                self.string = self.string.replace(
                    "VENC_TEMPORARY_REPLACEMENT_"+str(index),
                    new_chunk
                )
"""
class PreProcessor0ld():
    def __init__(self, string):
        self.blacklist = list()
        self.sub_strings = list()
        self.patterns_index = list()
        close_symbol_pos = list()
        open_symbol_pos	 = list()
        i		 = int()
        
        while i < len(string):
            if string[i:i+2] == ".:":
                open_symbol_pos.append(i)

            elif string[i:i+2] == ":.":
                close_symbol_pos.append(i)

            # At some point, when we get the same opening and closing symbols, it means that we just reach the end of a pattern
            # so we can do the real job.
            if len(close_symbol_pos) == len(open_symbol_pos) and len(close_symbol_pos) != 0 and len(open_symbol_pos) != 0:
                # Append non pattern substring
                self.sub_strings.append(string[i-close_symbol_pos[-1]:open_symbol_pos[0]])

                # Append pattern substring
                self.sub_strings.append(string[open_symbol_pos[0]:close_symbol_pos[-1]+2])

                # Push pattern substring index in queue
                self.patterns_index.append(len(self.sub_strings)-1)
                string = string[close_symbol_pos[-1]+2:]
                open_symbol_pos = list()
                close_symbol_pos = list()
                i=0
            
            else:
                i+=1

        # append last substring
        self.sub_strings.append(string)
        
        # To avoid markup language collision we split appart Code snippet from the rest of the entry content
        self.keep_appart_from_markup_index = list()

    def process_markup_language(self, markup_language, source):
        string = ""
        for index in range(0, len(self.sub_strings)):
            if not index in self.keep_appart_from_markup_index:
                string += self.sub_strings[index]
            
            else:
                string += "VENC_TEMPORARY_REPLACEMENT_"+str(index)
        try:
            string = parse_markup_language(string, markup_language, source)
        
        # catch error from reStructuredText
        except SystemMessage as e:
            try:
                line = int(str(e).split(':')[1])
                msg = str(e).split(':')[2].strip()
                handle_markup_language_error(source+": "+msg, line=line, string=string)

            except Exception as ee: 
                print(ee, len(string.split('\n')))
                handle_markup_language_error(source+", "+str(e))
        
        for pair in self.keep_appart_from_markup_index:
            index, paragraphe = pair
            if paragraphe:
                string = string.replace(
                    "<p>VENC_TEMPORARY_REPLACEMENT_"+str(index)+"</p>",
                    self.sub_strings[index]
                )
            else:
                string = string.replace(
                    "VENC_TEMPORARY_REPLACEMENT_"+str(index),
                    self.sub_strings[index]
                )

        return string
"""

class Processor():
    def __init__(self):
        self.forbidden = []
        self.functions		    = dict()
        self.current_input_string   = str()
        self.ressource              = str()
        self.errors                 = list()

        # Some patterns are contextual while others are constant in time.
        # To save time we wan't to perform two-pass analysis. In the first one
        # we're ignoring some given patterns which usualy are contextual. Once
        # non-contextual pattern are parsed the second pass occurs each time we
        # require the given string in every needed context
        self.blacklist = list()

    # Run any pattern and catch exception nicely
    def run_pattern(self, pattern, argv):
        try:
            output = self.functions[pattern](argv)
        
        except UnknownContextual as e:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = "{0["+str(e)[1:-1]+']}'
                )
        
        except KeyError as e:
            if str(e)[1:-1] == pattern:
                output =  self.handle_error(
                    messages.unknown_pattern.format(pattern),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = [':'+pattern+':']
                )
            else:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = [':'+str(e)[1:-1]+':','{0['+str(e)[1:-1]+']}', ':'+pattern+':'] # first item might be useless ???
                )

        except AttributeError as e:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = [str(e).split("'")[-2], ':'+pattern+':']
                )
        
        except IndexError:
            output = self.handle_error(
                pattern+": "+messages.not_enough_args,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                [pattern]
            )

        except PatternInvalidArgument as e:
            output = self.handle_error(
                messages.wrong_pattern_argument.format(e.name, e.value, pattern)+' '+e.message,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [".:"+pattern+"::"+"::".join(argv)+":."]
            )

        except GenericMessage as e: 
            output = self.handle_error(
                e.message,
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [".:"+pattern+"::"+"::".join(argv)+":."]
            )

        except FileNotFoundError as e:
            output = self.handle_error(
                messages.file_not_found.format(e.filename),
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = [e.filename ]
            )
        return str(output)

    # Print out notification to user and replace erroneous pattern
    def handle_error(self, error, default_output, error_origin = list()):
        err = get_formatted_message(error, "RED")+"\n"
            
        if self.ressource != str():
            err += get_formatted_message(messages.in_ressource.format(self.ressource)+"\n", "RED")
                
        if not err in venc2.helpers.errors:
            venc2.helpers.errors.append(err)
            # error_origin is a array of substring value to replace in faulty string.
            if error_origin != list():
                err+=(''.join(self.current_string).strip())
                for origin in error_origin:
                    err = highlight_value(err, origin)
            
            print(err+"\n")
        
        return default_output

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

    def if_not_present(self, string):
        for pattern in self.blacklist:
            if pattern in string:
                False

        return True

    """
    # Process queue
    def old_process(self, input_pre_processed, ressource, escape=False):
        self.ressource = ressource
        pre_processed = deepcopy(input_pre_processed)
        if len(pre_processed.patterns_index) == 0:
            return pre_processed
        
        self.current_string = pre_processed.sub_strings
        to_remove = list()
        for index in pre_processed.patterns_index:
            current_pattern = pre_processed.sub_strings[index][2:-2].split('::')[0]

            if current_pattern in ["CodeHighlight", "Latex2MathML", "IncludeFile", "audio", "video","EmbedContent"]:
                pre_processed.keep_appart_from_markup_index.append((index,True))
            
            elif current_pattern in ["SetColor"]:
                pre_processed.keep_appart_from_markup_index.append((index,False))

            # this is tested twice???
            if current_pattern in self.forbidden:
                self.handle_error(
                    messages.pattern_is_forbidden_here.format(current_pattern),
                    ",;"+current_pattern+";;"+";;".join(pre_processed.sub_strings[index][2:-2])+";,",
                    error_origin = [current_pattern]
                )

            if (not current_pattern in self.blacklist) and (not current_pattern in self.forbidden) :
               if current_pattern == "Escape":
                    pre_processed.sub_strings[index] = ''.join(pre_processed.sub_strings[index][2:-2].split('::')[1:])
                    to_remove.append(index)
                    continue
                    
                pre_processed.sub_strings[index] = self.process(pre_processed.sub_strings[index], escape)
                
                # check if there is residual patterns
                if self.if_not_present(pre_processed.sub_strings[index]):
                    to_remove.append(index)

        for index in to_remove:
            pre_processed.patterns_index = remove_by_value(pre_processed.patterns_index, index)

        return pre_processed
    """

    def process(self, pre_processed, escape=False):
        op, cp, string, lo, lc = pre_processed.open_pattern_pos, pre_processed.close_pattern_pos, pre_processed.string, pre_processed.len_open_pattern_pos, pre_processed.len_close_pattern_pos
        if lo == 0 and lc == 0:
            return pre_processed
        

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

            vop, vcp = op[i], cp[j]

            fields = [field.strip() for field in string[vop+2:vcp].split("::") if field != '']
            current_pattern = fields[0]
            
            if current_pattern in self.forbidden:
                self.handle_error(
                    messages.pattern_is_forbidden_here.format(current_pattern),
                    ",;"+current_pattern+";;"+";;".join(pre_processed.sub_strings[index][2:-2])+";,",
                    error_origin = [current_pattern]
                )

            """ réintégrer l'exclusi0n de certain pattern, réintégrer Escape N0Escape """
            if (not current_pattern in self.blacklist) and (not current_pattern in self.forbidden) :
                if current_pattern in ["CodeHighlight", "Latex2MathML", "IncludeFile", "audio", "video","EmbedContent"]:
                    new_chunk = pre_processed.keep_appart_from_markup_index_append(
                        True,
                        self.run_pattern(current_pattern, fields[1:]),
                        escape
                    )
            
                elif current_pattern in ["SetColor"]:
                    new_chunk = pre_processed.keep_appart_from_markup_index_append(
                        False,
                        self.run_pattern(current_pattern, fields[1:]),
                        escape,
                    )
            
                else:
                    new_chunk = self.run_pattern(current_pattern, fields[1:])
                    if escape:
                        new_chunk = cgi_escape(new_string)

                string = string[0:vop] + new_chunk + string[vcp+2:]
                        
                offset = len(new_chunk) - (vcp + 2 - vop)
                for k in range(1,lo):
                    if k >= i+1:
                        op[k] += offset

                    cp[k] += offset

                op.pop(i)
                cp.pop(j)
                lo -= 1
                lc -= 1
                continue

        if len(self.blacklist):
            pre_processed.len_open_pattern_pos, pre_processed.len_close_pattern_pos = lo, lc
            return pre_processed

        return self.process(pre_processed, escape)
