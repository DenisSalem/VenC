#! /usr/bin/env python3

#    Copyright 2016, 2024 Denis Salem
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
import os

from venc3.helpers import quirk_encoding
from venc3.patterns.processor import PatternTree

class Entry:  
    def __init__(self, filename, paths):
        date_format = paths["archives_directory_name"]
        self.previous_entry = None
        self.next_entry = None
        self.title = ''

        # Loading
        raw_data = open(os.getcwd()+"/entries/"+filename,'r').read()
        entry_parted = raw_data.split("---VENC-BEGIN-PREVIEW---\n")
        if len(entry_parted) == 2:
            entry_parted = [entry_parted[0]] + entry_parted[1].split("---VENC-END-PREVIEW---\n")
            if len(entry_parted) == 3:
                import yaml
                try:
                    metadata = yaml.load(entry_parted[0], Loader=yaml.FullLoader)

                except Exception as e:
                    from venc3.exceptions import VenCException
                    raise VenCException(("possible_malformed_entry", filename, ''), context=filename, extra=str(e))
                    
                if "markup_language" in metadata.keys():
                    markup_language = metadata["markup_language"]
                else:
                    from venc3.datastore.configuration import get_blog_configuration
                    markup_language = get_blog_configuration()["markup_language"]
                    
                # TODO : OPTIMISATION IMPORT theme and pre process only if required
                self.preview = PatternTree(entry_parted[1], filename+":preview", False if markup_language == "none" else True)
                self.content = PatternTree(entry_parted[2], filename+":content", False if markup_language == "none" else True)

            else:
                from venc3.l10n import messages; 
                cause = messages.missing_separator_in_entry.format("---VENC-END-PREVIEW---")
                from venc3.exceptions import VenCException
                raise VenCException(("possible_malformed_entry", filename, cause), context=filename)
        else:
            from venc3.l10n import messages; 
            cause = messages.missing_separator_in_entry.format("---VENC-BEGIN-PREVIEW---")
            from venc3.exceptions import VenCException
            raise VenCException(("possible_malformed_entry", filename, cause), context=filename)
        
        # Setting up optional metadata
        for key in metadata.keys():
            if not key in ("authors", "categories", "title"):
                if metadata[key] != None:
                    setattr(self, key, metadata[key])
                        
                else:
                    from venc3.prompt import notify
                    notify(("invalid_or_missing_metadata", key, filename), color="YELLOW")
                    setattr(self, key, '')

        # Fix missing or incorrect metadata
        for key in ("authors", "categories", "title"):
            if key not in metadata.keys() or metadata[key] == None:
                metadata[key] = '' if key == "title" else []

        try:
            self.chapter_level = str(len(str(metadata["chapter"]).split('.')))
            
        except:
            pass
    
        self.raw_metadata = metadata
        self.filename = filename
        self.id = int(filename.split('__')[0])
        
        raw_date = filename.split('__')[1].split('-')
        self.date = datetime.datetime(
            year=int(raw_date[2]),
            month=int(raw_date[0]),
            day=int(raw_date[1]),
            hour=int(raw_date[3]),
            minute=int(raw_date[4])
        )
        self.formatted_date = self.date.strftime(date_format)

        self.title = metadata["title"].replace(".:GetEntryTitle:.",'') # sanitize

        if type(metadata["authors"]) != list:
            from venc3.exceptions import VenCException
            raise VenCException(("entry_metadata_is_not_a_list", "authors", self.id), context=filename)
            
        self.authors = tuple(metadata["authors"])
            
        params = {
            "entry_id": self.id,
            "entry_title": self.title
        }

        sf = quirk_encoding(paths["entries_sub_folders"].format(**params))
        self.sub_folder = (sf+'/' if sf[-1] != '/' else sf) if len(sf) else ''
        self.path = "\x1a/"+quirk_encoding(self.sub_folder+paths["entry_file_name"].format(**params)).replace('//','/')
        
        if type(metadata["categories"]) != list:
            from venc3.exceptions import VenCException
            raise VenCException(("entry_metadata_is_not_a_list", "categories", self.id), context=filename)

        self.raw_categories = metadata["categories"]
        
        self.html_categories_tree = {}
        self.html_authors = {}
        self.html_categories_leaves = {}
        self.html_for_metadata = {}
        
# Iterate through entries folder
def yield_entries_content():
    try:
        for filename in os.listdir(os.getcwd()+"/entries"):
            exploded_filename = filename.split("__")
            try:
                date = exploded_filename[1].split('-')
                entry_id = int(exploded_filename[0])
                datetime.datetime(
                    year=int(date[2]),
                    month=int(date[0]),
                    day=int(date[1]),
                    hour=int(date[3]),
                    minute=int(date[4])
                ) 
                if entry_id >= 0:
                    yield filename

                else:
                    raise ValueError

            except ValueError:
                from venc3.prompt import notify
                notify(("invalid_entry_filename", filename), "YELLOW")

            except IndexError:
                from venc3.prompt import notify
                notify(("invalid_entry_filename", filename), "YELLOW")
    
    except FileNotFoundError as e:
        from venc3.exceptions import VenCException
        raise VenCException(("file_not_found", str(e)))

def get_latest_entryID():
    entries_list = sorted(yield_entries_content(), key = lambda entry : int(entry.split("__")[0]))
    if len(entries_list) != 0:
        return int(entries_list[-1].split("__")[0])
    else:
        return 0
