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

from multiprocessing import Process, Pipe
from threading import Thread

class Parallelism:
    def __init__(self, worker, finish, dispatcher, n, sub_chunk_len):
        self.threads = []
        self.processes = []
        self.n = n
        self.finish = finish
        for i in range(0, n):
            send_in, send_out = Pipe()
            recv_in, recv_out = Pipe()
            self.processes.append(
                Process(target=worker, args=(i,send_out,recv_in,))
            )
            self.threads.append(
                Thread(target=dispatcher, args=(i, self.processes[-1], sub_chunk_len, send_in, recv_out,))
            )
        
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
