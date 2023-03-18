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

import random

def get_random_number(node, _min, _max, _precision):    
        try:
            v = float(_min) + random.random() * (float(_max) - float(_min))
            return str(int(v)) if int(_precision) == 0 else str(round(v, int(_precision)))
            
        except ValueError as e:
            from venc3.exceptions import VenCException
            faulty_arg_name = {v: k for k, v in locals().items()}[e.args[0].split('\'')[1]]
            
            raise VenCException(
                ("wrong_pattern_argument", faulty_arg_name[1:], locals()[faulty_arg_name], "GetRandomNumber", str(e)),
                node
            )
