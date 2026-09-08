# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern · **Version:** 0.3.0 · **Stand:** 2026-09-08

## Zweck

Dieses Repository enthält den ausführbaren Kern von **TOOL_2026_Multi**. Das Dashboard zeigt die letzten fünf Ereignisse. Der Menüpunkt **Debug/Log** erklärt Vorgänge und Fehler einfach; parallel entsteht ein maschinenlesbares Protokoll.

## Ampel

| Bereich | Status | Bedeutung |
|---|---|---|
| Projektregeln | 🟢 | verbindlich definiert |
| Ordnertrennung | 🟢 | Laufzeitdaten, Entwicklung und Protokolle getrennt |
| Sicherungskonzept | 🟢 | Regeln und automatischer Sicherungsweg definiert |
| Prüfablauf | 🟢 | lokaler Ein-Klick-Prüfer vorhanden |
| Schnellstart | 🟢 | richtet die Umgebung ein, prüft und startet die Anwendung |
| Werkzeugfunktionen | 🔴 | noch nicht implementiert |
| Fehlerbericht im Werkzeug | 🟢 | TXT-Bericht und JSON-Zeile mit eindeutiger Kennung |
| Rückfallmanagement | 🟢 | erkennt wiederholte Fehlermuster datensparsam |
| Datei- und Datengrenzen | 🟢 | Manifest prüft getrennte Bereiche und Zeilengrenzen |

## Einfache Nutzung

1. Datei `schnellstart.sh` doppelklicken oder im Terminal starten.
2. Das Skript richtet die abgeschirmte Python-Umgebung ein.
3. Abhängigkeiten aus `requirements.txt` werden installiert.
4. Vor dem Start wird einmal geprüft.
5. Die Anwendung startet und zeigt die letzten fünf Ereignisse.

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

Laufzeitprotokolle bleiben lokal in `logs/`; verständliche Einzelberichte liegen in `berichte/`. Beide Ordner werden nicht in Git oder Sicherungs-ZIPs übernommen.
