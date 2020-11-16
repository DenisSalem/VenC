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

import datetime
import os
import shutil
import sys
import time

from . import CONTEXT
from . import ENVIRONMENT
from . import LOREM_IPSUM
from . import get_command_output
from . import set_python_version

PATH_TO_PELICAN = os.path.expanduser("~")+"/.local/bin/pelican"

def init_pelican_blog():
    set_python_version()
    ENVIRONMENT["Pelican"] = get_command_output([PATH_TO_PELICAN, "--version"]).strip()
    from distutils.dir_util import copy_tree
    copy_tree("pelican-benchmark-config", "pelican-benchmark")
    shutil.os.mkdir("pelican-benchmark/content")
    shutil.os.mkdir("pelican-benchmark/content/images")
    
def gen_pelican_entry():
    ID = CONTEXT["ENTRY_ID_COUNTER"]
    entry  = "Title: benchmark entry "+str(ID)+'\n'
    entry += "Category: "+CONTEXT["SAMPLE_CATEGORIES"][CONTEXT["CATEGORY_INDEX"]]+'\n'
    entry += "Authors: VenC Comparative Benchmark\n"
    entry += "Tags: ''\n"
    date = datetime.datetime.fromtimestamp(CONTEXT["DATETIME"])
    entry += "Date: "+date.strftime("%Y-%m-%d %H:%M")+"\n"
    entry += "Summary: ''\n\n"
    entry += LOREM_IPSUM*CONTEXT["CONTENT_SIZE_MULTIPLIER"]
    open("pelican-benchmark/content/benchmark-entry-"+str(ID)+".md", 'w').write(entry)

def benchmark_pelican():
    os.chdir("pelican-benchmark")
    start_timestamp = time.time()
    output = get_command_output([PATH_TO_PELICAN,"content"])
    time_command = time.time() - start_timestamp
    time_internal = None

    if "-v" in sys.argv:
        print(''.join(output))
        
    time_internal = float([line for line in output.split('\n') if line != ''][-1].split(' ')[-2])
            
    os.chdir("..")
    return {"time":time_command, "internal":time_internal}

def clear_pelican_blog():
    try:
        shutil.rmtree("pelican-benchmark")
        
    except FileNotFoundError:
        pass
