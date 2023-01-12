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

from multiprocessing import Process, Pipe
from threading import Thread

class SubProcess(Process):
    def __init__(self, t, a):
        super().__init__(target=t, args=a)
        self.r, self.s = Pipe()
        
    def run(self):
        try:
            super().run()
            
        except Exception as e:
            self.s.send(e)
            
        self.s.send(None)
        
    def join(self):
        r = self.r.recv()
        if r == None:
            return
            
        else:
            raise r

class Parallelism:
    def __init__(self, worker, finish, dispatcher, n, sub_chunk_len, params=None, debug=False):       
        self.threads = []
        self.processes = []
        self.n = n
        self.finish = finish
        self.dispatcher = dispatcher
        
        for i in range(0, n):    
            send_in, send_out = Pipe()
            recv_in, recv_out = Pipe()

            self.processes.append(
                SubProcess(worker, (i,send_out,recv_in, params))
            )
            self.threads.append(
                Thread(target=dispatcher, args=(i, self.processes[-1], sub_chunk_len, send_in, recv_out))
            )
    
    def kill(self):
        for i in range(0, self.n):
            self.processes[i].kill()
            self.threads[i].join()

    def join(self):
        for i in range(0, self.n):
            self.processes[i].join()
            self.threads[i].join()
            
        for i in range(0, self.n):
            if self.finish != None:
                self.finish(i)
            
    def start(self):
        for i in range(0, self.n):       
            self.processes[i].start()
            self.threads[i].start()
  
