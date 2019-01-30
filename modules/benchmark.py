from whoosh import qparser
from .search import searchParsed

standardLevels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]


def getQparser(index):
    parser = qparser.QueryParser("body", schema=index.schema, group=qparser.OrGroup)
    parser.remove_plugin_class(qparser.FieldsPlugin)
    parser.remove_plugin_class(qparser.WildcardPlugin)
    return parser


def execQuery(query, index, parser, modelScoring):
    # Parse the query
    q = parser.parse(query)
    # Prepare the result list
    qResults = []
    # Execute the query and save the results
    r = searchParsed(q, index, modelScoring, None)
    for hit in r:
        qResults.append(hit["id"])

    return qResults


def normalizeBenchmarkData(rawData):
    data = dict()
    for key in rawData:
        data[int(key)] = rawData[key]
    return data


def interpolatedPrecision(precision):
    for i in range(len(precision)-1):
        precision[i] = max(precision[i], precision[i+1])
    return precision


def standardPrecision(relevant, qResults):
    P = []
    P.insert(0, 1.0)

    recall_levels = []  # len(qResults)
    for i in range(len(qResults)):
        recall_levels.append(len(set(qResults[0:i]).intersection(relevant))/len(relevant))

    recall_set = list(set(recall_levels))
    std_index = []
    for level in standardLevels:
        val, idx = min((abs(val-level), idx) for (idx, val) in enumerate(recall_set))
        std_index.insert(standardLevels.index(level), recall_levels.index(recall_set[idx]))

    for i in range(1, len(standardLevels)):
        precision = len(set(qResults[0:std_index[i]]).intersection(relevant))/(std_index[i]+1)
        P.insert(i, precision)

    return P


def averagePrecisionRecalls(index, data, modelScoring):
    avgP = [0] * len(standardLevels)
    parser = getQparser(index)

    for query_id in data:
        # Extract benchmark data (query && relevant)
        query = data[query_id]["query"]
        relevant = data[query_id]["relevant"]
        # Parse && exec the query
        results = execQuery(query, index, parser, modelScoring)

        # Calculates the standard precision at all recall levels.
        stdP = standardPrecision(relevant, results)

        for i in range(len(standardLevels)):
            avgP[i] += stdP[i]

    for i in range(len(standardLevels)):
        avgP[i] = avgP[i]/len(data)

    return avgP


def interpolatedAveragePrecision(index, data, modelScoring):
    intAvgP = []
    parser = getQparser(index)

    for query_id in data:
        # Extract benchmark data (query && relevant)
        query = data[query_id]["query"]
        relevant = data[query_id]["relevant"]
        # Parse && exec the query
        results = execQuery(query, index, parser, modelScoring)

        # Calculates the standard precision at all recall levels.
        stdP = standardPrecision(relevant, results)
        intP = interpolatedPrecision(stdP)

        intAvgP.insert(query_id, sum(intP) / len(intP))

    return intAvgP
