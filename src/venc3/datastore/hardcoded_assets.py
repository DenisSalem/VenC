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

default_error_page = \
"""
<!DOCTYPE html>
<html>
    <head>
        <style type='text/css'>
            body {background-color: #404040; color: white; font-family:sans;font-weight:lighter;text-align:center;}
            span {background-color: white; color: #404040; border-radius: 3px;margin:2px;}
            div {position:fixed;display:block;width:223px;height:95px;top:50%%;left:50%%;margin-left:-111px;margin-top:-47px;}
        </style>
    </head>
    <body>
        <div>
            <p>V<span>en</span>C</p>
            %(code)d :  %(message)s. %(explain)s
        </div>
    </body>
</html>
"""
