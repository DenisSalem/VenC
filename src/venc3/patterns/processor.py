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

class Pattern:
    def __init__(self, vs, o, c):
        self.vs = vs
        self.o  = o
        self.c  = c

class VenCString:
    def __init__(self, string, context=None):
        self._str = string
        self.context = context
        self.shield = False
        self.patterns = []
        escape_indexes = []
        # This block get indexes of opening and closing patterns.
        op = VenCString.__find_pattern_boundaries(string, '.:')
        cp = VenCString.__find_pattern_boundaries(string, ':.')
        
        # This block sort pattern by nest order AND position in input string.
        patterns_append, escape_indexes_append = self.patterns.append, escape_indexes.append
        op_pop, cp_pop = op.pop, cp.pop
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
            
            if string[op[i]:op[i]+10] == ".:Escape::":    
                escape_indexes_append((op[i],cp[j]+2))
                
            patterns_append(Pattern(self, op[i], cp[j]+2))
            op_pop(i)
            cp_pop(j)
                
        escape_indexes = sorted(escape_indexes, key=lambda p:p[0], reverse=True)
        self.patterns =  sorted(self.patterns,  key=lambda p:p.o, reverse=True)

        # Drop escaped patterns
        for eo, ec in escape_indexes:
            for i in range(0, len(self.patterns)):
                o, c = self.patterns[i].o, self.patterns[i].c
                if eo == o and ec == c:
                    # updating string
                    escaped = string[eo+10:ec].strip()
                    offset = 12 + len(escaped) - (ec - eo - 10)
                    self._str = string[:eo] + escaped + string[ec:]
                    j = 0
                    # drop patterns and update higher indexes
                    while j < len(self.patterns):
                        if self.patterns[j].o >= eo and self.patterns[j].c <= ec:
                            self.patterns.pop(j)
                            continue
                        
                        elif self.patterns[j].o > ec:
                            self.patterns[j].o -= offset
                            self.patterns[j].c -= offset
                        
                        j+=1
                  
                    break
        
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
        return self._str

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self._str.__getitem__(key)
              
        return self._str[key]
        
vs = VenCString(" bla bla blab .:FUNC1:: moo :: foo :: bar :. bla bla bla .:Escape:: .:FUNC2:: zbim :: zbam :: .:FUNC3::zboom:. :. :. .:FUNC4:: BEWARE :: .:FUNC5:: THIS ONE IS TRICKY .:FUNC6::EVEN MORE DEEPER:. :. :.", "test")
print(vs)
for pattern in vs.patterns:
    print(vs[pattern.o:pattern.c])
