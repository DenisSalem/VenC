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

import latex2mathml.converter

from venc2.l10n import messages
from venc2.patterns.exceptions import PatternInvalidArgument

def Latex2MathML(argv):
    tex_math_string = argv[0]
    try:
        return latex2mathml.converter.convert(tex_math_string)

    except Exception as e:
        print(e)
        raise PatternInvalidArgument(
            "Tex math string",
            tex_math_string,
            messages.tex_math_error
        )
