# FMOD Verbesserungstool

## Installation

Dieses git repo klonen und `pip install -r requirements.txt` ausführen. Nun kann man mit `python tool.py` in jedem Ordner arbeiten (bitte tool.py in den Arbeitsordner kopieren).

## Nutzung

### Setup

Das Tool benötigt 2 Ordner: `done`, `not_done`. Im `not_done` bitte sämtliche PDFs legen. Die xlsx wo die Punkte hineingehören einfach in den selben Ordner wie `tool.py` legen.

Der Ordner sollte so aussehen:

```
tool.py
ueXPunkte.xlsx
done
not_done/
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    ...
```

`tool.py` öffnen und die Aufgaben richtig in das `max_p` dictionary eintragen. Die Schlüssel sind die Aufgaben Nummer und der Wert sind die maximalen Punkte.

Anschließend einmal `python tool.py extract` ausführen um die Datei `names.txt` zu generieren wo deine Bewertungen zwischengespeichert werden bevor sie zum Schluss in die Excel-Datei kopiert werden! Falls du manuell etwas ändern musst, kannst du das in der `names.txt` machen!

## Nutzung

Mit `python tool.py show` kann man sich die noch nicht fertigen Abgaben anzeigen lassen. Wenn man `python tool.py show -d` macht, sieht man welche schon Abgaben schon fertig sind.

Um den Verbesserungsvorgang zu starten ruft man `python tool.py correct MATNR` auf. Als Ausgabe bekommt man die schon erledigten Abgaben und anschließend die derzeitige Zeile der aktuellen. Das Tool wartet nun auf eine Bewertung für die erste Aufgabe. Hier ist es nun möglich die Abgabe des/der Studenten/in in einem PDF-Editor zu annotieren und nach Verbesserung des ersten Beispiels die Punkte im Tool einzugeben:

```
MAX POINTS FOR 1 : 3
Enter Points:2
```

Und Enter drücken um die Aufforderung für das nächste Beispiel zu bekommen. Nach jeder Eingabe bekommt man auch die Übersicht der aktuellen Abgabe immer wieder ausgegeben. Falls die Aufgabe mit vollen Punkten gelöst wurde, genügt es auch einfach nur Enter zu drücken ohne eine Zahl einzugeben, es wird die maximale Punkteanzahl eingetragen.

Nachdem alle Beispiele verbessert wurden wird die Summe ausgegeben. Diese bitte in die Abgabe annotieren. Das Tool wartet nun auf eine Eingabe. Bevor diese Eingabe passiert, ist es aber nötig die PDF zu speichern und zu schließen, da das Tool als nächstes die PDF laut Schema (also mit _copy.pdf) in den done Ordner verschieben möchte.

Zum Schluss werden alle noch nicht verbesserten Abgaben ausgegeben, von denen man sich eine Matrikelnummer für die nächste Verbesserung nehmen kann.

Falls ein Fehler beim korrigieren passiert, kann man das Programm mit Ctrl+C einfach unterbrechen und mit der Abgabe von vorne anfangen.

Nachdem alle Abgaben verbessert wurden, nimmt `python tool.py to_xlsx EXCELDATEIPFAD TUTORNAME` die names.txt und trägt alle Ergebnisse *in eine Kopie der Excel Datei* die mit `_done.xlsx` endet ein. Diese liegt im selben Ordner. Es werden noch einmal alle Abgaben ausgegeben als auch ganz rechts deren Summen.

Nun ist es nur mehr nötig zu checken ob in der `ueXPunkte_done.xlsx` alles passt, diese umbenennen, in den `done` Ordner zu packen und den ganzen `done` Ordner per Lieblingsprogramm hochzuladen.