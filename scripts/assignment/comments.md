## Comments on 01_get_ebook_ids.py
First I ran `type:Text AND language:de` in the `q` field of the Solr Dashboard. That yielded:
```
"response":{
    "numFound":2455,
    "start":0,
    "numFoundExact":true,
    "docs":[
      {
        "id":"417",
        "type":"Text",
        "title":"Dr. Martin Luther's Deutsche Geistliche Lieder\r\nThe Hymns of Martin Luther Set to Their Original Melodies, With an English Version",
        "language":[
          "de",
          "en"
        ],
        "authors":[
          "Luther, Martin, 1483-1546",
          "Allen, Nathan H. (Nathan Hale), 1848-1925 [Editor]",
          "Bacon, Leonard Woolsey, 1830-1907 [Editor]"
        ],
        "subjects":[
          "Hymns, German",
          "Lutheran Church -- Hymns"
        ],
        "issued":"1996-02-01T00:00:00Z",
        "_version_":1881187808436027393,
        "_root_":"417"
      }, [...]
```

Use cursorMark in search() of PySolr - otherwise PySolr gets kind of confused with `nextCursorMark`

---

## Comments on 02_fetch-works.py
Script Output
```
Insgesamt 2435 Volltextdateien erfolgreich heruntergeladen (Anzahl Fehler: 20).
```

He who reads the assignment in total ...

```
(base) k@Ixion:~/Dev/learning/bibinfo-suchmaschinentechnologie/suma-tech-assignment-indexing-retrieval/scripts/assignment$ python 02_fetch-works.py 
Verarbeite Datei /home/k/Dev/learning/bibinfo-suchmaschinentechnologie/suma-tech-assignment-indexing-retrieval/data/assignment-data/ebook_ids.txt. Lade E-Book-IDs.
Insgesamt 2455 E-Book-IDs gefunden.
2435 Dateien wurden bereits geladen.
20 E-Book-ID(s) wurden noch nicht geladen. IDs: ['38157', '15267', '25157', '31911', '36310', '29806', '33317', '32634', '30005', '11925', '33330', '33202', '29780', '32766', '5740', '38986', '34032', '31564', '33369', '17153']
0 leere Dateien wurden gefunden. IDs: []
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/38157.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/38157.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/15267.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/15267.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/25157.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/25157.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/31911.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/31911.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/36310.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/36310.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/29806.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/29806.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/33317.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/33317.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/32634.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/32634.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/30005.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/30005.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/11925.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/11925.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/33330.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/33330.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/33202.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/33202.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/29780.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/29780.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/32766.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/32766.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/5740.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/5740.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/38986.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/38986.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/34032.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/34032.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/31564.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/31564.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/33369.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/33369.txt.utf-8: 404
Herunterladen der Textdatei von https://www.gutenberg.org/ebooks/17153.txt.utf-8
Fehler beim Herunterladen der Datei von URL https://www.gutenberg.org/ebooks/17153.txt.utf-8: 404
Insgesamt 0 Volltextdateien erfolgreich heruntergeladen (Anzahl Fehler: 20).
Geladene IDs: [].
IDs mit Fehlern beim Laden: ['38157', '15267', '25157', '31911', '36310', '29806', '33317', '32634', '30005', '11925', '33330', '33202', '29780', '32766', '5740', '38986', '34032', '31564', '33369', '17153']
```

It works but can be done better - check for empty file directly after loading it

---

## Comments on 03_remove-header-footer.py

Script Output
```
Skript beendet.
2435 Dateien erfolgreich bereinigt.
0 Dateien ohne gültige Start- und End-Marker. IDs: []
```

---

## Create new Solr Core
`podman-compose exec solr solr create -c pg_fulltexts`

---

## Comments on 04_create_schema.py

---

## Comments on 05_index_fulltexts.py

Script Output
```
(suma-tech) k@Ixion:~/Dev/learning/bibinfo-suchmaschinentechnologie/suma-tech-assignment-indexing-retrieval/scripts/assignment$ python 05_index_fulltexts.py 
INDEXING SOLR RECORDS...

Successfully indexed batch of 1000 records (Total so far: 1000)...
Successfully indexed batch of 1000 records (Total so far: 2000)...
Successfully indexed final batch of 435 records.
Issuing final commit to Solr...

FINISHED INDEXING RECORDS
Successfully processed: 2435
Errors encountered: 0. IDs/Batches: []
```

---

