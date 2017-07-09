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

import os
import time
import yaml
import base64
import shutil
import subprocess

import VenC.l10n

from VenC.datastore.configuration import GetBlogConfiguration
from VenC.datastore.datastore import DataStore
from VenC.datastore.entry import EntryWrapper
from VenC.datastore.theme import ThemesDescriptor
from VenC.datastore.theme import Theme
from VenC.helpers import Die
from VenC.helpers import RmTreeErrorHandler 
from VenC.l10n import Messages
from VenC.pattern.processor import Processor
from VenC.pattern.processor import BlackList
from VenC.pattern.codeHighlight import CodeHighlight
from VenC.threads.main import Main

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
    processor.SetFunction("GetEntryMetadataIfExists", datastore.GetEntryMetadata)
    processor.SetFunction("GetBlogMetadataIfExists", datastore.GetEntryMetadata)
    processor.SetFunction("ForEntryTags", datastore.ForEntryTags)
    
    # Now we want to perform first parsing pass on entries
    htmlWrapper = EntryWrapper(theme.entry)
    rssWrapper = EntryWrapper(theme.rssEntry)

    # Setup contextual patterns black list
    BlackList.append("CodeHighlight")
    BlackList.append("GetEntryURL")
    BlackList.append("GetRelativeOrigin")
    
    for entry in datastore.GetEntries():
        entry.content = processor.BatchProcess(entry.content)

        entry.htmlWrapper = htmlWrapper
        entry.htmlWrapper.above = processor.BatchProcess(entry.htmlWrapper.above)
        entry.htmlWrapper.below = processor.BatchProcess(entry.htmlWrapper.below)
        
        entry.rssWrapper = rssWrapper
        entry.rssWrapper.above = processor.BatchProcess(entry.rssWrapper.above)
        entry.rssWrapper.below = processor.BatchProcess(entry.rssWrapper.below)

    # We want to process the remains patterns so we reset the black list
    Blacklist = list()

    main = Main("Test", datastore)

    # cleaning directory
    #shutil.rmtree("blog", ignore_errors=False, onerror=RmTreeErrorHandler)
    #os.makedirs("blog")
    #currentBlog = Blog(themeFolder, blogConfiguration)
    #currentBlog.export()

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
