# Iteration 16 – Kalender

## Ziel
Einen laienfreundlichen Kalender mit echten Tages-, Wochen-, Monats- und Jahresbereichen, Termineingabe und Erinnerung während des laufenden Provoware-Dashboards umsetzen.

## Daten
Speicherort:

```text
daten/kalender/termine.json
```

Ein Termin besitzt:
- eindeutige ID,
- Titel,
- optionale Notiz,
- Beginn,
- Ende,
- optionalen Erinnerungsabstand,
- Erstellzeit,
- Zeitpunkt der bereits angezeigten Erinnerung.

Beginn und Ende verwenden bewusst die **lokale Rechnerzeit**. Es wird keine Zeitzone erfunden oder still umgerechnet.

## Vier Ansichten
Die Ansichten sind echte Zeitbereiche und nicht nur verschiedene Beschriftungen:
- **Tag:** 00:00 bis zum nächsten Tag 00:00,
- **Woche:** Montag 00:00 bis zum folgenden Montag,
- **Monat:** erster Tag bis zum ersten Tag des Folgemonats,
- **Jahr:** 1. Januar bis 1. Januar des Folgejahres.

Ein Termin, der einen Bereich überlappt, wird dort angezeigt. Dadurch bleibt z. B. ein Termin über Mitternacht an beiden betroffenen Tagen sichtbar.

## Termine anlegen
Eingaben:
- Titel,
- optionale Notiz,
- Beginn,
- Ende,
- Erinnerung: keine, zum Beginn, 5/15/30/60 Minuten oder 1 Tag vorher.

Das Ende muss nach dem Beginn liegen. Ungültige Eingaben werden vor dem Schreiben abgewiesen.

## Erinnerungen
`CalendarReminderController` läuft als Kind des Dashboards alle 30 Sekunden. Deshalb funktioniert die Prüfung auch dann weiter, wenn das Kalenderfenster geschlossen ist, solange das Dashboard selbst läuft.

Ablauf:
1. fällige, noch nicht bestätigte Erinnerung bestimmen,
2. Meldung anzeigen,
3. erst nach Rückkehr aus der Meldung `reminded_at` atomar speichern.

Ein Schutz gegen Wiedereintritt verhindert, dass derselbe Timer während einer geöffneten Meldung dieselbe Erinnerung erneut startet.

### Bewusste Grenze
Wenn das gesamte Provoware-Dashboard beendet ist, läuft **kein** separater Linux-Hintergrunddienst. Erinnerungen bei vollständig geschlossenem Programm sind damit nicht Bestandteil dieser Iteration.

## Datensicherheit
Kalenderdaten werden über Tempdatei, `flush`, `fsync` und `os.replace` atomar ersetzt. Ein simulierter Fehler beim letzten Ersetzungsschritt muss den vorherigen Bestand unverändert lassen.

In dieser Iteration gibt es absichtlich **keine Termin-Löschfunktion**. Damit wird kein destruktiver Nebenweg eingeführt, den der Auftrag nicht verlangt.

## Abnahme
- leeres Projekt schreibt beim bloßen Lesen keine Kalenderdatei,
- Titel/Start/Ende werden validiert,
- Tag/Woche/Monat/Jahr besitzen korrekte Grenzen,
- Mehrtagestermine erscheinen in überlappenden Bereichen,
- Erinnerungen sind einmalig und werden erst nach Anzeige markiert,
- Erinnerungsprüfung funktioniert im Dashboard auch ohne geöffnetes Kalenderfenster,
- PySide6-Kalender folgt dem zentralen Zoom,
- bestehende Todo-, Profil-, Song-, Recovery-, Referenz-, Release-, Headless- und Restore-Gates bleiben grün.
