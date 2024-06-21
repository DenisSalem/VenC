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

from venc3.l10n import messages;

USAGE = \
    "\033[92m"+messages.full_documentation_there.format("https://venc.software")+"\033[0m\n" +\
    "-v\t--version\n" +\
    "-nb\t--new-blog <"+messages.arg_blog_name.format("1")+"> ["+messages.arg_blog_name.format("2")+"] [ ... ]\n" +\
    "-ne\t--new-entry <"+messages.arg_entry_name+"> ["+messages.arg_template_name+"]\n" +\
    "-xb\t--export-blog ["+messages.theme_name+"]\n" +\
    "-ex\t--edit-and-xport <"+messages.arg_input_filename+"> ["+messages.theme_name+"]\n" +\
    "-s\t--serv\n" +\
    "-xftp\t--export-via-ftp\n" +\
    "-rc\t--remote-copy\n" +\
    "-h\t--help\n" +\
    "-it\t--install-theme <"+messages.theme_name+">\n" \
    "-pt\t--print-themes\n" \
    "-ta\t--template-arguments <"+messages.arg_template_name+">"\
    
# Will be removed and replaced by argparse
def help(params):
    print(USAGE)

def template_arguments(params):
    from venc3.helpers import get_template
    from venc3.exceptions import VenCException, MissingTemplateArguments

    try:
        template_name = params[0]
        
    except:
        VenCException(("wrong_args_number","= 1",len(params))).die()   
    
    template_arguments = {}
    while '∞':
        try:
            template = get_template(template_name, '', template_arguments)
            if len(template_arguments.keys()) == 0:
                from venc3.prompt import notify
                notify(("this_template_has_no_arguments",))
                
            else:
                for arg in template_arguments.keys():
                    template = template.replace(arg, '\033[92m{'+template_arguments[arg]+'}\033[0m')
                    
                print(template)
    
            break
            
        except MissingTemplateArguments as e:
            template_arguments[str(e.key_error)[1:-1]] = str(e.key_error)[1:-1]
          
        except VenCException as e:
            e.die()

def print_path(params):
    from venc3 import package_data_path
    print(package_data_path)
    
def print_themes(params):
    import os
    import yaml

    from venc3 import package_data_path
    from venc3.datastore.configuration import get_blog_configuration
    blog_configuration = get_blog_configuration()
    paths = [package_data_path+"/themes/"] + (blog_configuration["paths"]["themes_locations"] if blog_configuration != None else [])
    for path in paths:
        try:
            themes_folder = os.listdir(path)
          
        except Exception as e:
            continue
            
        for theme in themes_folder:
            if (os.path.isdir(path+'/'+theme) and "config.yaml" in os.listdir(path+'/'+theme)) and not os.path.isdir(path+'/'+theme+"/config.yaml"):
                config = yaml.load(
                    open(path+'/'+theme+"/config.yaml",'r').read(),
                    Loader=yaml.FullLoader
                )
                try:
                    description = config["info"]["description"]
                                            
                except KeyError:
                    from venc3.l10n import messages
                    description = messages.theme_has_no_description
                    
                except TypeError:
                    from venc3.l10n import messages
                    description = messages.theme_has_no_description
    
            else:
                from venc3.l10n import messages
                description = messages.theme_has_no_description
    
            if os.path.isdir(path+'/'+theme) and "assets" in os.listdir(path+'/'+theme) and "chunks" in os.listdir(path+'/'+theme):
                from venc3.prompt import msg_format
                print("- "+msg_format["GREEN"]+theme+msg_format["END"]+":", description)

def version(params):
    from venc3 import venc_version
    print("VenC", venc_version)
    import platform
    print("Python", platform.python_version())
    deps = [
        "asciidoc3",
        "docutils",
        "latex2mathml",
        "mistletoe",
        "pygments",
    ]
    
    try:
        import pkg_resources
    
    except ModuleNotFoundError:
        print("pkg_resources",messages.not_installed)
        return

    for dep in deps:
        try:
            print("\t", dep, pkg_resources.get_distribution(dep).version)
        
        except pkg_resources.DistributionNotFound:
            print("\t", dep, messages.not_installed)
    
