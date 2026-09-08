# Änderungsverlauf

## 0.9.0 – 2026-09-08 – Songbibliothek vervollständigt

### Hinzugefügt
- freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags,
- kombinierbare Filter nach Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten,
- Favoritenkennzeichnung im Editor und Favoritenfilter in der Bibliothek,
- Bearbeitungsstatus `Idee`, `Entwurf`, `Überarbeitung`, `Fertig`,
- Sortierung nach letzter Bearbeitung, Titel, Genre, Tags und Status,
- Gruppierung nach Genre, Tags und Status,
- Versionswiederherstellung aus der schreibgeschützten Vorschau heraus,
- gezielte Logik- und Tk-GUI-Tests für Suche, Filter, Gruppierung, Status/Favorit und Restore.

### Schutz
- ältere Songdateien ohne Status/Favorit bleiben lesbar und erhalten nur sichere Standardwerte,
- Filtern, Sortieren und Gruppieren sind reine Ansichtsoperationen,
- vor jeder tatsächlichen Versionswiederherstellung wird der aktuelle Song erneut als Versionsstand gesichert,
- die Restore-Funktion akzeptiert nur die direkte Arbeitsdatei und den zugehörigen `.versionen/<Titel>/`-Pfad,
- fremde Versionspfade werden vor Schreibzugriff abgewiesen,
- Arbeitsdatei und Sicherungsstand werden atomar geschrieben,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.8.0 – 2026-09-08 – Songbibliothek und Versionsverwaltung

### Hinzugefügt
- Songbibliothek mit Titel, Genre, letzter Bearbeitung und Versionsanzahl,
- direktes Öffnen vorhandener Songs per Doppelklick, Enter oder Schaltfläche,
- bis zu fünf zuletzt bearbeitete Songs als Schnellkacheln im Dashboard,
- Song-Metadaten Stimmung, Stil, Stimme, Besonderheiten und Tags,
- automatische Versionsschnappschüsse vor geänderten Überschreibungen,
- schreibgeschützte Vorschau älterer Versionsstände,
- Exporte als TXT, Markdown, JSON und Nur-Songtext-TXT,
- Rückwärtslesen der bisherigen 0.7.0-Textdateien,
- gezielte Logik- und Tk-GUI-Tests für Bibliothek, Metadaten, Versionen, Kacheln und Exporte.

### Schutz
- das bestehende `.txt`-Arbeitsformat bleibt kanonisch; kein paralleles internes Songformat,
- identische Speicherungen erzeugen keinen Versionsmüll,
- Versionsstände werden getrennt unter `.versionen/` gesichert und nicht still überschrieben,
- Versionsansicht ist zunächst schreibgeschützt,
- Exporte verändern weder Arbeitsdatei noch Versionshistorie,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.7.0 – 2026-09-08 – Dashboard-Schnellspeicher und Songtexteditor

### Hinzugefügt
- einzeilige Entwickler-Schnelleingabe im Dashboardheader mit Enter- und Schaltflächenbestätigung,
- append-only Speicherung mit Zeitstempel in `Entwicklerinformation.txt`,
- Songtexteditor mit Titel, optionalem Genre, optionalem Sonstiges und Live-Vorschau,
- auswählbare Bereiche Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken und Instrumental,
- atomare Speicherung unter `daten/songtexte/<Titel>.txt`,
- Autosave alle fünf Minuten sowie bei Fokusverlust und beim Schließen,
- Logout-Schaltfläche mit Speichern aller offenen Songeditoren vor Sitzungsende,
- gezielte Logik- und Tk-GUI-Tests für Schnelleingabe, Speicherpfad, Bereichswechsel, Autosave und Logout.

### Schutz
- Schnellinfos überschreiben vorhandene Informationen nicht,
- Songdateien werden über eine temporäre Datei atomar ersetzt,
- ein Titelwechsel löscht keinen vorherigen Songstand,
- Logout wird gestoppt, wenn ein offener Songtext nicht gespeichert werden kann,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

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
