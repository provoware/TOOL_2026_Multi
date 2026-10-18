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


## Ergänzung aus Review 18.10.2026

- Informationen mit dem geplanten Code gemeinsam fertigstellen; Ergebnisse des danach laufenden CI in Artefakten und PR-Beschreibung ergänzen statt durch einen weiteren Evidenz-Commit erneut CI auszulösen.
- Prüfkandidat, hochgeladen, geprüft, gemergt und veröffentlicht ausdrücklich unterscheiden. Ein offener PR ist keine Änderung auf main.
- Historische Testzahlen immer mit zugehörigem SHA / Lauf nennen. Die 196/151 Tests des früheren lokalen Gesamtstands sind nicht die 188/144 Tests des isolierten GitHub-Stands.
- Qualitative Aussagen mit konkreten Beobachtungen begründen. Zwei PR-Läufe sind keine Zehn-main-Läufe-Vergleichsreihe; Cachetreffer sind keine gemessene Byteersparnis.
- Konzepte wie zusätzliche Leistungsdiagnose als geplant kennzeichnen. Keine erfundenen Messwerte, Prozentwerte, Fehlerquoten oder automatisch aktiven Funktionen eintragen.
