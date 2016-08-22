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

result = ("BBB" == patternProcessor.parse(".:FunctionA::AAA:."))
print(result,"\tSimple pattern recognition")

result = ("" == patternProcessor.parse(".:FunctionA::AAB:."))
print(result,"\tSimple pattern recognition with wrong parameters")

result = ("CCCDDD" == patternProcessor.parse(".:FunctionB:: .:FunctionA::AAA:. :: DDD :."))
print(result,"\tRecursive pattern recognition")

result = ("DDDEEE" == patternProcessor.parse(".:FunctionC:: EEE :: .:FunctionB::BBB:. :."))
print(result,"\tRecursive pattern recognition on second parameter")

result = ("DDDCCC" == patternProcessor.parse(".:FunctionC:: .:FunctionB::BBB:. :: .:FunctionB::BBB:. :."))
print(result,"\tRecursive pattern recognition on first and second parameter")

result = ("" == patternProcessor.parse(".:FunctionC:: .:FunctionB::BBB:. :: .:FunctionZ::BBB:. :."))
print(result,"\tRecursive pattern recognition on first and second parameter, with wrong second parameter")
