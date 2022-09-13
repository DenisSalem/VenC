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

def get_markers_indexes(string, begin=".:", end=":."):
    op, cp = [], []
    op_append, cp_append = op.append, cp.append
    string_find = string.find
    strip_begin, strip_end = [], []
    strip_begin_append, strip_end_append = strip_begin.append, strip_end.append
    i = 0
    l = len(string)
    offset=0
    begin_eq_escape = begin == ".:Escape::"
    while i < l:
        i = string_find(begin, i)
        if i == -1:
            i=0
            break
            
        if begin_eq_escape:
            j = 0
            while string[i+10+j] in [' ','\t','\n']:
                j+=1
                
            strip_begin_append(j)

        op_append(i)
        i+=2
    
    while i < l:
        i = string_find(end, i)
        if i == -1:
            i=0
            break
            
        if begin_eq_escape:
            j = 0
            while string[i-j-1] in [' ','\t','\n']:
                j+=1
            strip_end_append(j)

        cp_append(i)
            
        i+=2

    if begin_eq_escape:
        a = [ (op[i], strip_begin[i]) for i in range(0,len(op)) ]
        b = [ (cp[i], strip_end[i])   for i in range(0,len(cp)) ]
        return (a, b)
        
    return (op, cp)

def index_not_in_range(index, ranges, process_escapes):
    for o, c in ranges:
        try:
            if index >= o[0] and index <= (c[0] if process_escapes else c[0]+13):
                return False
        except TypeError:
            if index >= o and index <= (c if process_escapes else c+13):
                return False
                
    return True

class Legacy_2_0_2_VenCString():
    def __init__(self, string, ressource, process_escapes=False, meta_escapes=[]):
        self.open_pattern_pos, self.close_pattern_pos = get_markers_indexes(string)
        if len(meta_escapes):
            self.open_pattern_pos = [ v for v in self.open_pattern_pos if index_not_in_range(v, meta_escapes, False)]
            self.close_pattern_pos = [ v for v in self.close_pattern_pos if index_not_in_range(v, meta_escapes, False)]
        
        #Process escape
        self.escapes_o, self.escapes_c = get_markers_indexes(string, begin=".:Escape::", end="::EndEscape:.")
        leo, lec = len(self.escapes_o), len(self.escapes_c)

        if leo != lec:
            raise MalformedPatterns(leo > lec, True, ressource)
        
        escapes = []
        
        # Get ranges
        while len(self.escapes_o):
            if len(self.escapes_o) > 1:
                for i in range(1, len(self.escapes_o)):
                    if self.escapes_o[i][0] > self.escapes_c[i-1][0]:
                        o = self.escapes_o[0]
                        c = self.escapes_c[i-1]

                        escapes.append((o,c))
                        self.escapes_o = self.escapes_o[i:]
                        self.escapes_c = self.escapes_c[i:]
                        break
                        
                    else:
                        raise IllegalUseOfEscape(ressource)
                    
            else:
                if not len(meta_escapes) or index_not_in_range(self.escapes_o[0][0], meta_escapes, False):
                    escapes.append((
                        self.escapes_o[0],
                        self.escapes_c[0]
                    ))
                break

        if len(escapes) and process_escapes:
            # First removes open and closes indexes which
            # are actually referencing escapes indexes.
            
            # life is a bitch and sometimes escape indexes
            # aren't escaped properly
            escapes_murder_list = []
            
            for e in escapes:
                try:
                    self.open_pattern_pos.remove(e[0][0])
                    self.close_pattern_pos.remove(e[1][0]+11)
                    
                except ValueError:
                    escapes_murder_list.append(e)
            
            for victim in escapes_murder_list:
                escapes.remove(victim)
                
            # Remove Escape and EndEscapes, update indexes
            for i in range(0, len(escapes)):
                o,c = escapes[i]
                #bs and es are for begin strip and end strip
                o, bs = o
                c, es = c
                string = string[:o]+string[o+10+bs:]
                string = string[:c-10-bs-es]+string[c+3-bs:]

                # -1 to set close escape at the end of the escaped string
                escapes[i] = ((o, bs), (c-10-bs-es-1, es)) 
                
                # adjust pattern indexes
                self.open_pattern_pos = [(v-10-bs if v > o and v < c else (v-23-bs-es if v > c+13 else v)) for v in self.open_pattern_pos]
                self.close_pattern_pos = [(v-10-bs if v > o and v < c else (v-23-bs-es if v > c+13 else v)) for v in self.close_pattern_pos]
                
                escapes = escapes[:i+1]+[ ( (p[0][0]-23-bs-es, p[0][1]), (p[1][0]-23-bs-es, p[1][1])) for p in escapes[i+1:] ]
                
        # remove escaped patterns indexes
        if len(escapes):
            self.open_pattern_pos = [v for v in self.open_pattern_pos if index_not_in_range(v, escapes, process_escapes)]
            self.close_pattern_pos = [v for v in self.close_pattern_pos if index_not_in_range(v, escapes, process_escapes)]

        self.len_open_pattern_pos = len(self.open_pattern_pos)
        self.len_close_pattern_pos = len(self.close_pattern_pos)
            
        if self.len_open_pattern_pos != self.len_close_pattern_pos:
            print(string)
            print(self.len_open_pattern_pos,self.len_close_pattern_pos)
            raise MalformedPatterns(self.len_open_pattern_pos > self.len_close_pattern_pos, False, ressource)

        self.string = string
        self.ressource = ressource
        self.process_escapes = process_escapes
        self.keep_appart_from_markup_indexes = list()
        self.keep_appart_from_markup_inc = 0
        self.bop, self.bcp = [], []
        self.backup = None
            
    def restore(self):
        self.open_pattern_pos, self.close_pattern_pos, self.len_open_pattern_pos, self.len_close_pattern_pos, self.string = self.backup
        self.backup = None

    def keep_appart_from_markup_indexes_append(self, paragraphe, new_chunk):
        self.keep_appart_from_markup_indexes.append((self.keep_appart_from_markup_inc, paragraphe, new_chunk, False))
        output = "---VENC-TEMPORARY-REPLACEMENT-"+str(self.keep_appart_from_markup_inc)+'---'
        self.keep_appart_from_markup_inc +=1
        return output

    def process_markup_language(self, markup_language):
        try:
            self.string = parse_markup_language(self.string, markup_language, self.ressource)
        
        # catch error from reStructuredText
        except SystemMessage as e:
            try:
                line = int(str(e).split(':')[1])
                msg = str(e).split(':')[2].strip()
                handle_markup_language_error(self.ressource+": "+msg, line=line, string=string)

            except Exception as ee: 
                handle_markup_language_error(self.ressource+", "+str(e))
        
        self.replace_needles(in_entry=True)
        
    def replace_needles(self, in_entry=False):
        meta_escapes = []
           
        if in_entry or len(self.keep_appart_from_markup_indexes):            
            while "Missings triplet is not empty":                
                missings = []
    
                for quadruplet in self.keep_appart_from_markup_indexes:
                    identifier, paragraphe, new_chunk, ignore_patterns = quadruplet
                        
                    string = self.string
                    target = "---VENC-TEMPORARY-REPLACEMENT-"+str(identifier)+"---"
                    len_target = len(target)
                    len_new_chunk = len(new_chunk.strip())
                    try:
                        index = string.index(target)
                    
                    # In some case needle may be hidden in another needle.
                    except:
                        missings.append(quadruplet)
                        continue
                    
                    p_offset = 0
                    if paragraphe:
                        if string[index-3:index] == "<p>":
                            string = string[:index-3]+string[index:]
                            index -=3
                            p_offset -=3
    
                        if string[index+len_target:index+len_target+4] == "</p>":
                            string = string[:index+len_target]+string[index+len_target+4:]
                            p_offset -=4
    
                
                    self.string = string[:index]+new_chunk.strip().replace("\x1B\x1B","::")+string[index+len_target:]
                    
                    diff = len_new_chunk - len_target + p_offset
                    for i in range(0, len(meta_escapes)):
                        if index <= meta_escapes[i][0]:
                            meta_escapes[i] = [
                                meta_escapes[i][0]+diff,
                                meta_escapes[i][1]+diff
                            ]
                        
                    if ignore_patterns:
                        meta_escapes.append([
                            index,
                            index+len_new_chunk
                        ])
                                        
                if not len(missings):
                    break
                    
                self.keep_appart_from_markup_indexes = missings
        
        # After markup langage/needles processing done, indexes are messed up.
        # This is the last time entry content is preprocessed, so it must
        # handle escapes pattern now.
            
        self.fix_indexes(meta_escapes)
        
    def fix_indexes(self, meta_escapes=[]):
        self.__init__(self.string, self.ressource, True, meta_escapes)

vs = Legacy_2_0_2_VenCString(".:Escape:: .:TO_REMOVE::SOME_ARG:. ::EndEscape:. .:FUNC11:: .:FUNC12:. :. .:Escape:: .:TO_BE_REMOVED:. ::EndEscape:.  .:Escape:: .:TO_DROP_AS_WELL:. ::EndEscape:. .:FUNC1:: ARG1 .:EMBED::ARG2:. :. .:Escape:: .:FUNC_TO_DROP:. ::EndEscape:. "*100, "test")


for i in range(0, len(vs.open_pattern_pos)):
    o, c = vs.open_pattern_pos[i], vs.close_pattern_pos[i]
    print(i, vs.string[o:c+2])
