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


from time import time

from venc3.patterns.patterns_map import PatternsMap

class Pattern:
    def __init__(self, o, c):
        self.o, self.c = o, c
        self.shield = None
        self.flags = PatternsMap.FLAG_NONE
        self.payload = None
        self.patterns = []

    def __iter__(self):
        return iter((self.o, self.c))
    
class VenCString:  
    def __init__(self, string, context=None, shield=False):     
        self._str = string
        self.context = context
        self.patterns, escape_indexes = [], []
        patterns_append, escape_indexes_append = self.patterns.append, escape_indexes.append
        pattern_identifier = 0
                
        # This block get indexes of opening and closing patterns.
        op = VenCString.__find_pattern_boundaries(string, '.:')
        cp = VenCString.__find_pattern_boundaries(string, ':.')
                
        if len(op) != len(cp):
            self.op, self.cp = op, cp
            from venc3.exceptions import MalformedPatterns
            raise MalformedPatterns(self)
        
        # Pairing
        i, op_pop, cp_pop = 0, op.pop, cp.pop
        while i < len(op):
            o, c = op[i], cp[0]
            if i < len(op)-1:
                next_o = op[i+1]
                if o < next_o < c :
                    i+=1
                    continue

            o, c = op_pop(i), cp_pop(0)
            if string[o:o+10] == ".:Escape::":    
                escape_indexes_append((o,c+2))

            patterns_append(Pattern(o, c+2))
            i = 0

        escape_indexes.sort(key=lambda p:p[0], reverse=True)
        self.patterns.sort(key=lambda p:p.o, reverse=True)
        
        # Strong bottleneck happen for pattern escaping. But we don't care since there is no real use case
        # for regular user.

        # Drop escaped ... escapes
        i = 0
        escape_indexes_pop = escape_indexes.pop
        while i < len(escape_indexes) - 1:
            eo, ec = escape_indexes[i]
            if escape_indexes[i+1][1] > ec:
                escape_indexes_pop(i)
                
            else:
                i+=1

        # Drop escaped patterns
        for eo, ec in escape_indexes:
            # Binary search
            lo, hi = 0, len(self.patterns) - 1
            while lo < hi:
                mid = lo + (hi - lo) // 2
                if self.patterns[mid].c <= eo:
                    hi = mid
                    
                else:
                    lo = mid + 1

            # updating string
            escaped = string[eo+10:ec-2].strip()
            offset = (ec - eo) - len(escaped) 
            self._str = self._str[:eo] + escaped + self._str[ec:]

            while lo >=0:
                if self.patterns[lo].o >= eo and self.patterns[lo].c <= ec:
                    self.patterns.pop(lo)
                    if lo >= len(self.patterns) -1 :
                        lo -= 1 
                    continue

                else: 
                    applied_offset = (offset if self.patterns[lo].o > ec else 0)
                    self.patterns[lo].o -= applied_offset
                    self.patterns[lo].c -= applied_offset
     
                lo -=1

        # Make a tree by chunking group of patterns
        final_set_of_patterns = []
        while len(self.patterns):
            current_patterns_block = [self.patterns.pop(0)]

            while len(self.patterns):
                if self.patterns[0].c < current_patterns_block[0].c:
                    break
                    
                current_patterns_block.append(self.patterns.pop(0))
                                
            i, old_len_patterns = 0, len(current_patterns_block)
            while i < len(current_patterns_block):
                current_patterns_block = [ pattern for pattern in current_patterns_block if VenCString.__pattern_extraction(current_patterns_block[i], pattern) ]
                if old_len_patterns == len(current_patterns_block):
                    i+=1
                  
                else:
                    old_len_patterns = len(current_patterns_block)
                    
            final_set_of_patterns += current_patterns_block
                    
        self.patterns = final_set_of_patterns
        
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
    
    @staticmethod
    def __pattern_extraction(destination, target):
        if target.o > destination.o and target.c < destination.c:
            destination.patterns.append(target)
            return False
            
        return True

class VenCProcessor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
        
from math import log10
count= 1
step = 10**(log10(count)-1)

for i in range(0,count):
    if i % step == 0:
        print(i)
        
    vs = VenCString(".:TEST:: .:DEEPER_TEST:. :. .:LEVEL1:: .:LEVEL2:: .:LEVEL3:: .:LEVEL4:. :. :: .:LEVEL3_BIS:. .:LEVEL3_BIS_LE_RETOUR:. :. :."*1, "test")


def print_tree(vs, nodes, indent=''):
    for pattern in nodes.patterns:
        print_tree(vs, pattern, indent+'\t')
        print(indent+vs._str[pattern.o:pattern.c])

print_tree(vs, vs)


# ~ print(vs._str)
# ~ print()

# ~ i = 0
# ~ for pattern in vs.patterns:
    # ~ print(i, pattern.o, pattern.c, ">"+vs._str[pattern.o:pattern.c]+"<")
    # ~ i+=1

