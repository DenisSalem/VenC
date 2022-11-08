#!   /usr/bin/env python3

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
#
#
#

#
#
#

#

#
#
##
##################
# POSTERITY      #
# MUST           #
# REMEMBER THAT  #
# I PUT A DAMN   #
# TREMENDOUS     #
# EFFORT TO      #
# OPTIMIZE THE   #
# FOLLOWING      #
# CODE BELOW     #
# SO IT CAN RUN  #
# SO FAST IT CAN #
# ACTUALY BREAK  #
# THE CAUSALITY  #
# PRINCIPLE.     #
##################
                ##
                 #
                 
                 #
                 
                 
                 #
                 
from time import time

from venc3.patterns.patterns_map import PatternsMap

class Boundary:
    BONDARY_TYPE_OPENING = 1
    BONDARY_TYPE_CLOSING = -1
    
    def __init__(self, index, boundary_type):
        self.index = index
        self.boundary_type = boundary_type
        self.level = 0
        
    def __repr__(self):
        return '.:' if self.boundary_type == Boundary.BONDARY_TYPE_OPENING else ':.'

class Pattern:
    def __init__(self, s, o, c, sub_patterns, ID):
        self.o, self.c = o, c
        self.payload = s[o+2:c-2].split('::')
        self.sub_patterns = sub_patterns
        self.ID = '\x00'+str(ID)+'\x00'

class PatternTree:
    def __init__(self, string, context=""):
        self.string = string
        self.context = context
        self.ID = 0
        self.tree = self.__build_tree(
            PatternTree.__get_boundaries(string)
        )
              
    def __find_pattern_boundaries(string, symbol):
      index = 0
      boundary_type = Boundary.BONDARY_TYPE_OPENING if symbol == '.:' else Boundary.BONDARY_TYPE_CLOSING
      while '∞':
          index = string.find(symbol, index)
          if index == -1:
              break
              
          yield Boundary(index, boundary_type)
          index+=1
          
    def __get_boundaries(string):
        o = [o for o in PatternTree.__find_pattern_boundaries(string, '.:')]
        c = [c for c in PatternTree.__find_pattern_boundaries(string, ':.')]
        
        if len(o) != len(c):
            from venc3.exceptions import VenCException
            raise VenCException
        
        return tuple(sorted( 
            o + c,
            key = lambda x: x.index
        ))
    
    def __get_boundaries_block(boundaries, start):
        if boundaries[start].boundary_type == Boundary.BONDARY_TYPE_CLOSING:
            from venc3.exceptions import VenCException
            raise VenCException
        
        level = 0
        for i in range(start, len(boundaries)):
            level += boundaries[i].boundary_type
    
            if level == 0:
                return i

    def __apply_and_compute_offset_and_inc_id(self, pattern):
        self.string = self.string[:pattern.o] + pattern.ID + self.string[pattern.c:]
        offset = len(pattern.ID) - pattern.c + pattern.o
        pattern.c = pattern.o + len(pattern.ID)
        self.ID+=1
        return offset
        
    def __build_tree(self, boundaries, start=0, limit=None, previous_end=None, offset=0):
        if not limit:
            limit = len(boundaries)

        sub_patterns = []
        sub_patterns_append = sub_patterns.append
        parent_start, parent_offset = start, offset
        while start < limit:
            end = PatternTree.__get_boundaries_block(boundaries, start)
            if end - start - 1 > 0:
                offset, pattern = self.__build_tree(boundaries, start+1, end-1, end, offset)
                sub_patterns_append(pattern)
                
            else:
                pattern = Pattern(
                    self.string,
                    boundaries[start].index+offset,
                    boundaries[end].index+2+offset,
                    [],
                    self.ID
                )
                offset += self.__apply_and_compute_offset_and_inc_id(pattern)
                sub_patterns_append(pattern)
                
            start = end+1

        if previous_end:
            pattern = Pattern(
                self.string,
                boundaries[parent_start-1].index+parent_offset,
                boundaries[previous_end].index+2+offset,
                sub_patterns,
                self.ID
            )
            offset += self.__apply_and_compute_offset_and_inc_id(pattern)
            return offset, pattern
            
        else:
            return sub_patterns

iteration = 1000
n = 100

for i in range(0,iteration):
    pattern_tree = PatternTree('.:TEST:: .:DEEPER_TEST:. :. .:Escape_:: .:Escaped:. :. .:Escape_:: .:LEVEL1:: .:LEVEL2_BIS:: .:LEVEL3:. :. .:LEVEL2:: .:LEVEL3:: .:LEVEL4:. :. :: .:LEVEL3_BIS:. .:LEVEL3_BIS_LE_RETOUR:. :. :. :.'*n)
    # ~ pattern_tree = PatternTree(b'.:LEVEL1::_.:LEVEL2:._::_.:LEVEL2_BIS::_.:LEVEL3:._:._:.'*1)
    
def print_tree(tree, indent=''):
    for e in tree:
        print(indent, e.ID, e.payload)
        print_tree(e.sub_patterns, indent+'\t')
        
# ~ print_tree(pattern_tree.tree)
# ~ print(pattern_tree.string)
