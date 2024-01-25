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

import subprocess

from venc.exceptions import MalformedPatterns, VenCException
from venc.helpers import rm_tree_error_handler
from venc.patterns.non_contextual import theme_includes_dependencies
from venc.patterns.processor import Pattern, Processor
from venc.prompt import notify


def copy_recursively(src, dest):
    import errno
    import os
    import shutil

    try:
        listdir = os.listdir(src)
    except Exception as e:
        from venc.exceptions import VenCException

        VenCException(("exception_place_holder", e)).die()

    for filename in listdir:
        try:
            shutil.copytree(os.path.join(src, filename), os.path.join(dest, filename))

        except shutil.Error as e:
            from venc.prompt import notify

            notify(("directory_not_copied", str(e)), "YELLOW")

        except OSError as e:
            if e.errno == errno.ENOTDIR:
                shutil.copy(os.path.join(src, filename), os.path.join(dest, filename))

            else:
                from venc.prompt import notify

                notify(("directory_not_copied", str(e)), "YELLOW")


def export_via_ftp(params):
    export_blog(params)
    from venc.commands.remote import remote_copy

    remote_copy(None)


def setup_pattern_processor(parallel=False):
    processor = Processor()
    from venc.patterns.patterns_map import patterns_map

    processor.set_patterns(patterns_map.non_contextual["blog"])
    processor.set_patterns(patterns_map.non_contextual["entries"])
    processor.set_patterns(patterns_map.non_contextual["extra"])
    if not parallel:
        processor.set_patterns(patterns_map.non_contextual["non_parallelizable"])

    return processor


def process_non_parallelizables(datastore, patterns_map, thread_params):
    from venc.prompt import notify

    notify(("process_non_parallelizable",), prepend="├─ ")
    pattern_processor = Processor()
    pattern_processor.set_patterns(patterns_map.non_contextual["non_parallelizable"])
    from venc.patterns.processor import Pattern

    for l in thread_params["non_parallelizable"]:
        for entry_index in l:
            entry = datastore.entries[entry_index]
            if entry.preview.has_non_parallelizables:
                pattern_processor.process(
                    entry.preview,
                    Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE,
                )

            if entry.content.has_non_parallelizables:
                pattern_processor.process(
                    entry.content,
                    Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE,
                )

            if entry.html_wrapper.has_non_parallelizables:
                pattern_processor.process(
                    entry.html_wrapper.processed_string,
                    Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE,
                )

            if entry.rss_wrapper.has_non_parallelizables:
                pattern_processor.process(
                    entry.rss_wrapper.processed_string,
                    Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE,
                )

            if entry.atom_wrapper.has_non_parallelizables:
                pattern_processor.process(
                    entry.atom_wrapper.processed_string,
                    Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE,
                )


def process_non_contextual_patterns():
    from venc.datastore import datastore

    pattern_processor = setup_pattern_processor(datastore.workers_count > 1)
    from venc.datastore.theme import theme
    from venc.parallelism.export_entries import worker
    from venc.patterns.patterns_map import patterns_map
    from venc.patterns.third_party_wrapped_features.pygmentize import code_highlight

    if datastore.workers_count > 1:
        # There we setup chunks of entries send to workers throught dispatchers
        datastore.chunks_len = (len(datastore.entries) // datastore.workers_count) + 1

        from venc.parallelism.export_entries import split_datastore, thread_params

        thread_params["code_highlight_includes"] = [
            {} for i in range(0, datastore.workers_count)
        ]
        thread_params["non_parallelizable"] = [
            [] for i in range(0, datastore.workers_count)
        ]
        thread_params["worker_context_chunks"] = split_datastore(datastore)

        from venc.parallelism import Parallelism
        from venc.parallelism.export_entries import dispatcher, finish

        parallelism = Parallelism(
            worker,
            finish,
            dispatcher,
            datastore.workers_count,
            datastore.blog_configuration["pipe_flow"],
            (True, datastore, theme, code_highlight, patterns_map, pattern_processor),
        )
        parallelism.start()
        try:
            parallelism.join()

        except VenCException as e:
            parallelism.kill()
            e.die()

    if not datastore.blog_configuration["disable_chapters"]:
        for entry in datastore.entries:
            datastore.update_chapters(entry)

        datastore.build_chapter_indexes()

    if datastore.workers_count == 1:
        try:
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
                    pattern_processor,
                ),
            )
        except VenCException as e:
            e.die()

    try:
        if datastore.workers_count > 1:
            process_non_parallelizables(datastore, patterns_map, thread_params)
            pattern_processor.set_patterns(
                patterns_map.non_contextual["non_parallelizable"]
            )

        flags = Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_NON_PARALLELIZABLE

        pattern_processor.process(theme.header, flags)
        pattern_processor.process(theme.footer, flags)
        pattern_processor.process(theme.rss_header, flags)
        pattern_processor.process(theme.rss_footer, flags)
        pattern_processor.process(theme.atom_header, flags)
        pattern_processor.process(theme.atom_footer, flags)

    except VenCException as e:
        e.die()


def export_blog(params):
    theme_name = params[0] if len(params) else ""
    import time

    start_timestamp = time.time()
    from venc.datastore import init_datastore

    datastore = init_datastore()

    notify(("pre_process",), prepend="├─ ")

    from venc.datastore.theme import init_theme

    init_theme(theme_name)
    from venc.patterns.third_party_wrapped_features.pygmentize import (
        init_code_highlight,
    )

    init_code_highlight()
    from venc.patterns.patterns_map import init_pattern_map

    init_pattern_map()

    process_non_contextual_patterns()
    if not datastore.blog_configuration["disable_single_entries"]:
        notify(("link_entries",), prepend="├─ ")
        # Add required link between entries
        entries = datastore.entries
        for entry_index in range(0, len(entries)):
            current_entry = entries[entry_index]
            if entry_index > 0:
                entries[entry_index - 1].next_entry = current_entry
                current_entry.previous_entry = entries[entry_index - 1]

    # cleaning directory
    import os
    import shutil

    shutil.rmtree("blog", ignore_errors=False, onerror=rm_tree_error_handler)
    os.makedirs("blog")

    try:
        # Starting second pass and exporting
        from venc.threads.main import MainThread

        thread = MainThread()
        thread.do()

        if not datastore.blog_configuration["disable_archives"]:
            from venc.threads.archives import ArchivesThread

            thread = ArchivesThread()
            thread.do()

        if not datastore.blog_configuration["disable_categories"]:
            from venc.threads.categories import CategoriesThread

            thread = CategoriesThread()
            thread.do()

        if not datastore.blog_configuration["disable_single_entries"]:
            from venc.threads.entries import EntriesThread

            thread = EntriesThread()
            thread.do()

        if not datastore.blog_configuration["disable_chapters"]:
            from venc.threads.chapters import ChaptersThread

            thread = ChaptersThread()
            thread.do()

    except VenCException as e:
        e.die()

    # Copy assets and extra files
    notify(("copy_assets_and_extra_files",), prepend="└─ ")
    from venc.datastore.theme import theme, theme_assets_dependencies
    from venc.helpers import get_base_dir
    from venc.patterns.third_party_wrapped_features.pygmentize import code_highlight

    code_highlight.export_style_sheets()
    copy_recursively("extra/", "blog/")
    copy_recursively(os.path.join(theme.theme_folder, "assets"), "blog/")
    for depenpency in theme_assets_dependencies:
        try:
            shutil.copyfile(
                get_base_dir() + "/data/themes_assets/" + depenpency,
                "blog/" + depenpency,
            )

        except IsADirectoryError:
            shutil.copytree(
                get_base_dir() + "/data/themes_assets/" + depenpency,
                "blog/" + depenpency,
            )

        except FileNotFoundError as e:
            notify(("file_not_found", e.filename), color="YELLOW")

    notify(("task_done_in_n_seconds", round(time.time() - start_timestamp, 6)))


def edit_and_export(params):
    if len(paramas):
        entry_filename = params[0]
    else:
        from venc.prompt import die

        die(("missing_params", "--edit-and-export"))

    from venc.datastore import init_datastore

    datastore = init_datastore()

    try:
        if type(datastore.blog_configuration["text_editor"]) != list:
            from venc.helpers import die

            die(("blog_metadata_is_not_a_list", "text_editor"))

        proc = subprocess.Popen(
            datastore.blog_configuration["text_editor"] + [entry_filename]
        )
        proc.wait()

    except TypeError:
        from venc.helpers import die

        die(("unknown_text_editor", datastore.blog_configuration["text_editor"]))

    except Exception as e:
        raise e

    export_blog(params[1:])
