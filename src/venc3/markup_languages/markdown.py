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

from html import unescape

import mistletoe
from mistletoe import HTMLRenderer
from mistletoe import Document

class VenCRenderer(HTMLRenderer):
    def __init__(self):
        self.table_of_content = []
        super().__init__()
        
    def render_heading(self, token):
        template = '<h{level} id="{header_id}">{inner}</h{level}>'
        inner = self.render_inner(token)
        header_id = ''.join(e for e in unescape(inner) if e.isalnum())
        self.table_of_content.append((
            token.level,
            inner,
            header_id
        ))
        # TODO : It is possible to control default header level
        return template.format(level=token.level, inner=inner, header_id=header_id)

class VenCMarkdown:
    def __init__(self):
        self.renderer = VenCRenderer()
        
    def render(self, input_text):
        return self.renderer.render(Document(input_text))
