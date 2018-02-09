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
from VenC.helpers import RmTreeErrorHandler 
from VenC.l10n import Messages
from VenC.pattern.processor import MergeBatches
from VenC.pattern.processor import Processor
from VenC.pattern.processor import PreProcessor
from VenC.pattern.codeHighlight import CodeHighlight
from VenC.threads.mainThread import MainThread
from VenC.threads.datesThread import DatesThread
from VenC.threads.categoriesThread import CategoriesThread

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
    
        for param in rhemes_descriptor[argv[0]].keys():
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
    processor.cleanAfterAndBefore.append("CodeHighlight")

    notify(messages.pre_process)

    # Now we want to perform first parsing pass on entries and chunk
    for entry in datastore.get_entries():
        # Every chunks are preprocessed again because of contextual patterns
        entry.content = PreProcessor(MergeBatches(processor.BatchProcess(entry.content, not entry.doNotUseMarkdown)))

        entry.htmlWrapper = deepcopy(theme.entry)
        entry.htmlWrapper.above = PreProcessor(MergeBatches(processor.BatchProcess(entry.htmlWrapper.above, not entry.doNotUseMarkdown)))
        entry.htmlWrapper.below = PreProcessor(MergeBatches(processor.BatchProcess(entry.htmlWrapper.below, not entry.doNotUseMarkdown)))
        
        entry.rssWrapper = deepcopy(theme.rssEntry)
        entry.rssWrapper.above = PreProcessor(MergeBatches(processor.BatchProcess(entry.rssWrapper.above, not entry.doNotUseMarkdown)))
        entry.rssWrapper.below = PreProcessor(MergeBatches(processor.BatchProcess(entry.rssWrapper.below, not entry.doNotUseMarkdown)))

    theme.header = PreProcessor(MergeBatches(processor.BatchProcess(theme.header)))
    theme.footer = PreProcessor(MergeBatches( processor.BatchProcess(theme.footer)))
    theme.rssHeader = PreProcessor(MergeBatches(processor.BatchProcess(theme.rssHeader)))
    theme.rssFooter = PreProcessor(MergeBatches(processor.BatchProcess(theme.rssFooter)))

    # cleaning directory
    shutil.rmtree("blog", ignore_errors=False, onerror=RmTreeErrorHandler)
    os.makedirs("blog")

    # Starting second pass and exporting

    thread = MainThread(Messages.exportMainThread, datastore, theme)
    thread.Do()
    thread = DatesThread(Messages.exportArchives, datastore, theme)
    thread.Do()
    thread = CategoriesThread(Messages.exportCategories, datastore, theme)
    thread.Do()

    # Copy assets and extra files

    #codeHighlight.ExportStyleSheets()
    CopyRecursively("extra/","blog/")
    CopyRecursively("theme/assets/","blog/")

 
def CopyRecursively(src, dest):
    for filename in os.listdir(src):
        try:
            shutil.copytree(src+filename, dest+filename)
    
        except shutil.Error as e:
            Notify(Messages.directoryNotCopied % e, "YELLOW")

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src+filename, dest+filename)

            else:
                Notify(Messages.directoryNotCopied % e, "YELLOW")


def EditAndExport(argv):
    blogConfiguration = GetBlogConfiguration()

    if len(argv) != 1:
        Die(Messages.missingParams.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([blogConfiguration["textEditor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        Die(Messages.unknownTextEditor.format(blogConfiguration["textEditor"]))
    
    except:
        raise
    
    ExportBlog()
