#!/usr/bin/env python3
import os

FILE_PATH = "./datasets/NPL/doc-text"
OUT_PATH = "./datasets/NPL/docs/"
TERMINATOR = "   /\n"

if __name__ == "__main__":
    print("Splitting NPL's dataset documents...")
    os.makedirs(OUT_PATH, exist_ok=True)

    with open(FILE_PATH, "r") as f:
        next_line = f.readline()
        while next_line != "":
            doc_id = int(next_line)
            doc_body = ""
            next_line = f.readline()
            while next_line != TERMINATOR:
                doc_body += next_line
                next_line = f.readline()
            with open(OUT_PATH + str(doc_id) + ".txt", "w") as out:
                out.write(doc_body)
            next_line = f.readline()
