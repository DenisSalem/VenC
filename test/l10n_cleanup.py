#! /usr/bin/env python3

from venc3.l10n.fr import Messages as Messages_fr
from venc3.l10n.en import Messages as Messages_en
import os

messages_fr = Messages_fr()
messages_en = Messages_en()

not_founds = []

for attr in [item for item in dir(messages_en)if item[:2] != "__"]:
    found = False
    for root, dirs, files in os.walk("../src/"):
        if ("../src/venc3/l10n" in root) or  ("../src/share" in root):
            continue
            
        for f in files:
            try:
                fp = open(root+'/'+f).read()
            except UnicodeDecodeError:
                print(root+'/'+f)
                exit()
            
            if "messages."+attr in fp:
                found = True
                break
                
        if found:
            break
    
    if not found:
        not_founds.append(attr)
            
    
for nf in not_founds:
    print(nf)

print(len(dir(messages_en)), len(dir(messages_fr)))
