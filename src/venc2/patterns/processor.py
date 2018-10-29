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
import markdown
import venc2.l10n
import venc2.helpers

from copy import deepcopy
from docutils.core import publish_parts
from docutils.utils import SystemMessage

from venc2.helpers import get_formatted_message
from venc2.helpers import highlight_value
from venc2.helpers import notify
from venc2.helpers import remove_by_value
from venc2.helpers import PatternInvalidArgument
from venc2.l10n import messages

# Special case of KeyError
class UnknownContextual(KeyError):
    pass

OPEN_SYMBOL = ".:"
SEPARATOR = "::"
CLOSE_SYMBOL = ":."

markup_language_errors = []

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

# Because parsing is recursive we want to avoid useless computation
# by splitting a given string and mark where exactly are the patterns 
# we want to process.
class PreProcessor():
    def __init__(self, string):
        self.blacklist = list()
        self.sub_strings = list()
        self.patterns_index = list()
        close_symbol_pos = list()
        open_symbol_pos	 = list()
        i		 = int()
        
        while i < len(string):
            if string[i:i+2] == OPEN_SYMBOL:
                open_symbol_pos.append(i)

            elif string[i:i+2] == CLOSE_SYMBOL:
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
        
        for index in self.keep_appart_from_markup_index:
            string = string.replace(
                "<p>VENC_TEMPORARY_REPLACEMENT_"+str(index)+"</p>",
                self.sub_strings[index]
            )

        return string

def parse_markup_language(string, markup_language, source):
    if markup_language == "Markdown":
        string = markdown.markdown(string)
        
    elif markup_language == "reStructuredText":
        string = publish_parts(string, writer_name='html', settings_overrides={'doctitle_xform':False, 'halt_level': 2, 'traceback': True, "warning_stream":"/dev/null"})['html_body']

    elif markup_language != "none":
            err = messages.unknown_markup_language.format(markup_language, source)
            handle_markup_language_error(err)

    return string

class Processor():
    def __init__(self):
        self.functions		 = dict()
        self.currentString       = str()
        self.ressource           = str()
        self.errors              = list()
        self.clean_after_and_before = list()

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
                    error_origin = [':'+str(e)[1:-1]+':','{0['+str(e)[1:-1]+']}']
                )

        except AttributeError as e:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    ",;"+pattern+";;"+";;".join(argv)+";,",
                    error_origin = [str(e).split("'")[-2]]
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

        except FileNotFoundError as e:
            output = self.handle_error(
                messages.file_not_found.format(e.filename),
                ",;"+pattern+";;"+";;".join(argv)+";,",
                error_origin = e.filename
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

    # Process queue
    def batch_process(self, input_pre_processed, ressource, escape=False):
        self.ressource = ressource
        pre_processed = deepcopy(input_pre_processed)
        if len(pre_processed.patterns_index) == 0:
            return pre_processed
        
        self.current_string = pre_processed.sub_strings
        to_remove = list()
        for index in pre_processed.patterns_index:
            current_pattern = pre_processed.sub_strings[index][2:-2].split('::')[0]
            if current_pattern in ["CodeHighlight", "Latex2MathML","IncludeFile"]:
                pre_processed.keep_appart_from_markup_index.append(index)

            if not current_pattern in self.blacklist:
                pre_processed.sub_strings[index] = self.process(pre_processed.sub_strings[index], escape)
                
                # check if there is residual patterns
                if self.if_not_present(pre_processed.sub_strings[index]):
                    to_remove.append(index)

        for index in to_remove:
            pre_processed.patterns_index = remove_by_value(pre_processed.patterns_index, index)

        return pre_processed

    def process(self, string, escape):
        close_symbol_pos = list()
        open_symbol_pos	 = list()
        output		 = str()
        fields		 = list()
        i		 = int()

        while i < len(string):
            if string[i:i+2] == OPEN_SYMBOL:
                open_symbol_pos.append(i)

            elif string[i:i+2] == CLOSE_SYMBOL:
                close_symbol_pos.append(i)

            if len(close_symbol_pos) <= len(open_symbol_pos) and len(close_symbol_pos) != 0 and len(open_symbol_pos) != 0:
                if open_symbol_pos[-1] < close_symbol_pos[-1]:
                    fields = [field for field in string[open_symbol_pos[-1]+2:close_symbol_pos[-1]].split(SEPARATOR) if field != '']
                    if not fields[0] in self.blacklist:
                        output = self.run_pattern(fields[0], fields[1:])
                        if escape:
                            return self.process(
                                string[:open_symbol_pos[-1]]+
                                cgi.escape(output).encode(
                                    'ascii', 
                                    'xmlcharrefreplace'
                                ).decode(
                                    encoding='ascii'
                                )+
                                string[close_symbol_pos[-1]+2:],
                                escape
                            )

                        else:
                            return self.process(
                                string[:open_symbol_pos[-1]]+
                                str(output)+
                                string[close_symbol_pos[-1]+2:],
                                escape
                            )
            i+=1
    
        return string
