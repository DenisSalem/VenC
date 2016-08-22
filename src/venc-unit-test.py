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
        return "CCC"
    else:
        return ""

patternProcessor = VenC.pattern.processor(".:",":.","::")

patternProcessor.SetFunction("FunctionA", functionA)
patternProcessor.SetFunction("FunctionB", functionB)

result = ("BBB" == patternProcessor.parse(".:FunctionA::AAA:."))
print(result,"\tSimple pattern recognition")

result = ("" == patternProcessor.parse(".:FunctionA::AAB:."))
print(result,"\tSimple pattern recognition with wrong parameters")

result = ("CCC" == patternProcessor.parse(".:FunctionB:: .:FunctionA::AAA:. :."))
print(result,"\tRecursive pattern recognition")
