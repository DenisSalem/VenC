#! /usr/bin/env python3

from venc3.patterns.patterns_map import PatternsMap
import inspect

print(".:Table::")
from venc3.threads import Thread
for contextual in PatternsMap.CONTEXTUALS.keys():
    symbol = PatternsMap.CONTEXTUALS[contextual]
    attr = getattr(Thread, symbol)
    args = ', '.join([name for name in inspect.signature(attr).parameters][2:])
    print(contextual+"::"+args)
print(":.")
