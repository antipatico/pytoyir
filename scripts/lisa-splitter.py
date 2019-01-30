#!/usr/bin/env python3
import re
import os
filename = "./datasets/LISA/docs/"
Dir = "./datasets/LISA/"
doc_regex = r"^Document +(\d+)$"
file_regex = r"^LISA\d\.\d+$"


def representsFileName(s):
    m = re.match(doc_regex, s)
    if m:
        return m.group(1)
    return None


def splitFile(file):
    for line in file:
        # print(line)
        doc_num = representsFileName(line)
        if doc_num:
            f = open(filename+doc_num+".txt", "w+")
        elif line == "********************************************\n":
            f.close()
        elif not f.closed:
            f.write(line)


if __name__ == "__main__":
    print("Splitting LISA's dataset documents...")
    os.makedirs(filename, exist_ok=True)

    for filePath in os.listdir(Dir):
        if re.match(file_regex, filePath):
            with open(Dir+filePath, "r") as f:
                splitFile(f)
