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
    FLAG_ENTRY_RELATED = 2
    FLAG_CONTEXTUAL = 4
    FLAG_NON_PARALLELIZABLE = 8
    FLAG_WAIT_FOR_CHILDREN_TO_BE_PROCESSED = 16 # NOT IMPLEMENTED YET
    FLAG_ALL = 31
    
    def __init__(self, s, o, c, sub_patterns, root):
        self.ID = '\x00'+str(id(self))+'\x00'
        self.o, self.c = o, c
        self.root = root
        self.payload = s[o+2:c-2].split('::')
        self.payload_index = 0
        self.sub_patterns = sub_patterns
        offset = o + len(self.payload[0]) + 4
        limit = offset
        i = 0
        payload_index = 1
        len_sub_patterns = len(sub_patterns)
        
        # Is there an embed sub_pattern in
        if len(sub_patterns) and sub_patterns[0].o > o and sub_patterns[0].c < offset:
            from venc3.exceptions import VenCException
            raise VenCException(("this_pattern_is_embed_in_the_name_of_another_one", sub_patterns[0].payload[0]), sub_patterns[0])
        
        for arg in self.payload[1:]:
            limit += len(arg)
            while i < len_sub_patterns and sub_patterns[i].o < limit:
                sub_pattern = sub_patterns[i]
                sub_pattern.o -= offset
                sub_pattern.c -= offset
                sub_pattern.parent = self
                sub_pattern.payload_index += payload_index
                i+=1
                
            limit+=2
            offset = limit
            payload_index +=1
            
        pattern_name = self.payload[0]
        
        if pattern_name == "GetEntryContent":
            root.match_get_entry_content = True
            
        if pattern_name == "GetEntryPreview":
            root.match_get_entry_preview = True
        
        if pattern_name == "PreviewIfInThreadElseContent":
            root.match_get_entry_content = True
            root.match_get_entry_preview = True

        self.name_id = id(pattern_name)

        self.flags = Pattern.FLAG_NONE
        
        if pattern_name in PatternsMap.CONTEXTUALS.keys():
            self.flags = Pattern.FLAG_CONTEXTUAL
        
        for key in PatternsMap.NON_CONTEXTUALS.keys():
            if key != "entries" and pattern_name in PatternsMap.NON_CONTEXTUALS[key].keys():
                self.flags = Pattern.FLAG_NON_CONTEXTUAL
                break

        if pattern_name in PatternsMap.NON_CONTEXTUALS["entries"]:
            self.flags = Pattern.FLAG_ENTRY_RELATED
            
        if pattern_name in PatternsMap.NON_PARALLELIZABLES.keys():
            self.flags |= Pattern.FLAG_NON_PARALLELIZABLE

        if not self.flags:
            root.unknown_patterns.append(self)
            
class PatternTree:
    def __init__(self, string, context="", has_markup_language=False):
        self.has_markup_language = has_markup_language
        self.string = string
        self.context = context
        self.unknown_patterns = []
        self.has_non_parallelizables = False
        self.match_get_entry_content = False
        self.match_get_entry_preview = False
        self.sub_patterns = self.__build_tree(
            self.__get_boundaries(string)
        )
        
        for pattern in self.sub_patterns:
            pattern.parent = self
            pattern.payload_index = 0

        for pattern in self.unknown_patterns:
            if type(pattern.parent) == PatternTree or pattern.parent.payload[0] != "Escape":
                from venc3.exceptions import UnknownPattern
                raise UnknownPattern(pattern, self)
              
    def __find_pattern_boundaries(string, symbol, boundary_type):
      index = 0
      while '∞':
          index = string.find(symbol, index)
          if index == -1:
              break
              
          yield Boundary(index, boundary_type)
          index+=1
          
    def __get_boundaries(self, string):
        o = [o for o in PatternTree.__find_pattern_boundaries(string, '.:', Boundary.BONDARY_TYPE_OPENING)]
        c = [c for c in PatternTree.__find_pattern_boundaries(string, ':.', Boundary.BONDARY_TYPE_CLOSING)]
        
        if len(o) != len(c):
            from venc3.exceptions import MalformedPatterns
            raise MalformedPatterns(self, o, c)
        
        return tuple(sorted( 
            o + c,
            key = lambda x: x.index
        ))
    
    def __get_boundaries_block(self, boundaries, start, offset):
        if boundaries[start].boundary_type == Boundary.BONDARY_TYPE_CLOSING:
            from venc3.exceptions import VenCSyntaxError
            raise VenCSyntaxError(self, boundaries[start].index+offset, boundaries[start].index+2+offset)
        
        level = 0
        for i in range(start, len(boundaries)):
            level += boundaries[i].boundary_type
    
            if level == 0:
                return i

    def __apply_and_compute_offset_and_check_parallelizable(self, pattern):
        self.has_non_parallelizables |= pattern.flags & Pattern.FLAG_NON_PARALLELIZABLE
        self.string = self.string[:pattern.o] + pattern.ID + self.string[pattern.c:]
        offset = len(pattern.ID) - pattern.c + pattern.o
        pattern.c = pattern.o + len(pattern.ID)
        return offset
        
    def __build_tree(self, boundaries, start=0, limit=None, previous_end=None, offset=0):
        if not limit:
            limit = len(boundaries)

        sub_patterns = []
        sub_patterns_append = sub_patterns.append
        parent_start, parent_offset = start, offset
        while start < limit:
            end = self.__get_boundaries_block(boundaries, start, offset)
            if end - start - 1 > 0:
                offset, pattern = self.__build_tree(boundaries, start+1, end-1, end, offset)
                sub_patterns_append(pattern)
                
            else:
                pattern = Pattern(
                    self.string,
                    boundaries[start].index+offset,
                    boundaries[end].index+2+offset,
                    [],
                    self
                )                    
                offset += self.__apply_and_compute_offset_and_check_parallelizable(pattern)
                sub_patterns_append(pattern)
                
            start = end+1

        if previous_end:
            pattern = Pattern(
                self.string,
                boundaries[parent_start-1].index+parent_offset,
                boundaries[previous_end].index+2+offset,
                sub_patterns,
                self
            )
            offset += self.__apply_and_compute_offset_and_check_parallelizable(pattern)
            return offset, pattern
            
        else:
            return sub_patterns
            
    def reset_index(self, new_string):
        self.string = new_string
        for sub_pattern in self.sub_patterns:
            o = self.string.find(sub_pattern.ID)
            sub_pattern.c += o - sub_pattern.o
            sub_pattern.o = o
            
        # markup syntax might also change order of patterns in string
        # so it has to be reordered.
        self.sub_patterns = sorted(self.sub_patterns, key = lambda x: x.o)
        
    def match_pattern_flags(self, flag, sub_patterns=None):
        nodes = self.sub_patterns if sub_patterns == None else sub_patterns
        pattern_names = []
        for pattern in nodes:
            if flag & pattern.flags:
                pattern_names.append(pattern)
            pattern_names += self.match_pattern_flags(flag, sub_patterns=pattern.sub_patterns)
        return pattern_names

class Processor:
    def __init__(self):
        self.functions = {}
        self.set_patterns = self.functions.update
    
    def apply_pattern(self, parent, pattern, flags, payload_offset, recursion_error_triggered_by):
        if recursion_error_triggered_by == pattern.name_id:
            from venc3.exceptions import VenCException
            raise VenCException(("pattern_recursion_error", pattern.payload[0]), pattern)
            
        if pattern.payload[0] != "Escape":
            self.process(pattern, flags, recursion_error_triggered_by)
            
        pattern_name, *args = pattern.payload
        if (pattern.flags & (flags ^ Pattern.FLAG_NON_PARALLELIZABLE)) and ((flags & Pattern.FLAG_NON_PARALLELIZABLE) or (not(pattern.flags & Pattern.FLAG_NON_PARALLELIZABLE))):
            try:
                chunk = self.functions[pattern_name](pattern, *args)
                
            except TypeError as e:
                from venc3.exceptions import WrongPatternArgumentsNumber
                raise WrongPatternArgumentsNumber(pattern, pattern.root, self.functions[pattern_name], args)
            
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
                    
    def process(self, parent, flags, recursion_error_triggered_by=None):
        payload_offset = [
            0, # offset
            1 # payload_index
        ]
        parent_sub_patterns_filtered = []
        parent_sub_patterns, parent_sub_patterns_filtered_append = parent.sub_patterns, parent_sub_patterns_filtered.append
        i = 0
        while i < len(parent_sub_patterns):
            pattern = parent_sub_patterns[i]
            applied, leftovers = self.apply_pattern(parent, pattern, flags, payload_offset, recursion_error_triggered_by)
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
