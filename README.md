# FMOD Verbesserungstool

## Installation

Das tool lässt sich über pip für Python >3.7.1<=3.9 mit `pip install fmod_tool` installieren.

### DEV

Dieses git repo klonen und `poetry install` ausführen (poetry nötig). Nun kann man mit `tool` in jedem Ordner arbeiten
und weiter am Projekt arbeiten.

## Nutzung

### Setup

Das Tool benötigt 2 Ordner: `done`, `not_done`. Im `not_done` bitte sämtliche PDFs legen. Die Excel Datei sollte nicht
im `not_done` Ordner sein, verursacht aber keine Probleme.

Der Ordner sollte so aussehen:

```
ueXPunkte.xlsx
done
not_done/
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    3128481VornameNachname.pdf
    ...
```

Nach dem ersten mal ausführen von `tool` wird eine `settings.yml` erstellt. Diese bitte öffnen und bearbeiten
(Punkte eintragen und Präfenz für Abschluss nach Korrektur festlegen).

Anschließend einmal `tool extract` ausführen um die Datei `names.txt` zu generieren wo deine Bewertungen
zwischengespeichert werden bevor sie zum Schluss in die Excel-Datei kopiert werden! Falls du manuell etwas ändern musst,
kannst du das in der `names.txt` machen!

## Nutzung

Mit `tool show` kann man sich die noch nicht fertigen Abgaben anzeigen lassen. Wenn man `tool show -d` macht, sieht man
welche schon Abgaben schon fertig sind.

Um den Verbesserungsvorgang zu starten ruft man `tool correct MATNR` auf. Als Ausgabe bekommt man die schon erledigten
Abgaben und anschließend die derzeitige Zeile der aktuellen. Das Tool wartet nun auf eine Bewertung für die erste
Aufgabe. Hier ist es nun möglich die Abgabe des/der Studenten/in in einem PDF-Editor zu annotieren und nach Verbesserung
des ersten Beispiels die Punkte im Tool einzugeben:

```
MAX POINTS FOR 1 : 3
Enter Points:2
```

Und Enter drücken um die Aufforderung für das nächste Beispiel zu bekommen. Nach jeder Eingabe bekommt man auch die
Übersicht der aktuellen Abgabe immer wieder ausgegeben. Falls die Aufgabe mit vollen Punkten gelöst wurde, genügt es
auch einfach nur Enter zu drücken ohne eine Zahl einzugeben, es wird die maximale Punkteanzahl eingetragen.

Nachdem alle Beispiele verbessert wurden wird die Summe ausgegeben. Diese bitte in die Abgabe annotieren und die PDF
speichern (oder eine Kopie in `done` speichern). Das Tool wartet nun auf eine Eingabe. Nachdem Eingabe gedrückt wird,
geschieht jetzt das was in `settings.yml` gewählt wurde:

- "NOTHING": Die Original PDF bleibt im `not_done` Ordner (schlecht, da das `show` command damit durcheinander kommt)
- "REMOVE": Die Original PDF wird aus dem `not_done` Ordner gelöscht (standard, somit wird `show` richtig berechnet).
  Diese Option nutzen, falls man die PDF nicht in-place editiert und stattdessen die Kopie selbst in `done` speichert.
- "RENAME": Die Original PDF wird aus `not_done` nach `done` verschoben und ein `_copy.pdf` wird angehangen
  Diese Option nutzen, falls man die PDF in-place verändert und das Original nun die Annotationen hat.

Zum Schluss werden alle noch nicht verbesserten Abgaben ausgegeben, von denen man sich eine Matrikelnummer für die
nächste Verbesserung nehmen kann.

Falls ein Fehler beim korrigieren passiert, kann man das Programm mit Ctrl+C einfach unterbrechen und mit der Abgabe von
vorne anfangen.

Nachdem alle Abgaben verbessert wurden, nimmt `tool to_xlsx EXCELDATEIPFAD TUTORNAME` die names.txt und trägt
alle Ergebnisse *in eine Kopie der Excel Datei* die mit `_done.xlsx` endet ein. Diese liegt im selben Ordner. Es werden
noch einmal alle Abgaben ausgegeben als auch ganz rechts deren Summen.

Nun ist es nur mehr nötig zu checken ob in der `ueXPunkte_done.xlsx` alles passt, diese umbenennen, in den `done` Ordner
zu packen und den ganzen `done` Ordner per Lieblingsprogramm hochzuladen.

### Anmerkungen

Für jedes Kommando gibt es eine kurze Help die man mit sich anzeigen lassen kann indem man `--help` anhängt.

Jede/r ist eingeladen am Projekt zu helfen indem er/sie das Projekt auf Github forked und Vorschläge auf dem Fork macht.
Anschließend per Pull Request diese Änderungen vorschlagen! Danke vielmals für jegliche Hilfe.

Bei Fragen oder Bugs im Repo ein Ticket öffnen oder mir eine Email schreiben!