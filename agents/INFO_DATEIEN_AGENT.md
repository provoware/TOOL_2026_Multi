# INFO-DATEIEN-AGENT

## Zweck
Informationsdateien werden nur nach belegten Projektänderungen aktualisiert.

## Prüfreihenfolge
1. `MANIFEST.json` – Version, Prüfwege, Runtime-/Recovery-/Release-Dateien und neue Fachworkflows.
2. `CHANGELOG.md` – ausschließlich implementierte und geprüfte Änderungen.
3. `TODO.md` – Status nur mit Nachweis auf 🟢/BEHOBEN.
4. `README.md` – realer Start-, Prüf-, Sicherungs-, Recovery- und Arbeitsweg.
5. `ANLEITUNG_LAIEN.md` – nur nutzerrelevante Bedienänderungen.
6. `docs/` – nur fachlich betroffene Konzepte.
7. `texte/registry.json` – nur sichtbare Textänderungen.

## Zusätzliche Konsistenzprüfungen
- Neue Runtime-Dateien müssen im Manifest stehen und ihre `release`-Entscheidung begründen.
- Laufzeitdaten wie `daten/songtexte/` oder `Entwicklerinformation.txt` werden nicht als Quell-/Release-Dateien behandelt und niemals durch Doku- oder Releaseaufgaben überschrieben.
- Neue Speicherfunktionen müssen ihre Datenpfade, Überschreibungsregeln und Rückfalltests dokumentieren.
- Autosave darf erst als 🟢 gelten, wenn Zeitintervall sowie Fokus-/Schließweg automatisch geprüft sind.
- Neue Restore-/Wächter-/Datenschutzfunktionen dürfen erst als 🟢 dokumentiert werden, wenn der passende automatisierte Test bestanden hat.
- Ein Restore-Status `OK` ist nur zulässig nach SHA-256, neuem Restore-Ordner, Manifestvergleich, Vollprüfung und Headless-Start.
- Keine Datei nur wegen Datumswechsel ändern.
- Keine erfundenen Erfolge oder nicht ausgeführten Tests eintragen.
