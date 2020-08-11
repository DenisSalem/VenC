#! /usr/bin/env python3

#    Copyright 2016, 2019 Denis Salem
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

from copy import deepcopy
import os
import shutil
import subprocess
import time

from venc2.commands.remote import remote_copy
from venc2.datastore import DataStore
from venc2.datastore.theme import Theme
from venc2.helpers import die
from venc2.prompt import notify
from venc2.helpers import rm_tree_error_handler 
from venc2.l10n import messages
from venc2.patterns.non_contextual import theme_includes_dependencies
from venc2.patterns.code_highlight import CodeHighlight
from venc2.patterns.exceptions import MalformedPatterns
from venc2.patterns.patterns_map import PatternsMap
from venc2.patterns.processor import Processor
from venc2.patterns.processor import ProcessedString

# Initialisation of environment
start_timestamp = time.time()
datastore = None
code_highlight = None

theme_assets_dependencies = []

def copy_recursively(src, dest):
    import errno
    for filename in os.listdir(src):
        try:
            shutil.copytree(src+filename, dest+filename)
    
        except shutil.Error as e:
            notify(messages.directory_not_copied % e, "YELLOW")

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(src+filename, dest+filename)

            else:
                notify(messages.directory_not_copied % e, "YELLOW")
                
def export_and_remote_copy(argv=list()):
    export_blog(argv)
    remote_copy()

def init_theme(argv):
    theme_folder = "theme/"
    themes_folder = os.path.expanduser("~")+"/.local/share/VenC/themes/"
    if len(argv) == 1:
        if os.path.isdir(themes_folder+argv[0]):
            theme_folder = os.path.expanduser("~")+"/.local/share/VenC/themes/"+argv[0]+"/"
            
        else:
            die(messages.theme_doesnt_exists.format(argv[0]))
    
    if not os.path.isdir(theme_folder):
        die(messages.file_not_found.format(theme_folder))
        
    if "config.yaml" in os.listdir(theme_folder) and not os.path.isdir(themes_folder+"/config.yaml"):
        import yaml
        config = yaml.load(open(theme_folder+"/config.yaml",'r').read(), Loader=yaml.FullLoader)
        if "override" in config.keys() and type(config["override"]) == dict:
            # TODO : Be explicit about which value are updated
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
            append = theme_includes_dependencies.append
            for include_file in config["includes_dependencies"]:
                append(include_file)
                
    try:
        return Theme(theme_folder), theme_folder
        
    except MalformedPatterns as e:
        from venc2.helpers import handle_malformed_patterns
        handle_malformed_patterns(e)

def setup_pattern_processor(pattern_map):
    processor = Processor()
    for pattern_name in pattern_map.non_contextual["entries"].keys():
        processor.set_function(pattern_name, pattern_map.non_contextual["entries"][pattern_name])
    
    for pattern_name in pattern_map.non_contextual["blog"].keys():
        processor.set_function(pattern_name, pattern_map.non_contextual["blog"][pattern_name])
        
    for pattern_name in pattern_map.non_contextual["extra"].keys():
        processor.set_function(pattern_name, pattern_map.non_contextual["extra"][pattern_name])
    
    for pattern_name in pattern_map.contextual["names"].keys():
        processor.blacklist.append(pattern_name)
        
    for pattern_name in pattern_map.contextual["functions"].keys():
        processor.blacklist.append(pattern_name)
        
    for pattern_name in pattern_map.keep_appart_from_markup:
        processor.keep_appart_from_markup.append(pattern_name)

    processor.blacklist.append("Escape")
    return processor

def process_non_contextual_patterns(pattern_processor, theme):
    for entry in datastore.get_entries():
        if hasattr(entry, "markup_language"):
            markup_language = getattr(entry, "markup_language")

        else:
            markup_language = datastore.blog_configuration["markup_language"]
        
        pattern_processor.process(entry.preview)
        entry.preview.process_markup_language(markup_language)
        
        pattern_processor.process(entry.content)
        entry.content.process_markup_language(markup_language)

        entry.html_wrapper = deepcopy(theme.entry)
        pattern_processor.process(entry.html_wrapper.above)
        pattern_processor.process(entry.html_wrapper.below)
        
        entry.rss_wrapper = deepcopy(theme.rss_entry)
        pattern_processor.process(entry.rss_wrapper.above)
        pattern_processor.process(entry.rss_wrapper.below)
        
        entry.atom_wrapper = deepcopy(theme.atom_entry)
        pattern_processor.process(entry.atom_wrapper.above)
        pattern_processor.process(entry.atom_wrapper.below)
    
    pattern_processor.process(theme.header, no_markup=True)
    pattern_processor.process(theme.footer, no_markup=True) 
    pattern_processor.process(theme.rss_header, no_markup=True) 
    pattern_processor.process(theme.rss_footer, no_markup=True) 
    pattern_processor.process(theme.atom_header, no_markup=True)
    pattern_processor.process(theme.atom_footer, no_markup=True) 
    
def export_blog(argv=list()):
    global datastore
    if datastore == None:
        datastore = DataStore()
        
    global code_highlight
    code_highlight = CodeHighlight(datastore.blog_configuration["code_highlight_css_override"])
    theme, theme_folder = init_theme(argv)
    patterns_map = PatternsMap(datastore, code_highlight, theme)
    pattern_processor = setup_pattern_processor(patterns_map)
    
    notify("├─ "+messages.pre_process)

    process_non_contextual_patterns(pattern_processor, theme)
    # cleaning directory
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    # Starting second pass and exporting
    from venc2.threads.main import MainThread
    thread = MainThread(messages.export_main_thread, datastore, theme, patterns_map)
    thread.do()

    # ~ for entry in datastore.entries:
        # ~ if entry.id == 26:
            # ~ print(entry.content.string)

    if not datastore.blog_configuration["disable_archives"]:
        from venc2.threads.archives import ArchivesThread
        thread = ArchivesThread(messages.export_archives, datastore, theme, patterns_map)
        thread.do()

    if not datastore.blog_configuration["disable_categories"]:
        from venc2.threads.categories import CategoriesThread
        thread = CategoriesThread(messages.export_categories, datastore, theme, patterns_map)
        thread.do()

    if not datastore.blog_configuration["disable_single_entries"]:
        from venc2.threads.entries import EntriesThread
        thread = EntriesThread(messages.export_single_entries, datastore, theme, patterns_map)
        thread.do()

    if not datastore.blog_configuration["disable_chapters"]:
        from venc2.threads.chapters import ChaptersThread
        thread = ChaptersThread(messages.export_chapters, datastore, theme, patterns_map)
        thread.do()

    # Copy assets and extra files
    notify('└─ '+messages.copy_assets_and_extra_files)
    code_highlight.export_style_sheets()
    copy_recursively("extra/","blog/")
    copy_recursively(theme_folder+"assets/","blog/")
    for depenpency in theme_assets_dependencies:
        shutil.copyfile(os.path.expanduser("~")+"/.local/share/VenC/themes_assets/"+depenpency, "blog/"+depenpency)
    notify(messages.task_done_in_n_seconds.format(round(time.time() - start_timestamp,6)))


def edit_and_export(argv):
    global datastore
    datastore = DataStore()
    
    if len(argv) != 1:
        die(messages.missing_params.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([datastore.blog_configuration["text_editor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        die(messages.unknown_text_editor.format(datastore.blog_configuration["text_editor"]))
    
    except:
        raise
    
    export_blog()
