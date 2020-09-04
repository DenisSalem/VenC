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

from venc2.patterns.processor import ProcessedString    # The object holding the string and its states.
from venc2.patterns.processor import Processor          # The actual string processor, holding binded methods.

from venc2.patterns.exceptions import MalformedPatterns
from venc2.patterns.exceptions import PatternMissingArguments
from venc2.patterns.exceptions import PatternInvalidArgument
from venc2.patterns.exceptions import UnknownContextual

from venc2.helpers import GenericMessage

from test_engine import run_tests

from copy import deepcopy

def add(argv):
    try:
        a, b = tuple(argv)

    except Exception as e:
        raise PatternMissingArguments(e)

    return str( int(a) + int(b) )

def mul(argv):
    try:
        a, b = tuple(argv)
    
    except Exception as e:
        raise PatternMissingArguments(e)
    
    return str( int(a) * int(b) )

def greater(argv):
    try:
        a, b = tuple(argv)
    
    except Exception as e:
        raise PatternMissingArguments(e)
    
    return a if float(a) > float(b) else b

def upper(argv):
    try:
        a = argv[0]

    except:
        raise PatternMissingArguments()

    return a.upper()

def trigger_generic_message_exception(argv):
    raise GenericMessage("lol it will never work")

def trigger_pattern_invalid_argument_exception(argv):
    raise PatternInvalidArgument("some field", "some value", "some message")

def trigger_unknown_contextual_exception(argv):
    raise UnknownContextual()

processor = Processor()
processor.debug = True
processor.set_function("add", add)
processor.set_function("mul", mul)
processor.set_function("greater", greater)
processor.set_function("upper", upper)
processor.set_function("trigger_generic_message_exception", trigger_generic_message_exception)
processor.set_function("trigger_pattern_invalid_argument_exception", trigger_pattern_invalid_argument_exception)
processor.set_function("trigger_unknown_contextual_exception", trigger_unknown_contextual_exception)
processor.blacklist.append("blacklisted")

def test_pattern_processor(args, test_name):
    input_value, process_escapes = args
    ps = ProcessedString(input_value, test_name, process_escapes)
    processor.process(ps)
    return ps.string

def test_pattern_processor_restore(args, test_name):
    input_value, process_escapes = args
    ps = ProcessedString(input_value, test_name, process_escapes)
    states = ( list(ps.open_pattern_pos), list(ps.close_pattern_pos), int(ps.len_open_pattern_pos), int(ps.len_close_pattern_pos), str(ps.string))
    processor.process(ps, safe_process=True)
    ps.restore()
    return states == (ps.open_pattern_pos, ps.close_pattern_pos, ps.len_open_pattern_pos, ps.len_close_pattern_pos, ps.string)


def test_markup_language(args, test_name):
    input_value, markup_language, preserved = args
    ps = ProcessedString(input_value, test_name, False)
    p = deepcopy(processor)
    p.keep_appart_from_markup = preserved
    p.process(ps)
    ps.process_markup_language(markup_language)
    return ps.string.replace('\n', '')

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
        ("moo .:mul::3::3:. .:greater:: .:add::1::1:. :: .:mul::2::2:. :. foo .:upper::lower:. bar", False),
        "moo 9 4 foo LOWER bar",
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
        "moo 2 foo .:mul::1::1:. boo 4 bar",
        test_pattern_processor
    ),
    (
        "Escaping surrounded by Escape patterns.",
        ("moo .:Escape:: \t\n.:NoRage:. ::EndEscape:. foo .:Escape::\t \n.:mul::1::1:.\t \n::EndEscape:. boo .:Escape:: .:NoPattern:. What could possibly go wrong here? ::EndEscape:. bar", True),
        "moo .:NoRage:. foo .:mul::1::1:. boo .:NoPattern:. What could possibly go wrong here? bar",
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
        "moo 6 foo 6 bar mul::3::3:. boo",
        test_pattern_processor
    ),
    (
        "Escape missing closing symbols.",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar .:Escape:: .:mul::3::3 ::EndEscape:. boo", True),
        "moo 6 foo 6 bar .:mul::3::3 boo",
        test_pattern_processor
    ),
    (
        "Restore states.",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar boo", False),
        True,
        test_pattern_processor_restore
    ),
    (
        "Restore states (with escapes).",
        ("moo .:mul::2::3:. foo .:add::3::3:. bar .:Escape:: .:mul::3::3:. ::EndEscape:. boo", True),
        True,
        test_pattern_processor_restore
    ),
    (
        "Missing pattern args.",
        ("moo .:mul::2:. foo .:add::3::3:.", True),
        (PatternMissingArguments, [("expected",2), ("got",1)]),
        test_pattern_processor
    ),
    (
        "Missing unique and single pattern arg.",
        ("moo .:upper:. foo", True),
        (PatternMissingArguments, [("expected",1), ("got",0)]),
        test_pattern_processor
    ),
    (
        "Trigger GenericMessage.",
        ("moo .:trigger_generic_message_exception:. foo", True),
        (GenericMessage, [("message","lol it will never work")]),
        test_pattern_processor
    ),
    (
        "Trigger PatternInvalidArgument.",
        ("moo .:trigger_pattern_invalid_argument_exception:. foo", True),
        (PatternInvalidArgument, [("message","some message"), ("name", "some field"), ("value", "some value")]),
        test_pattern_processor
    ),
    (
        "Trigger KeyError when unknown pattern is met.",
        ("moo .:UnknownPattern:. foo", True),
        (KeyError, []),
        test_pattern_processor
    ),
    (
        "Trigger UnknownContextual when unknown pattern is met.",
        ("moo .:trigger_unknown_contextual_exception:. foo", True),
        (UnknownContextual, []),
        test_pattern_processor
    ),
    (
        "Markdown integration.",
        ("# Main title\n.:add::1::1:.", "Markdown", []),
        "<h1>Main title</h1><p>2</p>",
        test_markup_language
    ),
    (
        "Markdown integration when pattern produce html.",
        ("# Main title\n.:add::1::1:.", "Markdown", ["add"]),
        "<h1>Main title</h1>2",
        test_markup_language
    ),
    (
        "reStructuredText integration.",
        ("Main title\n==========\n.:add::1::1:.", "reStructuredText", []),
        "<div class=\"document\"><div class=\"section\" id=\"main-title\"><h1>Main title</h1><p>2</p></div></div>",
        test_markup_language
    ),
    (
        "reStructuredText integration integration when pattern produce html.",
        ("Main title\n==========\n.:add::1::1:.", "reStructuredText", ["add"]),
        "<div class=\"document\"><div class=\"section\" id=\"main-title\"><h1>Main title</h1>2</div></div>",
        test_markup_language
    ),
]

run_tests("Testing patterns processor...", tests)
