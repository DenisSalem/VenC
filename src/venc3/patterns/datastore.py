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

import datetime

def merge(iterable, string, separator, pattern):
    try:
        return separator.join([string.format(**something) for something in iterable])
    
    except KeyError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("unknown_contextual", str(e)), pattern)

class DatastorePatterns:
    def cherry_pick_metadata(self, pattern, source, if_exists,  path):
        from venc3.datastore.entry import Entry

        if not len(path):
            from venc3.exceptions import VenCException
            raise VenCException(("wrong_args_number", ">= 1", "0"), context=self)
            
        try:
            node = getattr(source, path[0]) if type(source) == Entry else source[path[0]]
            previous_key = path[0]
            for key in path[1:]:
                node = node[key]
                previous_key = key

            return str(node)
            
        except TypeError:
            from venc3.exceptions import VenCException
            raise VenCException(("field_is_not_of_type", previous_key, source.title if type(source) == Entry else"blog_configuration.yaml", dict), pattern)
            
        except Exception as e:
            if not type(e) in[KeyError, AttributeError]:
                raise e
            
            if if_exists:
                return ""
                
            if type(source) == Entry:
                exception_params = ("entry_has_no_metadata_like", source.title, ' -> '.join(path))
            else:
                exception_params = ("blog_has_no_metadata_like", ' -> '.join(path))
                
            from venc3.exceptions import VenCException
            raise VenCException(exception_params, pattern)
            
    def cherry_pick_blog_metadata(self, pattern, *branch):
        return self.cherry_pick_metadata(pattern, self.blog_configuration, False, branch)

    def cherry_pick_blog_metadata_if_exists(self, pattern, *branch):
        return self.cherry_pick_metadata(pattern, self.blog_configuration, True, branch)

    def cherry_pick_entry_metadata(self, pattern, *branch):
        return self.cherry_pick_metadata(pattern, self.requested_entry, False, branch)

    def cherry_pick_entry_metadata_if_exists(self, pattern, *branch):
        return self.cherry_pick_metadata(pattern, self.requested_entry, True, branch)
        
    def if_categories(self, pattern, if_true, if_false=''):
        if self.entries_per_categories != [] and not self.blog_configuration["disable_categories"]:
            return if_true
            
        else:
            return if_false
    
    def if_chapters(self, pattern, if_true, if_false=''):
        if self.chapters_index != [] and not self.blog_configuration["disable_chapters"]:
            return if_true
            
        else:
            return if_false
    
    def if_feeds_enabled(self, pattern, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"] and self.blog_configuration["disable_rss_feed"]:
            return if_false
            
        else: 
            return if_true
        
    def if_atom_enabled(self, pattern, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"]:
            return if_false

        else: 
            return if_true

    def if_metadata_is_true(self, key, if_true, if_false, source):          
        try:
            if type(source) == dict and source[key]:
                return if_true.strip()

            elif getattr(source,key):
                return if_true.strip()
        
        except (AttributeError, KeyError) as e:
            pass
        
        return if_false.strip()
        
    def if_blog_metadata_is_true(self, pattern, metadata_name, if_true, if_false=''):
        return self.if_metadata_is_true(metadata_name, if_true, if_false, self.blog_configuration)

    def if_entry_metadata_is_true(self, pattern, metadata_name, if_true, if_false=''):
        return self.if_metadata_is_true(metadata_name, if_true, if_false, self.requested_entry)
                
    def if_rss_enabled(self, pattern, if_true, if_false=''):
        if self.blog_configuration["disable_rss_feed"]:
            return if_false
            
        else:
            return if_true

    def if_infinite_scroll_enabled(self, pattern, if_true, if_false=''):            
        try:
            if self.blog_configuration["disable_infinite_scroll"]:
                return if_false
                                    
            else:
                return if_true
                    
        except KeyError:
            return if_true
                        
    def get_chapters(self, pattern, list_open, item_open, item_close, list_close):
        '''index,title,path,level,html_id'''
        key = list_open+item_open+item_close+list_close
        if not key in self.html_chapters.keys():
            self.html_chapters[key] = self.build_html_chapters(list_open, item_open, item_close, list_close, self.chapters_index, 0)

        return self.html_chapters[key]

    def get_entry_toc(self, pattern, open_ul, open_li, content, close_li, close_ul):
        '''id,level,title'''
        if hasattr(self.requested_entry, "toc"):
            output = self.build_entry_html_toc(self.requested_entry.toc, open_ul, open_li, content, close_li, close_ul)
            return "</p>"+output+"<p>" if pattern.root == pattern.parent and pattern.root.has_markup_language else output

        else:
            return ""
            
    def get_generation_timestamp(self, pattern, time_format):
        return datetime.datetime.strftime(self.generation_timestamp, time_format)
            
    def get_blog_metadata(self, pattern, metadata_name):
        # if exception is raised it will be automatically be catch by processor.
        try:
            return str(self.blog_configuration[metadata_name])
            
        except KeyError:
            from venc3.exceptions import VenCException
            raise VenCException(("blog_has_no_metadata_like", metadata_name), pattern)
            
    def get_blog_metadata_if_exists(self, pattern, metadata_name, if_true='', if_false='', ok_if_null=True):
        '''value'''
        try:
            value = self.blog_configuration[metadata_name]
            
        except KeyError:
            return if_false
        
        if len(if_true):
            if ok_if_null or (value != None and len(str(value))):
                return if_true.format(**{"value" : value})
                  
            else:
                return if_false
        else:
            return value
            
    def get_blog_metadata_if_not_null(self, pattern, metadata_name, if_true='', if_false=''):
        '''value'''
        try:
            return self.get_blog_metadata_if_exists(pattern, metadata_name, if_true, if_false, ok_if_null=False)
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            
    def get_entry_attribute_by_id(self, pattern, attribute, identifier):            
        key = attribute+identifier
        if not key in self.cache_get_entry_attribute_by_id.keys():
            try:
                entry = [entry for entry in self.entries if entry.id == int(identifier)][0]
                self.cache_get_entry_attribute_by_id[key] = getattr(entry, attribute)
            
            except ValueError:
                from venc3.exceptions import VenCException
                raise VenCException(("id_must_be_an_integer",), pattern)
                
            except AttributeError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("entry_has_no_metadata_like", entry.id), pattern)

            except IndexError:
                from venc3.exceptions import VenCException
                raise VenCException(("cannot_retrieve_entry_attribute_because_wrong_id",), pattern)
            
        return self.cache_get_entry_attribute_by_id[key]
    
    def get_entry_chapter_level(self, pattern):
        try:
            return self.requested_entry.chapter_level
            
        except:
            return ''
            
    def get_entry_chapter_path(self, pattern):
        if self.blog_configuration["disable_chapters"]:
            return ''
        else:
            from venc3.datastore.metadata import Chapter
            return self.requested_entry.chapter.path if hasattr(self.requested_entry, "chapter") and type(self.requested_entry.chapter) == Chapter else ''

    def get_entry_metadata(self, pattern, metadata_name):
        try:
            return str(getattr(self.requested_entry, metadata_name))
            
        except AttributeError:
            from venc3.exceptions import VenCException
            raise VenCException(
                ("entry_has_no_metadata_like", self.requested_entry.id, metadata_name),
                pattern
            )
            
    def get_entry_metadata_if_exists(self, pattern, metadata_name, string='', string2='', ok_if_null=True):
        '''value'''
        try:
            value = str(getattr(self.requested_entry,metadata_name ))

        except AttributeError:
            return string2
        
        if string == '':
            return value

        if ok_if_null or (value != None and len(value)):
            return string.format(**{"value" : value})
            
        else:
            return string2
            
    def get_entry_metadata_if_not_null(self, pattern, metadata_name, string='', string2=''):
        '''value'''
        return self.get_entry_metadata_if_exists(pattern, metadata_name, string, string2, ok_if_null=False)
        
    def get_entry_title(self, pattern):
        return self.requested_entry.title
    
    def get_entry_id(self, pattern):
        return str(self.requested_entry.id)
            
    def get_entry_year(self, pattern):
        return self.requested_entry.date.year

    def get_entry_month(self, pattern):
        return self.requested_entry.date.month
        
    def get_entry_day(self, pattern):
        return self.requested_entry.date.day

    def get_entry_hour(self, pattern):
        return self.requested_entry.date.hour
    
    def get_entry_minute(self, pattern):
        return self.requested_entry.date.minute

    def get_entry_date(self, pattern, date_format=''):
        return self.requested_entry.date.strftime(
            date_format if len(date_format) else self.blog_configuration["date_format"]
        )

    def get_entry_archive_path(self, pattern):
        return "\x1a/"+self.requested_entry.date.strftime(
            self.blog_configuration["paths"]["archives_directory_name"]
        )
    
    def get_chapter_attribute_by_index(self, pattern, attribute, index):
        if self.blog_configuration["disable_chapters"]:
            return ""
        
        key = attribute+index
        if not key in self.cache_get_chapter_attribute_by_index.keys():
            try:
                self.cache_get_chapter_attribute_by_index[key] = str(getattr(self.raw_chapters[index].chapter, attribute))
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("there_is_no_chapter_with_index", index), pattern)
                
            except AttributeError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("chapter_has_no_attribute_like", attribute), pattern)
                
        return self.cache_get_chapter_attribute_by_index[key]
            
    def get_entry_path(self, pattern):
        if self.blog_configuration["disable_single_entries"]:
            return ""
            
        else:
            if self.requested_entry.path[-10:] == "index.html":
                return self.requested_entry.path[:-10]
            else:
                return self.requested_entry.path

    def get_author_name(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "author_name")

    def get_blog_name(self, pattern):
        return self.blog_configuration["blog_name"]
        
    def get_blog_description(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "blog_description")

    def get_author_description(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "author_description")

        
    def get_blog_license(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "license")
    
    def get_blog_url(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "blog_url")

    def get_blog_language(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "blog_language")
    
    def get_author_email(self, pattern):
        return self.get_blog_metadata_if_exists(pattern, "author_email")

    def get_root_page(self, pattern):
        if self.root_page == None:
            self.root_page =  "\x1a/"+self.blog_configuration["paths"]["index_file_name"].format(**{"page_number":''})
            
        return self.root_page
        
    def get_entry_categories_tree(self, pattern, open_node, open_branch, close_branch, clode_node):
        '''value,html_id,count,weight,path,childs'''
        key = open_node+open_branch+close_branch+clode_node
        entry = self.requested_entry

        if not key in self.requested_entry.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                entry.html_categories_tree[key] = ''

            else:
                entry.html_categories_tree[key] = self.build_html_categories_tree(
                    pattern,
                    open_node,
                    open_branch,
                    close_branch,
                    clode_node,
                    self.extract_leaves(entry.id)
                )

        
        return entry.html_categories_tree[key]

    def get_blog_categories_tree_from_branches(self, pattern, branches, sub_tree_string, separator, open_node, open_branch, close_branch, close_node):
        '''value,html_id,count,weight,path,childs'''

        return self.get_categories_tree_from_branches(
            pattern,
            branches,
            sub_tree_string,
            separator,
            open_node,
            open_branch,
            close_branch,
            close_node,
            None
        )

    def get_entry_categories_tree_from_branches(self, pattern, branches, sub_tree_string, separator, open_node, open_branch, close_branch, close_node):
        '''value,html_id,count,weight,path,childs'''

        return self.get_categories_tree_from_branches(
            pattern,
            branches,
            sub_tree_string,
            separator,
            open_node,
            open_branch,
            close_branch,
            close_node,
            self.requested_entry
        )

        
    def get_categories_tree_from_branches(self, pattern, branches, sub_tree_string, sub_tree_separator, open_node, open_branch, close_branch, close_node, from_entry):
        branches = branches.strip()
        self.test_blog_configuration_field(pattern, branches, list)
        
        output = []
        
        for branch_name in self.blog_configuration[branches]:
            node = self.pick_branch(branch_name, None)
            if node != None and len(node.childs):
                if from_entry != None:
                    extracted_branches = self.extract_leaves(from_entry.id, node.childs)
                    if not len(extracted_branches):
                        continue
                        
                output.append(
                    sub_tree_string.format(
                        **self.node_to_dictionnary(
                            pattern,
                            node,
                            open_node,
                            open_branch,
                            close_branch,
                            close_node,
                            node.childs if from_entry == None else extracted_branches
                        )
                    )
                )
        
        return sub_tree_separator.join(output)
                
    def get_blog_categories_tree(self, pattern, open_node, open_branch, close_branch, close_node):
        '''value,html_id,count,weight,path,childs'''
        key = open_node+open_branch+close_branch+close_node
        # compute once categories tree and deliver baked html
        if not key in self.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                self.html_categories_tree[key] = ''

            else:
                self.html_categories_tree[key] = self.build_html_categories_tree(
                    pattern, 
                    open_node,
                    open_branch,
                    close_branch,
                    close_node,
                    self.entries_per_categories
                )

        return self.html_categories_tree[key]
            
    def for_entries_set(self, pattern, entries_subset_key, string):
        '''id,title,path,archive_path,chapter_path,...'''
        output = ""
        try:
            entries = self.cache_entries_subset[entries_subset_key.strip()]
            
        except KeyError:
            from venc3.exceptions import VenCException
            from venc3.l10n import messages
            raise VenCException(
                ("wrong_pattern_argument", "entries_subset_key", entries_subset_key, "ForEntriesSet", messages.argument_does_not_match_with_any_entries_subset),
                pattern
            )
        
        date_format = self.blog_configuration["date_format"]
        archives_directory_name = self.blog_configuration["paths"]["archives_directory_name"]
        for entry in entries:
            dataset = {
                "id" : entry.id,
                "title": entry.title,
                "path": entry.path,
                "archive_path": "\x1a/"+entry.date.strftime(archives_directory_name),
                "chapter_path": entry.chapter.path if entry.chapter != None else ""
            }
            dataset.update({ 
                attr: getattr(entry, attr) for attr in dir(entry) if type(getattr(entry, attr)) in [str, int, float]
            })
            while '∞':
                try:
                    output += string.format(**dataset)
                    break
                except KeyError as e:
                    dataset.update({str(e)[1:-1]:''})
                    
        return output

    def for_blog_archives(self, pattern, string, separator):
        '''value,path,count,weight,html_id'''
        from venc3.helpers import quirk_encoding
        key = string+','+separator
        if not key in self.cache_blog_archives.keys():
            if self.blog_configuration["disable_archives"]:
                self.cache_blog_archives[key] = ''

            else:
                archives = [{
                    "value" : o.value,
                    "html_id" : quirk_encoding(o.value),
                    "path" : o.path,
                    "count" : o.count,
                    "weight" : round(o.count / o.weight_tracker.value,2)
                } for o in self.entries_per_archives if o.value not in self.disable_threads]
                self.cache_blog_archives[key] = merge(archives, string, separator, pattern)

        return self.cache_blog_archives[key]

    def for_blog_metadata(self, pattern, metadata_name, string, separator=''):
        '''value,html_id'''
        return self.for_blog_metadata_if_exists(pattern, metadata_name, string, separator, raise_exception=True)

    def for_blog_metadata_if_exists(self, pattern, metadata_name, string, separator='', raise_exception=False):
        '''value,html_id'''
        key = metadata_name+','+string+','+separator+','+str(raise_exception)
        if not key in self.html_for_metadata:
            if not metadata_name in self.blog_configuration.keys():
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("blog_has_no_metadata_like", metadata_name), pattern)
                    
                self.html_for_metadata[key] = ""
                return ""
                
            if type(self.blog_configuration[metadata_name]) != list:
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("blog_metadata_is_not_a_list", metadata_name), pattern)

            from venc3.helpers import quirk_encoding
            self.html_for_metadata[key] = merge([{"value": v.strip(),"html_id":quirk_encoding(v.strip())} for v in self.blog_configuration[metadata_name]], string, separator, pattern)
        
        return self.html_for_metadata[key]

    def for_entry_metadata(self, pattern, metadata_name, string, separator=''):
        '''value,html_id'''
        return self.for_entry_metadata_if_exists(pattern, metadata_name, string, separator, raise_exception=True)

    def for_entry_metadata_if_exists(self, pattern, metadata_name, string, separator='', raise_exception=False):    
        '''value,html_id'''    
        entry = self.requested_entry
        key = metadata_name+string+separator
            
        if not key in entry.html_for_metadata:
            try:
                l = getattr(entry, metadata_name)
                if not type(l) in [list, tuple]:
                    from venc3.exceptions import VenCException
                    raise VenCException(("entry_metadata_is_not_a_list", metadata_name, entry), pattern)
                
            except AttributeError as e:
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("entry_has_no_metadata_like", entry.id, metadata_name), pattern)
                else:
                    entry.html_for_metadata[key] = ""
                    return ""
                
            try:
                from venc3.helpers import quirk_encoding
                entry.html_for_metadata[key] = separator.join([
                     string.format(**{"value": item.strip(),"html_id":quirk_encoding(item.strip())}) for item in l
                ])
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("unknown_contextual", str(e)), pattern)
            
        return entry.html_for_metadata[key]
            
    def for_entry_authors(self, pattern, string, separator=' '):
        '''value,html_id'''
        return self.for_entry_metadata(pattern, "authors", string, separator)

    def get_blog_metadata_tree(self, pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node):
        '''value,tree,html_id'''
        return self.get_blog_metadata_tree_if_exists(pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=True)

    def get_blog_metadata_tree_if_exists(self, pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=False):
        '''value,childs,html_id'''
        metadata_name = metadata_name.strip()
        key = metadata_name+','+open_node+','+open_branch+value_childs+','+value+','+close_branch+','+close_node+','+str(raise_exception)
        if key in self.html_tree_for_blog_metadata.keys():
            return self.html_tree_for_blog_metadata[key]
            
        if not metadata_name in self.blog_configuration.keys():
            if raise_exception:
                from venc3.exceptions import VenCException
                raise VenCException(("blog_has_no_metadata_like", metadata_name), pattern)
                
            else:
                self.html_tree_for_blog_metadata[key] = ""
                return ""
                
        self.html_tree_for_blog_metadata[key] = self.tree_for_metadata(self.blog_configuration[metadata_name], open_node, open_branch, value_childs, value, close_branch, close_node)
        return self.html_tree_for_blog_metadata[key]
        
    def get_entry_metadata_tree(self, pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node):
        '''value,childs,html_id'''
        return self.get_entry_metadata_tree_if_exists(pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=True)
        
    def get_entry_metadata_tree_if_exists(self, pattern, metadata_name, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=False):
        '''value,childs,html_id'''
        entry = self.requested_entry
        source = metadata_name.strip()
        if not hasattr(entry, metadata_name):
            if raise_exception:
                from venc3.exceptions import VenCException
                raise VenCException(("entry_has_no_metadata_like", entry.id, metadata_name), pattern)
                
            else:
                return ""
                
        return self.tree_for_metadata(getattr(entry, metadata_name), open_node, open_branch, value_childs, value, close_branch, close_node)


    def get_flattened_categories(self, pattern, string, separator, from_entry = False, from_branch = None):
        '''value,count,weight,path,html_id'''

        if self.blog_configuration["disable_categories"]:
            return ''
            
        key = string+'::'+separator+'::'+str(self.requested_entry.id if from_entry else None)+(("::"+str(from_branch.value)) if from_branch != None else '' ) 
        cache = self.requested_entry.html_categories_leaves if from_entry else self.html_categories_leaves

        if not key in cache.keys():
            from venc3.helpers import quirk_encoding
            output = merge(
                sorted(
                    [{
                        "value" : node.value,
                        "html_id": quirk_encoding(node.value),
                        "count" : node.count,
                        "weight" : round(node.count / self.categories_weight_tracker.value, 2),
                        "path" : node.path
                    } for node in self.extract_leaves(
                        self.requested_entry.id if from_entry else None,
                        from_branch.childs if from_branch != None else None
                    )],
                    key = lambda d : d["value"]
                ),
                string,
                separator,
                pattern
            )
        
            cache[key] = output
        
        return cache[key]             

    def get_flattened_categories_from_branches(self, pattern, branches, sub_tree_string, sub_tree_separator, string, separator, from_entry):
        '''value,count,weight,path,html_id'''

        branches = branches.strip()
        self.test_blog_configuration_field(pattern, branches, list)
        
        output = []
        
        from venc3.helpers import quirk_encoding
        
        for branch_name in self.blog_configuration[branches]:
            node = self.pick_branch(branch_name, None)
            # TODO: self.extract_leaves will be called twice ... Boooooo not coooool
            if node != None and len(self.extract_leaves(self.requested_entry.id if from_entry else None, node.childs)):
                output.append(sub_tree_string.format(**{
                    "value"  : node.value,
                    "html_id": quirk_encoding(node.value),
                    "count"  : node.count,
                    "weight" : round(node.count / self.categories_weight_tracker.value, 2),
                    "path"   : node.path,
                    "childs" : self.get_flattened_categories(pattern, string, separator, from_entry, node)
                }))
                
        return sub_tree_separator.join(output)
                
    def get_flattened_blog_categories(self, pattern, string, separator):
        '''value,html_id,count,weight,path'''
        return self.get_flattened_categories(pattern, string, separator)

    def get_flattened_blog_categories_from_branches(self, pattern, branches, sub_tree_string, sub_tree_separator, string, separator):
        '''value,html_id,count,weight,path,childs'''
        
        return self.get_flattened_categories_from_branches(pattern, branches, sub_tree_string, sub_tree_separator, string, separator, False)         
        
    def get_flattened_entry_categories(self, pattern, string, separator):
        '''value,html_id,count,weight,path'''

        return self.get_flattened_categories(pattern, string, separator, True)

    def get_flattened_entry_categories_from_branches(self, pattern, branches, sub_tree_string, sub_tree_separator, string, separator):
        '''value,html_id,count,weight,path,childs'''
        return self.get_flattened_categories_from_branches(pattern, branches, sub_tree_string, sub_tree_separator, string, separator, True)
        
    def pick_branch(self, branch_name, extracted_branch):
        for node in self.entries_per_categories if extracted_branch == None else extracted_branch:
            if branch_name == node.value:
                return node
                
        return None
         
    def range_entries_by_id(self, pattern, begin_at, end_at):
        key = 'rang_entries_by_id,'+begin_at+','+end_at
        if not str(id(key)) in self.cache_entries_subset.keys():
            try:
                begin_at= int(begin_at)
                
            except ValueError:
                from venc3.exceptions import VenCException
                from venc3.l10n import messages
                raise VenCException(
                    ("wrong_pattern_argument", "begin_at", begin_at, "RangeEntriesByID", messages.pattern_argument_must_be_integer),
                    pattern
                )
            
            try:
                end_at = int(end_at)
                
            except ValueError:
                from venc3.exceptions import VenCException
                from venc3.l10n import messages
                raise VenCException(
                    ("wrong_pattern_argument", "end_at", end_at, "RangeEntriesByID", messages.pattern_argument_must_be_integer),
                    pattern
                )
            
            entries = []
            if end_at > begin_at:
                entries = [entry for entry in self.entries if end_at >= entry.id >= begin_at]
                
            elif end_at < begin_at:
                entries = [entry for entry in self.entries[::-1] if end_at <= entry.id <= begin_at]
    
            else:
                entries = []
            
            self.cache_entries_subset[str(id(key))] = entries
            
        return str(id(key))
        
    def test_blog_configuration_field(self, pattern, field_name, field_type):
        if not field_name in self.blog_configuration.keys():
            from venc3.exceptions import VenCException
            raise VenCException(
                ("undefined_variable", field_name, "blog_configuration.yaml"),
                pattern
            )
            
        if type(self.blog_configuration[field_name]) != field_type:
            from venc3.exceptions import VenCException
            raise VenCException(
                ("field_is_not_of_type", field_name, field_type),
                pattern
            )
            
    def tree_for_metadata(self, source, open_node, open_branch, value_childs, value, close_branch, close_node):
        from venc3.helpers import quirk_encoding
        try:
            items = [
                open_branch+value.format(
                    **{"value":item}
                )+close_branch if type(item) != dict else open_branch+value_childs.format(
                    **{
                        "value" : tuple(item.keys())[0],
                        "html_id" : quirk_encoding(tuple(item.keys())[0]),
                        "childs": self.tree_for_metadata(tuple(item.values())[0], open_node, open_branch, value_childs, value, close_branch, close_node)
                    }
                )+close_branch for item in source
            ]
            
        except KeyError as e:
            from venc3.exceptions import VenCException
            raise VenCException(("unknown_contextual", str(e)), pattern)
            
        return open_node + (''.join(items))+ close_node
