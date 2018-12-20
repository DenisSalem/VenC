#! /usr/bin/python3
print("Testing Patterns processing...", end=' ')
from venc2.patterns.processor import ProcessedString # The object holding the string and its states
from venc2.patterns.processor import Processor # The actual string processor, holding binded methods.

def add(argv):
    a, b = tuple(argv)
    return str( int(a) + int(b) )

def mul(argv):
    a, b = tuple(argv)
    return str( int(a) * int(b) )

def greater(argv):
    a, b = tuple(argv)
    return a if float(a) > float(b) else b

def blacklisted(argv):
    return "blacklisted pattern is now running!"

def forbidden(argv):
    return "forbidden pattern is now running!"

processor = Processor()
processor.set_function("add", add)
processor.set_function("mul", mul)
processor.set_function("greater", greater)
processor.set_function("blacklisted", greater)

# Simple pattern detection
ps = ProcessedString("moo .:add::1::1:. foo", "Test 1")
processor.process(ps)
assert("moo 2 foo" == ps.string)

# Match two patterns
ps = ProcessedString("moo .:add::1::1:. foo .:mul::2::2:. bar", "Test 2")
processor.process(ps)
assert("moo 2 foo 4 bar" == ps.string)

# Recursive Patterns
ps = ProcessedString("moo .:greater:: .:add::1::1:. :: .:mul::2::2:. :. bar", "Test 3")
processor.process(ps)
assert("moo 4 bar" == ps.string)

# Recursive Patterns
ps = ProcessedString("moo .:greater:: .:add::1::1:. :: .:mul::2::2:. :. foo .:greater::1::2:. bar", "Test 4")
processor.process(ps)
assert("moo 4 foo 2 bar" == ps.string)

# Recursive Patterns 2
ps = ProcessedString("moo .:greater:: .:greater::1::2:. :: 0 :. bar", "Test 5")
processor.process(ps)
assert("moo 2 bar" == ps.string)

# Test against blacklisted pattern
processor.blacklist.append("blacklisted")
ps = ProcessedString("moo .:blacklisted:. foo .:greater::3::5:. bar", "Test 5")
processor.process(ps)
assert("moo .:blacklisted:. foo 5 bar" == ps.string)

print("Done.")
