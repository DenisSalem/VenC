#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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

import markdown2 as markdown

class VenCMarkdown(markdown.Markdown):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table_of_content = []
        
    def header_id_from_text(self, text, prefix, n):
        self.table_of_content.append((
            n,
            text,
            super().header_id_from_text(text, prefix, n)
        ))
        return self.table_of_content[-1][2]
        
    
    