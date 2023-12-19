#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
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

def VenCreStructuredText(source):
    try:
        from docutils.core import publish_parts
        from docutils.utils import SystemMessage
        string = publish_parts(source.string, writer_name='html', settings_overrides={'doctitle_xform':False, 'halt_level': 2, 'traceback': True, "warning_stream":"/dev/null"})['html_body']
        return string

    except ModuleNotFoundError:
        from venc3.prompt import die
        die(("module_not_found", 'docutils'))
            
    except SystemMessage as e:
        from venc3.markup_languages import handle_markup_language_error
        try:
            line = int(str(e).split(':')[1])
            msg = str(e).split(':')[2].strip()
            handle_markup_language_error( source.context+": "+msg, line=line, string=source.string)

        except Exception as e: 
            handle_markup_language_error(source.context+", "+str(e))
            
