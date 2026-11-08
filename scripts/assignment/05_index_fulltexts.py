import pysolr
from pathlib import Path

repoP = Path.cwd().parent.parent

FULLTEXT_PATH = repoP / "data/assignment-data/fulltexts"

MD_SOLR_CORE_URL = "http://localhost:8983/solr/my1stcore"
FT_SOLR_CORE_URL = "http://localhost:8983/solr/pg_fulltexts"

BATCH_SIZE = 100


def createSolRecord(ebookid: str, ebookidFilePath: Path, mdSolr) -> tuple[dict | None, str | None]:
    """Query metadata core and combine with local fulltext file."""
    try:
        result = mdSolr.search(f"id:{ebookid}")

        # sanity check
        if len(result.docs) != 1:
            return None, f"Error: Expected exactly 1 document in metadata core, got {len(result.docs)}"

        mdRecDict = result.docs[0]

        solrRecord = {
            "id": ebookid,
            "title": mdRecDict.get("title"),
            "authors": mdRecDict.get("authors"),
            "language": mdRecDict.get("language"),
            "subjects": mdRecDict.get("subjects"),
            "issued": mdRecDict.get("issued"),
            "fulltext": None
        }

        # try to read fulltext file
        with open(ebookidFilePath, encoding="utf-8") as ftfile:
            solrRecord["fulltext"] = ftfile.read()

        return solrRecord, None

    except Exception as ex:
        return None, f"Error: {ex}"


def indexAllRecords():
    
    successCount = 0
    errorList = []

    print("INDEXING SOLR RECORDS...\n")

    # initialize client connections
    mdSolr = pysolr.Solr(MD_SOLR_CORE_URL, timeout=30)
    ftSolr = pysolr.Solr(FT_SOLR_CORE_URL, timeout=30)

    batch = []

    for ebookidFilePath in FULLTEXT_PATH.glob("*_filtered.txt"):
        ebookid = ebookidFilePath.name.replace('_filtered.txt', '')

        solrRecord, errorCreate = createSolRecord(ebookid, ebookidFilePath, mdSolr)
        
        if errorCreate:
            print(f"[{ebookid}] Error during record creation: {errorCreate}")
            errorList.append(ebookid)
            continue

        batch.append(solrRecord)
        successCount += 1

        # if batch full send to Solr
        if len(batch) >= BATCH_SIZE:
            try:
                ftSolr.add(batch)
                print(f"Successfully indexed batch of {len(batch)} records (Total so far: {successCount})...")
                batch = [] # reset batch

            except Exception as ex:
                print(f"Error during batch indexing: {ex}")
                errorList.append(f"Batch ending at {ebookid}")

    # index remaining records in final partial batch
    if batch:
        try:
            ftSolr.add(batch)
            print(f"Successfully indexed final batch of {len(batch)} records.")
        except Exception as ex:
            print(f"Error during final batch indexing: {ex}")

    # commit once all documents are added
    print("Issuing final commit to Solr...")
    ftSolr.commit()

    print("\nFINISHED INDEXING RECORDS")
    print(f"Successfully processed: {successCount}")
    print(f"Errors encountered: {len(errorList)}. IDs/Batches: {errorList}")


if __name__ == "__main__":
    indexAllRecords()