from whoosh.fields import Schema, TEXT, STORED
from whoosh.analysis import LanguageAnalyzer
import os
import shutil
from whoosh import index


def getSchema():
    return Schema(path=STORED, id=STORED, body=TEXT(analyzer=LanguageAnalyzer("en")))


def openIndex(ixDir):
    return index.open_dir(ixDir)


def createIndex(docDir, ixDir):
    schema = getSchema()

    if not (docDir.endswith("/")):
        docDir = docDir+"/"
    os.makedirs(ixDir, exist_ok=True)
    ix = index.create_in(ixDir, schema)
    writer = ix.writer()
    for filename in os.listdir(docDir):
        _id = int(filename[:-4])
        filePath = docDir+filename
        with open(filePath) as f:
            writer.add_document(path=filePath, id=_id, body=f.read())

    writer.commit()


def deleteIndex(ixDir):
    shutil.rmtree(ixDir, ignore_errors=True)



