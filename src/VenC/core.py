#! /usr/bin/python
# -*- coding: utf-8 -*-

def PrintVersion(argv):
    print("VenC 1.0.0")

def GetMessages():
    import locale
    currentLocale = locale.getlocale()[0].split('_')[0]
    if currentLocale == 'fr':
        from VenC.languages import fr as language
    return language.Messages()

Messages = GetMessages()
