#! /usr/bin/python3

print("Testing Patterns processing...")
from venc2.patterns.processor import ProcessedString    # The object holding the string and its states
from venc2.patterns.processor import Processor          # The actual string processor, holding binded methods.

testname_input_output = [
    (
        "Simple pattern detection", 
        "moo .:add::1::1:. foo",
        "moo 2 foo",
        False
    ),
    (
        "Match two patterns",
        "moo .:add::1::1:. foo .:mul::2::2:. bar",
        "moo 2 foo 4 bar",
        False
    ),
    (
        "Recursive Patterns",
        "moo .:greater:: .:add::1::1:. :: .:mul::2::2:. :. bar",
        "moo 4 bar",
        False
    ),
    (
        "Recursive Patterns plus extra trailing pattern",
        "moo .:mul::3::3:. .:greater:: .:add::1::1:. :: .:mul::2::2:. :. foo .:greater::1::2:. bar",
        "moo 9 4 foo 2 bar",
        False
    ),
    (
        "Recursive Patterns (same call)",
        "moo .:greater:: .:greater::1::2:. :: 0 :. bar",
        "moo 2 bar",
        False
    ),
    (
        "Test against blacklisted pattern",
        "moo .:blacklisted:. foo .:greater::3::5:. bar",
        "moo .:blacklisted:. foo 5 bar",
        False
    ),
    (
        "Simple Escaping surrounded by simple patterns. Escape/EndEscape left intact.",
        "moo .:add::1::1:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:mul::2::2:. bar",
        "moo 2 foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo 4 bar",
        False
    ),
    (
        "Simple Escaping surrounded by simple patterns.",
        "moo .:add::1::1:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:mul::2::2:. bar",
        "moo 2 foo  .:mul::1::1:.  boo 4 bar",
        True
    ),
    (
        "Escaping surrounded by Escape patterns.",
        "moo .:Escape:: .:NoRage:. ::EndScape:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:Escape:: .:NoPattern:. What could possibly go wrong here? ::EndEscape:. bar",
        "moo 2 foo  .:mul::1::1:.  boo 4 bar",
        True
    )
]

def add(argv):
    a, b = tuple(argv)
    return str( int(a) + int(b) )

def mul(argv):
    a, b = tuple(argv)
    return str( int(a) * int(b) )

def greater(argv):
    a, b = tuple(argv)
    return a if float(a) > float(b) else b

processor = Processor()
processor.set_function("add", add)
processor.set_function("mul", mul)
processor.set_function("greater", greater)
processor.blacklist.append("blacklisted")

for test in testname_input_output:
    test_name, i, o, process_escapes = test
    ps = ProcessedString(i, test_name, process_escapes)
    processor.process(ps)
    assert o == ps.string, test_name
    print("\t", test_name, "pass")

print("Done.")
