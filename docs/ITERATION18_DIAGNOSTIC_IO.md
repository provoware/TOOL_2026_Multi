# Iteration 18 – Diagnose-I/O-Konsistenz

Stand: 2026-09-09

## Ziel
Den Diagnoseexport auf dieselben sicheren Temp-/fsync-/Replace-Regeln wie die produktiven Schreibwege bringen, ohne Append-Logs umzubauen.

## Umsetzung
- Diagnose-ZIP erhält einen eindeutigen temporären Dateinamen im Zielordner.
- Das vollständig geschriebene ZIP wird vor Veröffentlichung per `fsync` synchronisiert.
- Veröffentlichung erfolgt erst danach per atomarem `os.replace` mit bestmöglichem Verzeichnis-`fsync`.
- Tempdateien werden auch bei Replace-Fehlern entfernt.
- Die SHA-256-Datei nutzt `app.atomic_io.atomic_write_text` statt direktem `write_text`.
- Der Diagnose-Dateiname enthält Mikrosekunden, damit schnelle aufeinanderfolgende Exporte nicht denselben Zielnamen verwenden.

## Regression
`tests/test_diagnostics_logging.py` prüft zusätzlich:
1. zwei unmittelbar aufeinanderfolgende Diagnoseexporte erhalten verschiedene Dateinamen;
2. ein simulierter Replace-Fehler hinterlässt weder Teil-ZIP noch `.tmp` noch SHA-Datei;
3. bestehende Datenschutz-/ZIP-Prüfung bleibt aktiv.

## Abnahme / Evidence
- GitHub Actions `Grundprüfung`, Run #294, Commit `8b2863ac1983fd3cef8a4b6751c72f040e564d6c`: **success**.
- Der Workflow führt verbindlich `bash scripts/pruefen.sh --full` aus.
- Derselbe Workflow führt danach `python3 scripts/iteration_restore.py --output-dir "$RUNNER_TEMP/tool_restore"` aus.
- Damit sind Vollprüfung und Restore-Gate für den geprüften Produktionspatch grün nachgewiesen.

## Nicht verändert
- Append-only Ereignislogs;
- Nutzerdaten;
- Recovery-/Restore-Logik;
- Backup-Skript und Berichtsschreiber außerhalb des Diagnoseexports.

Diese Punkte bleiben getrennte spätere Konsistenz-Slices, damit diese Iteration klein und regressionsarm bleibt.
