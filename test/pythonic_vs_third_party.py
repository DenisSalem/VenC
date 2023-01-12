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

def find_pattern_boundaries():
    import re
    string = [ 'a' for i in range(0,50000) ]
    string[5] = ".:"
    string[104] = ".:"
    string[300] = ".:"
    string[1400] = ".:"
    string[4700] = ".:"
    string[30000] = ".:"
    string = ''.join(string)
    
    def find_all_re(string):
        return list(i.start() for i in re.finditer("\.:",string))

    def find_all_native(string):
      op = []
      op_append = op.append
      index=0
      while '∞':
          index = string.find('.:', index)
          if index == -1:
            return op
          op_append(index)
          index+=1
          
    import datetime
    t = datetime.datetime.now().timestamp()
    print("RE:", find_all_re(string), datetime.datetime.now().timestamp() - t)

    t = datetime.datetime.now().timestamp()
    print("NATIVE: ", find_all_native(string), datetime.datetime.now().timestamp() - t)
