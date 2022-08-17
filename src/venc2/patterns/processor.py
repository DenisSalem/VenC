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

from venc2.patterns.patterns_map import PatternsMap

class VenCString:
    def __init__(self):
        self.filtered_offset = 0
        self.filtered_patterns = []
        self.id = "\x00"+str(id(self))+"\x00"
        self.escape_pattern = False
        
    def update_child(self, new_chunk, child, apply_offset=True):
        self._str = self._str[:child.o]+new_chunk+self._str[child.c+2:]
        if apply_offset:
            offset = len(new_chunk) - (child.c + 2 - child.o)
            child.c += offset
            VenCString.__apply_offset(self.sub_strings, offset, child.o)
                  
    @staticmethod
    def __apply_offset(sub_strings, offset, o):
        for pattern in sub_strings:
            if pattern.o > o:
              pattern.o += offset
              pattern.c += offset
              VenCString.__apply_offset(pattern.sub_strings, offset, -1)
    
    def __str__(self):
        return self._str
        
    def __repr__(self):
        return self.id
                            
class PatternNode(VenCString):
    FLAG_NONE = 0
    FLAG_NON_CONTEXTUAL = 1
    FLAG_CONTEXTUAL = 2
    FLAG_NON_PARALLELIZABLE = 4
    FLAG_WAIT_FOR_CHILDREN_TO_BE_PROCESSED = 8 # NOT IMPLEMENTED YET
    FLAG_ALL = 16
    def __init__(self, string, o, c):
        super().__init__()
        self.o = o
        self.c = c
        self.flags = PatternNode.FLAG_NONE
        self._str = string[o:c+2]
        self.name = None
        self.args = []
        self.sub_strings = []

class PatternsStack(list):
    def __init__(self, string_under_processing):
        super().__init__()
        self.append(string_under_processing)
        for pattern in string_under_processing.filtered_patterns:
            pattern.filtered_offset = 0
            
        string_under_processing.filtered_patterns = []
        string_under_processing.filtered_offset = 0
        
    def pop(self, filtered):
        if not filtered:
            self[-2].sub_strings.pop(-1-self[-2].filtered_offset)
            
        return super().pop(-1)
        
    def filter(self):
        self[0].filtered_patterns.append(self[-1])
        self[-2].filtered_offset += 1        
    
class Processor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
    
    def process(self, string_under_processing, flags, parallel_processing=False):
        patterns_stack = PatternsStack(string_under_processing)
        patterns_stack_append = patterns_stack.append
        patterns_stack_filter = patterns_stack.filter
        patterns_stack_pop = patterns_stack.pop

        while '∞':
            # Nothing left to do. Exiting
            if not (len(string_under_processing.sub_strings) - string_under_processing.filtered_offset):
                break
                
            # Does the top of the stack has sub strings and is not an "Escape" pattern ?
            patterns_stack_tail = patterns_stack[-1]
            if len(patterns_stack_tail.sub_strings) - patterns_stack_tail.filtered_offset and not patterns_stack_tail.escape_pattern:
                patterns_stack_append(patterns_stack_tail.sub_strings[-1-patterns_stack_tail.filtered_offset])

            else:
                # Does the pattern if okay to be processed ?
                if patterns_stack_tail.flags & flags and not ((patterns_stack_tail.flags & PatternNode.FLAG_NON_CONTEXTUAL and):
                    pattern = patterns_stack_pop(False)
                    # TODO: Investigate pattern validation in datastructure building
                    if not pattern.name in self.functions.keys():
                        from venc2.exceptions import UnknownPattern
                        raise UnknownPattern(pattern, string_under_processing)
                        
                    parent = patterns_stack[-1]
                    if type(parent) == PatternNode:                               
                        chunk = self.functions[pattern.name](pattern, *pattern.args)
                        parent_args = parent.args
                        i = 2 + len(parent.name)
                        args_index = 0
                        # TODO: instead of searching shit, store data on datastructure building
                        while '∞':
                            current_parent_arg_len = len(parent_args[args_index])
                            parent_args_current_index = parent_args[args_index]
                            if  i + 2 < pattern.o and i + 2 + current_parent_arg_len > pattern.c:
                                parent_args[args_index] = parent_args_current_index[:pattern.o - (i + 2)]+chunk+parent_args_current_index[pattern.c - i:]
                                offset = len(parent_args[args_index]) - current_parent_arg_len
                                break
                              
                            i += 2 + len(parent_args[args_index])
                            args_index+=1
                    else:
                        chunk = self.functions[pattern.name](pattern, *pattern.args)
                        offset = len(chunk) - len(pattern.id)
                        parent_str = parent._str
                        parent._str = parent_str[:pattern.o]+chunk+parent_str[pattern.c+2:]
                        
                    # ~ except VenCException as e:


                    # At this point pattern has been processed and we got an new offset                    
                    parent_sub_strings = parent.sub_strings
                    for j in range(-parent.filtered_offset, 0): # adjusting parent sub strings indexes
                        parent_sub_strings[j].o += offset
                        parent_sub_strings[j].c += offset
                    
                    # pattern may hold some unprocessed patterns they have to be reintegrated
                    if len(pattern.sub_strings):
                        parent_filtered_offset = parent.filtered_offset
                        parent_sub_string = parent.sub_strings
                        #adjusting inner filtered indexes
                        for sub_string in pattern.sub_strings:
                            o = str(parent).find(sub_string.id) # possible bottleneck
                            if o > 0:
                                sub_string.c += o - sub_string.o
                                sub_string.o = o
                                
                        parent.sub_strings = parent_sub_string[:len(parent_sub_string)-parent_filtered_offset] + pattern.sub_strings + parent_sub_string[len(parent_sub_string)-parent_filtered_offset:]

                else:
                    patterns_stack_filter()
                    patterns_stack_pop(True)

class StringUnderProcessing(VenCString):
    def __init__(self, string, context):
        super().__init__()
        self._str = string
        self.context = context
        self.has_non_parallelizables = False
        self.filtered_pattern = []

        # This block get indexes of opening and closing patterns.
        self.op = StringUnderProcessing.__find_pattern_boundaries(string, '.:')
        self.cp = StringUnderProcessing.__find_pattern_boundaries(string, ':.')
        
        # This block sort pattern by nest order AND position in input string.
        self.sub_strings = []
        sub_strings_append = self.sub_strings.append
        op, cp, op_pop, cp_pop = self.op, self.cp, self.op.pop, self.cp.pop
        while len(op) or len(cp):
            if ((not len(op)) or (not len(cp))) and len(op) != len(cp):
                from venc2.exceptions import MalformedPatterns
                raise MalformedPatterns(self)
                
            diff = 18446744073709551616
            i = 0
            j = 0
            for io in range(0, len(op)):
                for ic in range(0, len(cp)):
                    d = cp[ic] - op[io]
                    if d > 0 and d < diff:
                        diff = d
                        i = io
                        j = ic
                        
            sub_strings_append(PatternNode(string, op[i],cp[j]))            
            op_pop(i)
            cp_pop(j)
          
        # Make a tree
        i = 0
        sub_strings = self.sub_strings
        sub_strings_pop = sub_strings.pop
        while i < len(sub_strings):
            for pattern in sub_strings[i+1:]:
                if sub_strings[i].o > pattern.o and sub_strings[i].c < pattern.c:
                    pattern.sub_strings.append(sub_strings_pop(i) )
                    i =-1
                    break
                    
            i+=1

        # - Make nested patterns indexes relatives to upper pattern.
        # - Set patterns name and args.
        # - Set pattern flags.
        # - Replace patterns by their unique identifier.
        self.__finalize_patterns_tree(sub_strings)
                
    def __finalize_patterns_tree(self, nodes, parent=None):
        if parent != None:
            parent.sub_strings = sorted(nodes, key = lambda n:n.o)
            nodes = parent.sub_strings
            
        else:
            self.sub_strings = sorted(nodes, key = lambda node:node.o)
            nodes = self.sub_strings
            
        for pattern in nodes:
            self.__finalize_patterns_tree(pattern.sub_strings, pattern)
            if parent != None:
                pattern.o -= parent.o 
                pattern.c -= parent.o
                parent.update_child(pattern.id, pattern)
                
            else:
                self.update_child(pattern.id, pattern)
                
            l = str(pattern)[2:-2].split('::')
            pattern.name = l[0]
            pattern.args += l[1:]
            if pattern.name == "Escape":
                pattern.escape_pattern = True

            self.__set_pattern_flags(pattern)
            
    def __set_pattern_flags(self, pattern):
        if not pattern.name in PatternsMap.CONTEXTUALS.keys():
            pattern.flags |= PatternNode.FLAG_NON_CONTEXTUAL
        else:
            pattern.flags |= PatternNode.FLAG_CONTEXTUAL
            
        if pattern.name in PatternsMap.NON_PARALLELIZABLES:
            pattern.flags |= PatternNode.FLAG_NON_PARALLELIZABLE
            self.has_non_parallelizables = True
    
    @staticmethod
    def __find_pattern_boundaries(string, symbol):
      l = list()
      l_append = l.append
      index=0
      while '∞':
          index = string.find(symbol, index)
          if index == -1:
            return l
          l_append(index)
          index+=1
    
    # Works like processor algorithm without special cases
    def flatten(self, highlight_pattern=None):
        patterns_stack = PatternsStack(self)
        patterns_stack_append = patterns_stack.append
        patterns_stack_filter = patterns_stack.filter
        patterns_stack_pop = patterns_stack.pop
        while '∞':
            # Nothing left to do. Exiting
            if not len(self.sub_strings):
                if highlight_pattern:
                    self._str = self._str.replace(
                        highlight_pattern.id,
                        "\033[91m" + ".:"+highlight_pattern.name+("::" if len(highlight_pattern.args) else "" )+("::".join(highlight_pattern.args))+":." + "\033[0m"
                    )
                return self._str
                
            if len(patterns_stack[-1].sub_strings):
                patterns_stack_append(patterns_stack[-1].sub_strings[-1])
            else:
                pattern = patterns_stack_pop(False)
                parent = patterns_stack[-1]
                match = pattern == highlight_pattern
                chunk = ".:"+pattern.name+("::" if len(pattern.args) else "" )+("::".join(pattern.args))+":."
                if type(parent) == PatternNode:
                    parent_args = parent.args
                    i = 2 + len(parent.name)
                    args_index = 0
                    while '∞':
                        current_parent_arg_len = len(parent_args[args_index])
                        parent_args_current_index = parent_args[args_index]
                        if  i + 2 < pattern.o and i + 2 + current_parent_arg_len > pattern.c:
                            parent_args[args_index] = parent_args_current_index[:pattern.o - (i + 2)]+chunk+parent_args_current_index[pattern.c - i:]
                            offset = len(parent_args[args_index]) - current_parent_arg_len
                            break
                          
                        i += 2 + len(parent_args[args_index])
                        args_index+=1
                else:
                    offset = len(chunk) - len(pattern.id)
                    parent_str = parent._str
                    parent._str = parent_str[:pattern.o]+chunk+parent_str[pattern.c+2:]
    
    def reset_index(self, new_string):
        self._str = new_string
        for sub_string in self.sub_strings:
            o = self._str.find(sub_string.id)
            sub_string.c += o - sub_string.o
            sub_string.o = o
