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

class PatternNode:
    def __init__(self, string, o, c):
        self.o = o
        self.c = c
        self.__str = string[o:c+2]
        # ~ self.non_parallelizable =
        # ~ self.non_contextual =
        self.childs = []
        
    def __str__(self):
        return self.__str
        
class ProcessorContext:
    def __init__(self):
        self.functions = {}

class StringUnderProcessing:
    def __init__(self, string, context):
        self.string = string
        self.context = context

        # This block get indexes of opening and closing patterns.
        self.op = StringUnderProcessing.__find_pattern_boundaries(string, '.:')
        self.cp = StringUnderProcessing.__find_pattern_boundaries(string, ':.')
        
        # This block sort pattern by nest order AND position in input string.
        self.pattern_nodes = []
        pattern_nodes_append = self.pattern_nodes.append
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
                        
            pattern_nodes_append(PatternNode(string, op[i],cp[j]))            
            op_pop(i)
            cp_pop(j)
          
        # Make a tree
        i = 0
        pattern_nodes = self.pattern_nodes
        while i < len(pattern_nodes):
            for pattern in pattern_nodes[i+1:]:
                if pattern_nodes[i].o > pattern.o and pattern_nodes[i].c < pattern.c:
                    pattern.childs.append( pattern_nodes.pop(i) )
                    i =-1
                    break
                    
            i+=1
            
        # Make nested patterns indexes relatives to upper pattern and replace 
        StringUnderProcessing.__finalize_patterns_tree(pattern_nodes)
                
    
    @staticmethod
    def __finalize_patterns_tree(nodes, parent=None):
        for pattern in nodes:
            StringUnderProcessing.__finalize_patterns_tree(pattern.childs, pattern)
            if parent != None:
                pattern.o = pattern.o - parent.o
                pattern.c = pattern.c - parent.o
                
        if parent != None:
            parent.childs = sorted(nodes, key = n:n.o)
    
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
          
    def __str__(self):
        return self.string
        
    def __repr__(self):
        return "\x00"+str(id(self))+"\x00"       
