#! /usr/bin/env python3

#    Copyright 2016, 2022 Denis Salem
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

theme_assets_dependencies = list()
theme_includes_dependencies = list()
theme = None

class Theme:
    def __init__(self, theme_folder):
        from venc2.exceptions import MalformedPatterns
        from venc2.patterns.processor import StringUnderProcessing
        try:
            self.header = StringUnderProcessing(open(theme_folder+"chunks/header.html",'r').read(), "header.html")
            self.footer = StringUnderProcessing(open(theme_folder+"chunks/footer.html",'r').read(), "footer.html")
            self.rss_header = StringUnderProcessing(open(theme_folder+"chunks/rssHeader.xml",'r').read(), "rssHeader.html")
            self.rss_footer = StringUnderProcessing(open(theme_folder+"chunks/rssFooter.xml",'r').read(), "rssFooter.html")
            self.atom_header = StringUnderProcessing(open(theme_folder+"chunks/atomHeader.xml",'r').read(), "atomHeader.html")
            self.atom_footer = StringUnderProcessing(open(theme_folder+"chunks/atomFooter.xml",'r').read(), "atomFooter.html")

            from venc2.datastore.entry import EntryWrapper
            self.entry = EntryWrapper(open(theme_folder+"chunks/entry.html",'r').read(), "entry.html")
            self.rss_entry = EntryWrapper(open(theme_folder+"chunks/rssEntry.xml",'r').read(),"rssEntry.xml")
            self.atom_entry = EntryWrapper(open(theme_folder+"chunks/atomEntry.xml",'r').read(),"atomEntry.xml")
            
            self.audio = open(theme_folder+"chunks/audio.html",'r').read()
            self.video = open(theme_folder+"chunks/video.html",'r').read()
    
        except MalformedPatterns as e:
            e.die()

        except FileNotFoundError as e:
            from venc2.prompt import die
            from venc2.l10n import messages
            die(messages.file_not_found.format(str(e.filename)))

def init_theme(theme_name=''):
    import os

    # Setting up paths
    theme_folder = "theme/"
    themes_folder = os.path.expanduser("~")+"/.local/share/VenC/themes/"
    if len(theme_name):
        if os.path.isdir(themes_folder+theme_name):
            theme_folder = themes_folder+theme_name+"/"
            
        else:
            from venc2.prompt import die
            from venc2.l10n import messages
            die(messages.theme_doesnt_exists.format(theme_name))
    
    if not os.path.isdir(theme_folder):
        from venc2.prompt import die
        from venc2.l10n import messages
        die(messages.file_not_found.format(theme_folder))
    
    # Override blog configuration
    if "config.yaml" in os.listdir(theme_folder) and not os.path.isdir(themes_folder+"/config.yaml"):
        import yaml
        config = yaml.load(open(theme_folder+"/config.yaml",'r').read(), Loader=yaml.FullLoader)
        if "override" in config.keys() and type(config["override"]) == dict:
            # TODO : Be explicit to user about which value are updated
            from venc2.datastore import datastore
            for param in config["override"].keys():
                if type(config["override"][param]) == dict and param in datastore.blog_configuration.keys() and type(datastore.blog_configuration[param]) == dict:
                    datastore.blog_configuration[param].update(config["override"][param])
                
                else:
                    datastore.blog_configuration[param] = config["override"][param]

        if "assets_dependencies" in config.keys() and type(config["assets_dependencies"]) == list:
            global theme_assets_dependencies
            theme_assets_dependencies = config["assets_dependencies"]
            
        if "includes_dependencies" in config.keys() and type(config["includes_dependencies"]) == list:
            global theme_includes_dependencies
            for include_file in config["includes_dependencies"]:
                theme_includes_dependencies.append(include_file)
                
    global theme
    theme = Theme(theme_folder)
