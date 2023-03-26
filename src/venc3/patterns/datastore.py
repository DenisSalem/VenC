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

from venc3.datastore.metadata import Chapter
from venc3.datastore.metadata import build_categories_tree

def merge(iterable, string, separator, node):
    try:
        return separator.join([string.format(**something) for something in iterable])
    
    except KeyError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("unknown_contextual", str(e)), node)

class DatastorePatterns:
    def if_categories(self, node, if_true, if_false=''):
        if self.entries_per_categories != [] and not self.blog_configuration["disable_categories"]:
            return if_true
            
        else:
            return if_false
    
    def if_chapters(self, node, if_true, if_false=''):
        if self.chapters_index != [] and not self.blog_configuration["disable_chapters"]:
            return if_true
            
        else:
            return if_false
    
    def if_feeds_enabled(self, node, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"] and self.blog_configuration["disable_rss_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")
            
        else: 
            return if_true.replace("{relative_origin}", "\x1a")
        
    def if_atom_enabled(self, node, if_true, if_false=''):
        if self.blog_configuration["disable_atom_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")

        else: 
            return if_true.replace("{relative_origin}", "\x1a")

    def if_metadata_is_true(self, key, if_true, if_false, source):            
        try:
            if type(source) == Entry and getattr(source, key):
                return if_true.strip()

            elif source[key]:
                return if_true.strip()
        
        except:
            pass
        
        return if_false.strip()
    def if_blog_metadata_is_true(self, node, key, if_true, if_false=''):
        return self.if_metadata_is_true(key, if_true, if_false, self.blog_configuration)

    def if_entry_metadata_is_true(self, node, key, if_true, if_false=''):
        return self.if_metadata_is_true(key, if_true, if_false, self.requested_entry)
                
    def if_rss_enabled(self, node, if_true, if_false=''):
        if self.blog_configuration["disable_rss_feed"]:
            return if_false.replace("{relative_origin}", "\x1a")
            
        else:
            return if_true.replace("{relative_origin}", "\x1a")

    def if_infinite_scroll_enabled(self, node, if_true, if_false=''):            
        try:
            if self.blog_configuration["disable_infinite_scroll"]:
                return if_false
                                    
            else:
                return if_true
                    
        except KeyError:
            return if_true
            
    def get_chapters(self, node, lo, io, ic, lc):
        key = lo+io+ic+lc
        if not key in self.html_chapters.keys():
            self.html_chapters[key] = self.build_html_chapters(lo, io, ic, lc, self.chapters_index, 0)

        return self.html_chapters[key]

    def get_entry_toc(self, node, open_ul, open_li, content, close_li, close_ul):
        key = open_ul+open_li+content+close_li+close_ul
        if not key in self.cache_entry_tocs.keys():
            self.cache_entry_tocs[key] = self.build_entry_html_toc(self.requested_entry, open_ul, open_li, content, close_li, close_ul)
        return self.cache_entry_tocs[key]
        
    def get_generation_timestamp(self, node, time_format):
        return datetime.datetime.strftime(self.generation_timestamp, time_format)
            
    def get_blog_metadata(self, node, field_name):
        # if exception is raised it will be automatically be catch by processor.
        try:
            return str(self.blog_configuration[field_name])
            
        except KeyError:
            raise VenCException(("blog_has_no_metadata_like", field_name), context=self)
            
    def get_blog_metadata_if_exists(self, node, field_name, if_true='', if_false='', ok_if_null=True):
        try:
            value = self.blog_configuration[field_name]
            
        except KeyError:
            return if_false
        
        if len(if_true):
            if ok_if_null or len(value):
                return if_true.format(**{"value" : value,"{relative_origin}":"\x1a"})
                  
            else:
                return if_false
        else:
            return value

    def get_blog_metadata_if_not_null(self, node, field_name, if_true='', if_false='', ):
        return self.get_blog_metadata_if_exists(node, field_name, if_true, if_false, ok_if_null=False)

    def get_entry_attribute_by_id(self, node, attribute, identifier):            
        key = attribute+identifier
        if not key in self.cache_get_entry_attribute_by_id.keys():
            try:
                entry = [entry for entry in self.entries if entry.id == int(identifier)][0]
                self.cache_get_entry_attribute_by_id[key] = getattr(entry, attribute)
            
            except ValueError:
                from venc3.exceptions import VenCException
                raise VenCException(("id_must_be_an_integer",), node)
                
            except AttributeError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("entry_has_no_metadata_like", argv[0]), node)

            except IndexError:
                from venc3.exceptions import VenCException
                raise VenCException(("cannot_retrieve_entry_attribute_because_wrong_id",), node)
            
        return self.cache_get_entry_attribute_by_id[key]
    
    def get_entry_chapter_level(self, node):
        try:
            return self.requested_entry.chapter_level
            
        except:
            return ''
            
    def get_entry_chapter_path(self, node):
        if self.blog_configuration["disable_chapters"]:
            return ''
        else:
            return self.requested_entry.chapter.path if hasattr(self.requested_entry, "chapter") and type(self.requested_entry.chapter) == Chapter else ''

    def get_entry_metadata(self, node, metadata_name):            
        try:
            return str(getattr(self.requested_entry, metadata_name))
            
        except AttributeError:
            from venc3.exceptions import VenCException
            raise VenCException(
                ("entry_has_no_metadata_like", metadata_name),
                node
            )
            
    def get_entry_metadata_if_exists(self, node, metadata_name, string='', string2='', ok_if_null=True):
        try:
            value = str(getattr(self.requested_entry,metadata_name ))

        except AttributeError:
            return string2
        
        if string == '':
            return value

        if len(value) or ok_if_null:
            return string.format(**{"value" : value, "relative_origin": "\x1a"})
            
        else:
            return string2
            
    def get_entry_metadata_if_not_null(self, node, metadata_name, string='', string2=''):
        return self.get_entry_metadata_if_exists(node, metadata_name, string, string2, ok_if_null=False)
        
    def get_entry_title(self, node):
        return self.requested_entry.title
    
    def get_entry_id(self, node):
        return str(self.requested_entry.id)
            
    def get_entry_year(self, node):
        return self.requested_entry.date.year

    def get_entry_month(self, node):
        return self.requested_entry.date.month
        
    def get_entry_day(self, node):
        return self.requested_entry.date.day

    def get_entry_hour(self, node):
        return self.requested_entry.date.hour
    
    def get_entry_minute(self, node):
        return self.requested_entry.date.minute

    def get_entry_date(self, node, date_format=''):
        return self.requested_entry.date.strftime(
            date_format if len(date_format) else self.blog_configuration["date_format"]
        )

    def get_entry_archive_path(self, node):
        return "\x1a"+self.requested_entry.date.strftime(
            self.blog_configuration["path"]["archives_directory_name"]
        )
    
    def get_chapter_attribute_by_index(self, node, attribute, index):
        if self.blog_configuration["disable_chapters"]:
            return ""
        
        key = attribute+index
        if not key in self.cache_get_chapter_attribute_by_index.keys():
            try:
                self.cache_get_chapter_attribute_by_index[key] = getattr(self.raw_chapters[index].chapter, attribute)
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("there_is_no_chapter_with_index", index), node)
                
            except AttributeError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("chapter_has_no_attribute_like", attribute), node)
                
        return self.cache_get_chapter_attribute_by_index[key]
            
    def get_entry_path(self, node):
        if self.blog_configuration["disable_single_entries"]:
            return
        else:
            if self.requested_entry.path[-10:] == "index.html":
                return self.requested_entry.path[:-10]
            else:
                return self.requested_entry.path

    def get_author_name(self, node):
        return self.get_blog_metadata_if_exists(node, "author_name")

    def get_blog_name(self, node):
        return self.blog_configuration["blog_name"]
        
    def get_blog_description(self, node):
      
        return self.get_blog_metadata_if_exists(node, "blog_description")

    def get_author_description(self, node):
        return self.get_blog_metadata_if_exists(node, "author_description")

        
    def get_blog_license(self, node):
        return self.get_blog_metadata_if_exists(node, "license")
    
    def get_blog_url(self, node):
        return self.blog_configuration["blog_url"]
    
    def get_blog_language(self, node):
        return self.get_blog_metadata_if_exists(node, "blog_language")
    
    def get_author_email(self, node):
        return self.get_blog_metadata_if_exists(node, "author_email")

    def get_root_page(self, node):
        if self.root_page == None:
            self.root_page =  "\x1a"+self.blog_configuration["path"]["index_file_name"].format(**{"page_number":''})
            
        return self.root_page
        
    def tree_for_entry_categories(self, node, open_node, open_branch, close_branch, clode_node):
        key = open_node+open_branch+close_branch+clode_node
        entry = self.requested_entry

        if not key in self.requested_entry.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                entry.html_categories_tree[key] = ''

            else:
                DatastorePatterns.build_entry_entry_categories_tree(entry)
                entry.html_categories_tree[key] = self.build_html_categories_tree(
                    open_node,
                    open_branch,
                    close_branch,
                    clode_node,
                    entry.categories_tree
                )
        
        return entry.html_categories_tree[key]

    def build_entry_entry_categories_tree(self, entry):
        if entry.categories_leaves == None:
            entry.categories_tree = []
            entry.categories_leaves = []
            pick_branches_and_leaves(
                self,
                entry.raw_categories,
                entry.categories_tree,
                entry.categories_leaves
            )

    def build_blog_categories_tree(self):
        if self.entries_per_categories == None:
            self.entries_per_categories = []
            self.categories_leaves = []
            path = self.blog_configuration["path"]["categories_sub_folders"]
            for entry_index in range(0, len(self.entries)):
                current_entry = self.entries[entry_index]
                build_categories_tree(
                    entry_index,
                    current_entry.raw_categories,
                    self.entries_per_categories,
                    self.categories_leaves,
                    self.categories_weight_tracker,
                    sub_folders="\x1a"+path
                )
            self.categories_leaves = [category for category in self.categories_leaves if len(category.childs) == 0]
                
    def tree_for_blog_categories(self, node, open_node, open_branch, close_branch, clode_node):
        key = open_node+open_branch+close_branch+clode_node
        # compute once categories tree and deliver baked html
        if not key in self.html_categories_tree.keys():
            if self.blog_configuration["disable_categories"]:
                self.html_categories_tree[key] = ''

            else:
                self.build_blog_categories_tree(self.blog_configuration["path"]["categories_sub_folders"])
                self.html_categories_tree[key] = self.build_html_categories_tree(
                    node, 
                    open_node,
                    open_branch,
                    close_branch,
                    clode_node,
                    self.entries_per_categories
                )

        return self.html_categories_tree[key]
        
        
    def range_entries_by_id(self, node, begin_at, end_at):
        key = 'rang_entries_by_id,'+begin_at+','+end_at
        if not str(id(key)) in self.cache_entries_subset.keys():
            try:
                begin_at= int(begin_at)
                
            except ValueError:
                from venc3.exceptions import VenCException
                from venc3.l10n import messages
                raise VenCException(
                    ("wrong_pattern_argument", "begin_at", begin_at, "RangeEntriesByID", messages.pattern_argument_must_be_integer),
                    node
                )
            
            try:
                end_at = int(end_at)
                
            except ValueError:
                from venc3.exceptions import VenCException
                from venc3.l10n import messages
                raise VenCException(
                    ("wrong_pattern_argument", "end_at", end_at, "RangeEntriesByID", messages.pattern_argument_must_be_integer),
                    node
                )
            
            entries = []
            if end_at > begin_at:
                entries = [entry for entry in self.entries if end_at >= entry.id >= begin_at]
                
            elif end_at < begin_at:
                entries = [entry for entry in self.entries if end_at >= entry.id >= begin_at]
    
            else:
                entries = []
            
            print(len(entries))
            self.cache_entries_subset[str(id(key))] = entries
            
        return str(id(key))
            
    def for_entries_set(self, node, entries_subset_key, string):
        output = ""
        try:
            entries = self.cache_entries_subset[entries_subset_key.strip()]
            
        except KeyError:
            from venc3.exceptions import VenCException
            from venc3.l10n import messages
            raise VenCException(
                ("wrong_pattern_argument", "entries_subset_key", entries_subset_key, "ForEntriesSet", messages.argument_does_not_match_with_any_entries_subset),
                node
            )
        
        date_format = self.blog_configuration["date_format"]
        archives_directory_name = self.blog_configuration["path"]["archives_directory_name"]
        for entry in entries:
            dataset = {
                "id" : entry.id,
                "title": entry.title,
                "url": entry.path,
                "archive_path": "\x1a"+entry.date.strftime(archives_directory_name),
                "reference_id":str(id(entry))
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

    def for_blog_archives(self, node, string, separator):
        key = string+','+separator
        if not key in self.cache_blog_archives.keys():
            if self.blog_configuration["disable_archives"]:
                self.cache_blog_archives[key] = ''

            else:
                archives = [{
                    "value" : o.value,
                    "path" : o.path,
                    "count" : o.count,
                    "weight" : round(o.count / o.weight_tracker.value,2)
                } for o in self.entries_per_archives if o.value not in self.disable_threads]
                self.cache_blog_archives[key] = merge(archives, string, separator, node)

        return self.cache_blog_archives[key]

    def for_blog_metadata(self, node, metadata_name, string, separator):
        return self.for_blog_metadata_if_exists(node, metadata_name, string, separator, raise_exception=True)

    def for_blog_metadata_if_exists(self, node, metadata_name, string, separator, raise_exception=False):
        key = metadata_name+','+string+','+separator+','+str(raise_exception)
        if not key in self.html_for_metadata:
            if not metadata_name in self.blog_configuration.keys():
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("blog_has_no_metadata_like", metadata_name), node)
                    
                self.html_for_metadata[key] = ""
                return ""
                
            if type(self.blog_configuration[metadata_name]) != list:
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("blog_metadata_is_not_a_list", metadata_name), node)
                    
                self.html_for_metadata[key] = ""
                
            self.html_for_metadata[key] = merge([{"value": v} for v in self.blog_configuration[metadata_name]], string, separator, node)
        
        return self.html_for_metadata[key]

    def for_entry_metadata(self, node, variable_name, string, separator):
        return self.for_entry_metadata_if_exists(node, variable_name, string, separator, raise_exception=True)

    def for_entry_metadata_if_exists(self, node, variable_name, string, separator, raise_exception=False):        
        entry = self.requested_entry
        key = variable_name+string+separator
            
        if not key in entry.html_for_metadata:
            try:
                l = getattr(entry, variable_name)
                if not type(l) in [list, tuple]:
                    from venc3.exceptions import VenCException
                    raise VenCException(("entry_metadata_is_not_a_list", variable_name, entry), node)
                
            except AttributeError as e:
                if raise_exception:
                    from venc3.exceptions import VenCException
                    raise VenCException(("entry_has_no_metadata_like", variable_name), node)
                else:
                    entry.html_for_metadata[key] = ""
                    return ""
                
            try:
                entry.html_for_metadata[key] = separator.join([
                     string.format(**{"value": item.strip()}) for item in l
                ])
                
            except KeyError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("unknown_contextual", str(e)), node)
            
        return entry.html_for_metadata[key]
            
    def for_entry_authors(self, node, string, separator=' '):
        return self.for_entry_metadata(node, "authors", string, separator)

    def tree_for_blog_metadata(self, node, source, open_node, open_branch, value_childs, value, close_branch, close_node):
        return self.tree_for_blog_metadata_if_exists(node, source, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=True)

    def tree_for_blog_metadata_if_exists(self, node, source, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=False):
        key = source+','+open_node+','+open_branch+value_childs+','+value+','+close_branch+','+close_node+','+str(raise_exception)
        if key in self.html_tree_for_blog_metadata.keys():
            return self.html_tree_for_blog_metadata[key]
            
        if not source in self.blog_configuration.keys():
            if raise_exception:
                from venc3.exceptions import VenCException
                raise VenCException(("blog_has_no_metadata_like", source), node)
                
            else:
                self.html_tree_for_blog_metadata[key] = ""
                return ""
                
        self.html_tree_for_blog_metadata[key] = self.tree_for_metadata(node, self.blog_configuration[source], open_node, open_branch, value_childs, value, close_branch, close_node)
        return self.html_tree_for_blog_metadata[key]
        
    def tree_for_entry_metadata(self, node, source, open_node, open_branch, value_childs, value, close_branch, close_node):
        return self.tree_for_entry_metadata_if_exists (node, source, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=True)
        
    def tree_for_entry_metadata_if_exists(self, node, source, open_node, open_branch, value_childs, value, close_branch, close_node, raise_exception=False):
        entry = self.requested_entry
        if not hasattr(entry, source):
            if raise_exception:
                from venc3.exceptions import VenCException
                raise VenCException(("entry_has_no_metadata_like", source), node)
                
            else:
                return ""
                
        return self.tree_for_metadata(node, getattr(entry, source), open_node, open_branch, value_childs, value, close_branch, close_node)
                    
    def tree_for_metadata(self, node, source, open_node, open_branch, value_childs, value, close_branch, close_node):
        try:
            items = [
                open_branch+value.format(
                    **{"value":item}
                )+close_branch if type(item) != dict else open_branch+value_childs.format(
                    **{
                        "value" : tuple(item.keys())[0],
                        "childs": self.tree_for_metadata(node, tuple(item.values())[0], open_node, open_branch, value_childs, value, close_branch, close_node)
                    }
                )+close_branch for item in source
            ]
            
        except KeyError as e:
            from venc3.exceptions import VenCException
            raise VenCException(("unknown_contextual", str(e)), node)
            
        return open_node + (''.join(items))+ close_node

    def leaves_for_entry_categories(self, pattern, string, separator):
        key = string+separator
        entry = self.requested_entry
        if not key in entry.html_categories_leaves.keys():
            if self.blog_configuration["disable_categories"]:
                entry.html_categories_leaves[key] = ''

            else:
                self.build_entry_entry_categories_tree(entry)
                entry.html_categories_leaves[key] = merge(
                    [ {
                        "value" : node.value,
                        "count" : node.count,
                        "weight" : round(node.count / self.categories_weight_tracker.value, 2),
                        "path" : node.path
                    } for node in entry.categories_leaves],
                    string,
                    separator,
                    pattern
                )
              
        return entry.html_categories_leaves[key]

    def leaves_for_blog_categories(self, node, string, separator):
        key = string+separator

        if not key in self.html_categories_leaves.keys():
            if self.blog_configuration["disable_categories"]:
                self.html_categories_leaves[key] = ''

            else:
                self.build_blog_categories_tree()
                self.html_categories_leaves[key] = merge(
                    [ {
                        "value" : node.value,
                        "count" : node.count,
                        "weight" : round(node.count / self.categories_weight_tracker.value,2),
                        "path" : node.path
                    } for node in self.categories_leaves],
                    string,
                    separator,
                    node
                )
        
        return self.html_categories_leaves[key]
        
    def wrapper_embed_content(self, node, content_url):
        cache = self.cache_embed_exists(content_url)
        if cache != "":
            return cache

        else:
            if self.embed_providers == dict():
                import os
                import json
                f = open(os.path.expanduser("~")+"/.local/share/VenC/embed_providers/oembed.json")
                self.embed_providers["oembed"] = {}
                j = json.load(f)
                for p in j:
                    self.embed_providers["oembed"][p["provider_url"]] = []
                    for e in p["endpoints"]:
                        self.embed_providers["oembed"][p["provider_url"]].append(e["url"])
                        
        from venc3.patterns.non_contextual import get_embed_content
        return get_embed_content(node, self.embed_providers, content_url)
