#! /usr/bin/python3


from VenC.constants import MsgFormat
from VenC.constants import ThemesDescriptor
from VenC.l10n import Messages;

def PrintVersion(argv):
    print("VenC 2.0.0")

def PrintHelp(argv=None):
    print("-v\t--version")
    print("-nb\t--new-blog <\""+Messages.argBlogName.format("1")+"\"> [\""+Messages.argBlogName.format("2")+"\" ... ]")
    print("-ne\t--new-entry <\""+Messages.argEntryName+"\"> [\""+Messages.argTemplateName+"\"]")
    print("-xb\t--export-blog ["+Messages.themeName+"]")
    print("-ex\t--edit-and-xport <\""+Messages.argInputFilename+"\">")
    print("-xftp\t--export-via-ftp")
    print("-rc\t--remote-copy")
    print("-h\t--help")
    print("-t\t--themes")
    print("-it\t--install-themes <"+Messages.themeName+">")

def PrintThemes(argv=None):
    for theme in ThemesDescriptor.keys():
        print ("- "+MsgFormat["GREEN"]+theme+MsgFormat["END"]+":", ThemesDescriptor[theme]["_themeDescription_"]+"\n")
