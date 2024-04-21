#! /usr/bin/env python3

import os


OFFSET = len(".:GetChapterAttributeByIndex::path::")

for filename in os.listdir("entries"):
    content = open("entries/"+filename, "r").read()
    index=0
    print("entries/"+filename)
    while True:
        try:
            index = content.index(".:GetChapterAttributeByIndex::path::", index)
            index_end = content.index(":.", index)
            
            chapter =  content[index:index_end+2].split("::")[2].split(".")
            
            # ~ if int(chapter[0]) >= 3:
                # ~ chapter[0] = str(int(chapter[0])+1)

            if chapter[0] == "8":
                chapter[0] = "3"
            
            new_pattern = ".:GetChapterAttributeByIndex::path::"+ (".".join(chapter))
            
            print("\t--", content[index-10:index]+ content[index:index_end+2]+ content[index_end+2:index_end+12])
            print("\t++", content[index-10:index]+ new_pattern + content[index_end+2:index_end+12])
            
            content = content[0:index] + new_pattern + content[index_end+2:]
            print("\tvv", content[index-10:index_end+12])

            index = index_end+2
            

        except ValueError as e:
            break
            
    open("entries/"+filename, "w").write(content)
            

