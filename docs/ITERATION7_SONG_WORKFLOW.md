# Iteration 7 – Dashboard-Schnellspeicher und Songtexteditor

## Ziel
Ersten produktiven Fachworkflow ergänzen, ohne Recovery-/Diagnosebasis umzubauen.

## Dashboard-Schnellinfo
- einzeilige Eingabe im Header,
- Bestätigung mit Enter oder Schaltfläche,
- append-only mit lokalem ISO-Zeitstempel,
- Zieldatei `Entwicklerinformation.txt`,
- leerer Inhalt wird nicht geschrieben.

## Songtexteditor
- eigener Editor als separates Fenster,
- Titel bestimmt den Dateinamen,
- Genre und Sonstiges optional,
- Bereiche: Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken, Instrumental,
- beliebig mehrere Bereiche möglich,
- fortlaufende Vorschau.

## Speicherung
- Ziel: `daten/songtexte/<Titel>.txt`,
- Dateiname wird gegen Pfadbestandteile bereinigt,
- atomarer Write über `.tmp` + `os.replace`,
- Titelwechsel löscht keinen alten Stand,
- Autosave alle 300 Sekunden,
- Save bei Fokusverlust, `Ctrl+S`, Editor-Schließen und Logout.

## Logout
Logout bedeutet in diesem Stand „Sitzung speichern und Anwendung beenden“. Es existiert noch keine Benutzer-/Loginverwaltung. Kann mindestens ein offener Songtext nicht gespeichert werden, bleibt die Anwendung geöffnet.

## Abnahme
- Logiktest für Append, Dateinamen, Rendern und atomare Songdatei,
- Tk-Test für Dashboardheader, Vorschau, Autosave-Intervall, Fokus-Saves, Bereichswechsel und Logout-Protokoll,
- bestehende Recovery-, Diagnose-, Release-, Headless- und Restore-Gates bleiben Teil der Vollprüfung.
