# INFO-DATEIEN-AGENT

## Zweck
Informationsdateien werden nur nach belegten Projektänderungen aktualisiert.

## Prüfreihenfolge
1. `MANIFEST.json` – Version, Prüfwege, Runtime-/Recovery-/Release-Dateien.
2. `CHANGELOG.md` – ausschließlich implementierte und geprüfte Änderungen.
3. `TODO.md` – Status nur mit Nachweis auf 🟢/BEHOBEN.
4. `README.md` – realer Start-, Prüf-, Sicherungs- und Recovery-Weg.
5. `ANLEITUNG_LAIEN.md` – nur nutzerrelevante Bedienänderungen.
6. `docs/` – nur fachlich betroffene Konzepte.
7. `texte/registry.json` – nur sichtbare Textänderungen.

## Zusätzliche Konsistenzprüfungen
- Neue Runtime-Dateien müssen im Manifest stehen und ihre `release`-Entscheidung begründen.
- Neue Restore-/Wächter-/Datenschutzfunktionen dürfen erst als 🟢 dokumentiert werden, wenn der passende automatisierte Test bestanden hat.
- Ein Restore-Status `OK` ist nur zulässig nach SHA-256, neuem Restore-Ordner, Manifestvergleich, Vollprüfung und Headless-Start.
- Keine Datei nur wegen Datumswechsel ändern.
- Keine erfundenen Erfolge oder nicht ausgeführten Tests eintragen.
