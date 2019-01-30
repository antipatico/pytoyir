#!/usr/bin/env python3
import json
import re


def parseRelevantLine(line):
    return [int(x) for x in re.sub(" +", " ", line.strip()).split(" ")]


if __name__ == "__main__":
    print("Preparing the benchmark data for the NPL dataset...")
    benchmark = dict()
    # Parse the query file
    with open("./datasets/NPL/query-text", "r") as f:
        next_line = f.readline()
        while next_line:
            query_id = int(next_line)
            query_body = ""
            next_line = f.readline()
            while next_line != "/\n":
                query_body += next_line
                next_line = f.readline()
            benchmark[int(query_id)] = {"query": query_body.replace("\n", " ").strip(), "relevant": []}
            next_line = f.readline()

    # Parse the relevant file
    with open("./datasets/NPL/rlv-ass", "r") as f:
        next_line = f.readline()
        while next_line:
            query_id = int(next_line)
            relevant = []
            next_line = f.readline()
            while next_line != "   /\n":
                relevant += parseRelevantLine(next_line)
                next_line = f.readline()
            benchmark[int(query_id)]["relevant"] = relevant
            next_line = f.readline()

    with open("./datasets/NPL/benchmark-data.json", "w+") as f:
        f.write(json.dumps(benchmark))
