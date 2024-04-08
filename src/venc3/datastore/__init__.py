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

from copy import deepcopy

import datetime
import os
import unidecode

from urllib.parse import quote as urllib_parse_quote
from venc3.datastore.configuration import get_blog_configuration
from venc3.datastore.archives import Archives
from venc3.datastore.entries import Entries
from venc3.datastore.metadata import MetadataNode
from venc3.datastore.metadata import Chapter
from venc3.datastore.taxonomy import Taxonomy
from venc3.prompt import notify
from venc3.exceptions import MalformedPatterns, VenCException
from venc3.patterns.datastore import DatastorePatterns
from venc3.helpers import quirk_encoding

class DataStore(DatastorePatterns, Taxonomy, Archives, Entries):
    def __init__(self):
        self.requested_entry = None
        self.embed_providers = {}
        self.in_child_process = False
        self.root_page = None
        self.blog_configuration = get_blog_configuration()
        self.sort_by = self.blog_configuration["sort_by"]
        self.disable_threads = self.blog_configuration["disable_threads"]
        
        try:
            from multiprocessing import cpu_count
            cpu_c = cpu_count()
            self.workers_count = cpu_c if cpu_c > 0 else 1
            
        except (ImportError, NotImplementedError):
            notify(("current_python_implementation_doesnt_support_parallelism",), color="YELLOW")
            self.workers_count = 1

        try:
            parallel_processing = self.blog_configuration["parallel_processing"]
            try:
                if 0 < int(parallel_processing) < self.workers_count:
                     self.workers_count = int(parallel_processing)
                     
                elif int(parallel_processing) < 1:
                    raise ValueError
                  
            except ValueError:
                notify(("wrong_value_for_parallel_processing",), color="YELLOW")
                
        except KeyError:
            notify(("no_parallel_processing_default_value", self.workers_count), color="YELLOW")

        self.html_for_metadata = {}
        self.html_tree_for_blog_metadata = {}
        self.html_chapters = {}
        
        # TODO : Cache should be voided when usage is complete
        
        self.cache_blog_archives = {}
        self.cache_entries_subset = {}
        self.cache_get_entry_attribute_by_id = {}
        self.cache_get_chapter_attribute_by_index = {}
        
        self.generation_timestamp = datetime.datetime.now()
        self.raw_chapters = {}
        self.chapters_index = []

        self.init_entries()
        self.init_archives()
        self.init_taxonomy()
                
    def build_chapter_indexes(self):
        # build chapters index
        path_chapters_sub_folders = self.blog_configuration["paths"]["chapters_sub_folders"]
        path_chapter_folder_name = self.blog_configuration["paths"]["chapter_directory_name"]
        
        for chapter in sorted(self.raw_chapters.keys(), key = lambda x : int(x.replace('.', ''))):
            top = self.chapters_index
            index = ''
            levels = [str(level) for level in chapter.split('.') if level != '']
            len_levels = len(levels)
                    
            for i in range(0, len_levels):
                l = levels[i]
                if index == '':
                    index = l

                else:
                    index += '.'+l

                f = filter(lambda c : c.index == index, top)
                try:
                    top = next(f).sub_chapters
                
                except StopIteration:
                    if index in self.raw_chapters.keys():
                        entry = self.raw_chapters[index]
                        try:
                            path = "\x1a/"+path_chapters_sub_folders+quirk_encoding(
                                path_chapter_folder_name.format(**{
                                    "chapter_name" : entry.title,
                                    "chapter_index" : index
                                })
                            )
                            
                        except KeyError as e:
                            from venc3.helpers import die
                            die(("variable_error_in_filename", e))
                            
                        top.append(
                            Chapter(index, self.raw_chapters[index], path)
                        )
                        entry.chapter = top[-1]
                        
                    else:
                        from venc3.prompt import notify
                        notify(("chapter_has_no_entry", index), color="YELLOW")
                        
    def build_entry_html_toc(self, toc, open_ul, open_li, content_format, close_li, close_ul):             
        output = open_ul
        i = 0
        while i < len(toc):                    
            current = toc[i]
            output += open_li+content_format.format(**{
                "level": current[0],
                "title": current[1],
                "id":current[2]
            })
            
            if i+1 < len(toc):
                if current[0] < toc[i+1][0]:
                    sub_list = []
                    for item in toc[i+1:]:
                        if current[0] < item[0]:
                           sub_list.append(item)
                        else:
                          break 
                      
                    output += self.build_entry_html_toc(sub_list, open_ul, open_li, content_format, close_li, close_ul)
                    i += len(sub_list)
                    
            output += close_li
            i += 1
          
        return output+close_ul

    def build_html_chapters(self, lo, io, ic, lc, top, level):          
        if top == []:
            return ''
            
        output = lo.format(**{"level" :level})
        
        from venc3.helpers import quirk_encoding
        
        for sub_chapter in top:
            output += io.format(**{
                "index": sub_chapter.index,
                "title": self.entries[sub_chapter.entry_index].title,
                "html_id" : quirk_encoding(self.entries[sub_chapter.entry_index].title),
                "path":  sub_chapter.path,
                "level": level
            })
            output += self.build_html_chapters(lo, io, ic, lc, sub_chapter.sub_chapters, level+1)
            output += ic
        output += lc

        return output

    def build_html_categories_tree(self, pattern, opening_node, opening_branch, closing_branch, closing_node, tree):
        if not len(tree):
            return ""
            
        output_string = opening_node
        for node in sorted(tree, key = lambda x : x.value):
            if node.value in self.disable_threads:
                continue

            variables = self.node_to_dictionnary(pattern, node, opening_node, opening_branch, closing_branch, closing_node, node.childs)
            output_string += opening_branch.format(**variables) + closing_branch.format(**variables)

        return output_string + closing_node

    def node_to_dictionnary(self, pattern, node, opening_node, opening_branch, closing_branch, closing_node, childs):
        return {
            "value" : node.value,
            "html_id": quirk_encoding(node.value),
            "count" : node.count,
            "weight" : round(node.count / node.weight_tracker.value,2),
            "path" : node.path,
            "childs" : self.build_html_categories_tree(
                pattern,
                opening_node,
                opening_branch,
                closing_branch,
                closing_node,
                childs
            )
        }

    def update_chapters(self, entry):
        try:
            if type(entry.chapter) == float:
                notify(("chapter_type_is_ambiguous", entry.id), color="YELLOW")
                
            chapter = str(entry.chapter)
            [ int(level) for level in chapter.split('.') if level != '']

        except ValueError as e: # weak test to check attribute conformity
            notify(("chapter_has_a_wrong_index", entry.id, chapter), color="YELLOW")
            return

        except AttributeError as e: # does entry has chapter?
            return

        if chapter in self.raw_chapters.keys():
            from venc3.prompt import die
            die((
                "chapter_already_exists",
                entry.title,
                entry.id,
                self.raw_chapters[chapter].title,
                self.raw_chapters[chapter].id,
                chapter
            ))
        else:
            self.raw_chapters[chapter] = entry
        
datastore = None

def init_datastore():
    global datastore
    datastore = DataStore()
    return datastore
