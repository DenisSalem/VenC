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

# Special case of KeyError
class UnknownContextual(KeyError):
    pass

class MalformedPatterns(Exception):
    def __init__(self, too_many_opening_symbols, escape, ressource):
        self.too_many_openings_symbols = too_many_opening_symbols
        self.escape = escape
        self.ressource = ressource

class PatternInvalidArgument(Exception):
    def __init__(self, name, value, message):
        self.name = name
        self.value = value
        self.message = message

