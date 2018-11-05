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

import errno
import os
import time
from copy import deepcopy
import yaml
import base64
import shutil
import subprocess

from venc2.datastore.datastore import DataStore
from venc2.datastore.theme import themes_descriptor
from venc2.datastore.theme import Theme
from venc2.helpers import die
from venc2.helpers import notify
from venc2.helpers import rm_tree_error_handler 
from venc2.l10n import messages
from venc2.patterns.code_highlight import CodeHighlight
from venc2.patterns.latex2mathml import Latex2MathML
from venc2.patterns.contextual import extra_contextual_pattern_names
from venc2.patterns.non_contextual import non_contextual_pattern_names
from venc2.patterns.processor import Processor
from venc2.patterns.processor import PreProcessor
from venc2.threads.categories import CategoriesThread
from venc2.threads.dates import DatesThread
from venc2.threads.entries import EntriesThread
from venc2.threads.main import MainThread

# Initialisation of environment
datastore = DataStore()
code_highlight = CodeHighlight(datastore.blog_configuration["code_highlight_css_override"])

non_contextual_pattern_names_entry = {
    # General entry data
    "GetEntryTitle" : "get_entry_title",
    "GetEntryID" : "get_entry_id",
    "GetEntryYear" : "get_entry_year",
    "GetEntryMonth" : "get_entry_month",
    "GetEntryDay" : "get_entry_day",
    "GetEntryHour" : "get_entry_hour", 
    "GetEntryMinute" : "get_entry_minute",
    "GetEntryDate" : "get_entry_date",
    "GetEntryDateURL" : "get_entry_date_url",
    "GetEntryURL" : "get_entry_url",
    "ForEntryAuthors" : "for_entry_authors", 
    "ForEntryTags" : "for_entry_tags",
    
    # Extra metadata getter
    "LeavesForEntryCategories" : "leaves_for_entry_categories",
    "TreeForEntryCategories" : "tree_for_entry_categories",
    "GetEntryMetadata" : "get_entry_metadata",
    "GetEntryMetadataIfExists" : "get_entry_metadata_if_exists"
}

non_contextual_pattern_names_entry_keys = non_contextual_pattern_names_entry.keys()

non_contextual_pattern_names_blog = {
    "GetAuthorName" : "get_author_name",
    "GetBlogName" : "get_blog_name",
    "GetBlogDescription" : "get_blog_description",
    "GetBlogKeywords" : "get_blog_keywords",
    "GetAuthorDescription" : "get_author_description",
    "GetBlogLicense" : "get_blog_license",
    "GetBlogURL" : "get_blog_url",
    "GetBlogLanguage" : "get_blog_language",
    "GetAuthorEmail" : "get_author_email",

    # Extra metadata getter
    "GetBlogMetadataIfExists" : "get_blog_metadata_if_exists", 
    "ForBlogDates" : "for_blog_dates",
    "TreeForBlogCategories" : "tree_for_blog_categories"
}

non_contextual_pattern_names_datastore = {
    **non_contextual_pattern_names_blog,
    **non_contextual_pattern_names_entry
}

non_contextual_pattern_names_ml = {
    "CodeHighlight" : code_highlight.highlight,
    "Latex2MathML" : Latex2MathML
}

contextual_pattern_names = {
    "GetRelativeOrigin" : "get_relative_origin",
    "IfInThread" : "if_in_thread",
    "IfInArchives" : "if_in_archives",
    "IfInCategories" : "if_in_categories",
    "IfInFirstPage" : "if_in_first_page",
    "IfInLastPage" : "if_in_last_page",
    "IfInEntryID" : "if_in_entry_id",
    "GetRelativeLocation" : "get_relative_location",
    "GetNextPage" : "get_next_page",
    "GetPreviousPage" : "get_previous_page",
    "ForPages" : "for_pages",
    "GetStyleSheets" : code_highlight.get_style_sheets,
    **extra_contextual_pattern_names
}

def export_and_remote_copy(argv=list()):
    notify(Messages.blog_recompilation)
    export_blog(argv)
    remote_copy()

def export_blog(argv=list()):
    # Initialisation of theme
    theme_folder = "theme/"

    if len(argv) == 1:
        if not argv[0] in themes_descriptor.keys():
            die(messages.theme_doesnt_exists.format(argv[0]))
        
        else:
            theme_folder = os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0]+"/"
    
        for param in themes_descriptor[argv[0]].keys():
            if param[0] != "_": # marker to detect field names we do not want to replace
                datastore.blog_configuration[param] = themes_descriptor[argv[0]][param]

    theme = Theme(theme_folder, non_contextual_pattern_names)

    # Set up of non-contextual patterns
    
    processor = Processor()

    for pattern_name in non_contextual_pattern_names_datastore.keys():
        processor.set_function(pattern_name, getattr(datastore, non_contextual_pattern_names_datastore[pattern_name]))
    
    for pattern_name in non_contextual_pattern_names_ml.keys():
        processor.set_function(pattern_name, non_contextual_pattern_names_ml[pattern_name])
    
    for pattern_name in non_contextual_pattern_names.keys():
        processor.set_function(pattern_name, non_contextual_pattern_names[pattern_name])
    
    # Blacklist contextual patterns
    for pattern_name in contextual_pattern_names.keys():
        processor.blacklist.append(pattern_name)

    notify(messages.pre_process)

    # Now we want to perform first parsing pass on entries and chunk
    for entry in datastore.get_entries():
        try:
            markup_language = getattr(entry, "markup_language")

        except AttributeError:
            markup_language = datastore.blog_configuration["markup_language"]
        
        entry.preview = PreProcessor(processor.batch_process(entry.preview, entry.filename).process_markup_language(markup_language, entry.filename))
        entry.content = PreProcessor(processor.batch_process(entry.content, entry.filename).process_markup_language(markup_language, entry.filename))
        entry.html_wrapper = deepcopy(theme.entry)
        entry.html_wrapper.above = PreProcessor(''.join(processor.batch_process(entry.html_wrapper.above, "entry.html", False).sub_strings))
        entry.html_wrapper.below = PreProcessor(''.join(processor.batch_process(entry.html_wrapper.below, "entry.html", False).sub_strings))
        
        entry.rss_wrapper = deepcopy(theme.rss_entry)
        entry.rss_wrapper.above = PreProcessor(''.join(processor.batch_process(entry.rss_wrapper.above, "rssEntry.html", False).sub_strings))
        entry.rss_wrapper.below = PreProcessor(''.join(processor.batch_process(entry.rss_wrapper.below, "rssEntry.html", False).sub_strings))
    
    processor.forbidden = non_contextual_pattern_names_entry_keys
    theme.header = PreProcessor(''.join(processor.batch_process(theme.header, "header.html").sub_strings))
    theme.footer = PreProcessor(''.join(processor.batch_process(theme.footer, "footer.html").sub_strings))
    theme.rssHeader = PreProcessor(''.join(processor.batch_process(theme.rss_header, "rssHeader.html").sub_strings))
    theme.rssFooter = PreProcessor(''.join(processor.batch_process(theme.rss_footer, "rssFooter.html").sub_strings))

    # cleaning directory
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    # Starting second pass and exporting

    thread = MainThread(messages.export_main_thread, datastore, theme, contextual_pattern_names, non_contextual_pattern_names_entry_keys)
    thread.do()

    if not datastore.blog_configuration["disable_archives"]:
        thread = DatesThread(messages.export_archives, datastore, theme, contextual_pattern_names, non_contextual_pattern_names_entry_keys)
        thread.do()

    if not datastore.blog_configuration["disable_categories"]:
        thread = CategoriesThread(messages.export_categories, datastore, theme, contextual_pattern_names, non_contextual_pattern_names_entry_keys)
        thread.do()

    if not datastore.blog_configuration["disable_single_entries"]:
        thread = EntriesThread(messages.export_single_entries, datastore, theme, contextual_pattern_names, non_contextual_pattern_names_entry_keys)
        thread.do() 

    # Copy assets and extra files

    code_highlight.export_style_sheets()
    copy_recursively("extra/","blog/")
    copy_recursively(theme_folder+"assets/","blog/")

 
def copy_recursively(src, dest):
    for filename in os.listdir(src):
        try:
            shutil.copytree(src+filename, dest+filename)
    
        except shutil.Error as e:
            notify(messages.directory_not_copied % e, "YELLOW")

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src+filename, dest+filename)

            else:
                notify(messages.directory_not_copied % e, "YELLOW")


def edit_and_export(argv):
    if len(argv) != 1:
        die(messages.missing_params.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([datastore.blog_configuration["text_editor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        die(messages.unknown_text_editor.format(datastore.blog_configuration["text_editor"]))
    
    except:
        raise
    
    export_blog()
