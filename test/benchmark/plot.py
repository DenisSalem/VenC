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

# This code is a draft

import sys
import json
from bokeh.plotting import figure, output_file, save

data = json.load(open(sys.argv[1], "r"))

p = figure(
    title="VenC Benchmark ({0})".format(data["environment"]["CPU"]),
    width=1920,
    height=1080
)
p.xaxis.axis_label = "Entries count"
p.yaxis.axis_label = "Time"

step = 10

p.line(
	[c*step for c in range(0, len(data["benchmark_data"]))],
	[v["time"] for v in data["benchmark_data"] ],
    color="#000000",
    legend_label = "VenC "+ data["environment"]["VenC"]+"\nPython "+data["environment"]["Python"]
)

p.line(
	[c*step for c in range(0, len(data["benchmark_data"]))],
	[v["internal"] for v in data["benchmark_data"] ],
    color="#808080",
    legend_label = "VenC "+data["environment"]["VenC"]+"\nPython "+data["environment"]["Python"]+" (internal)"
)

p.legend.location = "top_left"
p.sizing_mode = 'scale_width'

output_file("benchmark.html", title="VenC Benchmark ({0})".format(data["environment"]["CPU"]))
save(p)
