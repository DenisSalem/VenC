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
from venc2.prompt import notify

try:
    current_locale = locale.getlocale()[0]
    if current_locale != None:
        current_locale = current_locale.split('_')[0]
        
    else:
      notify("Your system locale seems to be undefined, VenC fallback to default.", color="YELLOW")
      current_locale = 'en'
      
    locale_err = False

except locale.Error as e:
    notify(e.args, color="YELLOW")
    current_locale = 'en'
    locale_err = True

if current_locale == 'fr':
    from venc2.l10n import fr as language

else:
    from venc2.l10n import en as language

messages = language.Messages()
