#! /usr/bin/python3

import locale
currentLocale = locale.getlocale()[0].split('_')[0]
if currentLocale == 'fr':
    from VenC.languages import fr as language
else:
    from VenC.languages import en as language

Messages = language.Messages()
