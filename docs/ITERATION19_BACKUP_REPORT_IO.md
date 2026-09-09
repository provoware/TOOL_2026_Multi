# Iteration 19 – Backup- und Berichtsschreiber

Stand: 2026-09-09

## Ziel

Den bestehenden Restore-/Backup-Schreibweg auf denselben abgesicherten Temp-, fsync- und Replace-Vertrag wie die bereits gehärteten Produktions- und Diagnose-Schreiber bringen, ohne Append-Logs oder fachliche Restore-Regeln zu verändern.

## Befund

`scripts/iteration_restore.py` verwendete für das Backup-ZIP noch einen festen `.tmp`-Namen. Die SHA-256-Begleitdatei und der RESTORE-JSON-Bericht wurden direkt mit `Path.write_text()` geschrieben. Damit bestanden Parallelitäts- und Teilwrite-Risiken, obwohl die fachliche Restore-Prüfung selbst bereits umfassend war.

## Änderung

- Backup-ZIP verwendet eine eindeutige Tempdatei im Zielordner.
- Fertiges und bereits validiertes ZIP wird vor `os.replace()` per Datei-`fsync` synchronisiert.
- Nach dem Replace erfolgt bestmöglicher Verzeichnis-`fsync`.
- Tempdatei wird auch bei Fehlern sicher entfernt.
- SHA-256-Begleitdatei und RESTORE-JSON verwenden `app.atomic_io.atomic_write_text`.
- Backup-Dateinamen verwenden Mikrosekunden, damit schnelle Mehrfachläufe nicht kollidieren.
- ZIP-`testzip()` wird ausgewertet und meldet einen beschädigten Eintrag explizit.

## Regression

`tests/test_restore.py` ergänzt:

1. simulierter `os.replace()`-Fehler muss einen bestehenden Backup-Stand unverändert lassen und die Tempdatei entfernen,
2. erfolgreicher ZIP-Bau muss ein valides Archiv ohne verbliebene Tempdatei liefern.

## Unverändert

- Restore-Pfadprüfung gegen ZIP-Traversal,
- Manifestvergleich,
- Vollprüfung im frisch wiederhergestellten Projekt,
- Headless-Startprüfung,
- Append-only Ereignislogs,
- Nutzerdaten und Fachlogik.

## Gate

Der Branch darf erst nach erfolgreicher GitHub-Grundprüfung einschließlich `bash scripts/pruefen.sh --full` und Restore-Gate gemergt werden.
