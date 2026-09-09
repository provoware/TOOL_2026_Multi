# Iteration 26 – Release- und Bericht-I/O-Härtung

## Hauptziel

Vor dem nächsten vollständigen Projekt-ZIP werden die verbliebenen **nicht-append** Schreibwege für Status-, Bericht-, Diagnose- und Release-Dateien auf denselben zentralen atomaren Schutzvertrag gebracht. Append-only-Ereignislogs bleiben bewusst Append-only.

## Befund

Die fachlichen Nutzerdatenpfade für Songs, Profile, Todos und Kalender verwenden bereits `app.atomic_io`. Beim vollständigen Audit blieben jedoch mehrere eigene Schreibimplementierungen übrig:

- Log-Quarantäne und bereinigtes JSONL in `app/log_maintenance.py`,
- Rückfall-Lernstatus in `app/regression.py`,
- menschenlesbare Ereignisberichte in `app/event_log.py`,
- Wächter-Absturzberichte in `scripts/process_watch.py`,
- Startstatus in `scripts/start_status.py`,
- Kubuntu-Abnahmeberichte in `scripts/kubuntu_abnahme.py`,
- Release-ZIP und Release-SHA in `scripts/veroeffentlichen.py`.

Zusätzlich hatten direkt gestartete Skripte, die nun `app.atomic_io` verwenden, keinen einheitlich abgesicherten Projekt-Importpfad. `scripts/diagnosepaket.py` besaß zudem eine eigene, funktional ähnliche ZIP-Publish-Implementierung.

## Ursächliche Lösung

`app.atomic_io` erhält mit `atomic_publish_file()` einen zentralen Publish-Schritt für bereits fertig erzeugte Dateien im selben Zielordner. Er führt Datei-`fsync`, atomaren `os.replace`, bestmöglichen Verzeichnis-`fsync` und Temp-Cleanup aus. `atomic_write_text()` verwendet diesen Publish-Schritt ebenfalls.

Die verbliebenen nicht-append Text-/JSON-Berichte und Statusdateien werden über `atomic_write_text()` geschrieben. Release- und Diagnose-ZIPs werden vor dem Publish validiert und anschließend über `atomic_publish_file()` veröffentlicht. Der Release-Schreiber verwendet eindeutige Tempdateien statt eines festen `.zip.tmp`-Namens; seine SHA-256-Begleitdatei wird atomar geschrieben.

Direkt startbare Skripte ergänzen ihren Projektroot kontrolliert in `sys.path`, bevor sie `app.*` importieren. Das schützt insbesondere die real verwendeten Aufrufe `python3 scripts/start_status.py`, `python3 scripts/kubuntu_abnahme.py`, `python3 scripts/diagnosepaket.py` und `python3 scripts/veroeffentlichen.py`.

Der bereits gehärtete Restore-ZIP-Pfad bleibt unverändert: Er besitzt schon eindeutige Tempdatei, Datei-/Verzeichnis-Synchronisation, atomaren Replace, Cleanup und eine gezielte Replace-Fehlerregression. Eine unnötige Umstellung würde keinen zusätzlichen Schutz erzeugen.

## Bewusst unverändert

- `logs/ereignisse.jsonl` bleibt Append-only.
- `Entwicklerinformation.txt` / Projekt-Notiz bleibt Append-only und `fsync`-gesichert.
- Logrotation verschiebt abgeschlossene Logs weiterhin per atomarem Rename und begrenzt Archive bewusst durch Entfernen alter Logarchive.
- Song-, Profil-, Todo- und Kalenderdatenformate bleiben unverändert.
- Backup-/Restore-Fachlogik und reale Kubuntu-Sichtabnahme werden nicht inhaltlich erweitert.

## Regression

Die automatische Prüfung deckt zusätzlich ab:

- Replace-Fehler bei Log-Quarantäne erhält den ursprünglichen Logbestand und hinterlässt keine Tempdatei,
- Diagnose-Skript ist direkt startbar und Diagnose-Publish-Fehler hinterlässt kein Teil-ZIP,
- Release-Replace-Fehler erhält ein bestehendes Release-ZIP, räumt Tempdateien auf und erzeugt keine falsche SHA-Datei,
- direkte Aufrufe von Startstatus, Prozesswächter und Kubuntu-Abnahme können Projektmodule importieren,
- `app/laptop_layout.py` ist jetzt ausdrücklich Bestandteil der Runtime-Dateiprüfung,
- Iterationsdokumente 22–26 werden in der Vollprüfung ausdrücklich auf Vorhandensein geprüft.

## Schutz

Keine Nutzerdatenmigration. Keine Produktfunktion. Keine neue Abhängigkeit. Alle Änderungen sind Git-reversibel. Fehlerprüfungen arbeiten mit temporären Testbeständen.

## Abnahme

### Technische Nullrunde

GitHub-Grundprüfung **#503** war vollständig erfolgreich:

- 81 Logik-/Regressionstests: `OK`,
- 52 PySide6-GUI-Tests: `OK`,
- Release-Manifest: 37 freigegebene Betriebsdateien,
- Schreibfehlersimulation: `OK`,
- Headless-Start: `OK`,
- Vollprojekt-Restore: `OK`,
- Restore-SHA-256: `c7ff7f7e107d815918e9d52a84302bd245baa19f301cb3d4730ee5acff4b0806`.

### Finaler Version-/Evidence-Head

Nach Synchronisierung auf Version **0.15.2** wurde der finale PR-Head `d386f9e848237ff400fc60c518f73645b6516cee` erneut von Null geprüft. GitHub-Grundprüfung **#513** war vollständig erfolgreich:

- 81 Logik-/Regressionstests: `OK`,
- 52 PySide6-GUI-Tests: `OK`,
- Release-Manifest: 37 freigegebene Betriebsdateien,
- Headless-Start: `OK`,
- Vollprojekt-Restore: `OK`,
- finale Restore-SHA-256: `560b9d9ca46ec3e0964f03b385941782e18e892d734c1b5e208dd69c6d4b5bf3`.

PR **#31** wurde anschließend ausschließlich für genau diesen geprüften Head per SHA-geschütztem Squash-Merge übernommen. Resultierender `main`-Commit: `00513bbaaee124da1e04a963aa70ce9e4757108e`.

Die nachfolgende Status-Synchronisierung verändert ausschließlich Projektmetadaten und Dokumentation; keine Produktions-, Nutzerdaten-, Backup- oder Restore-Logik.

**Status:** 🟢 technischer Patch vollständig geprüft und sicher in `main` übernommen; Status-Sync separat final zu prüfen.
