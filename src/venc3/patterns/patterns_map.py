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



class PatternsMap():    
    CONTEXTUALS = { # All of the below is loaded from Thread instanciated classes
        "ForPages":	                    "for_pages",
        "GetEntryContent":              "get_entry_content",
        "GetEntryPreview":              "get_entry_preview",
        "GetJSON-LD":	                  "get_JSONLD",
        "GetNextPage":	                "get_next_page",
        "GetPreviousPage":	            "get_previous_page",
        "GetRandomNumber":	            "get_random_number",
        "GetRelativeLocation":	        "get_relative_location",
        "GetRelativeRoot":	            "get_relative_root",
        "GetStyleSheets":	              "get_style_sheets",
        "GetThreadName":	              "get_thread_name",
        "IfInArchives":	                "if_in_archives",
        "IfInCategories":	              "if_in_categories",
        "IfInEntryID":	                "if_in_entry_id",
        "IfInFeed":	                    "if_in_feed",
        "IfInFirstPage":	              "if_in_first_page",
        "IfInLastPage":	                "if_in_last_page",
        "IfInMainThread":	              "if_in_main_thread",
        "IfInThread":	                  "if_in_thread",
        "IfInThreadAndHasFeeds":	      "if_in_thread_and_has_feeds",
        "IfPages":	                    "if_pages",
        "PreviewIfInThreadElseContent": "preview_if_in_thread_else_content",
    }

    NON_CONTEXTUALS = { # all of the below is loaded from datastore
        "entries" : { 
            "ForBlogMetadata":              "for_blog_metadata",
            "ForBlogMetadataIfExists":      "for_blog_metadata_if_exists",
            "ForEntryAuthors":	            "for_entry_authors",
            "ForEntryMetadata":	            "for_entry_metadata",
            "ForEntryMetadataIfExists":	    "for_entry_metadata_if_exists",   
            "GetEntryAttributeByID" :       "get_entry_attribute_by_id",
            "GetEntryArchivePath":	        "get_entry_archive_path",
            "GetEntryChapterLevel":         "get_entry_chapter_level",
            "GetEntryChapterPath":          "get_entry_chapter_path",
            "GetEntryDate":	                "get_entry_date",
            "GetEntryDay":	                "get_entry_day",
            "GetEntryHour":	                "get_entry_hour",
            "GetEntryID":	                  "get_entry_id",
            "GetEntryMetadata":	            "get_entry_metadata",
            "GetEntryMetadataIfExists":     "get_entry_metadata_if_exists",
            "GetEntryMetadataIfNotNull":    "get_entry_metadata_if_not_null",
            "GetEntryMinute":	              "get_entry_minute",
            "GetEntryMonth":	              "get_entry_month",
            "GetEntryPath":	                "get_entry_path",
            "GetEntryTitle":	              "get_entry_title",
            "GetEntryToC":                  "get_entry_toc",
            "GetEntryYear":	                "get_entry_year",
            "IfEntryMetadataIsTrue":	      "if_entry_metadata_is_true",
            "LeavesForEntryCategories":	    "leaves_for_entry_categories",
            "TreeForEntryCategories":	      "tree_for_entry_categories",
            "TreeForEntryMetadata":         "tree_for_entry_metadata",
            "TreeForEntryMetadataIfExists": "tree_for_entry_metadata_if_exists",   
        },
        "blog": {
            "ForBlogArchives":	            "for_blog_archives",
            "ForEntriesSet":	              "for_entries_set",
            "GetAuthorDescription":	        "get_author_description",
            "GetAuthorEmail":               "get_author_email",
            "GetAuthorName":	              "get_author_name",
            "GetBlogDescription":	          "get_blog_description",
            "GetBlogLanguage":	            "get_blog_language",
            "GetBlogLicense":	              "get_blog_license",
            "GetBlogMetadata":	            "get_blog_metadata",
            "GetBlogMetadataIfExists":	    "get_blog_metadata_if_exists",
            "GetBlogMetadataIfNotNull":	    "get_blog_metadata_if_not_null",
            "GetBlogName":	                "get_blog_name",
            "GetBlogURL":	                  "get_blog_url",
            "GetChapterAttributeByIndex" :  "get_chapter_attribute_by_index",
            "GetChapters" :                 "get_chapters",
            "GetRootPage":	                "get_root_page",
            "GetEmbedContent":	            "wrapper_embed_content",
            "GetGenerationTimestamp":	      "get_generation_timestamp",
            "IfAtomEnabled":	              "if_atom_enabled",
            "IfBlogMetadataIsTrue":	        "if_blog_metadata_is_true",
            "IfCategories":	                "if_categories",
            "IfChapters":	                  "if_chapters",
            "IfFeedsEnabled":	              "if_feeds_enabled",
            "IfInfiniteScrollEnabled":	      "if_infinite_scroll_enabled",
            "IfRSSEnabled":	                "if_rss_enabled",
            "LeavesForBlogCategories":	    "leaves_for_blog_categories",
            "RangeEntriesByID":             "range_entries_by_id",
            "TreeForBlogCategories":	      "tree_for_blog_categories",
            "TreeForBlogMetadata":          "tree_for_blog_metadata",
            "TreeForBlogMetadataIfExists":  "tree_for_blog_metadata_if_exists",   
        },
        "extra": { # Loaded from function localy imported
            "Audio":	                  "venc3.patterns.theme.get_audio",
            "CodeHighlight":	          "venc3.patterns.third_party_wrapped_features.pygmentize.highlight",
            "CodeHighlightInclude":	    "venc3.patterns.third_party_wrapped_features.pygmentize.highlight_include",
            "DisableMarkup":	          "venc3.patterns.non_contextual.disable_markup",
            "Escape":                   "venc3.patterns.non_contextual.escape",
            "GetVenCVersion":	          "venc3.patterns.non_contextual.get_venc_version",
            "IncludeFile":	            "venc3.patterns.non_contextual.include_file",
            "IncludeFileIfExists":	    "venc3.patterns.non_contextual.include_file_if_exists",
            "Kroki":	                  "venc3.patterns.third_party_wrapped_features.kroki.kroki",
            "Latex2MathML":	            "venc3.patterns.third_party_wrapped_features.latex2mathml.latex_2_mathml",
            "SetColor":	                "venc3.patterns.non_contextual.set_color",
            "SetStyle":	                "venc3.patterns.non_contextual.set_style",
            "Table":	                  "venc3.patterns.non_contextual.table",
            "Video":	                  "venc3.patterns.theme.get_video",
        },
    }

    NON_PARALLELIZABLES = {
        "ForEntriesSet":	              "for_entries_set",
        "GetChapterAttributeByIndex" :  "get_chapter_attribute_by_index",
        "GetChapters" :                 "get_chapters",
        "GetEntryAttributeByID" :       "get_entry_attribute_by_id",
        "RangeEntriesByID":             "range_entries_by_id",
    }
    
    def __init__(self):                
        import importlib
        self.non_contextual = {
            "extra":    dict(),
            "blog" :    dict(),
            "entries":  dict(),
            "non_parallelizable": dict()
        }
        
        from venc3.patterns.processor import Pattern
        
        for pattern_name in PatternsMap.NON_CONTEXTUALS["extra"].keys():
            pattern_location = PatternsMap.NON_CONTEXTUALS["extra"][pattern_name].split('.')
            function = pattern_location[-1]
            module = '.'+pattern_location[-2]
            package = '.'.join(pattern_location[:-2])
            self.non_contextual["extra"][pattern_name] = getattr(importlib.import_module(module, package), function)
            
        from venc3.datastore import datastore
        for pattern_name in PatternsMap.NON_CONTEXTUALS["blog"].keys():
            self.non_contextual["blog"][pattern_name] = getattr(datastore, PatternsMap.NON_CONTEXTUALS["blog"][pattern_name])

        for pattern_name in PatternsMap.NON_CONTEXTUALS["entries"].keys():
            self.non_contextual["entries"][pattern_name] = getattr(datastore, PatternsMap.NON_CONTEXTUALS["entries"][pattern_name])

        for pattern_name in PatternsMap.NON_PARALLELIZABLES.keys():
            self.non_contextual["non_parallelizable"][pattern_name] = getattr(datastore, PatternsMap.NON_PARALLELIZABLES[pattern_name])
            
def init_pattern_map():
    global patterns_map
    patterns_map = PatternsMap()
        
patterns_map = None

        
