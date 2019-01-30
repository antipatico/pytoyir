#!/usr/bin/env python3
"""A Python3 toy Information Retrieval system (using whoosh and pyenchant).

Usage:
  pytoyir.py -h | --help
  pytoyir.py --version
  pytoyir.py benchmark (npl|lisa) [--recall=<RECALL>|--interpolated] [--bm25f|--tf-idf|--freq]
  pytoyir.py search (npl|lisa) [-L=<max>] [-s] [-w] [-B] [--bm25f|--tf-idf|--freq] <query>
  pytoyir.py index (npl|lisa) [--delete]

Options:
  -h --help             Show this help screen.
  --version             Show version.
  -s --no-spell-check   Disable spell checking.
  -w --no-wildcard      Disable wildcard queries.
  -B --batch            Run in batch mode.
  -L --limit=<max>      Maximum number of results shown [Default: 10].
                        Use None for no limits.
  -R --recall=<RECALL>  Set a goal recall, then calculates the average
                        precision at the given recall level for all the queries.
                        If 'all', print the average precision for all the
                        standard recall levels.
  --interpolated        Calculates the interpolated average precision for each
                        query in the benchmark data.

Scoring Models:
  --bm25f               Use the BM25F probabilistic model
  --tf-idf              Use the TF-IDF model
  --freq                Use the Frequency model

Wildcard queries and spellchecking are enabled by default.
The default scoring model for the search if none is specified is BM25F.
Benchmarking is always in batch mode.

"""
import json
import re

from docopt import docopt
from whoosh import scoring

from modules.search import search
from modules.spellCheck import correct
from modules.index import createIndex, deleteIndex, openIndex
from modules.cli import confirm
from modules.utils import lazyInt
from modules.benchmark import interpolatedAveragePrecision, averagePrecisionRecalls, normalizeBenchmarkData, standardLevels


def parseLimit(limit):
    if limit == "None":
        return None
    return lazyInt(limit) if lazyInt(limit) > 0 else 10


def parseRecall(recall):
    try:
        if recall == "all":
            return recall
        return float("%.1f" % float(recall)) if 0.0 <= float("%.1f" % float(recall)) <= 1.0 else None
    except:
        return None


if __name__ == "__main__":
    arg = docopt(__doc__, version='pytoyir v0.1')

    if arg["lisa"]:
        basePath = "./datasets/LISA/"
    else:
        basePath = "./datasets/NPL/"

    indexDir = basePath + "index/"
    docDir = basePath + "docs/"
    benchmarkPath = basePath + "benchmark-data.json"

    if arg["search"]:
        query = arg['<query>']
        spellCheck = not arg["--no-spell-check"]
        batch = arg["--batch"]
        limit = parseLimit(arg["--limit"])
        wildcard = not arg["--no-wildcard"]

        if arg['--tf-idf']:
            modelScoring = scoring.TF_IDF()
        elif arg['--freq']:
            modelScoring = scoring.Frequency()
        else:
            modelScoring = scoring.BM25F()

        if spellCheck:
            fixed = correct(query)
            if fixed != query:
                if batch or confirm("Did you mean: `" + fixed + "`?"):
                    query = fixed

        print("Searching for `" + query + "`")
        index = openIndex(indexDir)
        r = search(query, index, modelScoring, limit, wildcard)

        for result in r:
            with open(result["path"], "r") as f:
                body = re.sub(" +", " ", f.read().replace("\n", " "))
                print("[%s] %s..." % (result["id"], " ".join(body.split(" ")[:10])))

        index.close()

        print("Found %d matching documents, displaying the first %d (use --limit to change this)" % (len(r), limit))

    elif arg['index']:
        if arg['--delete']:
            print("Removing the index stored in '" + indexDir + "'")
            deleteIndex(indexDir)
        else:
            print("Indexing documents of '" + docDir + "' into '" + indexDir + "'")
            createIndex(docDir, indexDir)

    elif arg['benchmark']:
        spellCheck = not arg["--no-spell-check"]
        goal = parseRecall(arg['--recall'])
        interpolated = arg['--interpolated']

        if arg['--tf-idf']:
            modelScoring = scoring.TF_IDF()
        elif arg['--freq']:
            modelScoring = scoring.Frequency()
        else:
            modelScoring = scoring.BM25F()

        with open(benchmarkPath, "r") as f:
            data = normalizeBenchmarkData(json.loads(f.read()))

        index = openIndex(indexDir)
        if goal is not None:
            avgP = averagePrecisionRecalls(index, data, modelScoring)
            if goal == "all":
                for precision, recall in enumerate(avgP):
                    print("At recall level %.1f the average precision is %.4f" % (precision/10, recall))
            else:
                print("At recall level %.1f the average precision is %.4f" % (goal, avgP[standardLevels.index(goal)]))
        elif interpolated:
            intAvgP = interpolatedAveragePrecision(index, data, modelScoring)
            for query_id, intP in enumerate(intAvgP):
                print("Query %d: %.4f" % (query_id, intP))
            print("Mean: %.4f" % (sum(intAvgP) / len(intAvgP)))
        else:
            print("You must either set a recall level or specify the --interpolated flag.")

        index.close()
