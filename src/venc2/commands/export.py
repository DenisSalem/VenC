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

from venc2.datastore.configuration import get_blog_configuration
from venc2.datastore.datastore import DataStore
from venc2.datastore.theme import themes_descriptor
from venc2.datastore.theme import Theme
from venc2.helpers import die
from venc2.helpers import notify
from venc2.helpers import rm_tree_error_handler 
from venc2.l10n import messages
from venc2.patterns.code_highlight import CodeHighlight
from venc2.patterns.contextual import extra_contextual_pattern_names
from venc2.patterns.non_contextual import non_contextual_pattern_names
from venc2.patterns.processor import merge_batches
from venc2.patterns.processor import Processor
from venc2.patterns.processor import PreProcessor
from venc2.threads.categories_thread import CategoriesThread
from venc2.threads.dates_thread import DatesThread
from venc2.threads.main_thread import MainThread

non_contextual_pattern_names_datastore = {
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
    
    # General blog data
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
    "GetEntryMetadata" : "get_entry_metadata",
    "GetEntryMetadataIfExists" : "get_entry_metadata_if_exists",
    "GetBlogMetadataIfExists" : "get_blog_metadata_if_exists", 
    "ForEntryAuthors" : "for_entry_authors", 
    "ForEntryTags" : "for_entry_tags",
    "ForBlogDates" : "for_blog_dates",
    "ForBlogCategories" : "for_blog_categories"
}

non_contextual_pattern_names_code_highlight = {
    "CodeHighlight" : "highlight",
    "GetStyleSheets" : "get_style_sheets"
}

contextual_pattern_names = {
    "GetRelativeOrigin" : "get_relative_origin",
    "IfInThread" : "if_in_thread",
    "GetRelativeLocation" : "get_relative_location",
    "GetNextPage" : "get_next_page",
    "GetPreviousPage" : "get_previous_page",
    "ForPages" : "for_pages",
    **extra_contextual_pattern_names
}

def export_and_remote_copy(argv=list()):
    notify(Messages.blog_recompilation)
    export_blog(argv)
    remote_copy()

def export_blog(argv=list()):
    # Initialisation of environment
    datastore = DataStore()

    # Initialisation of theme
    theme_folder = "theme/"

    if len(argv) == 1:
        if not argv[0] in themes_descriptor.keys():
            die(Messages.theme_doesnt_exists.format(argv[0]))
        
        else:
            theme_folder = os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0]+"/"
    
        for param in themes_descriptor[argv[0]].keys():
            if param[0] != "_": # marker to detect field names we do not want to replace
                datastore.blog_configuration[param] = themes_descriptor[argv[0]][param]

    theme = Theme(theme_folder)

    code_highlight = CodeHighlight()

    # Set up of non-contextual patterns
    
    processor = Processor()

    for pattern_name in non_contextual_pattern_names_datastore.keys():
        processor.set_function(pattern_name, getattr(datastore, non_contextual_pattern_names_datastore[pattern_name]))
    
    for pattern_name in non_contextual_pattern_names_code_highlight.keys():
        processor.set_function(pattern_name, getattr(code_highlight, non_contextual_pattern_names_code_highlight[pattern_name]))
    
    for pattern_name in non_contextual_pattern_names.keys():
        processor.set_function(pattern_name, non_contextual_pattern_names[pattern_name])
    
    # Blacklist contextual patterns
    for pattern_name in contextual_pattern_names.keys():
        processor.blacklist.append(pattern_name)

    for pattern_name in contextual_pattern_names.keys():
        processor.blacklist.append(pattern_name)

    """ Ugly piece of code """
    # List of patterns where we want to remove <p></p> tag
    processor.clean_after_and_before.append("CodeHighlight")

    notify(messages.pre_process)

    # Now we want to perform first parsing pass on entries and chunk
    for entry in datastore.get_entries():
        # Every chunks are preprocessed again because of contextual patterns
        entry.content = PreProcessor(merge_batches(processor.batch_process(entry.content, entry.filename, not entry.do_not_use_markdown)))

        entry.html_wrapper = deepcopy(theme.entry)
        entry.html_wrapper.above = PreProcessor(merge_batches(processor.batch_process(entry.html_wrapper.above, "entry.html", not entry.do_not_use_markdown)))
        entry.html_wrapper.below = PreProcessor(merge_batches(processor.batch_process(entry.html_wrapper.below, "entry.html",not entry.do_not_use_markdown)))
        
        entry.rss_wrapper = deepcopy(theme.rss_entry)
        entry.rss_wrapper.above = PreProcessor(merge_batches(processor.batch_process(entry.rss_wrapper.above, "rssEntry.html", not entry.do_not_use_markdown)))
        entry.rss_wrapper.below = PreProcessor(merge_batches(processor.batch_process(entry.rss_wrapper.below, "rssEntry.html", not entry.do_not_use_markdown)))
    
    theme.header = PreProcessor(merge_batches(processor.batch_process(theme.header, "header.html")))
    theme.footer = PreProcessor(merge_batches(processor.batch_process(theme.footer, "footer.html")))
    theme.rssHeader = PreProcessor(merge_batches(processor.batch_process(theme.rss_header, "rssHeader.html")))
    theme.rssFooter = PreProcessor(merge_batches(processor.batch_process(theme.rss_footer, "rssFooter.html")))

    # cleaning directory
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    # Starting second pass and exporting

    thread = MainThread(messages.export_main_thread, datastore, theme, contextual_pattern_names)
    thread.do()
    thread = DatesThread(messages.export_archives, datastore, theme, contextual_pattern_names)
    thread.do()
    thread = CategoriesThread(messages.export_categories, datastore, theme, contextual_pattern_names)
    thread.do()

    # Copy assets and extra files

    code_highlight.export_style_sheets()
    copy_recursively("extra/","blog/")
    copy_recursively("theme/assets/","blog/")

 
def copy_recursively(src, dest):
    for filename in os.listdir(src):
        try:
            shutil.copytree(src+filename, dest+filename)
    
        except shutil.Error as e:
            notify(Messages.directory_not_copied % e, "YELLOW")

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src+filename, dest+filename)

            else:
                notify(Messages.directory_not_copied % e, "YELLOW")


def edit_and_export(argv):
    blog_configuration = get_blog_configuration()

    if len(argv) != 1:
        die(Messages.missing_params.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([blog_configuration["textEditor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        die(Messages.unknown_text_editor.format(blog_configuration["textEditor"]))
    
    except:
        raise
    
    export_blog()
