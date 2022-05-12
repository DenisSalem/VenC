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
        "ForPages":	                    "for_pages",
        "GetJSON-LD":	                  "get_JSONLD",
        "GetNextPage":	                "get_next_page",
        "GetPreviousPage":	            "get_previous_page",
        "GetRandomNumber":	            "get_random_number",
        "GetRelaqtiveLocation":	        "get_relative_location",
        "GetRelativeOrigin":	          "get_relative_origin",
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
    }

    NON_CONTEXTUALS = { # all of the below is loaded from datastore
        "entries" : { 
            "ForEntryAuthors":	          "datastore.for_entry_authors",
            "ForEntryMetadata":	          "datastore.for_entry_metadata",
            #"ForEntryRange":	            "datastore.for_entry_range",                  #OE  TODO: NOT FINISHED YET
            "ForEntryTags":	              "datastore.for_entry_tags",
            "GetEntryDate":	              "datastore.get_entry_date",
            "GetEntryDateURL":	          "datastore.get_entry_date_url",
            "GetEntryDay":	              "datastore.get_entry_day",
            "GetEntryHour":	              "datastore.get_entry_hour",
            "GetEntryID":	                "datastore.get_entry_id",
            "GetEntryMetadata":	          "datastore.get_entry_metadata",
            "GetEntryMetadataIfExists":   "datastore.get_entry_metadata_if_exists",
            "GetEntryMetadataIfNotNull":  "datastore.get_entry_metadata_if_not_null",
            "GetEntryMinute":	            "datastore.get_entry_minute",
            "GetEntryMonth":	            "datastore.get_entry_month",
            "GetEntryTitle":	            "datastore.get_entry_title",
            "GetEntryToC":                "datastore.get_entry_toc",
            "GetEntryURL":	              "datastore.get_entry_url",
            "GetEntryYear":	              "datastore.get_entry_year",
            "IfEntryMetadataIsTrue":	    "datastore.if_entry_metadata_is_true",
            "LeavesForEntryCategories":	  "datastore.leaves_for_entry_categories",
            "TreeForEntryCategories":	    "datastore.tree_for_entry_categories",
        },
        "blog": {
            "ForBlogArchives":	          "datastore.for_blog_archives",
            "GetAuthorDescription":	      "datastore.get_author_description",
            "GetAuthorEmail":             "datastore.get_author_email",
            "GetAuthorName":	            "datastore.get_author_name",
            "GetBlogDescription":	        "datastore.get_blog_description",
            "GetBlogKeywords":	          "datastore.get_blog_keywords",
            "GetBlogLanguage":	          "datastore.get_blog_language",
            "GetBlogLicense":	            "datastore.get_blog_license",
            "GetBlogMetadata":	          "datastore.get_blog_metadata",
            "GetBlogMetadataIfExists":	  "datastore.get_blog_metadata_if_exists",
            "GetBlogMetadataIfNotNull":	  "datastore.get_blog_metadata_if_not_null",
            "GetBlogName":	              "datastore.get_blog_name",
            "GetBlogURL":	                "datastore.get_blog_url",
            "GetChapterAttributeByIndex": "datastore.get_chapter_attribute_by_index",
            "GetChapters" :               "datastore.get_chapters",
            "GetRootPage":	              "datastore.get_root_page",
            "GetEmbedContent":	          "datastore.wrapper_embed_content",
            "GetEntryAttributeByID":      "datastore.get_entry_attribute_by_id",
            "GetGenerationTimestamp":	    "datastore.get_generation_timestamp",
            "IfAtomEnabled":	            "datastore.if_atom_enabled",
            "IfBlogMetadataIsTrue":	      "datastore.if_blog_metadata_is_true",
            "IfCategories":	              "datastore.if_categories",
            "IfChapters":	                "datastore.if_chapters",
            "IfFeedsEnabled":	            "datastore.if_feeds_enabled",
            "IfInfiniteScrollEnabled":	    "datastore.if_infinite_scroll_enabled",
            "IfRSSEnabled":	              "datastore.if_rss_enabled",
            "LeavesForBlogCategories":	  "datastore.leaves_for_blog_categories",
            "TreeForBlogCategories":	    "datastore.tree_for_blog_categories",
        },
        "extra": { # Loaded from function localy imported
            "Audio":	                  "get_audio",
            "CodeHighlight":	          "highlight",
            "CodeHighlightInclude":	    "highlight_include",
            "DisableMarkup":	          "disable_markup",
            "GetVenCVersion":	          "get_venc_version",
            "IncludeFile":	            "include_file",
            "IncludeFileIfExists":	    "include_file_if_exists",
            "Kroki":	                  "kroki",
            "Latex2MathML":	            "latex_2_mathml",
            "SetColor":	                "set_color",
            "SetStyle":	                "set_style",
            "Table":	                  "table",
            "Video":	                  "get_video",
        },
    }

    NON_PARALLELIZABLES = (
        "GetChapterAttributeByIndex",
        "GetChapters",
        "GetEntryAttributeByID",
    )

    # TODO
    WAIT_FOR_CHILDREN_TO_BE_PROCESSED = ()
