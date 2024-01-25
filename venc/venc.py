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

import argparse

from .commands.print import USAGE
from .l10n import locale_err
from .prompt import notify


def main():
    if locale_err:
        notify(("cannot_get_current_locale",), color="YELLOW")

    parser = argparse.ArgumentParser(prog="VenC", usage="\n" + USAGE, add_help=False)
    parser.add_argument("-h", "--help", help="", action="store_const", const=".print")
    parser.add_argument(
        "-v", "--version", help="", action="store_const", const=".print"
    )
    parser.add_argument(
        "-pt", "--print-themes", help="", action="store_const", const=".print"
    )
    parser.add_argument(
        "-ta", "--template-arguments", help="", action="store_const", const=".print"
    )
    parser.add_argument(
        "-nb", "--new-blog", help="", action="store_const", const=".new"
    )
    parser.add_argument(
        "-ne", "--new-entry", help="", action="store_const", const=".new"
    )
    parser.add_argument(
        "-xb", "--export-blog", help="", action="store_const", const=".export"
    )
    parser.add_argument(
        "-ex", "--edit-and-export", help="", action="store_const", const=".export"
    )
    parser.add_argument(
        "-xftp", "--export-via-ftp", help="", action="store_const", const=".export"
    )
    parser.add_argument(
        "-rc", "--remote-copy", help="", action="store_const", const=".remote"
    )
    parser.add_argument(
        "-it", "--install-theme", help="", action="store_const", const=".install"
    )
    parser.add_argument("-s", "--serv", help="", action="store_const", const=".serv")
    parser.add_argument("params", nargs="*")
    args = parser.parse_args()

    commands = [
        item for item in dir(args) if (not item.startswith("_")) and item != "params"
    ]

    for command in commands:
        module = getattr(args, command)
        if module is not None:
            import importlib

            module = importlib.import_module(module, "venc.commands")
            function = getattr(module, command)
            function(args.params)
            exit()


if __name__ == "__main__":
    main()
