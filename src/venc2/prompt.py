#! /usr/bin/env python3

#    Copyright 2016, 2019 Denis Salem
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

msg_format = {
    "END" : '\033[0m',
    "GREEN" : '\033[92m',
    "RED" : '\033[91m',
    "YELLOW" : '\033[33m'
}

# Some data printed out may exceed few lines so
# it's nicer to highlight specific part of the output
def highlight_value(text, value, color="RED"):
    return text.replace(
        value,
        msg_format[color]+value+msg_format["END"]
    )

# Terminate nicely with notification
def die(msg, color="RED", extra=""):
    notify(msg, color)
    if len(extra):
        print(extra)
    exit()

# Being verborse is nice, with colours it's better
def notify(msg, color="GREEN"):
    print(get_formatted_message(msg, color), flush=True)

# Take care of setting up colours in printed out message
def get_formatted_message(msg, color="GREEN", prompt="VenC: "):
    return msg_format[color]+"\033[1m"+prompt+"\033[0m"+msg_format[color]+msg+msg_format["END"]


