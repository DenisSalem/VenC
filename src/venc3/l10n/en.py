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

class Messages:
    cannot_get_current_locale = "Cannot get current locale. Language set to english."
    blog_created = "Your blog has been created!"
    blogs_created = "Your blogs have been created!"
    chapter_has_a_wrong_index = "In entry #{0}, chapter index format is wrong: {1}."
    theme_installed = "Theme has been installed!"
    entry_written = "Entry has been saved!"
    file_not_found = "{0}: This file or directory does not exists."
    file_already_exists = "{0}: {1}: File or directory already exists."
    invalid_entry_filename = "{0}: Invalid entry filename."
    blog_name = "Blog name"
    blog_url = "The URL of your blog"
    missing_params = "{0}: Missing arguments."
    cannot_read_in = "{0}: Cannot read into {1}."
    nothing_to_do = "Nothing to do."
    unknown_command = "{0}: Unknown command."
    no_blog_configuration = "Blog's configuration file doesn't exists or you do not have right permissions."
    missing_mandatory_field_in_blog_conf = "Warning, the field \"{0}\" is missing in the blog's configuration file."
    username="Username: "
    ftp_host="FTP hostname"
    ftp_path="Absolute path of your blog on FTP server."
    clean_ftp_directory="Cleaning target FTP directory..."
    copy_to_ftp_directory="Copying your blog to target FTP directory..."
    possible_malformed_entry="Possible malformed entry {0}. {1} Abort."
    export_single_entries="Exporting local single entries..."
    export_archives="Exporting local entries grouped by dates..."
    export_main_thread="Exporting local main entries thread."
    export_categories="Exporting local entries grouped by categories..."
    export_chapters="Exporting local chapters..."
    wrong_args_number="Wrong arguments number : expected {0}, got {1}."
    unknown_pattern="The pattern '{0}'doesn't exists."
    unknown_contextual="Contextual variable {0} doesn't exists or is not available here."
    arg_blog_name="Blog name {0}"
    arg_entry_name="Entry name"
    arg_template_name="Template name"
    arg_input_filename="Filename"
    blog_folder_doesnt_exists="Destination folder doesn't exist. VenC doesn't care and will built a new one."
    theme_doesnt_exists = "{0}: Theme doesn't exists."
    unknown_text_editor = "{0}: unknown text editor."
    theme_name = "Theme name"
    unknown_language="Pygments: {0}: Unknown language."
    pre_process="Pre-processing theme and entries..."
    directory_not_copied="Directory not copied. Error: {0}"
    variable_error_in_filename="Variable error in main configuration file where paths and filenames are defined: {0} doesn't exists."
    wrong_pattern_argument="Argument '{0}' = '{1}' from pattern '{2}' is wrong: {3}"
    pattern_argument_must_be_integer="It must be a positive integer."
    wrong_permissions = "{0} : You don't have the right permissions on this file in {1}."
    unknown_markup_language = "{0}: Unsupported markup language."
    tex_math_error = "Malformed input string or unsupported markup from latex2mathml."
    missing_separator_in_entry = "Missing separator {0}."
    unknown_provider = "{0} is an unknown oembed provider."
    connectivity_issue = "A connectivity issue occured: {0}"
    ressource_unavailable = "{0}: Ressource is unavailable."
    response_is_not_json = "{0}: HTTP response is not JSON."
    server_port_is_invalid = "\"{0}\": is not a valid port number."
    serving_blog = "Server is now running on port : {0}."
    invalid_or_missing_metadata = "\"{0}\": Invalid value or missing metadata in entry \"{1}\"."
    malformed_patterns_missing_closing_symbols = "Malformed patterns in \"{0}\": One or more closing symbols are missing."
    malformed_patterns_missing_opening_symbols = "Malformed patterns in \"{0}\": One or more opening symbols are missing."
    loading_entries = "Loading entries..."
    chapter_already_exists = "Chapters \"{0}\" (id = {1}) and \"{2}\" (id = {3}) have the same index \"{4}\"."
    copy_assets_and_extra_files = "Copying extra files..."
    generating_jsonld_doc = "Generating JSON-LD document..."
    generating_jsonp_doc = "Generating JSONP document..."
    generating_jsonld_docs = "Generating JSON-LD documents..."
    task_done_in_n_seconds = "Task done in {0} seconds."
    nothing_to_serv = "Nothing to do. Try venc -xb before."
    theme_has_no_description = "This theme has no description."
    undefined_variable = "{0} is undefined in {1}."
    entry_has_no_metadata_like = "Entry has no metadata identified by \"{0}\"."
    blog_has_no_metadata_like = "Blog has no metadata identified by {0}."
    invalid_range = "Invalid range {0}:{1}."
    entry_metadata_is_not_a_list = "Metadata identified by \"{0}\" from entry {1} is not a list."
    blog_metadata_is_not_a_list = "Metadata identified by \"{0}\" blog configuration file is not a list."
    item_deleted_from_server = "Deleted from server: {0}"
    item_uploaded_to_server = "Uploaded to server: {0}"
    cannot_retrieve_entry_attribute_because_wrong_id = "Cannot retrieve entry attribute because the given id is unknown."
    id_must_be_an_integer = "Identifier must be an integer."
    there_is_no_chapter_with_index = "There is no chapter with index \"{0}\"."
    chapter_has_no_attribute_like = "Chapter has no attribute like \"{0}\"."
    start_thread = "Start CPU thread #{0}."
    link_entries = "Linking entries..."
    process_non_parallelizable = "Process non parallelizable patterns..."
    module_not_found = "Optional dependency \"{0}\"is not installed."
    in_ = "In {0}:"
    arg_must_be_an_integer = "Argument \"{0}\" must be an integer."
    syntax_error = "Syntax error : Pattern cannot start with \":.\"."
    current_entry_is_overriding_the_following = "Entry #{0} is overriding the following entries:\n{1}"
    argument_does_not_match_with_any_entries_subset="Argument does not match with any entries subset."
    pattern_recursion_error="Recursion error in pattern \"{0}\", function is calling itself too many times."
    the_following_is_overriden = "Setting identified by \"{0}\" is overriden by the following value \"{1}\" from {2}." 
    full_documentation_there = "Full documentation there: {0}."
    exception_place_holder = "{0}"
    categories_parse_error = "Categories are wrongly defined: {0} do not refer to a list."
    do_not_use_in_production = "For security reason do not use in production!"
    you_cannot_use_this_pattern_here = "You cannot use the pattern {0} in \"{1}\"."
    this_template_need_the_following_argument = "Template \"{0}\" need argument {1} to be defined."
    this_template_has_no_arguments = "this template has no arguments."
    # Will not be hooked by l10n_cleanup
    generating_rss = "Generating RSS feed..."
    generating_atom = "Generating Atom feed..."
