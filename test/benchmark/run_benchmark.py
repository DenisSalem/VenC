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
Nature of the benchmark:
    Each generated page have
        - RSS and ATOM Feed.
        - Categories list in header.
        - Navigation links in footer.
        - Ten entries
        
    Entries are generated individualy in addition of the following threads:
        - Categories
    
    Markup langage is set to markdown
"""

# Comment items you want to ignore
WILL_TESTS = [
    "VenC",

]

########################################################################

import datetime
import time
import vencbenchmark

from vencbenchmark.venc import init_venc_blog
from vencbenchmark.venc import gen_venc_entry
from vencbenchmark.venc import benchmark_venc
from vencbenchmark.venc import clear_venc_blog

import json

benchmark_data = []

output_filename = str(time.time())+".json"

def save_results():
    results = {
                "environment"   : vencbenchmark.ENVIRONMENT,
                "benchmark_data": benchmark_data
    }
    output = json.dumps(results)
    f = open(output_filename,"w")
    f.write(output)
    f.close()
    
def benchmark():
    print("Benchmark")
    for i in range(0, 1000):
        gen_venc_entry()
        series = []
        print("\tWith {0} entries...".format(vencbenchmark.CONTEXT["ENTRY_ID_COUNTER"]), end=('\r' if i != 999 else '\n'))
        for j in range(0,10):
            series.append(
                benchmark_venc()
            )
            
        average = {}
        average["time"] = sum([ v["time"] for v in series ]) / len(series)
        if "time_cache" in series[0].keys():
            average["time_cache"] = sum([ v["time_cache"] for v in series ]) / len(series)
            
        if series[0]["internal"] != None:
            average["internal"] =  sum([ v["internal"] for v in series ]) / len(series)
    
        benchmark_data.append(average)
        save_results()
            
        vencbenchmark.update_context()


        

print("VenC Benchmark v"+vencbenchmark.BENCHMARCH_VERSION)

try:
    clear_venc_blog()
    init_venc_blog()
    benchmark()
    clear_venc_blog()
    
except KeyboardInterrupt:
    pass
    
print("Done.")
