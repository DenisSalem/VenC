#! /usr/bin/python3

#    Copyright 2016, 2018 Denis Salem
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

from venc2.helpers import PatternInvalidArgument
from venc2.l10n import messages

def get_random_number(in_argv):
    arg_names=["min","max","decimal_number"]
    argv = []
    for i in range(0,3):
        try:
            argv.append(int(in_argv[i]))

        except ValueError:
            raise PatternInvalidArgument(arg_names[i],in_argv[i], messages.pattern_argument_must_be_integer)

    v = argv[0] + random.random() * (argv[1] - argv[0] + 1)
    return str(int(v)) if argv[2] == 0 else str(round(v, argv[2]))

extra_contextual_pattern_names = {
    "GetRandomNumber" : get_random_number
}
