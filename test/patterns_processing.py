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

from venc2.patterns.processor import StringUnderProcessing  # The object holding the string and its states.
from venc2.patterns.processor import Processor              # The actual string processor, holding binded methods.

def test_datastructure():
    def print_tree(nodes, parent=None, indent='\t'):
        for pattern in nodes:
            print(indent, str(parent)[pattern.o:pattern.c+2], pattern, pattern.name, pattern.args)
            print_tree(pattern.sub_strings, parent=pattern, indent=indent+'\t')
            
    s = ".:FUNC1:. .:FUNC2:: .:FUNC3::ARG3_1:. :: .:FUNC4::ARG4_1::ARG4_2:. .:FUNC5::ARG5_1::ARG5_2 .:FUNC6:. :. :. .:FUNC7::ARG7_1::ARG7_2 .:FUNC8::ARG8_1::ARG8_2:. :."

    print("INPUT:", s)
    sup = StringUnderProcessing(s, "test")
    print_tree(sup.sub_strings, sup)
    print("OUTPUT:", sup)
    print()

def test_process():
    def ADD(a,b,c=0):
        return str(int(a)+int(b)+int(c))
        
    def MUL(a,b,c=1):
        return str(int(a)*int(b)*int(c))
  
    s = " Simple math: .:ADD:: .:MUL:: 2 :: 6 :. :: .:MUL::4::4:. :. !! .:MUL::3:: .:ADD::3::6:. :."
    sup = StringUnderProcessing(s, "test")
    p = Processor()
    p.set_patterns({
        "ADD": ADD,
        "MUL": MUL
    })
    print(s)
    p.process(sup, True, True)
    print(sup)

test_datastructure()
test_process()

