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
import venc2.l10n
import venc2.helpers

from copy import deepcopy

from venc2.helpers import get_formatted_message
from venc2.helpers import highlight_value
from venc2.helpers import remove_by_value
from venc2.l10n import messages

# Special case of KeyError

class UnknownContextual(KeyError):
    pass

OPEN_SYMBOL = ".:"
SEPARATOR = "::"
CLOSE_SYMBOL = ":."

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

def merge_batches(batches):
    return ''.join(batches.sub_strings)

""" should be replaced by ''.join(sub_string) 
def get_final_string(processed):
    output = str()
    for chunk in processed.sub_strings:
        output += chunk

    return output
"""

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
                    "~§"+pattern+"§§"+"§§".join(argv)+"§~",
                    error_origin = "{0["+str(e)[1:-1]+']}'
                )
        
        except KeyError as e:
            if str(e)[1:-1] == pattern:
                output =  self.handle_error(
                    messages.unknown_pattern.format(pattern),
                    "~§"+pattern+"§§"+"§§".join(argv)+"§~",
                    error_origin = [':'+pattern+':']
                )
            else:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    "~§"+pattern+"§§"+"§§".join(argv)+"§~",
                    error_origin = [':'+str(e)[1:-1]+':','{0['+str(e)[1:-1]+']}']
                )

        except AttributeError as e:
                output = self.handle_error(
                    messages.unknown_contextual.format(e),
                    "~§"+pattern+"§§"+"§§".join(argv)+"§~",
                    error_origin = [str(e).split("'")[-2]]
                )
        
        except IndexError:
            output = self.handle_error(
                pattern+": "+messages.not_enough_args,
                "~§"+pattern+"§§"+"§§".join(argv)+"§~",
                [pattern]
            )

        return str(output)

    # Print out notification to user and replace erroneous pattern
    def handle_error(self, error, default_output, error_origin = list()):
        err = get_formatted_message(error, "RED")+"\n"
            
        if self.ressource != str():
            err += get_formatted_message(messages.in_ressource.format(self.ressource)+"\n", "RED")
                
        if not err in venc2.helpers.errors:
            venc2.helpers.errors.append(err)
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
    def batch_process(self, input_pre_processed, ressource, markdown=False, escape=False):
        self.ressource = ressource
        pre_processed = deepcopy(input_pre_processed)
        if len(pre_processed.patterns_index) == 0:
            return pre_processed
        
        self.current_string = pre_processed.sub_strings
        to_remove = list()
        for index in pre_processed.patterns_index:
            current_pattern = pre_processed.sub_strings[index][2:-2].split('::')[0]
            if not current_pattern in self.blacklist:
                pre_processed.sub_strings[index] = self.process(pre_processed.sub_strings[index], escape)
                
                # check if there is residual patterns
                if self.if_not_present(pre_processed.sub_strings[index]):
                    to_remove.append(index)

                if current_pattern in self.clean_after_and_before and markdown:
                    try:
                        pre_processed.sub_strings[index-1] = pre_processed.sub_strings[index-1][:-3] # remove <p>

                    except IndexError:
                        pass
                    
                    try:
                        pre_processed.sub_strings[index+1] = pre_processed.sub_strings[index+1][4:] # remove </p>

                    except IndexError:
                        pass

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
                if open_symbol_pos[-1] < close_symbol_pos[0]:
                    fields = [field for field in string[open_symbol_pos[-1]+2:close_symbol_pos[0]].split(SEPARATOR) if field != '']
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
                                string[close_symbol_pos[0]+2:],
                                escape=True
                            )

                        else:
                            return self.process(
                                string[
                                    :open_symbol_pos[-1]]+
                                    str(output)+
                                    string[close_symbol_pos[0]+2:
                                ],
                                escape=False
                            )
            i+=1
    
        return string
