#! /usr/bin/python3.13

import timeit
import unidecode
import unicodedata

# Broken, see framagit issue #130
def quirk_encoding_1(string):
    for char in ['\'',' ','%',':','&','\\']:
        string = string.replace(char,'-')
    return unidecode.unidecode(string)

# Work well but slower
def quirk_encoding_2(string):
    return unidecode.unidecode(''.join([ c if c.isalnum() or c in ('/','.',) else '-' for c in string]))

# Faster and run without unidecode dependancy
def quirk_encoding_3(string):
    return ''.join(c for c in unicodedata.normalize('NFD', ''.join([ c if c.isalnum() or c in ('/','.','\x1a') else '-' for c in string])) if unicodedata.category(c) != "Mn")
    
print(quirk_encoding_1("../Héllo Kitty Âéèà"), timeit.timeit(lambda: quirk_encoding_1("../Héllo Kitty Âéèà"), number=100000))
print(quirk_encoding_2("../Héllo Kitty Âéèà"), timeit.timeit(lambda: quirk_encoding_2("../Héllo Kitty Âéèà"), number=100000))
print(quirk_encoding_3("../Héllo Kitty Âéèà"), timeit.timeit(lambda: quirk_encoding_3("../Héllo Kitty Âéèà"), number=100000))
