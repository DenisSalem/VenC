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

class Messages:
    blogCreated = "Your blog has been created!"
    themeInstalled = "Theme has been installed!"
    entryWritten = "Entry has been saved!"
    fileNotFound = "{0}: This file or directory does not exists."
    fileAlreadyExists = "{0}: {1}: File or directory already exists."
    invalidEntryFilename = "{0}: Invalid entry filename."
    blogName = "Blog name"
    yourName = "Your name"
    blogDescription = "Short description of your blog"
    blogKeywords = "Some keywords about your blog"
    aboutYou = "About you"
    license = "The license applied to your blog"
    blogUrl = "The URL of your blog"
    blogLanguage = "The language of your blog"
    yourEmail = "Your e-mail"
    missingParams = "{0}: Missing arguments."
    cannotReadIn = "{0}: Cannot read into {1}."
    nothingToDo = "Nothing to do."
    unknownCommand = "{0}: Unknown command."
    noBlogConfiguration = "Blog's configuration file doesn't exists or you do not have right permissions."
    missingMandatoryFieldInBlogConf = "Warning, the field \"{0}\" is missing the blog's configuration file."
    username="Username: "
    userPasswd="User password: "
    ftpHost="FTP hostname"
    ftpPath="Absolute path of your blog on FTP server."
    cleanFtpDirectory="Cleaning target FTP directory..."
    copyToFtpDirectory="Copying your blog to target FTP directory..."
    possibleMalformedEntry="Possible malformed entry {0}. Abort."
    possibleMalformedBlogConfiguration="Possible malformed blog configuration. Abort."
    blogRecompilation="Recompilation of your blog locally..."
    exportArchives="Exporting local entries thread of '{0}'."
    exportMainThread="Exporting local main entries thread."
    exportMainThreadRss="Exporting local main RSS feed entries."
    exportCategories="Exporting local categories entries thread named '{0}'."
    exportCategoriesRss="Exporting local entries RSS feed thread from category '{0}'."
    missingMandatoryFieldInEntry="Field '{0}' in entry number {1} is missing."
    forUnknownValue="For: Value {0} isn't defined."
    recursiveForUnknownValue="RecursiveFor: Value {0} isn't defined."
    notEnoughArgs="Missing parameters."
    unknownPattern="The pattern '{0}'doesn't exists."
    unknownContextual="Contextual variable {0} doesn't exists."
    inRessource="In ressource '{0}'."
    somethingGoesWrongReturnEmptyString="An error occurs. Replacement with an empty string."
    argBlogName="Blog name {0}"
    argEntryName="Entry name"
    argTemplateName="Template name"
    argInputFilename="Filename"
    blogFolderDoesntExists="Destination folder doesn't exist. VenC doesn't care and will built a new one."
    themeDescriptionDummy = "The empty one. Aim to built your own from scratch."
    themeDescriptionGentle = "Theme with one column. It's light, clear and elegant. Fit nicely for a blog."
    themeDescriptionTessellation = "Theme with three columns. It's light, clear, and elegant. Fit nicely for a galery."
    themeDoesntExists = "{0}: Theme doesn't exists."
    unknownTextEditor = "{0}: unknown text editor."
    themeName = "Theme name"
    entryIsEmpty = "{0}: The content of the entry is empty."
    missingEntryContentInclusion = "Invalid theme. Missing entry content inclusion in entry.html and/or rssEntry.html"
    unknownLanguage="Pygments: {0}: Unknown language."

