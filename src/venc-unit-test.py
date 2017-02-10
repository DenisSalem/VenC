#! /usr/bin/python
# -*- coding: utf-8 -*-

import VenC.pattern

print("""#############################
# Testing Pattern Processor #
#############################\n""")

def functionA(argv):
    if argv[0].strip() == "AAA":
        return "BBB"
    else:
        return ""


def functionB(argv):
    if argv[0].strip() == "BBB":
        try:
            return "CCC"+argv[1].strip()
        except:
            return "CCC"
    else:
        return ""

def functionC(argv):
    if argv[1].strip() == "CCC":
        return "DDD"+argv[0].strip()
    else:
        return ""

patternProcessor = VenC.pattern.processor(".:",":.","::")

patternProcessor.SetFunction("FunctionA", functionA)
patternProcessor.SetFunction("FunctionB", functionB)
patternProcessor.SetFunction("FunctionC", functionC)

patternProcessor.preProcess("test1", ".:FunctionA::AAA:.")
patternProcessor.preProcess("test2", ".:FunctionA::AAB:.")
patternProcessor.preProcess("test3", ".:FunctionB:: .:FunctionA::AAA:. :: DDD :.")
patternProcessor.preProcess("test4", ".:FunctionC:: EEE :: .:FunctionB::BBB:. :.")
patternProcessor.preProcess("test5", ".:FunctionC:: .:FunctionB::BBB:. :: .:FunctionB::BBB:. :.")
patternProcessor.preProcess("test6", ".:FunctionC:: .:FunctionB::BBB:. :: .:FunctionZ::BBB:. :.")

result = ("BBB" == patternProcessor.parse("test1"))
print(result,"\tSimple pattern recognition")

result = ("" == patternProcessor.parse("test2"))
print(result,"\tSimple pattern recognition with wrong parameters")

result = ("CCCDDD" == patternProcessor.parse("test3"))
print(result,"\tRecursive pattern recognition")

result = ("DDDEEE" == patternProcessor.parse("test4"))
print(result,"\tRecursive pattern recognition on second parameter")

result = ("DDDCCC" == patternProcessor.parse("test5"))
print(result,"\tRecursive pattern recognition on first and second parameter")

result = ("" == patternProcessor.parse("test6"))
print(result,"\tRecursive pattern recognition on first and second parameter, with wrong second pattern")
