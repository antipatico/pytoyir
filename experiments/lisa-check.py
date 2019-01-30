#!/usr/bin/env python3
import re
import os
filename = "./datasets/LISA/docs/"
Dir = "./datasets/LISA/"
doc_regex = r"^Document +(\d+)$"
file_regex = r"^LISA\d\.\d+$"
done = []


def representsFileName(s):
    m = re.match(doc_regex, s)
    if m:
        return m.group(1)
    return None


def splitFile(file):
    global i, done
    for line in file:
        doc_num = representsFileName(line)
        if doc_num:
            if int(doc_num) in done:
                print(doc_num, "has a duplicate!")
            else:
                done.append(int(doc_num))
            i += 1
            pass
        elif line == "********************************************\n":
            pass
        elif not f.closed:
            pass


os.makedirs(filename, exist_ok=True)

i = 0
for filePath in os.listdir(Dir):
    if re.match(file_regex, filePath):
        print(filePath)
        with open(Dir+filePath, "r") as f:
            splitFile(f)

print(i)
