import requests
import pysolr

SOLR_BASE_URL = "http://localhost:8983/solr/pg_fulltexts"

def setupMltHandler():
    handlerEndpoint = f"{SOLR_BASE_URL}/config/requestHandler"
    
    # check if /mlt request handler already exists
    getRes = requests.get(handlerEndpoint)
    
    exists = False

    if getRes.status_code == 200:
        configData = getRes.json()
        
        # Solr returns request handlers inside the config response
        handlers = configData.get("config", {}).get("requestHandler", {})
        if "/mlt" in handlers:
            exists = True

    # if doesnt exist, create using POST to config API
    if not exists:
        print("Request-Handler '/mlt' nicht gefunden. Wird erstellt...")
        
        configPayload = {
            "add-requesthandler": {
                "name": "/mlt",
                "class": "solr.MoreLikeThisHandler",
                "defaults": {
                    "mlt.fl": "fulltext",
                    "mlt.mintf": 2,
                    "mlt.mindf": 5,
                    "mlt.minwl": 5,
                    "mlt.maxdfpct": 25,
                    "mlt.interestingTerms": "list",
                    # das Ausgangsdokument selbst soll nicht in der Trefferliste erscheinen
                    "mlt.match.include": "false",
                    "mlt.boost": "true"
                }
            }
        }
        
        postRes = requests.post(
            f"{SOLR_BASE_URL}/config",
            json=configPayload,
            headers={"Content-Type": "application/json"}
        )
        
        if postRes.status_code == 200:
            print("Request-Handler '/mlt' erfolgreich erstellt!")
        else:
            print(f"Fehler beim Erstellen des Handlers: {postRes.text}")
    else:
        print("Request-Handler '/mlt' ist bereits vorhanden.")


def getTopDoc(solr, query):

    params = {
        "qf": "title^5 authors^2 subjects^1 fulltext^2 fulltext_alternative^3",
        "defType": "edismax",
        "q.op": "OR",
        "mm": "10%",
        "fl": "id, title, authors",
        "rows": 1  # only top 1 doc
    }

    results = solr.search(query, **params)
    
    if not results or len(results) == 0:
        print("Keine Treffer für diese Suchanfrage gefunden!")
        return None

    # print info on doc
    topDoc = results.docs[0]
    print(f"\n--- Ausgangsdokument (Top-1 Treffer) ---")
    print(f"ID: {topDoc.get('id')}")
    print(f"Titel: {topDoc.get('title')}")
    print(f"Autor(en): {', '.join(topDoc.get('authors') or [])}")
    print("-" * 40)

    return topDoc


def runMLT(docId, strictMode=False):

    mltEndpoint = f"{SOLR_BASE_URL}/mlt"
    
    params = {
        "q": f"id:{docId}",
        "wt": "json",
        "rows": 3,
        # Minimum Word Length -> e.g. only keep words with 7+ letters (filters out short verbs/articles, keeps long nouns 
        # "mlt.minwl": 7,
        # Minimum Term Frequency -> word must appear at least 3 times in the source text (filters out accidental mentions)
        # "mlt.mintf": 3
    }

    # trying some params
    if strictMode:
        print("\n[INFO] Running in STRICT Mode (High word length & frequency thresholds)")
        params.update({
            "mlt.minwl": 7,
            "mlt.mintf": 3
        })
    else:
        print("\n[INFO] Running in STANDARD Mode (Default thresholds)")
        params.update({
            "mlt.minwl": 5,   # default from handler setup
            "mlt.mintf": 2
        })
    
    resMlt = requests.get(mltEndpoint, params=params)
    if resMlt.status_code != 200:
        print(f"Fehler bei der MLT-Abfrage: {resMlt.text}")
        return

    data = resMlt.json()
    
    # print interesting terms
    print("\n--- Interessanteste Terme des Ausgangsdokuments ---")
    interestingTerms = data.get("interestingTerms", [])
    if interestingTerms:
        print(", ".join(interestingTerms))
    else:
        print("Keine interessanten Terme gefunden.")
    print("-" * 50)

    # now print similar docs
    print("\n--- Ähnliche E-Books (MoreLikeThis Top-3) ---")
    docs = data.get("response", {}).get("docs", [])
    if not docs:
        print("Keine ähnlichen E-Books gefunden.")
        return

    for i, doc in enumerate(docs, start=1):
        print(f"""Ähnlicher Treffer # {i} (ID: {doc.get('id')}): {doc.get('title')}
          Autor: {', '.join(doc.get('authors') or [])}""")
        print("-" * 50)


if __name__ == "__main__":

    # Step 1: ensure MLT Handler is ready
    setupMltHandler()
    
    # Step 2: get user query and find Top-1 document
    solr = pysolr.Solr(SOLR_BASE_URL, timeout=30)
    userQuery = input("\nSuchanfrage für Ausgangsdokument: ").strip()
    
    topDoc = getTopDoc(solr,userQuery)

    if topDoc:

        # Step 3: run MoreLikeThis on the Top-1 document ID
        runMLT(
            topDoc.get('id'),
            strictMode=True             # toggle this
        )
    else:
        print("Keine Treffer für diese Suchanfrage.")
