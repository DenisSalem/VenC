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

PATH_TO_NIKOLA = os.path.expanduser("~")+"/.local/bin/nikola"

def init_nikola_blog():
    set_python_version()
    ENVIRONMENT["Nikola"] = get_command_output([PATH_TO_NIKOLA, "version"]).strip().replace("Nikola v", '')
    from distutils.dir_util import copy_tree
    copy_tree("nikola-benchmark-config", "nikola-benchmark")
    shutil.os.mkdir("nikola-benchmark/posts")
    
def gen_nikola_entry():
    ID = CONTEXT["ENTRY_ID_COUNTER"]
    date = datetime.datetime.fromtimestamp(CONTEXT["DATETIME"])
    
    entry = "---\n"
    entry += "category: "+CONTEXT["SAMPLE_CATEGORIES"][CONTEXT["CATEGORY_INDEX"]]+'\n'
    entry += "date: "+date.strftime("%Y-%m-%d %H:%M:%S")+'\n'
    entry += "description: ''\n"
    entry += "link: ''\n"
    entry += "slug: benchmark-entry-"+str(ID)+'\n'
    entry += "tags: ''\n"
    entry += "title: benchmark entry "+str(ID)+'\n'
    entry += "type: 'text'\n"
    entry += "---\n"
    entry += LOREM_IPSUM*CONTEXT["CONTENT_SIZE_MULTIPLIER"]
    open("nikola-benchmark/posts/benchmark-entry-"+str(ID)+".md", 'w').write(entry)

def benchmark_nikola():
    os.chdir("nikola-benchmark")
    try:
        shutil.rmtree("cache")
    
    except FileNotFoundError:
        pass
        
    try:
        os.remove(".doit.db")
    except FileNotFoundError:
        pass
        
    start_timestamp = time.time()
    output = get_command_output([PATH_TO_NIKOLA,"build"])
    time_command = time.time() - start_timestamp
    
    start_timestamp = time.time()
    output = get_command_output([PATH_TO_NIKOLA,"build"])
    time_cache = time.time() - start_timestamp
    
    time_internal = None
            
    os.chdir("..")
    return {"time":time_command, "internal":time_internal, "time_cache":time_cache}

def clear_nikola_blog():
    try:
        shutil.rmtree("nikola-benchmark")
        
    except FileNotFoundError:
        pass
