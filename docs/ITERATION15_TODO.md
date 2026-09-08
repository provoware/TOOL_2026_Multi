# Iteration 15 – Todo-Liste

## Ziel
Eine einfache, laienfreundliche Todo-Liste mit optionalem Termin, aktivem Bestand, Abhaken und getrenntem Archiv in das bestehende PySide6-Dashboard integrieren.

## Datenmodell
Speicherort:

```text
daten/todo/todo.json
```

Die Datei enthält gemeinsam:
- `active`: noch offene Aufgaben,
- `archive`: erledigte Aufgaben.

Ein Eintrag besitzt:
- eindeutige ID,
- Titel,
- optionale Notiz,
- optionalen Termin,
- Erstellzeit,
- bei archivierten Aufgaben zusätzlich Abschlusszeit.

## Sicherheitsregel beim Abhaken
Aktiver Bestand und Archiv werden bewusst **nicht** in zwei getrennte Dateien geschrieben. Beim Abhaken wird der Eintrag innerhalb desselben Datenobjekts aus `active` nach `archive` verschoben und anschließend genau einmal atomar gespeichert.

Ablauf:
1. vorhandenen Bestand vollständig lesen und validieren,
2. Aufgabe im Arbeitsspeicher aus `active` entfernen,
3. `completed_at` setzen,
4. denselben vollständigen Eintrag nach `archive` verschieben,
5. Tempdatei schreiben,
6. `flush` + `fsync`,
7. mit `os.replace` atomar ersetzen.

Schlägt der letzte Ersetzungsschritt fehl, bleibt die vorherige Datei unverändert.

## Oberfläche
Aufruf über:

```text
Planung → Todo-Liste
```

Funktionen:
- Titel eingeben,
- optionale Notiz,
- Termin über „Termin verwenden“ aktivieren,
- Aufgabe anlegen,
- aktive Aufgaben anzeigen,
- Aufgabe auswählen und abhaken,
- Archiv in eigener Registerkarte ansehen,
- zentraler Zoom 100/125/150/175/200 %.

## Bewusste Grenzen dieser Iteration
Nicht enthalten:
- Löschen aus dem Archiv,
- Wiederherstellen archivierter Aufgaben,
- wiederkehrende Aufgaben,
- Systembenachrichtigungen bei geschlossenem Programm.

Diese Punkte würden zusätzliche Daten- oder Produktentscheidungen erfordern und gehören nicht in den Minimalumfang dieser Iteration.

## Abnahme
- leeres Projekt erzeugt beim bloßen Anzeigen keine Todo-Datei,
- Titelpflicht und Terminformat werden validiert,
- Aufgaben mit und ohne Termin sind speicherbar,
- Abhaken verschiebt vollständig ins Archiv,
- simulierter `os.replace`-Fehler erhält den alten Bestand,
- PySide6-Eingabe, Termin, Archiv und Zoom werden automatisiert geprüft,
- bestehende Referenz-, Song-, Profil-, Recovery-, Release-, Headless- und Restore-Prüfungen bleiben grün.
