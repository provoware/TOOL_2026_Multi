# PROVOWARE – Optimierungsprotokoll

## 21.10.2026 – TOOL_2026_Multi: Defekte UTF-8-Ereignislogs sicher behandeln

**Repository:** `provoware/TOOL_2026_Multi`  
**Basis:** `main` bei `b7edb4397d69026321bf9ddfe55ef2904aedf5fe`  
**Arbeitszweig:** `auto/20261021-robuste-utf8-protokolle`  
**Fehlerkennung:** `LOG-UTF8-001`  
**Eingriff:** begrenzte Fehlerbehandlung, kein neues Format und keine zusätzliche Bibliothek.

### Ausgangsproblem

`quarantine_corrupt_jsonl()` liest `logs/ereignisse.jsonl` ausschließlich als UTF-8. Enthält die Datei beispielsweise das Byte `0xFF`, löst das Lesen einen `UnicodeDecodeError` aus. Der bisherige Schutz fing nur `OSError` ab. Dadurch konnte `EventLogger.record()` schon beim Warten des Logs scheitern. `EventLogger.recent()` fing diesen Ausnahmefall ebenfalls nicht ab.

### Konkrete Änderung

1. `app/log_maintenance.py` behandelt ungültige Textkodierung beim Loglesen ausdrücklich als nicht reparierbaren Zustand. Es gibt `0` zurück, **ohne das vorhandene Log umzuschreiben oder eine unvollständige Quarantäne zu erzeugen**.
2. `app/event_log.py` zeigt bei unlesbaren Logbytes sicher eine leere Trefferliste statt eines erneuten Ausnahmeabbruchs.
3. `tests/test_log_invalid_utf8.py` prüft den unveränderten Originalinhalt, das gefahrlose Lesen und das erfolgreiche Anlegen eines neuen Diagnoseberichts.

### Nutzermehrwert

Ein einzelnes beschädigtes Log kann künftig nicht mehr den vollständigen Diagnoseweg blockieren. Bereits vorhandene Originalbytes bleiben für eine spätere manuelle Untersuchung erhalten. Eine neue Diagnose kann angehängt und zusätzlich als Textbericht gespeichert werden.

### Prüfungen und Grenzen

- Neue gezielte Rückfalltests: `tests/test_log_invalid_utf8.py` (drei Testfälle).
- Bestehende angrenzende Tests: `tests/test_diagnostics_logging.py`.
- GitHub-Gesamtprüfung wird durch den Pull Request ausgelöst; ihr **tatsächliches** Ergebnis ist dem PR-Prüfstatus zu entnehmen. Dieser Bericht behauptet keine bereits erfolgte lokale Gesamtprüfung.
- **Bewusste Grenze:** Ein weiterhin ungültig kodiertes Altlog wird nicht automatisch repariert und dessen bisherige Einträge werden in der aktuellen Ereignisliste bis zur manuellen Wiederherstellung nicht angezeigt. Das Programm überschreibt oder löscht die Beweisdatei nicht.
- Tests laufen nur mit künstlichen Dateien in temporären Verzeichnissen; keine produktiven Nutzerdaten werden verändert.

### GitHub-Verweise

- [Entwicklungszweig](https://github.com/provoware/TOOL_2026_Multi/tree/auto/20261021-robuste-utf8-protokolle)
- [Pull Requests](https://github.com/provoware/TOOL_2026_Multi/pulls) – aktuellen Änderungsantrag und Prüfstatus ansehen.

### Nächste Empfehlung

Für eine spätere, **separat freizugebende** Verbesserung: beschädigte Logs nach gesicherter Originalkopie in einem ausdrücklichen Wiederherstellungsdialog prüfen und vorhandene gültige Datensätze selektiv anzeigen. Kein automatisches Reparieren im Hintergrund.
