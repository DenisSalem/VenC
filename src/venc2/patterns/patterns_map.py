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

# ~ from venc2.patterns.contextual import get_random_number
# ~ from venc2.patterns.non_contextual import get_venc_version, include_file, include_file_if_exists, set_color, set_style, table, disable_markup

from venc2.patterns.third_party_wrapped_features.latex2mathml import latex_2_mathml
from venc2.patterns.third_party_wrapped_features.kroki import kroki

# # Explicit args naming
# 0 Receive node data
# E Remove all old exceptions usage

class PatternsMap():
    CONTEXTUALS = { # All of the below is loaded from Thread instanciated classes
        "ForPages":	                    "for_pages",                                    #
        "GetJSON-LD":	                  "get_JSONLD",                                   #
        "GetNextPage":	                "get_next_page",                                #
        "GetPreviousPage":	            "get_previous_page",                            #
        "GetRandomNumber":	            "get_random_number",                            #
        "GetRelativeLocation":	        "get_relative_location",                        #
        "GetRelativeOrigin":	          "get_relative_origin",                          #
        "GetStyleSheets":	              "code_highlight.get_style_sheets",              #
        "GetThreadName":	              "get_thread_name",                              # 
        "IfInArchives":	                "if_in_archives",                               #
        "IfInCategories":	              "if_in_categories",                             #
        "IfInEntryID":	                "if_in_entry_id",                               #
        "IfInFeed":	                    "if_in_feed",                                   #
        "IfInFirstPage":	              "if_in_first_page",                              #
        "IfInLastPage":	                "if_in_last_page",                              #
        "IfInMainThread":	              "if_in_main_thread",                            #
        "IfInThread":	                  "if_in_thread",                                 #
        "IfInThreadAndHasFeeds":	      "if_in_thread_and_has_feeds",                   #
        "IfPages":	                    "if_pages",                                     #
    }

    NON_CONTEXTUALS = { # all of the below is loaded from datastore
        "entries" : { 
            "ForEntryAuthors":	          "datastore.for_entry_authors",                #OE
            "ForEntryMetadata":	          "datastore.for_entry_metadata",               #OE
            #"ForEntryRange":	            "datastore.for_entry_range",                  #OE  TODO: NOT FINISHED YET
            "ForEntryTags":	              "datastore.for_entry_tags",                   #OE
            "GetEntryDate":	              "datastore.get_entry_date",                   #OE
            "GetEntryDateURL":	          "datastore.get_entry_date_url",               #OE
            "GetEntryDay":	              "datastore.get_entry_day",                    #OE
            "GetEntryHour":	              "datastore.get_entry_hour",                   #OE
            "GetEntryID":	                "datastore.get_entry_id",                     #OE
            "GetEntryMetadata":	          "datastore.get_entry_metadata",               #OE
            "GetEntryMetadataIfExists":   "datastore.get_entry_metadata_if_exists",     #OE
            "GetEntryMetadataIfNotNull":  "datastore.get_entry_metadata_if_not_null",   #OE
            "GetEntryMinute":	            "datastore.get_entry_minute",                 #OE
            "GetEntryMonth":	            "datastore.get_entry_month",                  #OE
            "GetEntryTitle":	            "datastore.get_entry_title",                  #OE
            "GetEntryToC":                "datastore.get_entry_toc",                    #OE
            "GetEntryURL":	              "datastore.get_entry_url",                    #OE
            "GetEntryYear":	              "datastore.get_entry_year",                   #OE
            "IfEntryMetadataIsTrue":	    "datastore.if_entry_metadata_is_true",        #OE
            "LeavesForEntryCategories":	  "datastore.leaves_for_entry_categories",      #OE
            "TreeForEntryCategories":	    "datastore.tree_for_entry_categories",        #OE
        },
        "blog": {
            "ForBlogArchives":	          "datastore.for_blog_archives",                #OE
            "GetAuthorDescription":	      "datastore.get_author_description",           #OE
            "GetAuthorEmail":             "datastore.get_author_email",                 #OE
            "GetAuthorName":	            "datastore.get_author_name",                  #OE
            "GetBlogDescription":	        "datastore.get_blog_description",             #OE
            "GetBlogKeywords":	          "datastore.get_blog_keywords",                #OE
            "GetBlogLanguage":	          "datastore.get_blog_language",                #OE
            "GetBlogLicense":	            "datastore.get_blog_license",                 #OE
            "GetBlogMetadata":	          "datastore.get_blog_metadata",                #OE
            "GetBlogMetadataIfExists":	  "datastore.get_blog_metadata_if_exists",      #OE
            "GetBlogMetadataIfNotNull":	  "datastore.get_blog_metadata_if_not_null",    #OE
            "GetBlogName":	              "datastore.get_blog_name",                    #OE
            "GetBlogURL":	                "datastore.get_blog_url",                     #OE
            "GetChapterAttributeByIndex": "datastore.get_chapter_attribute_by_index",   #OE
            "GetChapters" :               "datastore.get_chapters",                     #OE
            "GetRootPage":	              "datastore.get_root_page",                    #OE
            "GetEmbedContent":	          "datastore.wrapper_embed_content",            #OE
            "GetEntryAttributeByID":      "datastore.get_entry_attribute_by_id",        #OE
            "GetGenerationTimestamp":	    "datastore.get_generation_timestamp",         #OE
            "IfAtomEnabled":	            "datastore.if_atom_enabled",                  #OE
            "IfBlogMetadataIsTrue":	      "datastore.if_blog_metadata_is_true",         #OE
            "IfCategories":	              "datastore.if_categories",                    #OE
            "IfChapters":	                "datastore.if_chapters",                      #OE
            "IfFeedsEnabled":	            "datastore.if_feeds_enabled",                 #OE
            "IfInfiniteScrollEnabled":	    "datastore.if_infinite_scroll_enabled",        #OE
            "IfRSSEnabled":	              "datastore.if_rss_enabled",                   #OE
            "LeavesForBlogCategories":	  "datastore.leaves_for_blog_categories",       #OE
            "TreeForBlogCategories":	    "datastore.tree_for_blog_categories",         #OE
        },
        "extra": { # Loaded from function localy imported
            "Audio":	                  "get_audio",                                    #OE
            "CodeHighlight":	          "highlight",                                    #OE
            "CodeHighlightInclude":	    "highlight_include",                            #OE
            "DisableMarkup":	          "disable_markup",                               #OE
            "GetVenCVersion":	          "get_venc_version",                             #OE
            "IncludeFile":	            "include_file",                                  #OE
            "IncludeFileIfExists":	    "include_file_if_exists",                        #OE
            "Kroki":	                  "kroki",                                        #OE
            "Latex2MathML":	            "latex_2_mathml",                               #OE
            "SetColor":	                "set_color",                                    #OE
            "SetStyle":	                "set_style",                                    #OE
            "Table":	                  "table",                                        #OE
            "Video":	                  "get_video",                                    #OE
        },
    }

    NON_PARALLELIZABLES = (
        "GetChapterAttributeByIndex",
        "GetChapters",
        "GetEntryAttributeByID",
    )

    # TODO
    WAIT_FOR_CHILDREN_TO_BE_PROCESSED = ()
