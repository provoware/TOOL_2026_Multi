# Fehler- und Rückfallmanagement

Version 1.0 · 2026-09-08

## Vier Schutzschichten

### 1. Fehlerprävention
- Eingaben vor Verwendung prüfen.
- Dateien zuerst in temporäre Ziele schreiben und erst nach erfolgreicher Prüfung austauschen.
- Nutzerdaten nie still überschreiben.
- Zeitabbruch und Wiederholungsgrenzen bei externen Vorgängen.
- Vor zerstörerischen Aktionen Sicherung oder Rücknahmeweg verlangen.

### 2. Fehler abfangen
- erwartbare Ausnahmen an sinnvollen Grenzen behandeln,
- unerwartete Ausnahmen zentral erfassen,
- Fehler nicht verschlucken,
- Anwendung wenn möglich in sicheren Zustand zurückführen.

### 3. Fehlertoleranz
- nicht betroffene Funktionen möglichst nutzbar lassen,
- Teilfehler kenntlich machen,
- beschädigte Einzelaufgabe abbrechen statt Gesamtbestand zu gefährden,
- bei unklarer Datenlage lieber sicher stoppen.

### 4. Rückfallmanagement
Für jeden bestätigten, wiederholbaren Fehler:
1. Ereigniskennung vergeben.
2. Ursache dokumentieren.
3. minimalen Fehlerfall festhalten.
4. Korrektur umsetzen.
5. Test hinzufügen, der vor der Korrektur fehlschlug und danach besteht.
6. angrenzende Risiken prüfen.
7. Ergebnis im Änderungsverlauf dokumentieren.

## Ereigniskennung

Schema: `BEREICH-ART-LAUFNUMMER`, zum Beispiel `START-FEHLER-001`.

## Menschlicher Bericht

Jeder relevante Bericht soll enthalten:
- WAS IST PASSIERT?
- WIE WURDE ES ERKANNT?
- WO IST ES PASSIERT?
- WAS IST GESCHÜTZT WORDEN?
- WAHRSCHEINLICHER GRUND
- LÖSUNGSMÖGLICHKEITEN
- TECHNISCHE DETAILS

Zusätzlich wird dasselbe Ereignis maschinenlesbar als eine JSON-Zeile gespeichert.

## Bericht beim Programmende

Sobald die erste echte Anwendung vorhanden ist, wird ein zentraler Abschlusswächter eingebunden. Er erzeugt bei normalem Beenden, abgefangenen Fehlern und soweit technisch möglich bei erkannten harten Abbrüchen einen TXT-Bericht und versucht ihn nach Programmende zu öffnen. Ein harter Prozessabbruch kann nicht innerhalb desselben abgestürzten Prozesses garantiert behandelt werden; dafür ist bei Bedarf ein separater Wächterprozess vorgesehen.
