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

import random

from venc2.patterns.exceptions import PatternInvalidArgument
from venc2.patterns.exceptions import PatternMissingArguments
from venc2.l10n import messages

arg_names=["min","max","decimal_number"]

def get_random_number(in_argv):
    try:
        mn, mx, precision = in_argv
    
    except ValueError as e:
        raise PatternMissingArguments(e)
    
    argv = []

    for i in range(0,3):
        try:
            argv.append(float(in_argv[i]))

        except ValueError:
            raise PatternInvalidArgument(arg_names[i],in_argv[i], messages.pattern_argument_must_be_integer)

    v = float(mn) + random.random() * (float(mx) - float(mn))
    return str(int(v)) if int(precision) == 0 else str(round(v, int(precision)))
