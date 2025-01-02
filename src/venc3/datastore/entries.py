#! /usr/bin/env python3

#    Copyright 2016, 2025 Denis Salem
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

from venc3.datastore.entry import Entry

multiprocessing_thread_params = None

# Iterate through entries folder
def yield_entries_content():
    import os
    try:
        for r, d, files in os.walk(os.getcwd()+"/entries"):
            for filename in files:
                exploded_filename = filename.split("__")
                try:
                    date = exploded_filename[1].split('-')
                    entry_id = int(exploded_filename[0])
                    import datetime
                    datetime.datetime(
                        year=int(date[2]),
                        month=int(date[0]),
                        day=int(date[1]),
                        hour=int(date[3]),
                        minute=int(date[4])
                    ) 
                    if entry_id >= 0:
                        yield r+'/'+filename
    
                    else:
                        raise ValueError
    
                except ValueError:
                    from venc3.prompt import notify
                    notify(("invalid_entry_filename", filename), "YELLOW")
    
                except IndexError:
                    from venc3.prompt import notify
                    notify(("invalid_entry_filename", filename), "YELLOW")
    
    except FileNotFoundError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("file_not_found", str(e)))

class Entries:
    def init_entries(self):
      
        self.entries = []

        from venc3.prompt import notify
        notify(("loading_entries",), prepend="┌─ ")
        
        from venc3.exceptions import VenCException
        
        try:
            paths = [path for path in yield_entries_content()]
            
            self.chunks_len = (len(paths)//self.workers_count)+1      
            if self.workers_count > 1:
                # There we setup chunks of entries send to workers throught dispatchers
                global multiprocessing_thread_params
                multiprocessing_thread_params = {
                    "chunked_filenames" :[],
                    "workers_count" : self.workers_count,
                    "entries": self.entries,
                    "paths": self.blog_configuration["paths"],
                    "cut_threads_kill_workers" : False
                }
                for i in range(0, self.workers_count):
                    multiprocessing_thread_params["chunked_filenames"].append(paths[:self.chunks_len])
                    paths = paths[self.chunks_len:]
                    
                paths = None
                
                from venc3.parallelism import Parallelism
                from venc3.parallelism.build_entries import dispatcher
                from venc3.parallelism.build_entries import finish
                from venc3.parallelism.build_entries import worker
                
                parallelism = Parallelism(
                    worker,
                    finish,
                    dispatcher,
                    self.workers_count,
                    self.blog_configuration["pipe_flow"]
                )
                
                parallelism.start()
                parallelism.join()
                    
            else:
                for path in paths:
                    self.entries.append(Entry(
                        path,
                        self.blog_configuration["paths"],
                    ))
                    
        except VenCException as e:
            if self.workers_count > 1:
                parallelism.kill()
                
            e.die()

        self.entries = sorted(self.entries, key = lambda entry : self.sort(entry))
        for i in range(0, len(self.entries)):
            self.entries[i].index = i

    def sort(self, entry):
        try:
            value = str(getattr(entry, self.sort_by))
            if self.sort_by == 'id':
                return int(value)
                
            return value

        except AttributeError:
            return ''
            
    def get_entries_for_given_date(self, value, reverse):
        index = 0
        for metadata in self.entries_per_archives:
            if value == metadata.value:
                break
            index += 1

        for entry in (self.entries_per_archives[index].related_to[::-1] if reverse else self.entries_per_archives[index].related_to):
            yield self.entries[entry]
            
    def get_entries(self, reverse=False):
        for entry in (self.entries[::-1] if reverse else self.entries):
            yield entry
