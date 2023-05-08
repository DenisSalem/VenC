#! /usr/bin/env python3

import importlib
import inspect

from venc3.patterns.datastore import DatastorePatterns
from venc3.patterns.patterns_map import PatternsMap
from venc3.threads import Thread

patterns = []

source = {
    "4.3" :  (PatternsMap.CONTEXTUALS, Thread),
    "4.4.1" : (PatternsMap.NON_CONTEXTUALS["entries"], DatastorePatterns),
    "4.4.2" : (PatternsMap.NON_CONTEXTUALS["blog"], DatastorePatterns),
    "4.4.3" : (PatternsMap.NON_CONTEXTUALS["extra"], )
}

for index in source.keys():
    for pattern in source[index][0]:
        symbol = source[index][0][pattern]
        if index == "4.4.3":
            pattern_location = symbol.split('.')
            function = pattern_location[-1]
            module = '.'+pattern_location[-2]
            package = '.'.join(pattern_location[:-2])
            attr = getattr(importlib.import_module(module, package), function)
        else:
            attr = getattr(source[index][1], symbol)
        args = ', '.join([(name if name != "argv" else "arg 1</li><li>arg 2</li><li>arg n...") for name in inspect.signature(attr).parameters if not name in ["self","pattern","raise_error", "raise_exception"]])
        value = "<a href=\".:GetChapterAttributeByIndex::path::"+index+":.#"+pattern.lower()+"\">"+pattern+"</a>"
        patterns.append((
            pattern,
            value,
            args
        ))

print(".:Table::")
print("Motifs::Arguments::Variables::NewLine::")
items = sorted(patterns, key = lambda x: x[0])
for i in range(0, len(items)):
    pattern = items[i]
    print(pattern[1]+"::<ul>"+''.join(["<li>"+v+"</li>" for v in pattern[2].split(",") if len(v)])+"</ul>:: "+("::NewLine::" if i < len(items)-1 else ""))
print(":.")
