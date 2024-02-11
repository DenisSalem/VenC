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
        "blg_url": str,
        "pipe_flow": int,
        "sort_by": str,
    }
    
def setup_optional_fields(blog_configuration):
        sanitize_optional_fields(blog_configuration)
    
        if (not "sort_by" in blog_configuration.keys() ) or blog_configuration["sort_by"] in ['', None]:
            blog_configuration["sort_by"] = "id"

        if not "pipe_flow" in blog_configuration.keys():
            blog_configuration["pipe_flow"] = 512
            
        if blog_configuration["blog_url"][-1:] == '/':
            blog_configuration["blog_url"] = blog_configuration["blog_url"][:-1]
            
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
        # - Server port
        # - ftp stufff
        # - blog_url
        # - code_highlight_css_override"
        # - path_encoding # TODO looks like shit to me
        # - server_port":                  8888,
        # - sort_by":                      "id",
        # - parallel_processing": 1
        # - code_highlight_css_override":  False,
        # - disable_threads":              [],
        # - disable_archives":             False,
        # - disable_categories":           False,
        # - disable_chapters":             False,
        # - disable_single_entries":       False,
        # - disable_main_thread":          False,
        # - disable_rss_feed":             False,
        # - disable_atom_feed":            False,
        # - text_editor":                  ["nano"],
        mandatory_fields = {
            "blog_name" : str,
            "date_format" : str,
            "entries_per_pages" : int,
            "columns" : int,
            "feed_length" : int,
            "reverse_thread_order" : bool,
            "markup_language" : str,
            "path": dict
        }

        for field in mandatory_fields.keys():
            if not field in blog_configuration.keys():
                from venc3.prompt import die
                die(("missing_mandatory_field_in_blog_conf", field))
            
            if not type(blog_configuration[field]) == mandatory_fields[field]:
                from venc3.prompt import die
                die(("field_is_not_of_type", field, "blog_configuration.yaml", mandatory_fields[field].__name__))
                
        if "blog_keywords" in blog_configuration.keys() and type(blog_configuration["blog_keywords"]) != list and not blog_configuration["blog_keywords"] == None:
            from venc3.prompt import die
            die(("blog_metadata_is_not_a_list", "blog_keywords"))
        
        #TODO: update doc about mandatory fields
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

        if "disable_threads" in blog_configuration.keys() and type(blog_configuration["disable_threads"]) != list and blog_configuration["disable_threads"] != None:
            from venc3.prompt import die
            die(("blog_metadata_is_not_a_list", "disable_threads"))
            
        else:
            blog_configuration["disable_threads"] = []


            
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
