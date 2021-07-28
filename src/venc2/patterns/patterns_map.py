#! /usr/bin/env python3

#    Copyright 2016, 2020 Denis Salem
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

from venc2.patterns.contextual import get_random_number
from venc2.patterns.latex2mathml import Latex2MathML
from venc2.patterns.non_contextual import get_venc_version, include_file, set_color, set_style, table, disable_markup

class PatternsMap():
    def __init__(self, datastore, code_highlight, theme):
        self.non_contextual = {
            "entries" : {
                # General entry data
                "GetEntryTitle" :   datastore.get_entry_title,
                "GetEntryID" :      datastore.get_entry_id,
                "GetEntryYear" :    datastore.get_entry_year,
                "GetEntryMonth" :   datastore.get_entry_month,
                "GetEntryDay" :     datastore.get_entry_day,
                "GetEntryHour" :    datastore.get_entry_hour, 
                "GetEntryMinute" :  datastore.get_entry_minute,
                "GetEntryDate" :    datastore.get_entry_date,
                "GetEntryDateURL" : datastore.get_entry_date_url,
                "GetEntryURL" :     datastore.get_entry_url,
                "ForEntryAuthors" : datastore.for_entry_authors, 
                "ForEntryTags" :    datastore.for_entry_tags,
    
                # Extra metadata getter
                "LeavesForEntryCategories" :    datastore.leaves_for_entry_categories,
                "TreeForEntryCategories" :      datastore.tree_for_entry_categories,
                "ForEntryMetadata" :            datastore.for_entry_metadata,
                "ForEntryRange" :               datastore.for_entry_range,
                "GetEntryMetadata" :            datastore.get_entry_metadata,
                "GetEntryMetadataIfExists" :    datastore.get_entry_metadata_if_exists,
                "GetEntryMetadataIfNotNull":    datastore.get_entry_metadata_if_not_null
            },
            "blog": {
                "GetAuthorName" :               datastore.get_author_name,
                "GetBlogName" :                 datastore.get_blog_name,
                "GetBlogDescription" :          datastore.get_blog_description,
                "GetBlogKeywords" :             datastore.get_blog_keywords,
                "GetAuthorDescription" :        datastore.get_author_description,
                "GetBlogLicense" :              datastore.get_blog_license,
                "GetBlogURL" :                  datastore.get_blog_url,
                "GetBlogLanguage" :             datastore.get_blog_language,
                "GetAuthorEmail" :              datastore.get_author_email,

                # Extra metadata getter
                "GetChapterAttributeByIndex":   datastore.get_chapter_attribute_by_index,
                "GetEntryAttributeByID":        datastore.get_entry_attribute_by_id,
                "GetBlogMetadata" :             datastore.get_blog_metadata, 
                "GetBlogMetadataIfExists" :     datastore.get_blog_metadata_if_exists, 
                "GetBlogMetadataIfNotNull":     datastore.get_blog_metadata_if_not_null, 
                "ForBlogArchives" :             datastore.for_blog_archives,
                "LeavesForBlogCategories" :     datastore.leaves_for_blog_categories,
                "TreeForBlogCategories" :       datastore.tree_for_blog_categories,
                "GetChapters" :                 datastore.get_chapters
            },
            "extra": {
                "IfInfiniteScrollEnabled":  datastore.if_infinite_scroll_enabled,
                "IfFeedsEnabled":           datastore.if_feeds_enabled,
                "IfRSSEnabled":             datastore.if_rss_enabled,
                "IfAtomEnabled":            datastore.if_atom_enabled,          
                "IfCategories":             datastore.if_categories,
                "IfChapters":               datastore.if_chapters,
                "GetEmbedContent":          datastore.wrapper_embed_content,
                "GetGenerationTimestamp":   datastore.get_generation_timestamp,
                "CodeHighlight" :           code_highlight.highlight,
                "CodeHighlightInclude" :    code_highlight.highlight_include,
                "Latex2MathML" :            Latex2MathML,
                "GetVenCVersion" :          get_venc_version,
                "IncludeFile" :             include_file,
                "SetColor" :                set_color,
                "SetStyle" :                set_style,
                "DisableMarkup":            disable_markup,
                "Video" :                   theme.get_video,
                "Audio" :                   theme.get_audio,
                "Table" :                   table
            }
        }

        self.non_contextual_entries_keys = self.non_contextual["entries"].keys()

        self.contextual = {
            "functions" : {
                "GetStyleSheets" :  code_highlight.get_style_sheets,
                "GetRootPage" :     datastore.get_root_page,
                "GetRandomNumber" : get_random_number
            },
            "names" : {
                # Patterns below are acquired dynamically because they depend on the context
                "GetJSON-LD" : "GetJSONLD",
                "IfInThread" : "if_in_thread",
                "IfInFeed" : "if_in_feed",
                "IfInThreadAndHasFeeds" : "if_in_thread_and_has_feeds",
                "IfInMainThread" : "if_in_main_thread",
                "IfInArchives" : "if_in_archives",
                "IfInCategories" : "if_in_categories",
                "IfInFirstPage" : "if_in_first_page",
                "IfInLastPage" : "if_in_last_page",
                "IfInEntryID" : "if_in_entry_id",
                "GetRelativeLocation" : "get_relative_location",
                "GetRelativeOrigin" : "get_relative_origin",
                "GetNextPage" : "get_next_page",
                "GetPreviousPage" : "get_previous_page",
                "GetThreadName": "get_thread_name",
                "ForPages" : "for_pages",
                "IfPages" : "if_pages"
            }
        }
        
        self.keep_appart_from_markup = [
            "CodeHighlight",
            "CodeHighlightInclude",
            "Latex2MathML",
            "IncludeFile",
            "SetStyle",
            "Audio",
            "Video",
            "GetEmbedContent",
            "Table",
            "DisableMarkup",
        ]
