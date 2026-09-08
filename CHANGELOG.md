# Änderungsverlauf

## 0.10.0 – 2026-09-08 – PySide6-Referenzdashboard

### Geändert
- gesamte produktive Oberfläche einheitlich auf **PySide6 6.11.2** migriert,
- Dashboardtitel auf `Provoware-Datenbank-Dashboard 2026` gesetzt,
- Dashboard nach dem bereitgestellten Dark-Orange-Referenzentwurf neu strukturiert: kompakter Header, Schnellkachelleiste, einklappbare linke Navigation, schmale Zeile „Zuletzt bearbeitet“, 2×2-Hauptkarten und Statusleiste,
- zentrale Qt/QSS-Standards für Farben, Abstände, Schriftgrößen, Fokus und Zoom eingeführt,
- Songeditor, Songbibliothek, Recovery-Zentrale und grafische Startanzeige auf PySide6 umgestellt,
- Recovery aus der Dashboard-Hauptfläche entfernt und als einzelner Navigationspunkt `Werkzeug → Recovery` geführt,
- GitHub-CI auf Qt-Offscreen-Prüfung und die für PySide6 benötigte `libegl1`-Systembibliothek umgestellt.

### Schutz
- bestehendes Song-Textformat und alle Nutzerdatenpfade bleiben unverändert,
- Autosave, Fokusverlust-Speicherung, Versionierung, Restore-Sicherung, Favoriten/Status, Metadaten und Exporte bleiben erhalten,
- geplante noch nicht freigegebene Dashboardbereiche verändern keine Daten,
- zusätzlicher Referenzlayout-Test prüft Kartenstruktur/-proportionen, Sidebarbreiten, Schnellkacheln, Dark-Orange-Akzent und exakt einen Recovery-Eintrag,
- produktive GUI-Dateien werden auf unerlaubte Tkinter-Reste geprüft,
- bestehende Logik-, Sicherheits-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Gates bleiben verbindlich.

## 0.9.1 – 2026-09-08 – CI-Wartung

### Geändert
- GitHub Actions Checkout von `actions/checkout@v4` auf `actions/checkout@v7.0.1` aktualisiert.

### Schutz
- keine fachliche Funktion, Songdatei oder Laufzeitlogik verändert,
- vollständige bestehende Logik-, Tk-GUI-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Prüfung bleibt unverändert verbindlich.

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
