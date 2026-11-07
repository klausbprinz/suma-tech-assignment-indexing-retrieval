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

```