# Ordnerstruktur und Übertragungsregeln

Version 1.1 · 2026-09-08

| Pfad | Zweck | Ins Nutzer-ZIP? | Git? |
|---|---|---:|---:|
| `app/` | Anwendung | ja | ja |
| `configs/` | versionierte Einstellungen | ja | ja |
| `transfer/basisdaten/` | ausschließlich bewusst zu übertragende Basisdaten | separates Transferpaket | nein |
| `nutzerdaten/` | lokale Nutzerdaten | nein | nein |
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

Die Regeln sind zusätzlich im `separation`-Block des Manifests maschinenlesbar. Eine Datei darf nicht gleichzeitig Basisübertragung, Protokoll oder Entwicklerdokumentation sein.
