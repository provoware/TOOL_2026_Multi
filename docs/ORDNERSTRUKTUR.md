# Ordnerstruktur und Übertragungsregeln

Version 1.0 · 2026-09-08

| Pfad | Zweck | Ins Nutzer-ZIP? | Git? |
|---|---|---:|---:|
| `app/` | Anwendung | ja | ja |
| `daten/` | nötige Basisdaten | nur wenn für Betrieb nötig | ja, sofern keine privaten Laufzeitdaten |
| `texte/` | sichtbare Texte und Textregistrierung | ja | ja |
| `scripts/` | Start-/Prüfhelfer | ja, soweit für Betrieb nötig | ja |
| `tests/` | automatische Prüfungen | normalerweise nein | ja |
| `docs/` | Entwicklerdokumentation | normalerweise nein | ja |
| `logs/` | Laufzeitprotokolle | nein | nein |
| `berichte/` | lokale Fehlerberichte | nein | nein |
| `backups/` | Sicherungen | nein | nein |
| `.venv/` | lokale Python-Umgebung | nein | nein |
| `tmp/` | temporäre Dateien | nein | nein |

## Grundsatz

Veröffentlichungen enthalten nur, was der Nutzer zum Starten und Benutzen braucht. Diagnosepakete werden separat erzeugt, damit keine Protokolle oder Entwicklerunterlagen versehentlich mit Basisdaten vermischt werden.
