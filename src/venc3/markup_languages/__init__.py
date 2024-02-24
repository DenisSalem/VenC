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

import importlib

def handle_markup_language_error(message, line=None, string=None):
    from venc3.prompt import notify
    notify(("exception_place_holder", message), "RED")
    if string != None:
        lines = string.split('\n')
        for lineno in range(0,len(lines)):
            if line - 1 == lineno:
                print('\033[91m'+lines[lineno]+'\033[0m')
            else:
                print(lines[lineno])
    exit(-1)


def import_wrapper(markup_language):
    key = {
        "Markdown" :         ("markdown",         "VenCMarkdown",         "mistletoe"),
        "asciidoc" :         ("asciidoc",         "VenCAsciiDoc",         "asciidoc3"),
        "reStructuredText" : ("restructuredtext", "VenCreStructuredText", "docutils")
    }
    
    try:
        m = importlib.import_module("venc3.markup_languages."+key[markup_language][0])
        return getattr(m, key[markup_language][1])
        
    except ModuleNotFoundError:
        from venc3.exceptions import VenCException
        raise VenCException(("module_not_found", key[markup_language][2]))  

def process_markup_language(source, markup_language, entry):
    if markup_language == "Markdown":
        do_table_of_content = ":content" == source.context[-8:]
        venc_markdown = import_wrapper(markup_language)(do_table_of_content)
        string = venc_markdown.render(source.string)
        if do_table_of_content:
            entry.toc = tuple(venc_markdown.renderer.table_of_content)

    elif markup_language == "asciidoc":
        string = import_wrapper(markup_language)(source, {})
        
    elif markup_language == "reStructuredText":
        from venc3.markup_languages.restructuredtext import VenCreStructuredText
        string = import_wrapper(markup_language)(source)
                
    elif markup_language != "none":
        from venc3.l10n import messages
        err = messages.unknown_markup_language.format(markup_language, source.context)
        handle_markup_language_error(err)
        
    else:
        return
        
    source.reset_index(string)
