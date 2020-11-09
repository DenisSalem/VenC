#! /usr/bin/env python3

#   Copyright 2016, 2020 Denis Salem
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

"""
Requirement:

    To run properly every tested softwares must be installed on the system.

Nature of the benchmark:

    Each generated page have
        - RSS and ATOM Feed.
        - Hierarchical categories list in header/
        - Archives list by by month.
        - Navigation links in footer.

"""

# Comment items you want to ignore
WILL_TESTS = [
    "VenC"
]

# Comment items you want to pass
WILL_PERFOM_STAGES = [
    "init",
    "clear"
]


# Set to False for debugging
BE_QUIET = False

########################################################################

import os
import sys
import shutil

benchmark_version = "1.0.0"

STDOUT = sys.stdout
DEVNULL = open(os.devnull, "w")

def be_quiet(fun, args):
    if BE_QUIET:
        sys.stdout = DEVNULL
        
    fun(args)
    if BE_QUIET:
        sys.stdout = STDOUT
    
# Wil hold Interpreter/Compiler version as well as content generator version.
environment = {}

def init_venc_blog():
    from venc2.commands.new import new_blog
    from venc2 import venc_version
    if not "Python" in environment.keys():
        environment["Python"] = sys.version.replace('\n', '') 
        environment["VenC"] = venc_version
    
    be_quiet(new_blog, ["venc-benchmark"])

def clear_venc_blog():
    shutil.rmtree("venc-benchmark")

stages = {
    "init": {
        "VenC" : init_venc_blog
    },
    "clear" : { 
        "VenC" : clear_venc_blog
    }
}

print("VenC Comparative Benchmark v"+benchmark_version)

for stage in WILL_PERFOM_STAGES:
    print(stage+':')
    for item in WILL_TESTS:
        print('\t'+item)
        stages[stage][item]()
    

print("Done.")
