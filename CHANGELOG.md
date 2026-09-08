# Änderungsverlauf

## 0.6.0 – 2026-09-08 – Debug- und Recovery-Zentrale

### Hinzugefügt
- kombinierbare Filter nach Schweregrad und Bereich,
- Ereignisdetails per Doppelklick, Enter oder Schaltfläche,
- Wiederholungszähler und dauerhaft gespeichertes erstes Auftreten,
- zentrale Zoomstufen 100/125/150/175/200 Prozent,
- standardmäßig eingeklappte technische Details,
- gefahrlose `ENOSPC`-/`EROFS`-Simulation ohne echten Datenträgerverbrauch,
- automatisierte Tk-GUI-Prüfung für Tastatur, Fokus, Detailansicht und Zoom.

### Bedienung
- `F5` aktualisiert,
- `Ctrl++` und `Ctrl+-` ändern die Anzeigegröße,
- `Ctrl+0` setzt auf 100 Prozent,
- `Escape` schließt Detailfenster,
- interaktive Filter, Tabelle und Schaltflächen sind in der Fokusreihenfolge.

### Schutz
- Schreibfehlersimulation arbeitet ausschließlich in temporären Testpfaden,
- vorhandener Bestand muss bei simuliertem Fehler unverändert bleiben,
- ohne echte Tk-Sitzung wird die GUI-Prüfung nicht als bestanden gewertet,
- vorhandene Restore-, Diagnose-, Redaktions- und Wächter-Gates bleiben aktiv.

## 0.5.0 – 2026-09-08 – Diagnose- und Logging-Härtung

### Hinzugefügt
- Größen-/Altersrotation für das Ereignislog mit maximal fünf Archiven,
- Quarantäne beschädigter JSONL-Zeilen mit bereinigter Beweiskopie,
- datenschutzgeprüftes Diagnosepaket mit SHA-256,
- eigenes `ENDE`-Ereignis bei kontrolliertem Programmabschluss,
- gezielte Tests für Rotation, Quarantäne, Diagnoseexport und normales Programmende.

### Schutz
- beschädigte Logzeilen werden nicht mehr still verworfen,
- gültige Logzeilen bleiben beim Bereinigen atomar erhalten,
- Diagnosepakete enthalten nur bereinigte Textkopien und keine unveränderten Rohprotokolle,
- Datenschutzprüfung läuft unmittelbar vor ZIP-Übernahme erneut,
- vorhandene Restore-, Headless- und Wächter-Gates bleiben aktiv.

## 0.4.0 – 2026-09-08 – Recovery-Härtung

### Hinzugefügt
- vollständige Iterations-ZIP-/Restore-Kette mit SHA-256, sicherem Entpacken, Manifestvergleich, Vollprüfung und Headless-Start,
- fensterlose Startabnahme über `python3 -m app.main --headless-check`,
- separate Prozesswache `scripts/process_watch.py`,
- zentrale Log-Bereinigung `app/redaction.py`,
- gezielte Sicherheits-, Wächter- und Restore-Tests,
- sechsten Start-Checkpoint für Prozesswache/Headless-Gate,
- CI-Restore-Gate auf jedem Push und Pull Request.

## 0.3.0 – 2026-09-08 – Regression, Start, Standards und Release
- `REG-LOG-001` behebt `recent(0)`.
- globale UI-Standards, Start-Checkpoints und manifestgesteuerter Releasefilter ergänzt.
