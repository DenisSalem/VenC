#! /usr/bin/python
# -*- coding utf-8 -*-

import VenC.core
import markdown
import yaml
import os

class entry:
    def __init__(self, entryFilename):
        try:
            source = open(entryFilename, 'r').read()
        except FileNotFoundError as e:
            print("VenC: "+VenC.core.Messages.fileNotFound.format(entryFilename))
