#! /usr/bin/env python3

#   Copyright 2016, 2019 Denis Salem
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

import locale
import os
import yaml

override_locale = None

try:
    blog_configuration = yaml.load(
        open(
            os.getcwd()+"/blog_configuration.yaml",
            'r'
        ).read(),
        Loader=yaml.FullLoader
    )
    
    override_locale = blog_configuration["blog_locale"]
        
except Exception as e:
    # if blog_locale is not defined and VenC will fall back to default
    # if blog_clonfiguration.yaml is not available and exception will be caught later.
    pass
    
try:        
    if override_locale != None:
        current_locale = '.'.join(override_locale)
        
    else:
        current_locale = '.'.join(locale.getlocale())
        
    if current_locale == None:
        from venc3.prompt import get_formatted_message
        print(get_formatted_message("Your system locale seems to be undefined, VenC fallback to default.", "YELLOW"), flush=True)
        current_locale = 'en'
    
    locale.setlocale(locale.LC_ALL, current_locale)
    locale_err = False
    current_locale = current_locale.split('_')[0]
    
except locale.Error as e:
    from venc3.prompt import get_formatted_message
    print(get_formatted_message(str(e.args)+" "+str(current_locale), "YELLOW"), flush=True)
    current_locale = 'en'
    locale_err = True

if current_locale == 'fr':
    from venc3.l10n import fr as language

else:
    from venc3.l10n import en as language

messages = language.Messages()
