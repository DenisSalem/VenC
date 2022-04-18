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

from venc2.datastore.entry import Entry

# ~ def split_datastore(datastore):
    # ~ chunks = []
    # ~ entries = datastore.entries
    # ~ datastore.entries = []
    # ~ for i in range(0, datastore.workers_count):
        # ~ chunks.append(entries[:datastore.chunks_len])
        # ~ entries = entries[datastore.chunks_len:]
        
    # ~ return chunks

def dispatcher(dispatcher_id, process, sub_chunk_len, send_in, recv_out):
    output_context = []
    
    send_in.send(thread_params)
    chunked_filenames = thread_params["chunked_filenames"]
    try:
        while len(chunked_filenames[dispatcher_id]):
            if thread_params["cut_threads_kill_workers"]:
                process.kill()
                
            current = chunked_filenames[dispatcher_id][:sub_chunk_len]
            chunked_filenames[dispatcher_id] = chunked_filenames[dispatcher_id][sub_chunk_len:]
            send_in.send(current)
            current = None
            output_context += recv_out.recv()
            
    except:
        thread_params["cut_threads_kill_workers"] = True
        process.kill()
        return
                
    send_in.send([])
    thread_params["chunked_filenames"][dispatcher_id] = output_context
    
def worker(worker_id, send_out, recv_in):        
    worker_params = send_out.recv()
    
    notify("│  "+("└─ " if worker_id == worker_params["workers_count"] - 1 else "├─ ")+messages.start_thread.format(worker_id+1))
    
    chunk = send_out.recv()

    output = []
    while len(chunk):
        for filename in chunk:
            output.append(Entry(
                filename,
                worker_params["paths"],
                worker_params["encoding"]
            ))
        
        recv_in.send(output)
        output = None
        chunk = send_out.recv()
            
def finish(worker_id):
    thread_params["entries"] += thread_params["chunked_filenames"][worker_id]
    thread_params["chunked_filenames"][worker_id] = None
