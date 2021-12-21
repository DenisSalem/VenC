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

from venc2.l10n import messages
from venc2.prompt import notify

def handle_markup_language_error(message, line=None, string=None):
    notify(message, "RED")
    if string != None:
        lines = string.split('\n')
        for lineno in range(0,len(lines)):
            if line - 1 == lineno:
                print('\033[91m'+lines[lineno]+'\033[0m')
            else:
                print(lines[lineno])
    exit(-1)
            
def process_markup_language(source, markup_language, entry=None):
        if markup_language == "Markdown":
            try:
                from venc2.markup_languages.markdown import VenCMarkdown
                
            except ModuleNotFoundError:
                from venc2.prompt import die
                die(messages.module_not_found.format('markdown2'))

            venc_markdown = VenCMarkdown(extras=["header-ids", "footnotes"])
            string = venc_markdown.convert(source.string)
            if entry != None:
                entry.toc = tuple(venc_markdown.table_of_content)

        elif markup_language == "asciidoc":
            #TODO: support metadata parametrisation
            from venc2.markup_languages.asciidoc import VenCAsciiDoc
            string = VenCAsciiDoc(source, {})
            
        elif markup_language == "reStructuredText":
            from venc2.markup_languages.restructuredtext import VenCreStructuredText
            string = VenCreStructuredText(source)
                    
        elif markup_language != "none":
            err = messages.unknown_markup_language.format(markup_language, source.ressource)
            handle_markup_language_error(err)
            
        if markup_language != "none":
            source.string = string
            source.replace_needles(in_entry=True)


