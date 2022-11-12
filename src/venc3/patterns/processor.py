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
        self.sub_patterns = self.__build_tree(
            PatternTree.__get_boundaries(string)
        )
        for pattern in self.sub_patterns:
            pattern.parent = self
            pattern.payload_index = 0
              
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
    
    def apply_pattern(self, parent, pattern, flags, payload_offset):
        self.process(pattern, flags)
        pattern_name, *args = pattern.payload
        if (pattern.flags & (flags ^ Pattern.FLAG_NON_PARALLELIZABLE)) and ((flags & Pattern.FLAG_NON_PARALLELIZABLE) or (not(pattern.flags & Pattern.FLAG_NON_PARALLELIZABLE))):
            chunk = self.functions[pattern_name](pattern, *args)
            len_chunk = len(chunk)
            if type(parent) == Pattern:
                if payload_offset[1] != pattern.payload_index:
                    payload_offset[0] = 0
                    payload_offset[1] = pattern.payload_index
                    
                ss = parent.payload[pattern.payload_index]
                parent.payload[pattern.payload_index] = ss[:pattern.o + payload_offset[0]] + chunk + ss[pattern.c+payload_offset[0]:]
                payload_offset[0] += len_chunk - pattern.c + pattern.o
                    
            else:
                ss = parent.string          
                parent.string = ss[:pattern.o + payload_offset[0]] + chunk + ss[pattern.c + payload_offset[0]:]
                payload_offset[0] += len_chunk - pattern.c + pattern.o
                
            return (True, pattern.sub_patterns)
        else:
            pattern.o += payload_offset[0]
            pattern.c += payload_offset[0]  
            return (False, pattern.sub_patterns)
                    
    def process(self, parent, flags):
        payload_offset = [
            0, # offset
            1 # payload_index
        ]
        parent_sub_patterns_filtered = []
        parent_sub_patterns, parent_sub_patterns_filtered_append = parent.sub_patterns, parent_sub_patterns_filtered.append
        i = 0
        while i < len(parent_sub_patterns):
            pattern = parent_sub_patterns[i]
            applied, leftovers = self.apply_pattern(parent, pattern, flags, payload_offset)
            if not applied:
                parent_sub_patterns_filtered_append(pattern)
                
            if len(leftovers):
                
                parent_payload = parent.payload[pattern.payload_index] if type(parent) == Pattern else parent.string
                for leftover in leftovers:
                    o = parent_payload.find(leftover.ID)
                    if o > 0:
                        leftover.c = o + leftover.c - leftover.o
                        leftover.o = o
                        leftover.payload_index = pattern.payload_index
                        parent_sub_patterns_filtered_append(leftover)
                    
            i+=1
        parent.sub_patterns = parent_sub_patterns_filtered

def DUMMY_1(node):
    return "entry_name"

def DUMMY_2(node, arg1, arg2):
    return "-=["+arg1.upper()+"]=- -=["+arg2[::-1].upper()+"]=-"

def DUMMY_3(node, arg1, arg2, arg3):
    return "((("+arg1+"//"+arg2+"//"+arg3+")))"

def DUMMY_CONTEXTUAL(node, arg1, arg2):
    return "++"+arg1+"**"+arg2+"++"

pt = PatternTree(".:GetEntryTitle:. .:GetEntryMetadataIfExists:: .:GetEntryTitle:. :: .:GetEntryTitle:. :. .:GetEntryMetadataIfNotNull:: .:IfInEntryID:: moo :: .:GetEntryTitle:. :. :: .:GetEntryTitle:. :: .:GetEntryMetadataIfExists:: .:GetEntryTitle:. :: .:GetEntryTitle:. :. :. .:GetEntryTitle:.")

p = Processor()
p.set_patterns({
    "GetEntryTitle" : DUMMY_1,
    "GetEntryMetadataIfExists" : DUMMY_2,
    "GetEntryMetadataIfNotNull" : DUMMY_3,
    "IfInEntryID" : DUMMY_CONTEXTUAL
})

p.process(pt, Pattern.FLAG_NON_CONTEXTUAL)
print(pt.string)

p.process(pt, Pattern.FLAG_CONTEXTUAL)
print(pt.string)
