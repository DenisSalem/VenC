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

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.datastore.datastore import DataStore
from VenC.datastore.theme import ThemesDescriptor
from VenC.datastore.theme import Theme
from VenC.helpers import Die
from VenC.helpers import Notify
from VenC.helpers import RmTreeErrorHandler 
from VenC.l10n import Messages
from VenC.pattern.processor import MergeBatches
from VenC.pattern.processor import Processor
from VenC.pattern.processor import PreProcessor
from VenC.pattern.codeHighlight import CodeHighlight
from VenC.threads.mainThread import MainThread
from VenC.threads.datesThread import DatesThread
from VenC.threads.categoriesThread import CategoriesThread

def ExportAndRemoteCopy(argv=list()):
    Notify(Messages.blogRecompilation)
    ExportBlog(argv)
    RemoteCopy()

def ExportBlog(argv=list()):

    # Initialisation of environment
    datastore = DataStore()

    # Initialisation of theme
    themeFolder = "theme/"

    if len(argv) == 1:
        if not argv[0] in ThemesDescriptor.keys():
            Die(Messages.themeDoesntExists.format(argv[0]))
        
        else:
            themeFolder = os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0]+"/"
    
        for param in ThemesDescriptor[argv[0]].keys():
            if param[0] != "_": # marker to detect field names we do not want to replace
                datastore.blogConfiguration[param] = ThemesDescriptor[argv[0]][param]

    theme = Theme(themeFolder)

    codeHighlight = CodeHighlight()

    # Set up of non-contextual patterns
    
    processor = Processor()

    # General entry data
    processor.SetFunction("GetEntryTitle", datastore.GetEntryTitle)
    processor.SetFunction("GetEntryID", datastore.GetEntryID)
    processor.SetFunction("GetEntryYear", datastore.GetEntryYear)
    processor.SetFunction("GetEntryMonth", datastore.GetEntryMonth)
    processor.SetFunction("GetEntryDay", datastore.GetEntryDay)
    processor.SetFunction("GetEntryHour", datastore.GetEntryHour)
    processor.SetFunction("GetEntryMinute", datastore.GetEntryMinute)
    processor.SetFunction("GetEntryDate", datastore.GetEntryDate)
    processor.SetFunction("GetEntryURL", datastore.GetEntryURL)
    
    # General blog data
    processor.SetFunction("GetAuthorName", datastore.GetAuthorName)
    processor.SetFunction("GetBlogName", datastore.GetBlogName)
    processor.SetFunction("GetBlogDescription", datastore.GetBlogDescription)
    processor.SetFunction("GetBlogKeywords", datastore.GetBlogKeywords)
    processor.SetFunction("GetAuthorDescription", datastore.GetAuthorDescription)
    processor.SetFunction("GetBlogLicense", datastore.GetBlogLicense)
    processor.SetFunction("GetBlogURL", datastore.GetBlogURL)
    processor.SetFunction("GetBlogLanguage", datastore.GetBlogLanguage)
    processor.SetFunction("GetAuthorEmail", datastore.GetAuthorEmail)

    # Extra metadata getter
    processor.SetFunction("GetEntryMetadata", datastore.GetEntryMetadata)
    processor.SetFunction("GetEntryMetadataIfExists", datastore.GetEntryMetadataIfExists)
    processor.SetFunction("GetBlogMetadataIfExists", datastore.GetBlogMetadataIfExists)
    processor.SetFunction("ForEntryTags", datastore.ForEntryTags)
    processor.SetFunction("ForBlogDates", datastore.ForBlogDates)
    processor.SetFunction("ForBlogCategories", datastore.ForBlogCategories)
    processor.SetFunction("CodeHighlight", codeHighlight.Highlight)
    processor.SetFunction("GetStyleSheets", codeHighlight.GetStyleSheets)
    
    # Setup contextual patterns black list
    processor.blacklist.append("GetRelativeOrigin")
    processor.blacklist.append("GetRelativeLocation")
    processor.blacklist.append("GetNextPage")
    processor.blacklist.append("GetPreviousPage")
    processor.blacklist.append("ForPages")

    # List of patterns where we want to remove <p></p> tag
    processor.cleanAfterAndBefore.append("CodeHighlight")

    Notify(Messages.preProcess)

    # Now we want to perform first parsing pass on entries and chunk
    
    
    for entry in datastore.GetEntries():
        # Every chunks are preprocessed again because of contextual patterns
        entry.content = PreProcessor(MergeBatches( processor.BatchProcess(entry.content, not entry.doNotUseMarkdown)))

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
    thread = CategoriesThread(Messages.exportArchives, datastore, theme)
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
