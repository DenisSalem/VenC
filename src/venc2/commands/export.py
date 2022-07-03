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

from copy import deepcopy
import shutil
import subprocess
import time

# ~ MIGHT BE DEPRECATED
from venc2.datastore.theme import Theme
from venc2.prompt import notify
from venc2.helpers import rm_tree_error_handler 
from venc2.l10n import messages
from venc2.markup_languages import process_markup_language
from venc2.patterns.non_contextual import theme_includes_dependencies
from venc2.patterns.code_highlight import CodeHighlight
from venc2.patterns.exceptions import MalformedPatterns
from venc2.patterns.patterns_map import PatternsMap
from venc2.patterns.processor import Processor
        
start_timestamp = time.time()

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
                
def export_and_remote_copy(theme_name=''):
    export_blog(theme_name='')
    from venc2.commands.remote import remote_copy
    remote_copy()

def setup_pattern_processor(parallel=False):        
    processor = Processor()
    from venc2.patterns.patterns_map import patterns_map
    processor.set_patterns(patterns_map.non_contextual["blog"])
    processor.set_patterns(patterns_map.non_contextual["entries"])
    processor.set_patterns(patterns_map.non_contextual["extra"])
        
    return processor

def process_non_parallelizables_pre_processed(run_pattern, entry_pre_processed):
    for np in entry_pre_processed.non_parallelizables:
        index = entry_pre_processed.string.index(np[0])
        new_chunk = run_pattern(np[1], np[2])
        entry_pre_processed.string = entry_pre_processed.string.replace(np[0], new_chunk)
        offset = len(new_chunk) - len(np[0])
        for e in entry_pre_processed.sorted_pattern_coordinates:
            if e.o > index:
                e.o+=offset
                
            if e.c > index:
              e.c+=offset
            
def process_non_parallelizables(datastore, patterns_map, thread_params):
    notify("├─ "+messages.process_non_parallelizable)
    pattern_processor = Processor()
    for pattern_name in patterns_map.non_contextual["non_parallelizable"].keys():
        pattern_processor.set_function(pattern_name, patterns_map.non_contextual["non_parallelizable"][pattern_name])
        
    pattern_processor.blacklist += patterns_map.contextual["names"].keys()
    pattern_processor.blacklist += patterns_map.contextual["functions"].keys()
    pattern_processor.blacklist.append("Escape")
    
    for l in thread_params["non_parallelizable"]:
        for entry_index in l:
            entry = datastore.entries[entry_index]
            process_non_parallelizables_pre_processed(pattern_processor.run_pattern, entry.preview)
            process_non_parallelizables_pre_processed(pattern_processor.run_pattern, entry.content)
            process_non_parallelizables_pre_processed(pattern_processor.run_pattern, entry.html_wrapper.processed_string,)
            process_non_parallelizables_pre_processed(pattern_processor.run_pattern, entry.rss_wrapper.processed_string)
            process_non_parallelizables_pre_processed(pattern_processor.run_pattern, entry.atom_wrapper.processed_string)
                    
def process_non_contextual_patterns():
    pattern_processor = setup_pattern_processor()
    from venc2.datastore import datastore
    from venc2.datastore.theme import theme

    if datastore.workers_count > 1:
        # There we setup chunks of entries send to workers throught dispatchers
        datastore.chunks_len = (len(datastore.entries)//datastore.workers_count)+1

        from venc2.parallelism.export_entries import split_datastore, thread_params

        thread_params["cut_threads_kill_workers"] = False
        thread_params["code_highlight_includes"] = [{} for i in range(0, datastore.workers_count)]
        thread_params["non_parallelizable"] = [[] for i in range(0, datastore.workers_count)]
        thread_params["worker_context_chunks"] = split_datastore(datastore)
    
        from venc2.parallelism import Parallelism
        from venc2.parallelism.export_entries import worker, finish, dispatcher
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
                pattern_processor
            )
        )
        parallelism.start()
        parallelism.join()
        if thread_params["cut_threads_kill_workers"]:
            exit(-1)

    from venc2.helpers import die    
    die("INTEGRATION IN PROGRESS!")

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
                pattern_processor
            )
        )


    if datastore.workers_count > 1:
        process_non_parallelizables(datastore, patterns_map, thread_params)
    
    pattern_processor.process(theme.header)
    theme.header.replace_needles()
    
    pattern_processor.process(theme.footer)    
    theme.footer.replace_needles()
    
    pattern_processor.process(theme.rss_header) 
    theme.rss_header.replace_needles()
    
    pattern_processor.process(theme.rss_footer)
    theme.rss_footer.replace_needles()
    
    pattern_processor.process(theme.atom_header)
    theme.atom_header.replace_needles()
    
    pattern_processor.process(theme.atom_footer) 
    theme.atom_footer.replace_needles()
        
    return theme, theme_folder, code_highlight, patterns_map
    
# TODO: https://openweb.eu.org/articles/comment-construire-un-flux-atom
def export_blog(theme_name=''):
    from venc2.datastore import init_datastore
    init_datastore()
    
    notify("├─ "+messages.pre_process)
    
    from venc2.datastore.theme import init_theme
    init_theme(theme_name)
    from venc2.patterns.third_party_wrapped_features.pygmentize import init_code_highlight
    init_code_highlight()
    from venc2.patterns.patterns_map import init_pattern_map
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
    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    # Starting second pass and exporting
    from venc2.threads.main import MainThread
    thread = MainThread(messages.export_main_thread, datastore, theme, patterns_map)
    thread.do()

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
        try:
            shutil.copyfile(os.path.expanduser("~")+"/.local/share/VenC/themes_assets/"+depenpency, "blog/"+depenpency)
        
        except IsADirectoryError:
            shutil.copytree(os.path.expanduser("~")+"/.local/share/VenC/themes_assets/"+depenpency, "blog/"+depenpency)

        except FileNotFoundError as e:
            notify(messages.file_not_found.format(e.filename), color="YELLOW")
    
    notify(messages.task_done_in_n_seconds.format(round(time.time() - start_timestamp,6)))

def edit_and_export(argv):    
    if len(argv) != 1:
        from venc2.helpers import die
        die(messages.missing_params.format("--edit-and-export"))
    
    try:
        proc = subprocess.Popen([datastore.blog_configuration["text_editor"], argv[0]])
        while proc.poll() == None:
            pass

    except TypeError:
        from venc2.helpers import die
        die(messages.unknown_text_editor.format(datastore.blog_configuration["text_editor"]))
    
    except:
        raise
    
    export_blog()
