#! /usr/bin/python3

#    Copyright 2016, 2017 Denis Salem
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

import VenC.l10n

from VenC.datastore.configuration import get_blog_configuration
from VenC.datastore.datastore import DataStore
from VenC.datastore.theme import themes_descriptor
from VenC.datastore.theme import Theme
from VenC.helpers import die
from VenC.helpers import notify
from VenC.helpers import rm_tree_error_handler 
from VenC.l10n import Messages
from VenC.pattern.processor import merge_batches
from VenC.pattern.processor import Processor
from VenC.pattern.processor import PreProcessor
from VenC.pattern.code_highlight import CodeHighlight
from VenC.threads.main_thread import MainThread
from VenC.threads.dates_thread import DatesThread
from VenC.threads.categories_thread import CategoriesThread

non_contextual_patterns_name_datastore = [
    # General entry data
    "GetEntryTitle",
    "GetEntryID",
    "GetEntryYear",
    "GetEntryMonth",
    "GetEntryDay", 
    "GetEntryHour",
    "GetEntryMinute",
    "GetEntryDate", 
    "GetEntryDateURL",
    "GetEntryURL",
    
    # General blog data
    "GetAuthorName", 
    "GetBlogName", 
    "GetBlogDescription", 
    "GetBlogKeywords", 
    "GetAuthorDescription", 
    "GetBlogLicense", 
    "GetBlogURL", 
    "GetBlogLanguage",
    "GetAuthorEmail", 

    # Extra metadata getter
    "GetEntryMetadata", 
    "GetEntryMetadataIfExists", 
    "GetBlogMetadataIfExists", 
    "ForEntryAuthors", 
    "ForEntryTags", 
    "ForBlogDates", 
    "ForBlogCategories",
]

non_contextual_patterns_name_code_highlight = [
    "CodeHighlight",
    "GetStyleSheets"
]

contextual_patterns_blacklist = [
    "GetRelativeOrigin",
    "IfInThread",
    "GetRelativeLocation",
    "GetNextPage",
    "GetPreviousPage",
    "ForPages"
]

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

    for pattern_name in non_contextual_patterns_name_datastore:
        processor.set_function(pattern_name, getattr(datastore, pattern_name)
    
    for pattern_name in non_contextual_patterns_name_code_highlight:
        processor.set_function(pattern_name, getattr(code_highligth, pattern_name)
    
    # Setup contextual patterns black list
    for pattern_name in contextual_patterns_blacklist:
        processor.blacklist.append(pattern_name)

    # List of patterns where we want to remove <p></p> tag
    processor.clean_after_and_before.append("CodeHighlight")

    notify(messages.pre_process)

    # Now we want to perform first parsing pass on entries and chunk
    for entry in datastore.get_entries():
        # Every chunks are preprocessed again because of contextual patterns
        entry.content = PreProcessor(merge_batches(processor.batch_process(entry.content, not entry.do_not_use_markdown)))

        entry.html_wrapper = deepcopy(theme.entry)
        entry.html_wrapper.above = PreProcessor(mergeBatches(processor.batch_process(entry.html_wrapper.above, not entry.do_not_use_markdown)))
        entry.html_wrapper.below = PreProcessor(mergeBatches(processor.batch_process(entry.html_wrapper.below, not entry.do_not_use_markdown)))
        
        entry.rss_wrapper = deepcopy(theme.rssEntry)
        entry.rss_wrapper.above = PreProcessor(merge_batches(processor.batch_process(entry.rss_wrapper.above, not entry.do_not_use_markdown)))
        entry.rss_wrapper.below = PreProcessor(merge_batches(processor.batch_process(entry.rss_wrapper.below, not entry.do_not_use_markdown)))

    theme.header = PreProcessor(merge_batches(processor.batch_process(theme.header)))
    theme.footer = PreProcessor(merge_batches(processor.batch_process(theme.footer)))
    theme.rssHeader = PreProcessor(merge_batches(processor.batch_process(theme.rss_header)))
    theme.rssFooter = PreProcessor(merge_batches(processor.batch_process(theme.rss_footer)))

    # cleaning directory
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    # Starting second pass and exporting

    thread = MainThread(Messages.export_main_thread, datastore, theme)
    thread.Do()
    thread = DatesThread(Messages.export_archives, datastore, theme)
    thread.Do()
    thread = CategoriesThread(Messages.export_categories, datastore, theme)
    thread.Do()

    # Copy assets and extra files

    #codeHighlight.ExportStyleSheets()
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
