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
    
    p.process(sup, PatternNode.FLAG_ALL)
    
    if verbose:
        print(sup)
        
    if str(sup) != "Simple math: 28 27":
        die("test_full_process: expected string mismatch with output")

def test_filter_process_1(verbose=False):
    def CAPITALIZE(node, a):
        return a.upper()
    
    def IF_SOMETHING(node, a,b):
        return a.strip()
        
    s = ".:IF_SOMETHING::As Above::So Below:. .:CAPITALIZE::[ bla .:IF_SOMETHING:: .:IF_SOMETHING::lololol::moo foo bar:. :: moo foo bar:. bla]:. .:IF_SOMETHING::True::False:."
    sup = StringUnderProcessing(s, "test_filter_process")
    sup.sub_strings[0].flags = PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[1].sub_strings[0].flags = PatternNode.FLAG_CONTEXTUAL # if .:IF_SOMETHING:: .:IF_SOMETHING::lololol::moo foo bar:. :: moo foo bar:. 
    sup.sub_strings[1].sub_strings[0].sub_strings[0].flags = PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[2].flags = PatternNode.FLAG_NON_CONTEXTUAL

    p = Processor()
    p.set_patterns({
        "CAPITALIZE":   CAPITALIZE,
        "IF_SOMETHING": IF_SOMETHING
    })
    p.process(sup, PatternNode.FLAG_NON_CONTEXTUAL)
    if verbose:
        for pattern in sup.sub_strings:
            print(str(sup)[pattern.o:pattern.c+2], pattern.id)
            if pattern.id != str(sup)[pattern.o:pattern.c+2]:
                die("test_filter_process_1, first pass: expected string mismatch with output")
        print(sup)
        
    p.process(sup, PatternNode.FLAG_CONTEXTUAL)
    if verbose:
        print(sup)
        
    if str(sup) != "As Above [ BLA lololol BLA] True":
        die("test_filter_process_1, second pass: expected string mismatch with output")

def test_escape(verbose=False):    
    s = ".:Escape:: .:BullshitPattern::Bullshit args:. :. .:Escape:: .:Escape:: .:BullshitPattern::Bullshit args:. :. ::EndEscape:."
    sup = StringUnderProcessing(s, "test_escape")
    if verbose:
      print(s)
      print(sup)
    p = Processor()
    from venc3.patterns.non_contextual import escape
    p.set_patterns({
        "Escape": escape
    })


    p.process(sup, PatternNode.FLAG_NON_CONTEXTUAL)
    if verbose:
      print(str(sup))
          
    if str(sup) != " .:BullshitPattern::Bullshit args:.   .:Escape:: .:BullshitPattern::Bullshit args:. :. ::EndEscape":
        die("test_escape: expected string mismatch with output")    

def test_filter_process_2():
    def NON_CONTEXTUAL_1(node):
        return "non_contextual_1"
        
    def NON_CONTEXTUAL_2(node, arg):
        return 'non_contextual_2('+arg+')'
        
    def NON_CONTEXTUAL_3(node):
        return "non_contextual_3"
        
    def CONTEXTUAL_1(node,arg):
        return 'contextual_1('+arg+')'
        
    s = ".:NON_CONTEXTUAL_1:. .:NON_CONTEXTUAL_2:: .:CONTEXTUAL_1:: .:NON_CONTEXTUAL_3:. :. :."
    sup = StringUnderProcessing(s, "test_pass1_pass2")
    
    sup.sub_strings[0].flags = PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[1].flags = PatternNode.FLAG_NON_CONTEXTUAL
    sup.sub_strings[1].sub_strings[0].flags = PatternNode.FLAG_CONTEXTUAL
    sup.sub_strings[1].sub_strings[0].sub_strings[0].flags = PatternNode.FLAG_NON_CONTEXTUAL
    
    p = Processor()
    p.set_patterns({
        "NON_CONTEXTUAL_1" : NON_CONTEXTUAL_1,
        "NON_CONTEXTUAL_2" : NON_CONTEXTUAL_2,
        "NON_CONTEXTUAL_3" : NON_CONTEXTUAL_3,
        "CONTEXTUAL_1" : CONTEXTUAL_1,
    })
    p.process(sup, PatternNode.FLAG_NON_CONTEXTUAL)
    p.process(sup, PatternNode.FLAG_CONTEXTUAL)
    if str(sup) != "non_contextual_1 non_contextual_2( contextual_1( non_contextual_3 ) )":
        die("test_filter_process_2: expected string mismatch with output")

def test_sub_patterns_reintegration_pass_1():
    s = ".:SetStyle:: :: :: .:GetRelativeOrigin:. :. .:SetStyle:: :: :: .:GetRelativeOrigin:. :. .:SetStyle:: :: :: .:GetRelativeOrigin:. :."
    from venc3.patterns.non_contextual import set_style
    sup = StringUnderProcessing(s, "test_sub_patterns_reintegration")
    p = Processor()
    p.set_patterns({"SetStyle": set_style})
    p.process(sup, PatternNode.FLAG_NON_CONTEXTUAL)
    ref = []
    for sub_string in sup.sub_strings:
        if sub_string.name != "GetRelativeOrigin":
            die("test_sub_patterns_reintegration: reintegrated sub pattern doesn't match.")

        ref.append("<span id=\"\" class=\"\">"+sub_string.id+"</span>")
        
    if str(sup) != ' '.join(ref):
        die("test_sub_patterns_reintegration: expected string mismatch with output.")

def test_sub_patterns_reintegration_pass_2():
    def get_relative_origin(node):
        return "../"
        
    s = ".:SetStyle::blue::red::test:. .:SetStyle:: :: :: .:GetRelativeOrigin:. :.123.:SetStyle:: :: :: .:GetRelativeOrigin:. :. .:GetRelativeOrigin:. .:SetStyle:: :: :: .:GetRelativeOrigin:. :."
    from venc3.patterns.non_contextual import set_style
    sup = StringUnderProcessing(s, "test_sub_patterns_reintegration")
    p = Processor()
    p.set_patterns({
        "SetStyle": set_style,
        "GetRelativeOrigin":get_relative_origin
    })
    
    p.process(sup, PatternNode.FLAG_NON_CONTEXTUAL)

    p.process(sup, PatternNode.FLAG_CONTEXTUAL)
        
    if str(sup) != "<span id=\"blue\" class=\"red\">test</span> <span id=\"\" class=\"\">../</span>123<span id=\"\" class=\"\">../</span> ../ <span id=\"\" class=\"\">../</span>":
        die("test_sub_patterns_reintegration_pass_2: expected string mismatch with output.")

test_datastructure()
test_full_process()
test_filter_process_1()
test_filter_process_2()
test_escape()
test_sub_patterns_reintegration_pass_1()
test_sub_patterns_reintegration_pass_2()
notify("Test passed")
