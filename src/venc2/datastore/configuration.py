#! /usr/bin/python3

#   Copyright 2016, 2017 Denis Salem

#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

import os
import yaml

from venc2.helpers import die
from venc2.helpers import notify
from venc2.l10n import messages

def get_blog_configuration():
    try:
        blog_configuration = yaml.load(open(os.getcwd()+"/blog_configuration.yaml",'r').read())
        
        mandatory_fields = [
            "blog_name",
            "text_editor",
            "date_format",
	    "author_name",
	    "blog_description",
	    "blog_keywords",
	    "author_description",
	    "license",
	    "blog_url",
            "ftp_host",
	    "blog_language",
	    "author_email",
	    "entries_per_pages",
            "columns",
	    "rss_thread_lenght",
            "reverse_thread_order",
            "markup_language",
            "disable_threads",
            "disable_main_thread",
            "disable_archives",
            "disable_categories",
            "disable_single_entries",
            "path_encoding"
        ]

        everything_is_okay = True
        for field in mandatory_fields:
            if not field in blog_configuration.keys():
                everything_is_okay = False
                notify(messages.missing_mandatory_field_in_blog_conf.format(field),"RED")
        
        mandatory_fields = [
            "index_file_name",
	    "category_directory_name",
	    "dates_directory_name",
	    "entry_file_name",
	    "rss_file_name",
            "ftp",
            "entries_sub_folders",
            "categories_sub_folders",
            "dates_sub_folders"
        ]

        for field in mandatory_fields:
            if not field in blog_configuration["path"].keys():
                everything_is_okay = False
                notify(messages.missing_mandatory_field_in_blog_conf.format(field),"RED")

        if not blog_configuration["markup_language"] in ["none", "Markdown", "reStructuredText"]:
                everything_is_okay = False
                notify(messages.unknown_markup_language.format(blog_configuration["markup_language"], "blog_configuration.yaml"),"RED")

        if not everything_is_okay:
            exit()

        return blog_configuration

    except FileNotFoundError:
        die(messages.no_blog_configuration)

    except PermissionError:
        die(messages.no_blog_configuration)

    except yaml.scanner.ScannerError:
        die(messages.possible_malformed_blogC_configuration)
