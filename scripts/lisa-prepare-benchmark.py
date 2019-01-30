#!/usr/bin/env python3
import json
import re


def parseIntLine(line):
    return [int(x) for x in re.sub(" +", " ", line.strip()).split(" ")]


if __name__ == "__main__":
    print("Preparing the benchmark data for the LISA dataset...")
    benchmark = dict()
    # Parse the query file
    with open("./datasets/LISA/LISA.QUE", "r") as f:
        next_line = f.readline()
        while next_line:
            query_id = int(next_line)
            query_body = ""
            next_line = f.readline()
            while not next_line.endswith(" #\n"):
                query_body += next_line
                next_line = f.readline()
            query_body += next_line[:-3]
            benchmark[int(query_id)] = {"query": re.sub(" +", " ", query_body.replace("\n", " ")).strip(), "relevant": []}
            next_line = f.readline()

    # Parse the relevant file
    with open("./datasets/LISA/LISARJ.NUM", "r") as f:
        next_line = f.readline()
        while next_line:
            ints = parseIntLine(next_line)
            query_id = ints[0]
            relevant_count = ints[1]
            relevant = []
            while len(ints) - 2 < relevant_count:
                next_line = f.readline()
                ints += parseIntLine(next_line)
            for j in range(2, relevant_count+2):
                relevant.append(ints[j])
            benchmark[int(query_id)]["relevant"] = relevant
            next_line = f.readline()

    with open("./datasets/LISA/benchmark-data.json", "w+") as f:
        f.write(json.dumps(benchmark))
