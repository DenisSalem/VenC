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

from venc3.patterns.processor import PatternNode
from venc3.patterns.processor import Processor              # The actual string processor, holding binded methods.
from venc3.patterns.processor import StringUnderProcessing  # The object holding the string and its states.
from venc3.prompt import die
from venc3.prompt import notify



def test_datastructure(verbose=False):  
    ref = [ "FUNC"+str(i) for i in range(1,9) ]
    def print_tree(nodes, parent, indent='\t'):
        output = []
        for pattern in nodes:                
            if type(parent) == PatternNode:
                if verbose:
                    print(indent, parent.args[pattern.parent_argument_index][pattern.o:pattern.c+2], pattern, pattern.name, pattern.args)
                if parent.args[pattern.parent_argument_index][pattern.o:pattern.c+2] != "\x00"+str(id(pattern))+"\x00":
                    die("test_datastructure: identifier mismatch with extracted identifier string from parent.")
            else:
                if verbose:
                    print(indent, parent._str[pattern.o:pattern.c+2], pattern, pattern.name, pattern.args)              
                if parent._str[pattern.o:pattern.c+2] != "\x00"+str(id(pattern))+"\x00":
                    die("test_datastructure: identifier mismatch with extracted identifier string from parent.")
            output += [pattern.name] + print_tree(pattern.sub_strings, pattern, indent=indent+'\t')
            
        return output
    s = ".:FUNC1:. .:FUNC2:: .:FUNC3::ARG3_1:. :: .:FUNC4::ARG4_1::ARG4_2:. .:FUNC5::ARG5_1::ARG5_2 .:FUNC6:. :. :. .:FUNC7::ARG7_1::ARG7_2 .:FUNC8::ARG8_1::ARG8_2:. :."

    sup = StringUnderProcessing(s, "test_datastructure")
    if ref != print_tree(sup.sub_strings, sup):
        die("test_datastructure: patterns aren't sorted.")
        
    if verbose:
        print("OUTPUT:", sup)

def test_process_no_flatten(verbose=False):
    def GET_SOME_DATA(node, a,b,c=0):
        return "some_data({0},{1},{2})".format(a,b,c)
        
    def GET_ANOTHER_KIND_OF_DATA(node, a,b,c=1):
        return "another_kind_of_data({0},{1},{2})".format(a,b,c)

    s = ".:GET_SOME_DATA::moo::foo:. .:GET_SOME_DATA::bar::foo::moo:. .:GET_ANOTHER_KIND_OF_DATA::zbim:: .:GET_SOME_DATA::zbam::zboom:. :."
    sup = StringUnderProcessing(s, "test_full_process")

    p = Processor()
    p.set_patterns({
        "GET_SOME_DATA": GET_SOME_DATA,
        "GET_ANOTHER_KIND_OF_DATA": GET_ANOTHER_KIND_OF_DATA
    })
    
    if verbose:
        print(s)
    
    p.process(sup, PatternNode.FLAG_ALL)
    
    if verbose:
        print(sup)
        
    ref = ' '.join([string.id for string in sup.sub_strings])
    if str(sup) != ref:
        die("test_process_no_flatten: expected root string mismatch with output")

    if verbose:
        print("\t",sup.sub_strings[2].id, sup.sub_strings[2].output)
        
    ref = "another_kind_of_data(zbim, {0} ,1)".format(sup.sub_strings[2].sub_strings[0].id)
    if sup.sub_strings[2].output != ref:
        die("test_process_no_flatten: expected sub string mismatch with output")
        
    return sup

def test_process_flatten(sup, verbose=False):
    if "some_data(moo,foo,0) some_data(bar,foo,moo) another_kind_of_data(zbim, some_data(zbam,zboom,0) ,1)" != sup.flatten():
        die("test_process_flatten: expected string mismatch with output")
    
test_datastructure()
sup = test_process_no_flatten()
test_process_flatten(sup)

notify("Test passed")
