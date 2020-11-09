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
import shutil
import sys

from . import be_quiet
from . import ENVIRONMENT
from . import CONTEXT
from . import LOREM_IPSUM

def init_venc_blog():
    from venc2.commands.new import new_blog
    from venc2 import venc_version
    if not "Python" in ENVIRONMENT.keys():
        ENVIRONMENT["Python"] = sys.version.replace('\n', '') 
        ENVIRONMENT["VenC"] = venc_version
    
    be_quiet(new_blog, ["venc-benchmark"])
    from distutils.dir_util import copy_tree
    copy_tree("venc-benchmark-config", "venc-benchmark")

def gen_venc_entry():
    ID = CONTEXT["ENTRY_ID_COUNTER"]
    entry  = "title: benchmark entry "+str(ID)+'\n'
    entry += "authors: VenC Comparative Benchmark\n"
    entry += "categories: "+CONTEXT["SAMPLE_CATEGORIES"][CONTEXT["CATEGORY_INDEX"]]+'\n'
    entry += "tags: ''"
    entry += "---VENC-BEGIN-PREVIEW---\n"
    entry += "---VENC-END-PREVIEW---\n"+(LOREM_IPSUM*CONTEXT["CONTENT_SIZE_MULTIPLIER"])
    date = datetime.datetime.fromtimestamp(CONTEXT["DATETIME"])
    entry_date = str(date.month)+'-'+str(date.day)+'-'+str(date.year)+'-'+str(date.hour)+'-'+str(date.minute)
    output_filename = str(ID)+"__"+entry_date+"__"+"benchmark_entry_"+str(ID)
    open("venc-benchmark/entries/"+output_filename, 'w').write(entry)
   
def clear_venc_blog():
    try:
        shutil.rmtree("venc-benchmark")
        
    except FileNotFoundError:
        pass
