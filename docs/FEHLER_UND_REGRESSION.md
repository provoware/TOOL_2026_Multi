# Fehler- und Rückfallmanagement

Version 1.1 · 2026-09-08

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

Zusätzlich wird dasselbe Ereignis maschinenlesbar als eine JSON-Zeile in `logs/ereignisse.jsonl` gespeichert. Die Anwendung ignoriert beim Lesen einzelne beschädigte Zeilen, damit ältere brauchbare Ereignisse sichtbar bleiben.

## Mitlernende Rückfallerkennung

`app/regression.py` bildet aus Bereich, Ausnahmeart und vereinfachter Ursache eine gekürzte Prüfsumme. Dadurch erkennt das Werkzeug wiederkehrende technische Muster, ohne den vollständigen Fehlertext in der Lernhistorie zu speichern. Zähler und letzter Zeitpunkt liegen atomar geschrieben in `logs/rueckfaelle.json`. Ab dem zweiten Auftreten ergänzt das Werkzeug einen Präventionshinweis. Das ist bewusst regelbasiert und nachvollziehbar; es verändert weder Programmcode noch Nutzerdaten selbstständig.

## Bericht beim Programmende

Der Programmeinstieg und die Tkinter-Oberfläche besitzen zentrale Ausnahmegrenzen. Abgefangene Fehler erzeugen JSONL- und TXT-Berichte und lassen nicht betroffene Oberflächenbereiche möglichst verfügbar. Ein harter Prozessabbruch kann nicht innerhalb desselben abgestürzten Prozesses garantiert behandelt werden; ein separater Wächterprozess bleibt deshalb eine spätere Erweiterung.

### 8. Einheitlicher Lebenszyklus

Ein erstmals erkanntes Fehlermuster ist `OFFEN`, ab der Wiederholung `BEOBACHTET`. `BEHOBEN` darf erst gesetzt werden, wenn eine dauerhafte Rückfalltest-Kennung im Format `REG-…` zugeordnet und die Prüfung erfolgreich ausgeführt wurde. Diese Iteration erfasst Status und Testkennung; das sichere Abschließen bestätigter Fehler bleibt offen, bis ein echter behobener Fehler vorliegt.
