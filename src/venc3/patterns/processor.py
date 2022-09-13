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
            o, c = op[i], cp[i]
            if i < len(op)-1:
                next_o = op[i+1]
                if o < next_o < c :
                    i+=1
                    continue

            o, c = op_pop(i), cp_pop(0)
            if string[o:o+10] == ".:Escape::":    
                escape_indexes_append((o,c+2))

            patterns_append((o, c+2))
            i = 0

        escape_indexes.sort(key=lambda p:p[0], reverse=True)
        self.patterns.sort(key=lambda p:p[0], reverse=True)

        # ~ # Drop escaped ... escapes
        i = 0
        escape_indexes_pop = escape_indexes.pop
        while i < len(escape_indexes) - 1:
            eo, ec = escape_indexes[i]

            if escape_indexes[i+1][1] > ec:
                escape_indexes_pop(i)
                
            else:
                i+=1

        # ~ # Drop escaped patterns
        for eo, ec in escape_indexes:
            # ~ # Binary search
            lo, hi = 0, len(self.patterns) - 1
            while lo < hi:
                mid = lo + (hi - lo) // 2
                if self.patterns[mid][1] <= eo:
                    hi = mid
                    
                else:
                    lo = mid + 1

            # updating string
            escaped = string[eo+10:ec-2].strip()
            offset = (ec - eo) - len(escaped) 
            self._str = self._str[:eo] + escaped + self._str[ec:]

            while lo >=0:
                if self.patterns[lo][0] >= eo and self.patterns[lo][1] <= ec:
                    self.patterns.pop(lo)
                    if lo >= len(self.patterns) -1 :
                        lo -= 1 
                    continue

                else: 
                    o, c = self.patterns[lo]
                    applied_offset = (offset if o > ec else 0)
                    self.patterns[lo] = (
                        o - applied_offset,
                        c - applied_offset,
                    )
                    
                lo -=1

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

class VenCProcessor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update                

vs = VenCString(".:Escape:: :. .:Escape:: .:Escape:: .:DROPED:. :. :. .:Escape:: .:PATTERN1:. :. .:PATTERN2:: .:PATTERN3:. :. .:Escape:: .:PATTERN4:. :."*1000, "test")

i = 0
# ~ print(vs._str)
# ~ print()

for pattern in vs.patterns:
    print(i, pattern[0], pattern[1], ">"+vs._str[pattern[0]:pattern[1]]+"<")
    i+=1
