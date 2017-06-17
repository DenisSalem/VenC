#! /usr/bin/python3

import VenC.l10n; 

MsgFormat = {
    "END" : '\033[0m',
    "GREEN" : '\033[92m',
    "RED" : '\033[91m',
    "YELLOW" : '\033[33m'
}

ThemesDescriptor = {
    "dummy": {"columns":1,"_themeDescription_": VenC.l10n.Messages.themeDescriptionDummy},
    "gentle": {"columns":1,"_themeDescription_": VenC.l10n.Messages.themeDescriptionGentle},
    "tessellation": {"columns":3,"_themeDescription_": VenC.l10n.Messages.themeDescriptionTessellation},
}


