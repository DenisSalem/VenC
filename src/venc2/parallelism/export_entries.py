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

def dispatcher(dispatcher_id, process, sub_chunk_len, send_in, recv_out):
    output_context = []
    global datastore
    send_in.send(datastore)
    try:
        while len(thread_params["worker_context_chunks"][dispatcher_id]):
            if thread_params["cut_threads_kill_workers"]:
                process.kill()
                
            current = thread_params["worker_context_chunks"][dispatcher_id][:sub_chunk_len]
            thread_params["worker_context_chunks"][dispatcher_id] = thread_params["worker_context_chunks"][dispatcher_id][sub_chunk_len:]
            send_in.send(current)
            current = None
            output_context += recv_out.recv()

    except:
        thread_params["cut_threads_kill_workers"] = True
        process.kill()
        return
        
    send_in.send([])
    thread_params["code_highlight_includes"][dispatcher_id], thread_params["non_parallelizable"][dispatcher_id]= recv_out.recv()
    thread_params["worker_context_chunks"][dispatcher_id] = output_context
    
def worker(worker_id, send_out, recv_in, single_process_argv=None):
    if single_process_argv == None:
        datastore = send_out.recv()
    
        # TODO : could be avoided by sending Theme
        theme, theme_folder = init_theme(datastore.init_theme_argv)
        code_highlight = CodeHighlight(datastore.blog_configuration["code_highlight_css_override"])
        patterns_map = PatternsMap(datastore, code_highlight, theme)
        pattern_processor = setup_pattern_processor(patterns_map, parallel = True if single_process_argv == None else False)
        chunk = send_out.recv()
    else:
        datastore, theme, theme_folder, code_highlight, pattern_processor = single_process_argv
        chunk = datastore.entries
    
    notify("│  "+("└─ " if worker_id == datastore.workers_count - 1 else "├─ ")+messages.start_thread.format(worker_id+1))
    default_markup_language = datastore.blog_configuration["markup_language"]

    non_parallelizable = []
    non_parallelizable_append = non_parallelizable.append

    while len(chunk):
        for entry in chunk:
            entry_has_non_parallelizable = False
            datastore.requested_entry = entry
            
            if hasattr(entry, "markup_language"):
                markup_language = getattr(entry, "markup_language")
                
            else:
                markup_language = default_markup_language
                
            entry_has_non_parallelizable |= pattern_processor.process(entry.content)
            process_markup_language(entry.content, markup_language, entry)

            entry_has_non_parallelizable |= pattern_processor.process(entry.preview)
            process_markup_language(entry.preview, markup_language, None)
                
            entry.html_wrapper = deepcopy(theme.entry)
            entry_has_non_parallelizable |= pattern_processor.process(entry.html_wrapper.processed_string)
            entry.html_wrapper.processed_string.replace_needles()
           
            entry.rss_wrapper = deepcopy(theme.rss_entry)
            entry_has_non_parallelizable |= pattern_processor.process(entry.rss_wrapper.processed_string)
            entry.rss_wrapper.processed_string.replace_needles()
            
            entry.atom_wrapper = deepcopy(theme.atom_entry)
            entry_has_non_parallelizable |= pattern_processor.process(entry.atom_wrapper.processed_string)
            entry.atom_wrapper.processed_string.replace_needles()
            
            if entry_has_non_parallelizable:
                non_parallelizable_append(entry.index)

        if single_process_argv == None:
            recv_in.send(chunk)
            chunk = send_out.recv()
            
        else:
            break
            
    if single_process_argv == None:
        recv_in.send((code_highlight.includes, non_parallelizable))

def finish(worker_id):
    global datastore
    datastore.entries += thread_params["worker_context_chunks"][worker_id]
    thread_params["worker_context_chunks"][worker_id] = None
    global code_highlight
    for key in thread_params["code_highlight_includes"][worker_id].keys():
        if not key in code_highlight.includes.keys():
            code_highlight.includes[key] = thread_params["code_highlight_includes"][worker_id][key]
    thread_params["code_highlight_includes"][worker_id] = None
