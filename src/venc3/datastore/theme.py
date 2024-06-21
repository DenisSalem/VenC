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
theme = None

class Theme:
    def __init__(self, theme_folder):
        self.theme_folder = theme_folder
        from venc3.exceptions import MalformedPatterns
        from venc3.exceptions import VenCException
        from venc3.patterns.processor import PatternTree
        
        try:
            self.header = PatternTree(open(theme_folder+"chunks/header.html",'r').read(), "header.html")
            self.footer = PatternTree(open(theme_folder+"chunks/footer.html",'r').read(), "footer.html")
            self.rss_header = PatternTree(open(theme_folder+"chunks/rssHeader.xml",'r').read(), "rssHeader.html")
            self.rss_footer = PatternTree(open(theme_folder+"chunks/rssFooter.xml",'r').read(), "rssFooter.html")
            self.atom_header = PatternTree(open(theme_folder+"chunks/atomHeader.xml",'r').read(), "atomHeader.html")
            self.atom_footer = PatternTree(open(theme_folder+"chunks/atomFooter.xml",'r').read(), "atomFooter.html")

            for attr_name in dir(self):
                attr = getattr(self, attr_name)
                if type(attr) == PatternTree:
                    from venc3.patterns.processor import Pattern
                    matchs = attr.match_pattern_flags(Pattern.FLAG_ENTRY_RELATED)
                    if len(matchs):
                        from venc3.exceptions import PatternsCannotBeUsedHere
                        raise PatternsCannotBeUsedHere(matchs)

            self.entry = PatternTree(open(theme_folder+"chunks/entry.html",'r').read(), "entry.html")

            self.rss_entry = PatternTree(open(theme_folder+"chunks/rssEntry.xml",'r').read(),"rssEntry.xml")
            self.atom_entry = PatternTree(open(theme_folder+"chunks/atomEntry.xml",'r').read(),"atomEntry.xml")

            self.enable_entry_content = self.entry.match_get_entry_content | self.rss_entry.match_get_entry_content | self.atom_entry.match_get_entry_content
            self.enable_entry_preview = self.entry.match_get_entry_preview | self.rss_entry.match_get_entry_preview | self.atom_entry.match_get_entry_preview

            self.audio = open(theme_folder+"chunks/audio.html",'r').read()
            self.video = open(theme_folder+"chunks/video.html",'r').read()
    
        except VenCException as e:
            e.die()

        except FileNotFoundError as e:
            from venc3.exceptions import VenCException
            VenCException(("file_not_found", e.filename)).die()

def init_theme(theme_name=''):
    import os
    from venc3 import package_data_path
    from venc3.datastore import datastore

    # Setting up paths
    theme_folder = "theme/"
    themes_locations = [package_data_path+"/themes/"]+(datastore.blog_configuration["paths"]["themes_locations"] if datastore.blog_configuration != None else [])
    
    if len(theme_name):
        for themes_location in themes_locations:
            if os.path.isdir(themes_location+'/'+theme_name):
                theme_folder = themes_location+'/'+theme_name+"/"
                break;
                
        if theme_folder == "theme/" and len(theme_name):
            from venc3.prompt import die
            die(("theme_doesnt_exists", theme_name))
    
    if not os.path.isdir(theme_folder):
        from venc3.prompt import die
        die(("file_not_found", theme_folder))
    
    # Override blog configuration
    if "config.yaml" in os.listdir(theme_folder) and not os.path.isdir(theme_folder+"/config.yaml"):
        import yaml
        config = yaml.load(open(theme_folder+"/config.yaml",'r').read(), Loader=yaml.FullLoader)
        if "override" in config.keys():
            from venc3.prompt import notify
            if type(config["override"]) == dict:
                for param in config["override"].keys():
                    notify(
                      (
                          "the_following_is_overriden",
                          param,
                          config["override"][param],
                          theme_folder+"config.yaml"
                      ),
                      color="YELLOW"
                    )
    
                    if type(config["override"][param]) == dict and param in datastore.blog_configuration.keys() and type(datastore.blog_configuration[param]) == dict:
                        datastore.blog_configuration[param].update(config["override"][param])
                    
                    else:
                        datastore.blog_configuration[param] = config["override"][param]
            else:
                notify(("field_is_not_of_type", "override", "config.yaml", "dict"), color="YELLOW")
                

        if "assets_dependencies" in config.keys() and type(config["assets_dependencies"]) == list:
            global theme_assets_dependencies
            theme_assets_dependencies += [str(item) for item in config["assets_dependencies"] if len(str(item))]
                
    global theme
    theme = Theme(theme_folder)
