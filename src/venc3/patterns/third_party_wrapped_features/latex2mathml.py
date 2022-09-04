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


def latex_2_mathml(node, tex_math_string):
    try:
        import latex2mathml.converter
        
    except:
        from venc3.exceptions import VenCException
        from venc3.l10n import messages
        raise VenCException(messages.module_not_found.format('latex2mathml'))
    
    try:    
        return latex2mathml.converter.convert(tex_math_string)

    except:
        from venc3.l10n import messages
        from venc3.patterns.exceptions import PatternInvalidArgument
        raise VenCException(messages.tex_math_error)
