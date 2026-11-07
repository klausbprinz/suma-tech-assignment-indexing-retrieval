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

    num_of_downloads = 0
    num_of_errors = 0

    print(f"Verarbeite Datei {EBOOK_ID_PATH}")


    with open(EBOOK_ID_PATH, "r", encoding="utf-8") as file:
        for ebookid in file:
            ebookid = ebookid.strip()   # get rid of "\n"     
            url = f"https://www.gutenberg.org/ebooks/{ebookid}.txt.utf-8"
            print(f"Herunterladen der Textdatei von {url}")
            output_file = FULLTEXT_PATH / f"{ebookid}.txt"
            if download_file(url, output_file):
                num_of_downloads += 1
            else:
                num_of_errors += 1

    print(f"Insgesamt {num_of_downloads} Volltextdateien erfolgreich heruntergeladen (Anzahl Fehler: {num_of_errors}).")