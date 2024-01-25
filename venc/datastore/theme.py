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

import os
import pkgutil
import sys

import yaml
from venc.exceptions import PatternsCannotBeUsedHere, VenCException
from venc.patterns.processor import Pattern, PatternTree
from venc.prompt import die

theme_assets_dependencies = list()
theme = None


class Theme:
    def __init__(self, theme_name):
        self.theme_folder = os.path.join(
            os.path.dirname(sys.modules["venc"].__file__), "data", "themes", theme_name
        )
        try:
            for attr, file_, check_match in [
                ("header", "header.html", True),
                ("footer", "footer.html", True),
                ("rss_header", "rssHeader.xml", True),
                ("rss_footer", "rssFooter.xml", True),
                ("atom_header", "atomHeader.xml", True),
                ("atom_footer", "atomFooter.xml", True),
                ("entry", "entry.html", False),
                ("rss_entry", "rssEntry.xml", False),
                ("atom_entry", "atomEntry.xml", False),
                ("audio", "audio.html", False),
                ("video", "video.html", False),
            ]:
                setattr(
                    self,
                    attr,
                    PatternTree(
                        str(
                            pkgutil.get_data(
                                "venc", f"data/themes/{theme_name}/chunks/{file_}"
                            )
                        )
                    ),
                )
                if check_match:
                    matchs = getattr(self, attr).match_pattern_flags(
                        Pattern.FLAG_ENTRY_RELATED
                    )
                    if len(matchs):
                        raise PatternsCannotBeUsedHere(matchs)

            self.enable_entry_content = (
                self.entry.match_get_entry_content
                | self.rss_entry.match_get_entry_content
                | self.atom_entry.match_get_entry_content
            )
            self.enable_entry_preview = (
                self.entry.match_get_entry_preview
                | self.rss_entry.match_get_entry_preview
                | self.atom_entry.match_get_entry_preview
            )

        except VenCException as e:
            e.die()

        except FileNotFoundError as e:
            raise VenCException(("file_not_found", e.filename)).die() from e


def init_theme(theme_name=""):
    # Override blog configuration
    config_file = pkgutil.get_data("venc", f"data/themes/{theme_name}/config.yaml")
    if config_file is None:
        die(("file_not_found", f"venc/data/themes/{theme_name}/config.yaml"))
    config = yaml.load(config_file, Loader=yaml.FullLoader)

    if "override" in config.keys():
        from venc.prompt import notify

        if isinstance(config["override"], dict):
            from venc.datastore import datastore

            for param in config["override"].keys():
                notify(
                    (
                        "the_following_is_overriden",
                        param,
                        config["override"][param],
                        "config.yaml",
                    ),
                    color="YELLOW",
                )

                if (
                    isinstance(config["override"][param], dict)
                    and param in datastore.blog_configuration
                    and isinstance(datastore.blog_configuration[param], dict)
                ):
                    datastore.blog_configuration[param].update(
                        config["override"][param]
                    )

                else:
                    datastore.blog_configuration[param] = config["override"][param]
        else:
            notify(
                ("field_is_not_of_type", "override", "config.yaml", "dict"),
                color="YELLOW",
            )

    if "assets_dependencies" in config.keys() and isinstance(
        config["assets_dependencies"], list
    ):
        global theme_assets_dependencies
        theme_assets_dependencies += [
            str(item) for item in config["assets_dependencies"] if len(str(item))
        ]

    global theme
    theme = Theme(theme_name)
