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

def dispatcher(dispatcher_id, process, sub_chunk_len, send_in, recv_out):
    output_context = []
    from venc3.datastore.entries import multiprocessing_thread_params
    send_in.send(multiprocessing_thread_params)
    chunked_filenames = multiprocessing_thread_params["chunked_filenames"]
    try:
        while len(chunked_filenames[dispatcher_id]):
            if multiprocessing_thread_params["cut_threads_kill_workers"]:
                process.kill()
                break
                
            current = chunked_filenames[dispatcher_id][:sub_chunk_len]
            chunked_filenames[dispatcher_id] = chunked_filenames[dispatcher_id][sub_chunk_len:]
            send_in.send(current)
            current = None
            output_context += recv_out.recv()
            
    except:
        multiprocessing_thread_params["cut_threads_kill_workers"] = True
        process.kill()
        return
                
    send_in.send([])
    multiprocessing_thread_params["chunked_filenames"][dispatcher_id] = output_context
    
def worker(worker_id, send_out, recv_in, single_process_argv=None):
    from venc3.datastore.entry import Entry
    from venc3.prompt import notify

    worker_params = send_out.recv()
    
    notify(("start_thread", worker_id+1), prepend="│  "+("└─ " if worker_id == worker_params["workers_count"] - 1 else "├─ "))
    
    chunk = send_out.recv()

    output = []
    while len(chunk):
        for filename in chunk:
            output.append(Entry(
                filename,
                worker_params["paths"],
            ))
        
        recv_in.send(output)
        output = None
        chunk = send_out.recv()
            
def finish(worker_id):
    from venc3.datastore.entries import multiprocessing_thread_params
    multiprocessing_thread_params["entries"] += multiprocessing_thread_params["chunked_filenames"][worker_id]
    multiprocessing_thread_params["chunked_filenames"][worker_id] = None
