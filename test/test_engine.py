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
