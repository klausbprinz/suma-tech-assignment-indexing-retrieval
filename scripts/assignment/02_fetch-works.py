import requests
import re
import os
import time

from pathlib import Path

repoP = Path.cwd().parent.parent

EBOOK_ID_PATH = repoP / "data/assignment-data/ebook_ids.txt"
FULLTEXT_PATH = repoP / "data/assignment-data/fulltexts"

FULLTEXT_PATH.mkdir(exist_ok=True)

def download_file(url, filename):
    """
    Lädt eine UTF-8-codierte Textdatei von der angegebenen URL herunter und speichert sie als UTF-8-codierte Textdatei
    unter dem angegebenen Namen im lokalen Dateisystem. Bei der Textdatei handelt es sich um den Volltext eines
    E-Books aus dem Project Gutenberg. Die Funktion wartet zufällig zwischen 0.5 und 2 Sekunden, bevor sie die Datei
    von der angegebenen URL herunterlädt, um den Webserver von Project Gutenberg nicht zu überlasten.

    Parameter:
    - url (str): URL der Textdatei, die vom Project Gutenberg heruntergeladen werden soll.
    - filename (str): Der Name der lokal abzuspeichernden Datei.
    """

    # zwischen 0.5 und 2 Sekunden zufällig warten
    time.sleep(0.5 + 1.5 * (os.urandom(1)[0] / 255))

    response = requests.get(url, timeout=60, stream=True)
    response.encoding = 'utf-8'
    if response.status_code == requests.codes.ok:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Datei erfolgreich heruntergeladen und gespeichert unter {filename}")
        return True

    print(f"Fehler beim Herunterladen der Datei von URL {url}: {response.status_code}")
    return False

if __name__ == "__main__":
    
    if not EBOOK_ID_PATH.exists():
        print(f"Die Datei 'ebook_ids' wurde nicht gefunden. Bitte passen Sie den Pfad an.")
        exit(1)

    overallFilesToLoad = []

    filesAlreadyLoaded = []
    filesNotLoaded = []

    filesEmpty = []

    filesLoadedNew = []
    filesErrorsNew = []

    num_of_downloads = 0
    num_of_errors = 0

    print(f"Verarbeite Datei {EBOOK_ID_PATH}. Lade E-Book-IDs.")


    with open(EBOOK_ID_PATH, "r", encoding="utf-8") as file:
        overallFilesToLoad = [line.strip() for line in file if line.strip()]

    print(f"Insgesamt {len(overallFilesToLoad)} E-Book-IDs gefunden.")

    # print("Checke, welche schon geladen wurden (Datei vorhanden).")

    filesAlreadyLoaded = [file.stem for file in FULLTEXT_PATH.glob("*.txt") if not file.name.endswith("_filtered.txt")]

    print(f"{len(filesAlreadyLoaded)} Dateien wurden bereits geladen.")

    # print("Checke, welche noch nicht geladen wurden (Datei nicht vorhanden).")

    filesNotLoaded = list(set(overallFilesToLoad) - set(filesAlreadyLoaded))

    print(f"{len(filesNotLoaded)} E-Book-ID(s) wurden noch nicht geladen. IDs: {filesNotLoaded}")

    # print("Checke, ob geladene Dateien leer sind.")

    # this is slow!
    # for ebookFile in FULLTEXT_PATH.glob("*.txt"):
    #     with open(ebookFile) as ef:
    #         if not ef.read():
    #             filesEmpty.append(ebookFile.name.replace(".txt", ""))

    # for a faster way:
    for ebookFile in FULLTEXT_PATH.glob("*.txt"):
        if ebookFile.stat().st_size == 0:       # fetch metadata about file and read relevant property
            filesEmpty.append(ebookFile.stem)

    print(f"{len(filesEmpty)} leere Dateien wurden gefunden. IDs: {filesEmpty}")

    filesNotLoaded.extend(filesEmpty)

    # load missing
    for ebookid in filesNotLoaded:
  
        url = f"https://www.gutenberg.org/ebooks/{ebookid}.txt.utf-8"
        print(f"Herunterladen der Textdatei von {url}")
        output_file = FULLTEXT_PATH / f"{ebookid}.txt"
        if download_file(url, output_file):
            num_of_downloads += 1
            filesLoadedNew.append(ebookid)
        else:
            num_of_errors += 1
            filesErrorsNew.append(ebookid)

    print(f"Insgesamt {num_of_downloads} Volltextdateien erfolgreich heruntergeladen (Anzahl Fehler: {num_of_errors}).")
    print(f"Geladene IDs: {filesLoadedNew}.")
    print(f"IDs mit Fehlern beim Laden: {filesErrorsNew}")