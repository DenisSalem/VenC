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

thread_params = {}

def split_datastore(datastore):
    chunks = []
    entries = datastore.entries
    datastore.entries = []
    for i in range(0, datastore.workers_count):
        chunks.append(entries[:datastore.chunks_len])
        entries = entries[datastore.chunks_len:]
        
    return chunks

def dispatcher(dispatcher_id, process, sub_chunk_len, send_in, recv_out):
    output_context = []
    from venc3.parallelism.export_entries import thread_params
    try:
        while len(thread_params["worker_context_chunks"][dispatcher_id]):            
            current = thread_params["worker_context_chunks"][dispatcher_id][:sub_chunk_len]
            thread_params["worker_context_chunks"][dispatcher_id] = thread_params["worker_context_chunks"][dispatcher_id][sub_chunk_len:]
            send_in.send(current)
            current = None
            output_context += recv_out.recv()
            
        send_in.send([])
        thread_params["code_highlight_includes"][dispatcher_id], thread_params["non_parallelizable"][dispatcher_id]= recv_out.recv()
        thread_params["worker_context_chunks"][dispatcher_id] = output_context
    
    except Exception as e:
        return e
                
def worker(worker_id, send_out, recv_in, process_argv=None):
    from venc3.markup_languages import process_markup_language
    from venc3.exceptions import VenCException
    
    datastore, theme, code_highlight, patterns_map, pattern_processor = process_argv[1:]

    chunk = send_out.recv() if send_out != None else datastore.entries

    from venc3.prompt import notify
    notify(("start_thread", worker_id+1), prepend="│  "+("└─ " if worker_id == datastore.workers_count - 1 else "├─ "))
    default_markup_language = datastore.blog_configuration["markup_language"]

    non_parallelizable = []
    non_parallelizable_append = non_parallelizable.append
    from copy import deepcopy

    from venc3.patterns.processor import Pattern
    pattern_processor_match = Pattern.FLAG_NON_CONTEXTUAL | Pattern.FLAG_ENTRY_RELATED
    if recv_in == None:
        pattern_processor_match |= Pattern.FLAG_NON_PARALLELIZABLE
    
    while len(chunk):
        for entry in chunk:
            entry_has_non_parallelizable = False
            datastore.requested_entry = entry
            
            if hasattr(entry, "markup_language"):
                markup_language = getattr(entry, "markup_language")
                
            else:
                markup_language = default_markup_language

            if theme.enable_entry_content:
                process_markup_language(entry.content, markup_language, entry)
                
            if theme.enable_entry_preview:
                process_markup_language(entry.preview, markup_language, entry)
                
            pattern_processor.process(entry.content, pattern_processor_match)
            pattern_processor.process(entry.preview, pattern_processor_match)                   
                
            entry.html_wrapper = deepcopy(theme.entry)
            pattern_processor.process(entry.html_wrapper, pattern_processor_match)
           
            entry.rss_wrapper = deepcopy(theme.rss_entry)
            pattern_processor.process(entry.rss_wrapper, pattern_processor_match)
            
            entry.atom_wrapper = deepcopy(theme.atom_entry)
            pattern_processor.process(entry.atom_wrapper, pattern_processor_match)
            
            if \
              entry.content.has_non_parallelizables or \
              entry.preview.has_non_parallelizables or \
              entry.html_wrapper.has_non_parallelizables or \
              entry.atom_wrapper.has_non_parallelizables or \
              entry.rss_wrapper.has_non_parallelizables:
                non_parallelizable_append(entry.index)
        
        if recv_in != None and send_out != None:
            recv_in.send(chunk)
            chunk = send_out.recv()
            
        else:
            break
        
    if recv_in != None:
        recv_in.send((code_highlight.includes, non_parallelizable))

def finish(worker_id):
    from venc3.datastore import datastore
    datastore.entries += thread_params["worker_context_chunks"][worker_id]
    thread_params["worker_context_chunks"][worker_id] = None
    from venc3.patterns.third_party_wrapped_features.pygmentize import code_highlight
    for key in thread_params["code_highlight_includes"][worker_id].keys():
        if not key in code_highlight.includes.keys():
            code_highlight.includes[key] = thread_params["code_highlight_includes"][worker_id][key]
    thread_params["code_highlight_includes"][worker_id] = None
