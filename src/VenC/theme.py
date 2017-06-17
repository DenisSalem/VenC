#! /usr/bin/python3

from VenC.l10n import Messages

ThemesDescriptor = {
    "dummy": {"columns":1,"_themeDescription_": Messages.themeDescriptionDummy},
    "gentle": {"columns":1,"_themeDescription_": Messages.themeDescriptionGentle},
    "tessellation": {"columns":3,"_themeDescription_": Messages.themeDescriptionTessellation},
}

class Theme:
    def __init__(self, themeFolder):
        self.header = str()
        self.footer = str()
        self.entry = str()
        self.rssHeader = str()
        self.rssFooter = str()
        self.rssEntry = str()

        try:
            self.header = open(themeFolder+"chunks/header.html",'r').read()
            self.footer = open(themeFolder+"chunks/footer.html",'r').read()
            self.entry = open(themeFolder+"chunks/entry.html",'r').read()
            self.rssHeader = open(themeFolder+"chunks/rssHeader.html",'r').read()
            self.rssFooter = open(themeFolder+"chunks/rssFooter.html",'r').read()
            self.rssEntry = open(themeFolder+"chunks/rssEntry.html",'r').read()

        except FileNotFoundError as e:
            Die(Messages.fileNotFound.format(str(e.filename)))
