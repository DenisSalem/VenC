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

from venc3.patterns.patterns_map import PatternsMap

class VenCString:
    def __init__(self):
        self.id = "\x00"+str(id(self))+"\x00"
        self.output = None
                  
    def __repr__(self):
        return self.id
        
    def __str__(self):
        return self._str

    @staticmethod
    def apply_offset(sub_strings, offset, o):
        for pattern in sub_strings:
            if pattern.o > o:
              pattern.o += offset
              pattern.c += offset
              VenCString.apply_offset(pattern.sub_strings, offset, -1)
              
    def flatten(self, parent=None):
        target = parent if parent else self
        for string in target.sub_strings[::-1]:
            self.flatten(string)
            output = string.output if string.output else ".:"+string.name+"::"+('::'.join(string.args))+":."
            if type(target) == PatternNode:
                o = target.output.find(string.id)
                if o > 0:
                    string.c += o - string.o
                    string.o = o
                    target.output = target.output[:string.o] + output +target.output[string.c+2:]
                
            else:
                target._str = target._str[:string.o] + output + target._str[string.c+2:]
                    
        if parent == None:
            return target.output if type(target) == PatternNode else target._str
            
class PatternNode(VenCString):
    FLAG_NONE = 0
    FLAG_NON_CONTEXTUAL = 1
    FLAG_CONTEXTUAL = 2
    FLAG_NON_PARALLELIZABLE = 4
    FLAG_WAIT_FOR_CHILDREN_TO_BE_PROCESSED = 8 # NOT IMPLEMENTED YET
    FLAG_ALL = 15
    def __init__(self, root, string, o, c):
        super().__init__()
        self._str = string[o:c+2]
        self.args = []
        self.escape_pattern = False
        self.flags = PatternNode.FLAG_NONE
        self.name = None
        self.parent_argument_index = 0
        self.sub_strings = []
        
        self.o = o
        self.c = c

class Processor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
        
    def process(self, node, flags):
        for string in node.sub_strings:
            self.process(string, flags)
            if string.flags & flags:
                string.output = self.functions[string.name](string, *string.args)
    
class StringUnderProcessing(VenCString):
    def __init__(self, string, context):
        super().__init__()
        self._str = string
        self.context = context
        self.has_non_parallelizables = False

        # This block get indexes of opening and closing patterns.
        self.op = StringUnderProcessing.__find_pattern_boundaries(string, '.:')
        self.cp = StringUnderProcessing.__find_pattern_boundaries(string, ':.')
        
        # This block sort pattern by nest order AND position in input string.
        self.sub_strings = []
        sub_strings_append = self.sub_strings.append
        op, cp, op_pop, cp_pop = self.op, self.cp, self.op.pop, self.cp.pop
        while len(op) or len(cp):
            if ((not len(op)) or (not len(cp))) and len(op) != len(cp):
                from venc3.exceptions import MalformedPatterns
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
                        
            sub_strings_append(PatternNode(self, string, op[i],cp[j]))            
            op_pop(i)
            cp_pop(j)
          
        # Make a tree
        i = 0
        sub_strings = self.sub_strings
        sub_strings_pop = sub_strings.pop
        while i < len(sub_strings):
            for pattern in sub_strings[i+1:]:
                if sub_strings[i].o > pattern.o and sub_strings[i].c < pattern.c:
                    pattern.sub_strings.append(sub_strings_pop(i))
                    i =-1
                    break
                    
            i+=1

        # - Make nested patterns indexes relatives to their parent.
        # - Set patterns name and args.
        # - Set pattern flags.
        # - Replace patterns by their unique identifier.
        self.__finalize_patterns_tree_pass_1(sub_strings)
        
        # ~ Make nested patterns indexes relatives to their parent arguments.
        self.__finalize_patterns_tree_pass_2(sub_strings)

    def __finalize_patterns_tree_pass_1(self, nodes, parent=None):
        target = parent if parent else self
        target.sub_strings = sorted(nodes, key = lambda n:n.o)
        nodes = target.sub_strings
        
        for pattern in nodes:
            self.__finalize_patterns_tree_pass_1(pattern.sub_strings, pattern) 

            if parent:
                pattern.o -= parent.o
                pattern.c -= parent.o

            target._str = target._str[:pattern.o]+pattern.id+target._str[pattern.c+2:]
            offset = len(pattern.id) - (pattern.c + 2 - pattern.o)
            pattern.c += offset
            VenCString.apply_offset(target.sub_strings, offset, pattern.o)

            l = pattern._str[2:-2].split('::')
            pattern.name, pattern.args = l[0], l[1:]
            self.__set_pattern_flags(pattern)
            
    def __finalize_patterns_tree_pass_2(self, nodes, parent=None):
        if parent:
            parent_args = parent.args
            relative_index = 0
            parent_argument_index = 0
            
        for pattern in nodes:
            self.__finalize_patterns_tree_pass_2(pattern.sub_strings, pattern)
            if parent:             
                pattern.o -= 4 + len(parent.name)
                pattern.c -= 4 + len(parent.name)
                o, c,has_iterated = pattern.o, pattern.c, False
                
                while relative_index < o:
                    has_iterated = True
                    pattern.o, pattern.c = o - relative_index, c -relative_index
                    pattern.parent_argument_index = parent_argument_index
                    relative_index += 2+len(parent_args[parent_argument_index])
                    parent_argument_index += 1
                
                if has_iterated:
                    relative_index -= 2+len(parent_args[parent_argument_index-1])
                    parent_argument_index-=1
            
    def __set_pattern_flags(self, pattern):            
        pattern_name = pattern.name
        if not pattern_name in PatternsMap.CONTEXTUALS.keys():
            pattern.flags = PatternNode.FLAG_NON_CONTEXTUAL
            
        else:
            pattern.flags = PatternNode.FLAG_CONTEXTUAL
            
        if pattern_name in PatternsMap.NON_PARALLELIZABLES:
            pattern.flags = PatternNode.FLAG_NON_PARALLELIZABLE
            self.has_non_parallelizables = True
            
        if pattern_name == "Escape":
            pattern.escape_pattern = True    
            
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
    
    def reset_index(self, new_string):
        self._str = new_string
        for sub_string in self.sub_strings:
            o = self._str.find(sub_string.id)
            sub_string.c += o - sub_string.o
            sub_string.o = o
