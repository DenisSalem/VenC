#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
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

BLOG_CONFIGURATION = None

def setup_sub_folder(blog_configuration, key):
    from venc3.helpers import quirk_encoding
    try:
        path = quirk_encoding(blog_configuration["path"][key])
            
    except UnicodeEncodeError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("encoding_error_in_sub_folder_path", key))
                    
    blog_configuration["path"][key] = (path if path[-1] == '/' else path+'/' ) if (path != '/' and len(path)) else ''

def get_blog_configuration():
    global BLOG_CONFIGURATION
    if BLOG_CONFIGURATION != None:
        return BLOG_CONFIGURATION
  
    import os
    import yaml
    
    try:
        blog_configuration = yaml.load(
            open(
                os.getcwd()+"/blog_configuration.yaml",
                'r'
            ).read(),
            Loader=yaml.FullLoader
        )
        
        mandatory_fields = [
            "blog_name",
            "blog_url",
            "date_format",
            "ftp_host",
            "entries_per_pages",
            "columns",
            "feed_length",
            "reverse_thread_order",
            "markup_language",
            "disable_main_thread",
            "disable_archives",
            "disable_categories",
            "disable_chapters",
            "disable_single_entries",
            "code_highlight_css_override",
            "server_port",
            "disable_rss_feed",
            "disable_atom_feed",
            "sort_by",
        ]

        for field in mandatory_fields:
            if not field in blog_configuration.keys():
                from venc3.prompt import die
                die(("missing_mandatory_field_in_blog_conf", field))
                
        if "blog_keywords" in blog_configuration.keys() and type(blog_configuration["blog_keywords"]) != list and not blog_configuration["blog_keywords"] == None:
            from venc3.prompt import die
            die(("blog_metadata_is_not_a_list", "blog_keywords"))
        
        mandatory_fields = [
            "index_file_name",
            "category_directory_name",
            "chapter_directory_name",
            "archives_directory_name",
            "entry_file_name",
            "rss_file_name",
            "atom_file_name",
            "ftp",
            "entries_sub_folders",
            "categories_sub_folders",
            "archives_sub_folders",
            "chapters_sub_folders",
        ]

        for field in mandatory_fields:
            if not field in blog_configuration["path"].keys():
                from venc3.prompt import die
                die(("missing_mandatory_field_in_blog_conf", field))
                
            elif not field in ["index_file_name","ftp","rss_file_name","atom_file_name","entry_file_name","archives_directory_name"]:
                setup_sub_folder(blog_configuration, field)
                
        if not "https://schema.org" in blog_configuration.keys():
            blog_configuration["https://schema.org"] = {}
            
        if not blog_configuration["markup_language"] in ["none", "Markdown", "reStructuredText"]:
            from venc3.prompt import die
            die(("unknown_markup_language", blog_configuration["markup_language"], "blog_configuration.yaml"))

        if (not "sort_by" in blog_configuration.keys() ) or blog_configuration["sort_by"] in ['', None]:
            blog_configuration["sort_by"] = "id"

        if blog_configuration["blog_url"][-1:] == '/':
            blog_configuration["blog_url"] = blog_configuration["blog_url"][:-1]

        if "disable_threads" in blog_configuration.keys() and type(blog_configuration["disable_threads"]) != list and blog_configuration["disable_threads"] != None:
            from venc3.prompt import die
            die(("blog_metadata_is_not_a_list", "disable_threads"))
        else:
            blog_configuration["disable_threads"] = []

        if not "pipe_flow" in blog_configuration.keys():
            blog_configuration["pipe_flow"] = 512
            
        BLOG_CONFIGURATION = blog_configuration
        return BLOG_CONFIGURATION

    except FileNotFoundError:
        from venc3.prompt import die
        die(("no_blog_configuration",))

    except PermissionError:
        from venc3.prompt import die
        die(("no_blog_configuration",))

    except yaml.scanner.ScannerError as e:
        from venc3.prompt import die, notify
        notify(("in_", "blog_configuration.yaml"), color="RED")
        die(("exception_place_holder", str(e)))

    except VenCException as e:
        e.die()
