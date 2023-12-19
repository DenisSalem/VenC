#! /usr/bin/env python3

import mistletoe
from mistletoe import HTMLRenderer
from mistletoe import Document

test = """

# TITRE

## disable_shit_and_stuff

"""
class VenCRenderer(HTMLRenderer):
    def render_heading(self, token):
        template = '<h{level} id="{alternate}">{inner}</h{level}>'
        inner = self.render_inner(token)
        # TODO : It is possible to control default header level
        return template.format(level=token.level, inner=inner, alternate=''.join(e for e in inner if e.isalnum()))
        
r = VenCRenderer()
print(r.render(Document(test)))
