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
    def __init__(self, string, context=None):
        self._str = string
        self.context = context
        self.patterns, escape_indexes = [], []
        pattern_identifier = 0
        
        # This block get indexes of opening and closing patterns.
        op = VenCString.__find_pattern_boundaries(string, '.:')
        cp = VenCString.__find_pattern_boundaries(string, ':.')
        
        print("sort pattern by nest order AND position in input string.")

        # This block sort pattern by nest order AND position in input string.
        patterns_append, escape_indexes_append = self.patterns.append, escape_indexes.append
        op_pop, cp_pop = op.pop, cp.pop
        while len(op) or len(cp):
            if ((not len(op)) or (not len(cp))) and len(op) != len(cp):
                from venc3.exceptions import MalformedPatterns
                self.op, self.cp = op, cp
                raise MalformedPatterns(self)
                
            i, j, diff= 0, 0, 18446744073709551616
            for io in range(0, len(op)):
                for ic in range(0, len(cp)):
                    d = cp[ic] - op[io]
                    if d > 0 and d < diff:
                        diff = d
                        i = io
                        j = ic
                            
            if string[op[i]:op[i]+10] == ".:Escape::":    
                escape_indexes_append((op[i], cp[j]+2))
            
            else:    
                patterns_append((op[i], cp[j]+2, "\x00"+str(pattern_identifier)+"\x00" ))

            pattern_identifier += 1
            op_pop(i), cp_pop(j)
        
        print("DONE")
        print("SORT BY O")
        escape_indexes = sorted(escape_indexes, key=lambda p:p[0], reverse=True)
        self.patterns =  sorted(self.patterns, key=lambda p:p[0], reverse=True)
        print("DONE")
        # Drop escaped ... escapes
        # ~ i = 0
        # ~ while i < len(escape_indexes) - 1:
            # ~ eo, ec = escape_indexes[i]
            # ~ if escape_indexes[i+1][1] > ec:
                # ~ escape_indexes.pop(i+1)
            # ~ else:
              # ~ i+=1

        # ~ # Drop escaped patterns
        # ~ for eo, ec in escape_indexes:
            # ~ # Binary search
            # ~ lo, hi = 0, len(self.patterns) - 1
            # ~ while lo < hi:
                # ~ mid = lo + (hi - lo) // 2
                # ~ if self.patterns[mid][1] <= eo:
                    # ~ hi = mid
                    
                # ~ else:
                    # ~ lo = mid + 1
                                        
            # ~ # updating string
            # ~ escaped = string[eo+10:ec-2].strip()
            # ~ offset = (ec - eo) - len(escaped) 
            # ~ self._str = self._str[:eo] + escaped + self._str[ec:]
            
            # ~ while lo >=0:
                # ~ if self.patterns[lo][0] > eo and self.patterns[lo][1] < ec:
                    # ~ p = self.patterns.pop(lo)
                    # ~ # when you pop the highest item index lo must updated
                    # ~ lo -= 1 if lo >= len(self.patterns) -1 else 0 
                    # ~ continue
                    
                # ~ else:
                    # ~ o, c, identifier = self.patterns[lo]
                    # ~ applied_offset = (offset if o > ec else 0)
                    # ~ self.patterns[lo] = (
                        # ~ o - applied_offset,
                        # ~ c - applied_offset,
                        # ~ identifier
                    # ~ )
                # ~ lo -=1
                
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

class VenCProcessor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update                

vs = VenCString(".:Escape:: .:TO_REMOVE::SOME_ARG:. :. .:FUNC11:: .:FUNC12:. :. .:Escape:: .:Escape:: .:TO_BE_REMOVED:. :. :.  .:Escape:: .:TO_DROP_AS_WELL:. :. .:FUNC1:: ARG1 .:EMBED::ARG2:. :. .:Escape:: .:FUNC_TO_DROP:. :. "*1000, "test")

print(vs)

i = 0
for pattern in vs.patterns:
    print(i, pattern[0], pattern[1], vs[pattern[0]:pattern[1]])
    i+=1
