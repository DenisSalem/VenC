#! /usr/bin/env python3

#    Copyright 2016, 2019 Denis Salem
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

import difflib
import os
import sys
os.chdir("themes/tested")
        
from venc2.commands.export import export_blog
from venc2.helpers import GenericMessage
from venc2.prompt import get_formatted_message 

from test_engine import run_tests

def tree_list_dir(root_path, clear):
    l = []
    a = l.append
    for t in os.walk(root_path):
        for f in t[2]:
            a(  '/'.join((t[0]+'/'+f).split('/')[clear:]) )
            
    return l
    

def test_theme(args, test_name):
    refs, theme = args
    null = open('/dev/null', 'w')
    stdout = sys.stdout

    sys.stdout = null
    
    export_blog([theme])
    
    sys.stdout = stdout

    tested = tree_list_dir('blog', 1)
    refs = tree_list_dir('../refs/'+(theme.capitalize()), 3)
    
    extra = []
    tested_exists = []
    tested_extra_append = extra.append
    tested_exists_append = tested_exists.append
    for f in tested:
        if not f in refs:
            tested_extra_append(f)
        else:
            tested_exists_append(f)

    missings = []
    refs_exists = []
    missings_append = missings.append
    refs_exists_append = refs_exists.append
    
    for f in refs:
        if not f in tested:
            missings_append(f)
            
        else:
            refs_exists_append(f)
            
    len_missings = len(missings)
    len_extra = len(extra)
    
    for f in missings:
        print(get_formatted_message("\t\tMissing: "+f, color="RED", prompt=""))

    for f in extra:
        print(get_formatted_message("\t\tExtra: "+f, color="RED", prompt=""))
    
    diff = difflib.Differ()
    mismatch = False
    for index in range(0, len(refs_exists)):
        try:
            file_ref  = open('../refs/'+(theme.capitalize())+'/'+refs_exists[index], 'r').read().split('\n')
            file_tested = open('blog/'+tested_exists[index], 'r').read().split('\n')
            
        except UnicodeDecodeError:
            continue
            
        line_index = 0
        for l in diff.compare(file_ref, file_tested):
            if (l[0] in ['-','+']) and (not "Page generated" in l):
                print(get_formatted_message("\t\tMismatch: "+("refs: \t" if l[0] == '-' else "tested:\t")+refs_exists[index]+": "+str(line_index+1)+": "+l, color="RED", prompt=""))
                mismatch = True

            elif l[0] == '?':
                line_index -= 2
                
            line_index += 1
    
    if len_missings or len_extra or mismatch:
        return False
        
    else:
        return True
        
tests = [
    (
        "Gentle.", 
        ("../refs/Gentle", "gentle"),
        True,
        test_theme
    ),
    (
        "Tessellation.", 
        ("../refs/Tessellation", "tessellation"),
        True,
        test_theme
    ),
    (
        "Academik.", 
        ("../refs/Academik", "academik"),
        True,
        test_theme
    ),
]

run_tests("Testings default themes compliance", tests)
os.chdir("../..")

