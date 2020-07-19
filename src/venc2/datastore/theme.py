#! /usr/bin/env python3

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

from venc2.datastore.entry import EntryWrapper
from venc2.prompt import die
from venc2.l10n import messages
from venc2.patterns.processor import ProcessedString
from venc2.patterns.exceptions import IllegalUseOfEscape

class Theme:
    def __init__(self, theme_folder):
        try:
            self.header = ProcessedString(open(theme_folder+"chunks/header.html",'r').read(), "header.html", True)
            self.footer = ProcessedString(open(theme_folder+"chunks/footer.html",'r').read(), "footer.html", True)
            self.rss_header = ProcessedString(open(theme_folder+"chunks/rssHeader.xml",'r').read(), "rssHeader.html", True)
            self.rss_footer = ProcessedString(open(theme_folder+"chunks/rssFooter.xml",'r').read(), "rssFooter.html", True)
            self.atom_header = ProcessedString(open(theme_folder+"chunks/atomHeader.xml",'r').read(), "atomHeader.html", True)
            self.atom_footer = ProcessedString(open(theme_folder+"chunks/atomFooter.xml",'r').read(), "atomFooter.html", True)

            self.entry = EntryWrapper(open(theme_folder+"chunks/entry.html",'r').read(), "entry.html")
            self.rss_entry = EntryWrapper(open(theme_folder+"chunks/rssEntry.xml",'r').read(),"rssEntry.xml")
            self.atom_entry = EntryWrapper(open(theme_folder+"chunks/atomEntry.xml",'r').read(),"atomEntry.xml")
            
            self.audio = open(theme_folder+"chunks/audio.html",'r').read()
            self.video = open(theme_folder+"chunks/video.html",'r').read()

        except IllegalUseOfEscape as e:
            die(messages.illegal_use_of_escape.format(e.ressource))
            
        except FileNotFoundError as e:
            die(messages.file_not_found.format(str(e.filename)))

    def get_media(self, media_type, argv):
        source = ""
        for ext in argv[1].split(','):
            # Set media once, and get complete path later.
            source += str("<source src=\"{0}.{1}\" type=\""+media_type+"/{1}\">\n").format(argv[0].strip(), ext.strip())
        
        f = {}
        f["source"] = source
        f["poster"] = ""
        if media_type == "video":
            f["poster"] = argv[2].strip()

        return getattr(self, media_type).format(**f)

    def get_audio(self, argv):
        return self.get_media("audio", argv)

    def get_video(self, argv):
        return self.get_media("video", argv)

