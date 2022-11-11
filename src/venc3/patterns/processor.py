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
                 
from time import time

from venc3.patterns.patterns_map import PatternsMap

class Boundary:
    BONDARY_TYPE_OPENING = 1
    BONDARY_TYPE_CLOSING = -1
    
    def __init__(self, index, boundary_type):
        self.index = index
        self.boundary_type = boundary_type
        self.level = 0

class Pattern:
    FLAG_NONE = 0
    FLAG_NON_CONTEXTUAL = 1
    FLAG_CONTEXTUAL = 2
    FLAG_NON_PARALLELIZABLE = 4
    FLAG_WAIT_FOR_CHILDREN_TO_BE_PROCESSED = 8 # NOT IMPLEMENTED YET
    FLAG_ALL = 15
    
    def __init__(self, s, o, c, sub_patterns, ID):
        self.o, self.c = o, c
        self.payload = s[o+2:c-2].split('::')
        self.sub_patterns = sub_patterns
        offset = o + len(self.payload[0]) + 4
        limit = offset
        i = 0
        payload_index = 1
        len_sub_patterns = len(sub_patterns)
        for item in self.payload[1:]:
            limit += len(item)
            while i < len_sub_patterns and sub_patterns[i].o < limit:
                sub_pattern = sub_patterns[i]
                sub_pattern.o -= offset
                sub_pattern.c -= offset
                sub_pattern.parent = self
                sub_pattern.payload_index = payload_index
                i+=1
                
            limit+=2
            offset = limit
            payload_index +=1
            
        self.ID = '\x00'+str(ID)+'\x00'

        pattern_name = self.payload[0]
        self.flags = Pattern.FLAG_NONE
        if pattern_name in PatternsMap.CONTEXTUALS.keys():
            self.flags = Pattern.FLAG_CONTEXTUAL
        
        for key in PatternsMap.NON_CONTEXTUALS.keys():
            if pattern_name in PatternsMap.NON_CONTEXTUALS[key].keys():
                self.flags = Pattern.FLAG_NON_CONTEXTUAL
                break
            
        if pattern_name in PatternsMap.NON_PARALLELIZABLES:
            pattern.flags |= Pattern.FLAG_NON_PARALLELIZABLE

        if not self.flags:
            from venc3.exceptions import VenCException
            raise VenCException
            
class PatternTree:
    def __init__(self, string, context=""):
        self.string = string
        self.context = context
        self.ID = 0
        self.tree = self.__build_tree(
            PatternTree.__get_boundaries(string)
        )
        for pattern in self.tree:
            pattern.parent = self
              
    def __find_pattern_boundaries(string, symbol, boundary_type):
      index = 0
      while '∞':
          index = string.find(symbol, index)
          if index == -1:
              break
              
          yield Boundary(index, boundary_type)
          index+=1
          
    def __get_boundaries(string):
        o = [o for o in PatternTree.__find_pattern_boundaries(string, '.:', Boundary.BONDARY_TYPE_OPENING)]
        c = [c for c in PatternTree.__find_pattern_boundaries(string, ':.', Boundary.BONDARY_TYPE_CLOSING)]
        
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
            
class Processor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
    
    def process(self, parent, flags):
        offset = 0
        for pattern in parent.tree:
            process(pattern.sub_patterns, flags)
            pattern_name, *args = pattern.payload
            if (pattern.flags & (flags ^ Pattern.FLAG_NON_PARALLELIZABLE)) and ((flags & Pattern.FLAG_NON_PARALLELIZABLE) or (not(pattern.flags & Pattern.FLAG_NON_PARALLELIZABLE))):
                chunk = self.functions[pattern_name](pattern, *args)
                len_chunk = len(chunk)
                if type(pattern.parent) == Pattern:
                else:
                  
