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

from venc3.datastore.entry import Entry

multiprocessing_thread_params = None

class Entries:
    def init_entries(self):
      
        self.entries = []

        from venc3.prompt import notify
        notify(("loading_entries",), prepend="┌─ ")
        
        from venc3.exceptions import VenCException
        
        try:
            from venc3.datastore.entry import yield_entries_content
            filenames = [filename for filename in yield_entries_content()]
            
            self.chunks_len = (len(filenames)//self.workers_count)+1      
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
                    multiprocessing_thread_params["chunked_filenames"].append(filenames[:self.chunks_len])
                    filenames = filenames[self.chunks_len:]
                    
                filenames = None
                
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
                for filename in filenames:
                    self.entries.append(Entry(
                        filename,
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
