from whoosh import qparser


def searchParsed(q, index, modelScoring, limit):
    with index.searcher(closereader=False, weighting=modelScoring) as s:
        return s.search(q, limit=limit)


def search(query, index, weighting, limit, wildcard):
    parser = qparser.QueryParser("body", schema=index.schema, group=qparser.OrGroup)
    parser.remove_plugin_class(qparser.FieldsPlugin)
    if not wildcard:
        parser.remove_plugin_class(qparser.WildcardPlugin)

    q = parser.parse(query)

    return searchParsed(q, index, weighting, limit)
