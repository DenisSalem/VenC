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

from venc3.prompt import get_formatted_message 

def run_tests(tests_name, tests):
    print(tests_name)
    for test in tests:
        test_name, args, o, fun = test
        try:
            assert o == fun(args, test_name), test_name
            print(get_formatted_message("\t"+test_name+" Pass", prompt=""))
   
        except AssertionError as e:

            if str(e) == test_name:
                print(get_formatted_message("\t"+test_name+" Failed", color="RED", prompt=""))

            else:
                print(get_formatted_message("\t"+test_name+" "+str(e), color="RED", prompt=""))

        except Exception as venc_defined_exception:
            try:
                err, args = o
                assert type(venc_defined_exception) == err
            
            except AssertionError:
                print(get_formatted_message("\t"+test_name+" "+str(err)+" != "+str(type(venc_defined_exception)), color="RED", prompt=""))
                continue
            
            params_okay = True
            for arg in args:
                try:
                    attr, value = arg
                    assert getattr(venc_defined_exception, attr) == value, attr+" != "+str(value)

                except AssertionError as e:
                    print(get_formatted_message("\t"+test_name+" "+str(e), color="RED", prompt=""))
                    params_okay = False

            if params_okay:
                print(get_formatted_message("\t"+test_name+" Pass", prompt=""))

    print("Done.")
