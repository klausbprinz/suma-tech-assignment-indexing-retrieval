"""Legt im Solr-Core pg_fulltexts ein Schema fuer die Volltexte an.

Nutzt die Solr Schema-API, zum Anlegen von Indexfeldtypen, Indexfeldern und Copy-Fields.

Es wird ein neuer Feldtypen definiert:

    - text_de_custom
        - verwendeter Tokenizer: StandardTokenizerFactory
        - Filterkette, welche die Tokens durchlaufen sollen: LowerCaseFilterFactory, 
        StopFilterFactory (auf Basis der Datei stopwords_de.txt), GermanMinimalStemFilterFactory
"""

import requests

SOLR_CORE_URL = "http://localhost:8983/solr/pg_fulltexts"

FIELD_TYPES = [
    {
        "name": "text_de_custom",
        "class": "solr.TextField",
        "positionIncrementGap": "100",
        "analyzer": {
            "tokenizer": {"class": "solr.StandardTokenizerFactory"},
            "filters": [
                {"class": "solr.LowerCaseFilterFactory"},
                {"class": "solr.StopFilterFactory", "words": "lang/stopwords_de.txt", "ignoreCase": "true"},
                {"class": "solr.GermanMinimalStemFilterFactory"},
            ],
        },
    },
]

FIELDS = [
    # eindeutige ID des E-Books aus dem Project Gutenberg
    {"name": "id", "type": "string", "stored": True, "indexed": True, "multiValued": False},

    # Titel des E-Books
    {"name": "title", "type": "text_de", "stored": True, "indexed": True, "multiValued": False},

    # Name des bzw. der Autoren des E-Books
    {"name": "authors", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},

    # Sprache des E-Books
    {"name": "language", "type": "string", "stored": True, "indexed": True, "multiValued": True},

    # Thema bzw. Themen des E-Books
    {"name": "subjects", "type": "text_general", "stored": True, "indexed": True, "multiValued": True},

    # Datum der Veröffentlichung des E-Books
    {"name": "issued", "type": "pdate", "stored": True, "indexed": True, "multiValued": False},

    # Volltext des E-Books
    {"name": "fulltext", "type": "text_de", "stored": False, "indexed": True, "multiValued": False, "termVectors": True},

    # Volltext des E-Books
    {"name": "fulltext_alternative", "type": "text_de_custom", "stored": False, "indexed": True, "multiValued": False},
]

COPY_FIELDS = [
    {"source": "fulltext", "dest": "fulltext_alternative"},
]

def get_existing_field_type_names(solr_core_url: str) -> set:
    resp = requests.get(f"{solr_core_url}/schema/fieldtypes", timeout=30)
    resp.raise_for_status()
    return {t["name"] for t in resp.json().get("fieldTypes", [])}

def get_existing_field_names(solr_core_url: str) -> set:
    resp = requests.get(f"{solr_core_url}/schema/fields", timeout=30)
    resp.raise_for_status()
    fields = resp.json().get("fields", [])
    return {f["name"] for f in fields}

def get_existing_copy_fields(solr_core_url: str) -> set:
    resp = requests.get(f"{solr_core_url}/schema/copyfields", timeout=30)
    resp.raise_for_status()
    return {(c["source"], c["dest"]) for c in resp.json().get("copyFields", [])}

def create_schema(solr_core_url: str = SOLR_CORE_URL) -> None:
    existing_types = get_existing_field_type_names(solr_core_url)
    new_types = [t for t in FIELD_TYPES if t["name"] not in existing_types]
    if new_types:
        resp = requests.post(f"{solr_core_url}/schema", json={"add-field-type": new_types}, timeout=30)
        resp.raise_for_status()
        print(f"{len(new_types)} Feldtyp(en) angelegt: {[t['name'] for t in new_types]}")
    else:
        print("Alle Feldtypen sind bereits vorhanden.")

    existing_fields = get_existing_field_names(solr_core_url)
    new_fields = [f for f in FIELDS if f["name"] not in existing_fields]
    if new_fields:
        resp = requests.post(f"{solr_core_url}/schema", json={"add-field": new_fields}, timeout=30)
        resp.raise_for_status()
        print(f"{len(new_fields)} Feld(er) angelegt: {[f['name'] for f in new_fields]}")
    else:
        print("Alle Felder sind bereits im Schema vorhanden.")

    existing_copy_fields = get_existing_copy_fields(solr_core_url)
    new_copy_fields = [
        c for c in COPY_FIELDS if (c["source"], c["dest"]) not in existing_copy_fields
    ]
    if new_copy_fields:
        resp = requests.post(f"{solr_core_url}/schema", json={"add-copy-field": new_copy_fields}, timeout=30)
        resp.raise_for_status()
        print(f"{len(new_copy_fields)} Copy-Field(s) angelegt: {new_copy_fields}")
    else:
        print("Alle Copy-Fields sind bereits vorhanden.")

if __name__ == "__main__":
    create_schema()
