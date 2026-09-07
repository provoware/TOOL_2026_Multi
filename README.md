# TOOL_2026_Multi

> **Status:** 🟡 Entwicklungsgrundlage · **Version:** 0.1.0 · **Stand:** 2026-09-08

## Zweck

Dieses Repository ist die saubere Entwicklungsgrundlage für **TOOL_2026_Multi**. Die eigentliche Werkzeugfunktion wird erst in klar abgegrenzten Iterationen ergänzt. Entwicklung, Prüfung, Sicherung und Fehlerbehandlung werden von Anfang an nachvollziehbar und laienfreundlich geführt.

## Ampel

| Bereich | Status | Bedeutung |
|---|---|---|
| Projektregeln | 🟢 | verbindlich definiert |
| Ordnertrennung | 🟢 | Laufzeitdaten, Entwicklung und Protokolle getrennt |
| Sicherungskonzept | 🟢 | Regeln und automatischer Sicherungsweg definiert |
| Prüfablauf | 🟢 | lokaler Ein-Klick-Prüfer vorhanden |
| Schnellstart | 🟡 | vorbereitet; startet die Anwendung sobald `app/main.py` vorhanden ist |
| Werkzeugfunktionen | 🔴 | noch nicht implementiert |
| Fehlerbericht im Werkzeug | 🔴 | folgt mit der ersten ausführbaren Anwendung |

## Einfache Nutzung

1. Datei `schnellstart.sh` doppelklicken oder im Terminal starten.
2. Das Skript richtet die abgeschirmte Python-Umgebung ein.
3. Abhängigkeiten aus `requirements.txt` werden installiert.
4. Vor dem Start wird einmal geprüft.
5. Sobald die Anwendung vorhanden ist, startet sie automatisch.

```bash
bash schnellstart.sh
```

## Wichtige Dateien

- `AGENTS.md` – verbindliche Arbeitsregeln für Entwicklung.
- `TODO.md` – offene Arbeit, Priorität und nächste Iteration.
- `CHANGELOG.md` – nachvollziehbare Änderungen.
- `MANIFEST.json` – maschinenlesbarer Projektstand.
- `ANLEITUNG_LAIEN.md` – kurze Anleitung ohne unnötige Fachsprache.
- `docs/ENTWICKLUNGSREGELN.md` – vollständiges Entwicklungsverfahren.
- `docs/FEHLER_UND_REGRESSION.md` – Fehlervermeidung, Fehlerbehandlung und Rückfalltests.
- `docs/BACKUP_KONZEPT.md` – Sicherung und Wiederherstellung.
- `docs/ORDNERSTRUKTUR.md` – was wohin gehört und was nicht übertragen wird.
- `scripts/pruefen.sh` – begrenzte, automatische Qualitätsprüfung.
- `scripts/backup_erstellen.sh` – lokaler Sicherungspunkt mit Prüfsumme.

## Grundsatz

**Planen → klein ändern → prüfen → Ergebnis sichern → dokumentieren → erst dann weiter.**

Keine verdeckten Endlosschleifen, keine unnötigen Komplettumbauten und keine ungeprüften Änderungen an Nutzerdaten.
