#! /usr/bin/env python3

#    Copyright 2016, 2021 Denis Salem
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

import subprocess
import time

from venc3.exceptions import VenCException, MalformedPatterns
from venc3.helpers import rm_tree_error_handler
from venc3.l10n import messages
from venc3.patterns.non_contextual import theme_includes_dependencies
from venc3.patterns.processor import Processor, PatternNode
from venc3.prompt import notify

start_timestamp = time.time()

def copy_recursively(src, dest):
    import errno, os, shutil
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
                
def export_and_remote_copy(theme_name=''):
    export_blog(theme_name='')
    from venc3.commands.remote import remote_copy
    remote_copy()

def setup_pattern_processor(parallel=False):        
    processor = Processor()
    from venc3.patterns.patterns_map import patterns_map
    processor.set_patterns(patterns_map.non_contextual["blog"])
    processor.set_patterns(patterns_map.non_contextual["entries"])
    processor.set_patterns(patterns_map.non_contextual["extra"])
    if not parallel:
        processor.set_patterns(patterns_map.non_contextual["non_parallelizable"])

    return processor
            
def process_non_parallelizables(datastore, patterns_map, thread_params):
    notify("├─ "+messages.process_non_parallelizable)
    pattern_processor = Processor()
    pattern_processor.set_patterns(patterns_map.non_contextual["non_parallelizable"])
    from venc3.patterns.processor import PatternNode
    for l in thread_params["non_parallelizable"]:
        for entry_index in l:
            entry = datastore.entries[entry_index]
            if entry.preview.has_non_parallelizables:
                pattern_processor.process(entry.preview, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
            
            if entry.content.has_non_parallelizables:
                pattern_processor.process(entry.content, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
            
            if entry.html_wrapper.processed_string.has_non_parallelizables:
                pattern_processor.process(entry.html_wrapper.processed_string, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
                
            if entry.rss_wrapper.processed_string.has_non_parallelizables:
                pattern_processor.process(entry.rss_wrapper.processed_string, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
                
            if entry.atom_wrapper.processed_string.has_non_parallelizables:
                pattern_processor.process(entry.atom_wrapper.processed_string, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
                    
def process_non_contextual_patterns():
    from venc3.datastore import datastore
    pattern_processor = setup_pattern_processor(datastore.workers_count > 1)
    from venc3.datastore.theme import theme
    from venc3.patterns.third_party_wrapped_features.pygmentize import code_highlight
    from venc3.patterns.patterns_map import patterns_map
    from venc3.parallelism.export_entries import worker
    
    if datastore.workers_count > 1:
        # There we setup chunks of entries send to workers throught dispatchers
        datastore.chunks_len = (len(datastore.entries)//datastore.workers_count)+1

        from venc3.parallelism.export_entries import split_datastore, thread_params

        thread_params["code_highlight_includes"] = [{} for i in range(0, datastore.workers_count)]
        thread_params["non_parallelizable"] = [[] for i in range(0, datastore.workers_count)]
        thread_params["worker_context_chunks"] = split_datastore(datastore)
    
        from venc3.parallelism import Parallelism
        from venc3.parallelism.export_entries import finish, dispatcher
        parallelism = Parallelism(
            worker,
            finish,
            dispatcher,
            datastore.workers_count,
            datastore.blog_configuration["pipe_flow"],
            (
                True,
                datastore,
                theme,
                code_highlight,
                patterns_map,
                pattern_processor
            )
        )
        parallelism.start()
        try:
            parallelism.join()
            
        except VenCException as e:
            e.die()

    if not datastore.blog_configuration["disable_chapters"]:
        for entry in datastore.entries:
            datastore.update_chapters(entry)
    
        datastore.build_chapter_indexes()      

    if datastore.workers_count == 1:
        worker(
            0,
            None,
            None,
            (
                False,
                datastore,
                theme,
                code_highlight,
                patterns_map,
                pattern_processor
            )
        )

    try:
        if datastore.workers_count > 1:
            process_non_parallelizables(datastore, patterns_map, thread_params)
            pattern_processor.set_patterns(patterns_map.non_contextual["non_parallelizable"])
        
        pattern_processor.process(theme.header, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
        pattern_processor.process(theme.footer, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
        pattern_processor.process(theme.rss_header, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE) 
        pattern_processor.process(theme.rss_footer, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
        pattern_processor.process(theme.atom_header, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE)
        pattern_processor.process(theme.atom_footer, PatternNode.FLAG_NON_CONTEXTUAL | PatternNode.FLAG_NON_PARALLELIZABLE) 

    except VenCException as e:    
        e.die()

# TODO: https://openweb.eu.org/articles/comment-construire-un-flux-atom
def export_blog(theme_name=''):
    from venc3.datastore import init_datastore
    datastore = init_datastore()
    
    notify("├─ "+messages.pre_process)
    
    from venc3.datastore.theme import init_theme
    init_theme(theme_name)
    from venc3.patterns.third_party_wrapped_features.pygmentize import init_code_highlight
    init_code_highlight()
    from venc3.patterns.patterns_map import init_pattern_map
    init_pattern_map()
    
    process_non_contextual_patterns()
    if not datastore.blog_configuration["disable_single_entries"]:
        notify("├─ "+messages.link_entries)
        # Add required link between entries
        entries = datastore.entries
        for entry_index in range(0, len(entries)):
            current_entry = entries[entry_index]
            if entry_index > 0:
                entries[entry_index-1].next_entry = current_entry
                current_entry.previous_entry = entries[entry_index-1]

    # cleaning directory
    import os, shutil
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")


    try:
        # Starting second pass and exporting
        from venc3.threads.main import MainThread
        thread = MainThread()
        thread.do()
        if not datastore.blog_configuration["disable_archives"]:
            from venc3.threads.archives import ArchivesThread
            thread = ArchivesThread()
            thread.do()
    
        if not datastore.blog_configuration["disable_categories"]:
            from venc3.threads.categories import CategoriesThread
            thread = CategoriesThread()
            thread.do()
    
        if not datastore.blog_configuration["disable_single_entries"]:
            from venc3.threads.entries import EntriesThread
            thread = EntriesThread()
            thread.do()
    
        if not datastore.blog_configuration["disable_chapters"]:            
            from venc3.threads.chapters import ChaptersThread
            thread = ChaptersThread()
            thread.do()
            
    except VenCException:
        if not e.context:
            e.context = string_under_processing
            e.extra = string_under_processing.flatten(highlight_pattern=pattern)
    
        e.die()
        
    # Copy assets and extra files
    notify('└─ '+messages.copy_assets_and_extra_files)
    from venc3.patterns.third_party_wrapped_features.pygmentize import code_highlight
    from venc3.datastore.theme import theme, theme_assets_dependencies
    code_highlight.export_style_sheets()
    copy_recursively("extra/","blog/")
    copy_recursively(theme.theme_folder+"assets/","blog/")
    for depenpency in theme_assets_dependencies:
        try:
            shutil.copyfile(os.path.expanduser("~")+"/.local/share/VenC/themes_assets/"+depenpency, "blog/"+depenpency)
        
        except IsADirectoryError:
            shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes_assets/"+depenpency, "blog/"+depenpency)

        except FileNotFoundError as e:
            notify(messages.file_not_found.format(e.filename), color="YELLOW")
    
    notify(messages.task_done_in_n_seconds.format(round(time.time() - start_timestamp,6)))

def edit_and_export(argv):    
    if len(argv) != 1:
        from venc3.helpers import die
        die(messages.missing_params.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([datastore.blog_configuration["text_editor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        from venc3.helpers import die
        die(messages.unknown_text_editor.format(datastore.blog_configuration["text_editor"]))
    
    except:
        raise
    
    export_blog()
