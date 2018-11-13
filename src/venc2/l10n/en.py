#! /usr/bin/python3

#    Copyright 2016, 2018 Denis Salem
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
    theme_installed = "Theme has been installed!"
    entry_written = "Entry has been saved!"
    file_not_found = "{0}: This file or directory does not exists."
    file_already_exists = "{0}: {1}: File or directory already exists."
    invalid_entry_filename = "{0}: Invalid entry filename."
    blog_name = "Blog name"
    your_name = "Your name"
    blog_description = "Short description of your blog"
    blog_keywords = "Some keywords about your blog"
    about_you = "About you"
    license = "The license applied to your blog"
    blog_url = "The URL of your blog"
    blog_language = "The language of your blog"
    your_email = "Your e-mail"
    missing_params = "{0}: Missing arguments."
    cannot_read_in = "{0}: Cannot read into {1}."
    nothing_to_do = "Nothing to do."
    unknown_command = "{0}: Unknown command."
    no_blog_configuration = "Blog's configuration file doesn't exists or you do not have right permissions."
    missing_mandatory_field_in_blog_conf = "Warning, the field \"{0}\" is missing in the blog's configuration file."
    username="Username: "
    user_password="User password: "
    ftp_host="FTP hostname"
    ftp_path="Absolute path of your blog on FTP server."
    clean_ftp_directory="Cleaning target FTP directory..."
    copy_to_ftp_directory="Copying your blog to target FTP directory..."
    possible_malformed_entry="Possible malformed entry {0}. {1} Abort."
    possible_malformed_blog_configuration="Possible malformed blog configuration. Abort."
    blog_recompilation="Recompilation of your blog locally..."
    export_single_entries="Exporting local single entries..."
    export_archives="Exporting local entries sorted by dates..."
    export_main_thread="Exporting local main entries thread."
    export_main_thread_rss="Exporting local main RSS feed entries."
    export_categories="Exporting local entries sorted by categories..."
    export_categoriesRss="Exporting local entries RSS feed thread from category '{0}'."
    missing_mandatory_field_in_entry="Field '{0}' in entry number {1} is missing."
    for_unknown_value="For: Value {0} isn't defined."
    recursive_for_unknown_value="RecursiveFor: Value {0} isn't defined."
    not_enough_args="Missing parameters."
    unknown_pattern="The pattern '{0}'doesn't exists."
    unknown_contextual="Contextual variable {0} doesn't exists."
    in_ressource="In ressource '{0}'."
    something_goes_wrong_return_empty_string="An error occurs. Replacement with an empty string."
    arg_blog_name="Blog name {0}"
    arg_entry_name="Entry name"
    arg_template_name="Template name"
    arg_input_filename="Filename"
    blog_folder_doesnt_exists="Destination folder doesn't exist. VenC doesn't care and will built a new one."
    theme_description_dummy = "The empty one. Aim to built your own from scratch."
    theme_description_gentle = "Theme with one column. It's light, clear and elegant. Fit nicely for a blog."
    theme_description_tessellation = "Theme with three columns. It's light, clear, and elegant. Fit nicely for a galery."
    theme_doesnt_exists = "{0}: Theme doesn't exists."
    unknown_text_editor = "{0}: unknown text editor."
    theme_name = "Theme name"
    entry_is_empty = "{0}: The content of the entry is empty."
    missing_entry_content_inclusion = "Invalid theme. Missing entry content inclusion in entry.html and/or rssEntry.html"
    unknown_language="Pygments: {0}: Unknown language."
    pre_process="Pre-processing theme and entries..."
    directory_not_copied="Directory not copied. Error: %s"
    variable_error_in_filename="Variable error in main configuration file where paths and filenames are defined: {0} doesn't exists."
    wrong_pattern_argument="Argument '{0}' = '{1}' from pattern '{2}' is wrong."
    pattern_argument_must_be_integer="It must be a positive integer."
    wrong_permissions = "{0} : You don't have the right permissions on this file in {1}."
    unknown_markup_language = "{0}: Unsupported markup language."
    tex_math_error = "Malformed input string or unsupported markup from latex2mathml."
    missing_separator_in_entry = "Missing separator {0}."
    pattern_is_forbidden_here = "The pattern '{0}' is forbidden here."
    unknown_provider = "{0} is an unknown oembed provider."
