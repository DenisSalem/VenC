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

import os 
import sys

# Sometimes format fail with {something} not found in given dict.
class SafeFormatDict(dict):
    def __missing__(self, key):
        return '{'+key+'}'

def export_extra_data(origin, destination=""):
    import os
    import shutil

    try:
        folder = os.listdir(origin)
        for item in folder:
            if os.path.isdir(origin+"/"+item):
                try:
                    os.mkdir(os.getcwd()+"/blog/"+destination+item)
                    export_extra_data(origin+'/'+item, item+'/')
                except Exception as e:
                    #TODO : VenCException pleaaaaaase
                    raise e
            else:
                shutil.copy(origin+"/"+item, os.getcwd()+"/blog/"+destination+item)
    except:
        raise

def get_base_dir():
    python_prefix = sys.prefix
    virtualenv_prefix = sys.real_prefix if hasattr(sys, 'real_prefix') else sys.prefix
    return virtualenv_prefix if python_prefix != virtualenv_prefix else os.path.expanduser("~")+"/.local"

def quirk_encoding(string):
    import unidecode
    return unidecode.unidecode(
        string.replace(
            '\'',
            '-'
        ).replace(
            ' ',
            '-'
        ).replace(
            '%',
            '-'
        ).replace(
            ':',
            '-'
        )
    )

def rm_tree_error_handler(function, path, excinfo):
    from venc3.prompt import notify
    
    if path == "blog" and excinfo[0] == FileNotFoundError:
        notify(("blog_folder_doesnt_exists",),"YELLOW")
        return

    notify(("exception_place_holder", str(function)),"RED")
    notify(("exception_place_holder", str(path)),"RED")
    notify(("exception_place_holder", str(excinfo[0])),"RED")
    exit()
    
def get_template(template_name, entry_name='', template_args={}):
    import os

    from venc3.helpers import get_template

    found_template = False
    templates_paths = [
        os.getcwd()+'/templates/'+template_name,
        get_base_dir()+"/share/VenC/themes_templates/"+template_name
    ]
    
    for template_path in templates_paths:
        try:
            template = open(template_path, 'r').read().format(**template_args)
            parted = template.split("---VENC-BEGIN-PREVIEW---")
            if len(parted) != 2:
                from venc3.l10n import messages; 
                cause = messages.missing_separator_in_entry.format("---VENC-BEGIN-PREVIEW---")
                from venc3.exceptions import VenCException
                raise VenCException(("possible_malformed_entry", template_path, cause), context=template_path)
            
            import yaml
            try:
                parted[0] = yaml.dump(yaml.load(parted[0], Loader=yaml.FullLoader))
                
            except yaml.scanner.ScannerError as e:
                from venc3.exceptions import VenCException
                raise VenCException(("possible_malformed_entry",template_path, ''), context=template_path, extra=str(e))
                
            return "---VENC-BEGIN-PREVIEW---".join(parted)
            
        except KeyError as e:
            from venc3.exceptions import MissingTemplateArguments
            raise MissingTemplateArguments(template_name, e)
            
        except FileNotFoundError:
            pass
            
        except PermissionError:
            from venc3.exceptions import VenCException
            raise VenCException(("wrong_permissions", template_path))
    
    from venc3.exceptions import VenCException
    from venc3.l10n import messages
    msg = "\n"+ messages.file_not_found.format(templates_paths[0])+"\n"+ messages.file_not_found.format(templates_paths[1])
    raise VenCException(("exception_place_holder", msg))
  
