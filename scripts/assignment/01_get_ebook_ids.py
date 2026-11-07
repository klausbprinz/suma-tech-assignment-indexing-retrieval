import pysolr
from pathlib import Path

repoP = Path.cwd().parent.parent

solrCoreUrl = "http://localhost:8983/solr/my1stcore"
outputFilePath = repoP / "data/assignment-data/ebook_ids.txt"

def getEbookIds():
    # connect to solr core
    solr = pysolr.Solr(solrCoreUrl, timeout=30)
    
    query = "language:de AND type:Text"
    
    # pysolr handles deep paging via cursorMark='*'
    results = solr.search(
        query,
        sort="id asc",
        fl="id",
        cursorMark="*"
    )
    
    # extract ids
    allIds = [doc.get("id") for doc in results if "id" in doc]

    # write to text file
    with open(outputFilePath, "w", encoding="utf-8") as f:
        for ebookId in allIds:
            f.write(f"{ebookId}\n")
            
    print(f"Anzahl gespeicherter E-Book-IDs: {len(allIds)}")

if __name__ == "__main__":
    getEbookIds()