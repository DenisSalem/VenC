#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import VenC.core
import VenC.new

command_index = {"-v":                  [VenC.core.PrintVersion, 0],
                "-nb":                  [VenC.new.blog, -1],
                "-ne":                  [VenC.new.entry, 2],
                #"-xb":                  [VenC.exportBlog.exportBlog, 0],
                #"--export-blog":        [VenC.exportBlog.exportBlog, 0],
                "--new-entry":          [VenC.new.entry, 2],
                "--new-blog":           [VenC.new.blog, -1],
                "--version":            [VenC.core.PrintVersion, 0]}
def argv_handler(argv=None):
    argv = argv if argv != None else sys.argv[1:]
    if argv != []: 
       if argv[0] in command_index:
           if command_index[argv[0]][1] != -1: 
               arguments = argv[1:command_index[argv[0]][1]+1]
           else:
               arguments = list()
               for argument in argv[1:]:
                   if argument not in command_index.keys():
                       arguments.append(argument)
                   else:
                       break
           command_index[argv[0]][0](arguments)
           argv_handler(argv[len(arguments)+1:])
       else:
           print(VenC.core.Messages.unknownCommand.format(argv[0]))
           argv_handler(argv[1:])
if sys.argv[1:] != []: 
    argv_handler()
else:
    print("VenC: "+VenC.core.Messages.nothingToDo)

