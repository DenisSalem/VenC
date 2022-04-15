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

from venc2.exceptions import MalformedPatterns
from venc2.patterns.patterns_map import PatternsMap

class VenCString:
    def __init__(self):
        self.filtered_offset = 0
        self.filtered_patterns = []
        self.id = "\x00"+str(id(self))+"\x00"
        
    def update_child(self, new_chunk, child):
        self._str = self._str[:child.o]+new_chunk+self._str[child.c+2:]
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
                        
class PatternNode(VenCString):
    FLAG_NONE = 0
    FLAG_NON_CONTEXTUAL = 1
    FLAG_NON_PARALLELIZABLE = 2
    FLAG_WAIT_FOR_CHILDREN_TO_PROCESSED = 4
    
    def __init__(self, string, o, c):
        super().__init__()
        self.o = o
        self.c = c
        self.flags = PatternNode.FLAG_NONE
        self._str = string[o:c+2]
        self.name = None
        self.args = []
        self.sub_strings = []
                
class Processor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
    
    def process(self, string_under_processing, non_contextual, non_parallelizable):
        branch = [ string_under_processing ]
        branch_append = branch.append
        branch_pop = branch.pop
        
        for pattern in string_under_processing.filtered_patterns:
            pattern.filtered_offset = 0
            
        string_under_processing.filtered_patterns = []
        
        # Yes, we're walking a tree with an iterative implementation ...
        while '∞':
            if len(string_under_processing.sub_strings) == string_under_processing.filtered_offset:
                return
            
            # looping until sub_string is empty of non filtered pattern
            if len(branch[-1].sub_strings) - branch[-1].filtered_offset:
                tail_filtered_offset = branch[-1].filtered_offset
                tail_sub_strings = branch[-1].sub_strings
                # pick the right node or skip it.
                if  tail_sub_strings[-1-tail_filtered_offset].flags & PatternNode.FLAG_NON_CONTEXTUAL == non_contextual and \
                    tail_sub_strings[-1-tail_filtered_offset].flags & PatternNode.FLAG_NON_PARALLELIZABLE == non_parallelizable :
                    branch_append(tail_sub_strings[-1-tail_filtered_offset])
                    
                else:
                    if not branch[-1] in string_under_processing.filtered_patterns:
                        string_under_processing.filtered_patterns.append(branch[-1])
                        
                    branch[-1].filtered_offset+=1
                    
                continue
                
            try:
                node = branch_pop()
                tail = branch[-1]

                if hasattr(tail, "args"):
                    chunk = self.functions[node.name](node, *node.args)
                    parent_args = tail.args
                    i = 2 + len(tail.name)
                    args_index = 0
                    while '∞':                      
                        if  i + 2 < node.o and i + 2 + len(parent_args[args_index]) > node.c:
                            o = node.o - (i + 2)
                            c = node.c - (i + 2)
                            old_parent_arg_len = len(parent_args[args_index])
                            parent_args[args_index] = parent_args[args_index][:o]+chunk+parent_args[args_index][c+2:]
                            new_parent_arg_len = len(parent_args[args_index])
                            offset = new_parent_arg_len - old_parent_arg_len
                        
                            break
                          
                        i += 2 + len(parent_args[args_index])
                        args_index+=1
                        
                else:
                    chunk = self.functions[node.name](node, *node.args)
                    offset = len(chunk) - len(node.id)
                    branch[-1]._str = str(tail)[:node.o]+chunk+str(tail)[node.c+2:]
                    
                # adjusting filtered indexes
                tail_sub_strings = tail.sub_strings
                for j in range(-tail.filtered_offset, 0):
                    tail_sub_strings[j].o += offset
                    tail_sub_strings[j].c += offset
                
                if len(node.sub_strings):
                  tail_filtered_offset = tail.filtered_offset
                  #adjusting inner filtered indexes
                  for sub_string in node.sub_strings:
                      o = str(branch[-1]).find(sub_string.id) # possible bottleneck
                      if o > 0:
                          sub_string.c += o - sub_string.o
                          sub_string.o = o
                  tail.sub_strings = tail_sub_strings[:-1-tail_filtered_offset]+node.sub_strings+tail_sub_strings[-tail_filtered_offset:]
                  
                else:
                    tail_sub_strings.pop(-1-tail.filtered_offset)
                
            except Exception as e:
                raise e
                e.die()
            
    def load_patterns_map(self):
        return self

class StringUnderProcessing(VenCString):
    def __init__(self, string, context):
        super().__init__()
        self._str = string
        self.context = context
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
            StringUnderProcessing.__set_pattern_flags(pattern)
            
    @staticmethod
    def __set_pattern_flags(pattern):
        if not pattern.name in PatternsMap.CONTEXTUALS.keys():
            pattern.flags |= PatternNode.FLAG_NON_CONTEXTUAL
            
        if pattern.name in PatternsMap.NON_PARALLELIZABLES.keys():
            pattern.flags |= PatternNode.FLAG_NON_PARALLELIZABLE
       
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
