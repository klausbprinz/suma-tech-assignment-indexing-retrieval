import pysolr
import locale
from datetime import datetime

SOLR_CORE_URL = "http://localhost:8983/solr/pg_fulltexts"

# set locale for German date formatting (e.g., month names)
try:
    locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")
except:
    pass # fallback if locale not installed


def search(solr, query):
    
    # Defining Runtime Search Request Parameters
    # = query-time request parameters for the Extended DisMax (edismax) query parser
    # this tells Solr's search engine how to behave for that specific search
    params = {
        # Query Fields
        # look for terms in user query across these specific fields, multiply matches by ..
        "qf": "title^5 authors^2 subjects^1 fulltext^2 fulltext_alternative^3",

        # Use Extended DisMax Query Parser
        # = don't use basic search parser, use Extended DisMax parse so field weights and smart matching
        # can be applied
        "defType": "edismax",

        # Operator -> OR: multiple words matches documents containing any of them
        "q.op": "OR",

        # Minimum Match(mm) -> when multiple terms are entered, at least 10% of them must match
        "mm": "10%",

        # Boost Function -> to give higher relevance scores to newer books
        # when finding matching docs, give extra score boost to ...
        "bf": "recip(ms(NOW,issued),3.16e-11,1,1)",

        # Return Fields
        "fl": "id, title, issued, authors, language, subjects, score",

        # Top 10 Ranking
        "rows": 10

    }

    results = solr.search(query, **params)

    if not results or len(results) == 0:
        print("Ihre Suchanfrage liefert keine Treffer!")
        return

    print(f"\n* * * Insgesamt {results.hits} Suchergebnisse gefunden – {len(results)} Treffer werden angezeigt. * * *\n")

    # einzelne Suchergebnisse ausgeben
    for i, result in enumerate(results, start=1):

        issued = datetime.fromisoformat(result.get("issued").replace("Z", "+00:00"))
        
        print(f"""Suchtreffer # {i} (ID: {result.get('id')}): {result.get("title")}
          Autor: {", ".join(result.get("authors") or [])}
          Aufnahmedatum: {issued:%d. %B %Y}
          Sprache: {', '.join(result.get('language') or [])}
          Themengebiete: {', '.join(result.get('subjects') or [])}
          Score-Wert: {result.get("score")}""")

if __name__ == "__main__":
    print("Gib eine Suchanfrage ein oder 'quit!' zum Verlassen.")
    solr = pysolr.Solr(SOLR_CORE_URL)

    while True:
        user_query = input("Suchanfrage: ").strip()
        if user_query.lower() == "quit!":
            break
        elif user_query:
            search(solr, user_query)