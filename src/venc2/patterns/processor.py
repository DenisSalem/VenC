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

from venc2.exceptions import VenCException, MalformedPatterns
from venc2.patterns.patterns_map import PatternsMap

class VenCString:
    def __init__(self):
        self.filtered_offset = 0
        self.filtered_patterns = []
        self.id = "\x00"+str(id(self))+"\x00"
        
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
    
    def process(self, string_under_processing, flags):
        patterns_stack = PatternsStack(string_under_processing)
        patterns_stack_append = patterns_stack.append
        patterns_stack_filter = patterns_stack.filter
        patterns_stack_pop = patterns_stack.pop

        while '∞':
            # Nothing left to do. Exiting
            if not (len(string_under_processing.sub_strings) - string_under_processing.filtered_offset):
                break
                
            # Does the top of the stack has sub strings ?
            if len(patterns_stack[-1].sub_strings) - patterns_stack[-1].filtered_offset:
                patterns_stack_append(patterns_stack[-1].sub_strings[-1-patterns_stack[-1].filtered_offset])

            else:
                # Does the pattern if okay to be processed ?
                if flags == PatternNode.FLAG_ALL or patterns_stack[-1].flags & flags:
                    try:
                        pattern = patterns_stack_pop(False)
                        parent = patterns_stack[-1]
                        if type(parent) == PatternNode:
                            chunk = self.functions[pattern.name](pattern, *pattern.args)
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
                            chunk = self.functions[pattern.name](pattern, *pattern.args)
                            offset = len(chunk) - len(pattern.id)
                            parent_str = parent._str
                            parent._str = parent_str[:pattern.o]+chunk+parent_str[pattern.c+2:]
                        
                    except VenCException as e:
                        e.die()

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
                        parent.sub_strings = parent_sub_string[len(parent_sub_string)-parent_filtered_offset-1:] + pattern.sub_strings + parent_sub_string[:len(parent_sub_string)-parent_filtered_offset-1]
                        
                else:
                    patterns_stack_filter()
                    patterns_stack_pop(True)
                

      
    # ~ def process(self, string_under_processing, flags):
        # ~ branch = [ string_under_processing ]
        # ~ branch_append = branch.append
        # ~ branch_pop = branch.pop
        
        # ~ for pattern in string_under_processing.filtered_patterns:
            # ~ pattern.filtered_offset = 0
            
        # ~ string_under_processing.filtered_patterns = []
        # ~ # Yes, we're walking a tree with an iterative implementation ...
        # ~ # Because I want the code to run so fast it actualy has to break causality principle.
        # ~ while '∞':
            # ~ if len(string_under_processing.sub_strings) == string_under_processing.filtered_offset:
                # ~ return

            # ~ # looping until sub_string is empty of non filtered pattern            
            # ~ if len(branch[-1].sub_strings) - branch[-1].filtered_offset:
                # ~ tail_filtered_offset = branch[-1].filtered_offset
                # ~ tail_sub_strings = branch[-1].sub_strings
                # ~ # pick the right node or skip it.
                # ~ if flags & tail_sub_strings[-1-tail_filtered_offset].flags:
                    # ~ branch_append(tail_sub_strings[-1-tail_filtered_offset])
                    
                # ~ else:
                    # ~ string_under_processing.filtered_patterns.append(branch[-1])
                    # ~ branch[-1].filtered_offset+=1
                    # ~ continue
            
            # ~ try:
                # ~ node = branch_pop()
                # ~ tail = branch[-1]

                # ~ if hasattr(tail, "args"):
                    # ~ chunk = self.functions[node.name](node, *node.args)
                    # ~ parent_args = tail.args
                    # ~ i = 2 + len(tail.name)
                    # ~ args_index = 0
                    # ~ while '∞':                      
                        # ~ if  i + 2 < node.o and i + 2 + len(parent_args[args_index]) > node.c:
                            # ~ o = node.o - (i + 2)
                            # ~ c = node.c - (i + 2)
                            # ~ old_parent_arg_len = len(parent_args[args_index])
                            # ~ parent_args[args_index] = parent_args[args_index][:o]+chunk+parent_args[args_index][c+2:]
                            # ~ new_parent_arg_len = len(parent_args[args_index])
                            # ~ offset = new_parent_arg_len - old_parent_arg_len
                            # ~ break
                          
                        # ~ i += 2 + len(parent_args[args_index])
                        # ~ args_index+=1
                        
                # ~ else:
                    # ~ try:
                        # ~ chunk = self.functions[node.name](node, *node.args)
                    # ~ except Exception as e: # TODO Handle type error with too much or not enough args
                        # ~ print(node.name, node.args)
                        # ~ raise e
                    # ~ offset = len(chunk) - len(node.id)
                    # ~ branch[-1]._str = str(tail)[:node.o]+chunk+str(tail)[node.c+2:]
                
                # ~ # adjusting filtered o,c
                # ~ tail_sub_strings = tail.sub_strings
                # ~ for j in range(-tail.filtered_offset, 0):
                    # ~ tail_sub_strings[j].o += offset
                    # ~ tail_sub_strings[j].c += offset
                
                # ~ if len(node.sub_strings):
                  # ~ tail_filtered_offset = tail.filtered_offset
                  # ~ #adjusting inner filtered indexes
                  # ~ for sub_string in node.sub_strings:
                      # ~ o = str(branch[-1]).find(sub_string.id) # possible bottleneck
                      # ~ if o > 0:
                          # ~ sub_string.c += o - sub_string.o
                          # ~ sub_string.o = o

                  # ~ tail.sub_strings = tail_sub_strings[:-1-tail_filtered_offset] + node.sub_strings + (tail_sub_strings[-tail_filtered_offset:] if tail_filtered_offset > 0 else [])

                # ~ else:
                    # ~ tail_sub_strings.pop(-1-tail.filtered_offset)
                
            # ~ except VenCException as e:
                # ~ raise e.die()

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
    
    def reset_index(self, new_string):
        self._str = new_string
                
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
