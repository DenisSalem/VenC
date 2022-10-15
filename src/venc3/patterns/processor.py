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

def __find_pattern_boundaries(string, symbol):
  index = 0
  boundary_type = Boundary.BONDARY_TYPE_OPENING if symbol == ".:" else Boundary.BONDARY_TYPE_CLOSING
  while '∞':
      index = string.find(symbol, index)
      if index == -1:
          break
          
      yield Boundary(index, boundary_type)
      index+=1


class Boundary:
    BONDARY_TYPE_OPENING = True
    BONDARY_TYPE_CLOSING = False
    
    def __init__(self, index, boundary_type):
        self.index = index
        self.boundary_type = boundary_type
        self.level = 0
        
    def __repr__(self):
        return ".:" if self.boundary_type == Boundary.BONDARY_TYPE_OPENING else ":."

def __get_boundaries(string):
    o = [o for o in __find_pattern_boundaries(string, ".:")]
    c = [c for c in __find_pattern_boundaries(string, ":.")]
    
    if len(o) != len(c):
        from venc3.exceptions import VenCException
        raise VenCException
    
    return sorted( 
        o + c,
        key = lambda x: x.index
    )

def __get_boundaries_block(boundaries):
    if boundaries[0].boundary_type == Boundary.BONDARY_TYPE_CLOSING:
        from venc3.exceptions import VenCException
        raise VenCException
    
    level = 0
    for i in range(0, len(boundaries)):
        if boundaries[i].boundary_type == Boundary.BONDARY_TYPE_CLOSING:
          level -= 1
          
        else:
          level += 1
          
        if level == 0:
            block = boundaries[:i+1]
            del boundaries[:i+1]
            return block

s = ".:LEVEL1:. .:LEVEL2:: .:LEVEL3:. :."*1000
for i in range(0, 1000):
    b = __get_boundaries(s)
    blocks = []
    while len(b):
        blocks.append(
            __get_boundaries_block(b)
        )
