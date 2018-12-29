#! /usr/bin/python3

from venc2.patterns.processor import ProcessedString    # The object holding the string and its states
from venc2.patterns.processor import Processor          # The actual string processor, holding binded methods.
from venc2.patterns.exceptions import MalformedPatterns

from test_engine import run_tests

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

def test_pattern_processor(args, test_name):
    input_value, process_escapes = args
    ps = ProcessedString(input_value, test_name, process_escapes)
    processor.process(ps)
    return ps.string

tests = [
    (
        "Simple pattern detection.", 
        ("moo .:add::1::1:. foo", False),
        "moo 2 foo",
        test_pattern_processor
    ),
    (
        "Match two patterns.",
        ("moo .:add::1::1:. foo .:mul::2::2:. bar", False),
        "moo 2 foo 4 bar",
        test_pattern_processor
    ),
    (
        "Recursive Patterns.",
        ("moo .:greater:: .:add::1::1:. :: .:mul::2::2:. :. bar", False),
        "moo 4 bar",
        test_pattern_processor
    ),
    (
        "Recursive Patterns plus extra trailing pattern.",
        ("moo .:mul::3::3:. .:greater:: .:add::1::1:. :: .:mul::2::2:. :. foo .:greater::1::2:. bar", False),
        "moo 9 4 foo 2 bar",
        test_pattern_processor
    ),
    (
        "Recursive Patterns (same call).",
        ("moo .:greater:: .:greater::1::2:. :: 0 :. bar", False),
        "moo 2 bar",
        test_pattern_processor
    ),
    (
        "Test against blacklisted pattern.",
        ("moo .:blacklisted:. foo .:greater::3::5:. bar", False),
        "moo .:blacklisted:. foo 5 bar",
        test_pattern_processor
    ),
    (
        "Simple Escaping surrounded by simple patterns. Escape/EndEscape left intact.",
        ("moo .:add::1::1:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:mul::2::2:. bar", False),
        "moo 2 foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo 4 bar",
        test_pattern_processor
    ),
    (
        "Simple Escaping surrounded by simple patterns.",
        ("moo .:add::1::1:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:mul::2::2:. bar", True),
        "moo 2 foo  .:mul::1::1:.  boo 4 bar",
        test_pattern_processor
    ),
    (
        "Escaping surrounded by Escape patterns.",
        ("moo .:Escape:: .:NoRage:. ::EndEscape:. foo .:Escape:: .:mul::1::1:. ::EndEscape:. boo .:Escape:: .:NoPattern:. What could possibly go wrong here? ::EndEscape:. bar", True),
        "moo  .:NoRage:.  foo  .:mul::1::1:.  boo  .:NoPattern:. What could possibly go wrong here?  bar",
        test_pattern_processor
    ),
    (
        "Raise MalformedPatterns: Missing closing escape symbols.",
        ("moo .:Escape:: ::endescape:. bar", True),
        (MalformedPatterns,[("too_many_opening_symbols", True), ("escape", True)]),
        test_pattern_processor
    ),
    (
        "Raise MalformedPatterns: Missing opening escape symbols.",
        ("moo .:escape:: ::EndEscape:. bar", True),
        (MalformedPatterns,[("too_many_opening_symbols", False), ("escape", True)]),
        test_pattern_processor
    ),
    (
        "Raise MalformedPatterns: Missing opening symbols.",
        ("moo .:mul::2::3:. foo add::3::3:.", False),
        (MalformedPatterns,[("too_many_opening_symbols", False), ("escape", False)]),
        test_pattern_processor
    ),
    (
        "Raise MalformedPatterns: Missing closing symbols.",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar .:", False),
        (MalformedPatterns,[("too_many_opening_symbols", True), ("escape", False)]),
        test_pattern_processor
    ),
    (
        "Escape missing opening symbols.",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar .:Escape:: mul::3::3:. ::EndEscape:. boo", True),
        "moo 6 foo 6 bar  mul::3::3:.  boo",
        test_pattern_processor
    ),
    (
        "Escape missing closing symbols.",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar .:Escape:: .:mul::3::3 ::EndEscape:. boo", True),
        "moo 6 foo 6 bar  .:mul::3::3  boo",
        test_pattern_processor
    ),
]

run_tests("Testing patterns processor...", tests)
