#! /usr/bin/python3

from venc2.helpers import get_formatted_message 

def run_tests(tests_name, tests):
    print(tests_name)
    for test in tests:
        test_name, args, o, fun = test
        try:
            assert o == fun(args, test_name), test_name
            print(get_formatted_message("\t"+test_name+" Pass", prompt=""))
   
        except AssertionError as e:
            print(get_formatted_message("\t"+test_name+" "+str(e), color="RED", prompt=""))

        except Exception as e:
            try:
                err, args = o
                assert type(e) == err
                for arg in args:
                    attr, value = arg
                    assert getattr(e, attr) == value, attr+" != "+str(value)
                print(get_formatted_message("\t"+test_name+" Pass", prompt=""))

            except AssertionError as e:
                print(get_formatted_message("\t"+test_name+" "+str(e), color="RED", prompt=""))

    print("Done.")
