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

def sanitize_optional_fields(blog_configuration):
    fields = {
        "blog_keywords": list,
        "blog_url": str, # TODO: check when used
        "code_highlight_css_override": bool,
        "disable_archives": bool,
        "disable_atom_feed": bool,
        "disable_categories": bool,
        "disable_chapters": bool,
        "disable_infinite_scroll" : bool,
        "disable_main_thread": bool,
        "disable_rss_feed" : bool,
        "disable_single_entries": bool,
        "disable_threads": list,
        "ftp_host": str, # TODO: check when used
        "path_encoding": str, 
        "parallel_processing": int,
        "pipe_flow": int,
        "server_port": int,
        "sort_by": str,
        "text_editor": list # TODO: check when used
    }

    for field in fields.keys():
        if field in blog_configuration.keys():
            if not type(blog_configuration[field]) == fields[field]:
                from venc3.prompt import die
                die(("field_is_not_of_type", field, "blog_configuration.yaml", fields[field].__name__))
                
    if not type(blog_configuration["paths"]["ftp"]) == str:  # TODO: check when used
        from venc3.prompt import die
        die(("field_is_not_of_type", field, "blog_configuration.yaml", fields[field].__name__))
                
def setup_optional_fields(blog_configuration):
        sanitize_optional_fields(blog_configuration)
    
        if not "sort_by" in blog_configuration.keys():
            blog_configuration["sort_by"] = "id"

        if not "pipe_flow" in blog_configuration.keys():
            blog_configuration["pipe_flow"] = 512

        if not "path_encoding" in blog_configuration.keys():
            blog_configuration["path_encoding"] = "" # TODO: plz, what da fuck is this shit ?

        if not "disable_threads" in blog_configuration.keys():
            blog_configuration["disable_threads"] = []

        if not "parallel_processing" in blog_configuration.keys():
            blog_configuration["parallel_processing"] = 1

        if not "server_port" in blog_configuration.keys():
            blog_configuration["server_port"] = 8888
                        
        fields_set_to_false = [
          "code_highlight_css_override",
          "disable_archives",
          "disable_atom_feed",
          "disable_categories",
          "disable_chapters",
          "disable_main_thread",
          "disable_rss_feed",
          "disable_single_entries",
        ]
        
        for field in fields_set_to_false:
            if not field in blog_configuration.keys():
                blog_configuration[field] = False
                
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
        
        # TODO: Not mandatory anymore
        # - server port
        # - ftp_host
        # - ftp
        # - text_editor
        
        #TODO: update doc about mandatory fields

        mandatory_fields = {
            "blog_name" : str,
            "date_format" : str,
            "entries_per_pages" : int,
            "columns" : int,
            "feed_length" : int,
            "reverse_thread_order" : bool,
            "markup_language" : str,
            "paths": dict
        }

        for field in mandatory_fields.keys():
            if not field in blog_configuration.keys():
                from venc3.prompt import die
                die(("missing_mandatory_field_in_blog_conf", field))
            
            if not type(blog_configuration[field]) == mandatory_fields[field]:
                from venc3.prompt import die
                die(("field_is_not_of_type", field, "blog_configuration.yaml", mandatory_fields[field].__name__))
        
        mandatory_fields = {
            "index_file_name" : str,
            "category_directory_name" : str,
            "chapter_directory_name" : str,
            "archives_directory_name" : str,
            "entry_file_name" : str,
            "rss_file_name" : str,
            "atom_file_name" : str,
            "entries_sub_folders" : str,
            "categories_sub_folders" : str,
            "archives_sub_folders" : str,
            "chapters_sub_folders" : str,
        }

        for field in mandatory_fields:
            if not field in blog_configuration["paths"].keys():
                from venc3.prompt import die
                die(("missing_mandatory_field_in_blog_conf", field))
                
            if not type(blog_configuration["paths"][field]) == mandatory_fields[field]:
                from venc3.prompt import die
                die(("field_is_not_of_type", field, "blog_configuration.yaml", mandatory_fields[field].__name__))

        if not blog_configuration["markup_language"] in ["none", "Markdown", "reStructuredText", "asciidoc"]:
            from venc3.prompt import die
            die(("unknown_markup_language", blog_configuration["markup_language"], "blog_configuration.yaml"))
        
        setup_optional_fields(blog_configuration)
                        
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
