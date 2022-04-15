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

from venc2.patterns.processor import PatternNode
from venc2.patterns.processor import Processor              # The actual string processor, holding binded methods.
from venc2.patterns.processor import StringUnderProcessing  # The object holding the string and its states.
from venc2.prompt import die
from venc2.prompt import notify

def test_datastructure(verbose=False):  
    ref = [ "FUNC"+str(i) for i in range(1,9) ]
    def print_tree(nodes, parent=None, indent='\t'):
        output = []
        for pattern in nodes:
            if verbose:
                print(indent, str(parent)[pattern.o:pattern.c+2], pattern, pattern.name, pattern.args)
            if str(parent)[pattern.o:pattern.c+2] != "\x00"+str(id(pattern))+"\x00":
                die("test_datastructure: identifier mismatch with extracted identifier string from parent.")
            output += [pattern.name] + print_tree(pattern.sub_strings, parent=pattern, indent=indent+'\t')
            
        return output
    s = ".:FUNC1:. .:FUNC2:: .:FUNC3::ARG3_1:. :: .:FUNC4::ARG4_1::ARG4_2:. .:FUNC5::ARG5_1::ARG5_2 .:FUNC6:. :. :. .:FUNC7::ARG7_1::ARG7_2 .:FUNC8::ARG8_1::ARG8_2:. :."

    sup = StringUnderProcessing(s, "test_datastructure")
    if ref != print_tree(sup.sub_strings, sup):
        die("test_datastructure: patterns aren't sorted.")
        
    if verbose:
        print("OUTPUT:", sup)

def test_full_process(verbose=False):
    def ADD(node, a,b,c=0):
        return str(int(a)+int(b)+int(c))
        
    def MUL(node, a,b,c=1):
        return str(int(a)*int(b)*int(c))
  
    s = "Simple math: .:ADD:: .:MUL:: 2 :: 6 :. :: .:MUL::4::4:. :. .:MUL::3:: .:ADD::3::6:. :."
    sup = StringUnderProcessing(s, "test_full_process")
    p = Processor()
    p.set_patterns({
        "ADD": ADD,
        "MUL": MUL
    })
    
    if verbose:
        print(s)
    
    p.process(sup, True, False)
    
    if verbose:
        print(sup)
        
    if str(sup) != "Simple math: 28 27":
        die("test_full_process: expected string mismatch with output")

def test_filter_process(verbose=False):
    def CAPITALIZE(node, a):
        return a.upper()
    
    def IF_SOMETHING(node, a,b):
        return a.strip()
        
    s = ".:IF_SOMETHING::As Above::So Below:. .:CAPITALIZE::[ bla .:IF_SOMETHING:: .:IF_SOMETHING::lololol::moo foo bar:. :: moo foo bar:. bla]:. .:IF_SOMETHING::True::False:."
    sup = StringUnderProcessing(s, "test_filter_process")
    sup.sub_strings[0].flags ^= PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[1].sub_strings[0].flags ^= PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[1].sub_strings[0].sub_strings[0].flags ^= PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[2].flags ^= PatternNode.FLAG_NON_CONTEXTUAL

    p = Processor()
    p.set_patterns({
        "CAPITALIZE":   CAPITALIZE,
        "IF_SOMETHING": IF_SOMETHING
    })
    p.process(sup, True, False)
    if verbose:
        for pattern in sup.sub_strings:
            print(str(sup)[pattern.o:pattern.c+2], pattern.id)
            if pattern.id != str(sup)[pattern.o:pattern.c+2]:
                die("test_filter_process: expected string mismatch with output")
        print(sup)
    p.process(sup, False, False)
    if verbose:
        print(sup)
        
    if str(sup) != "As Above [ BLA lololol BLA] True":
        die("test_filter_process: expected string mismatch with output")

test_datastructure()
test_full_process()
test_filter_process(True)
