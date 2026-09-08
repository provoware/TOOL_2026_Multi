# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern · **Version:** 0.3.0 · **Stand:** 2026-09-08

## Zweck

Dieses Repository enthält den ausführbaren Kern von **TOOL_2026_Multi**. Das Dashboard zeigt die letzten fünf Ereignisse, erklärt Fehler verständlich und führt Status zusätzlich über ein Ampelsystem. Die Entwicklungsgrundlage besitzt nun einen rückfallgesicherten Fehlerfall, globale Oberflächenstandards, einen grafisch unterstützten Startweg und einen strikt manifestgesteuerten Veröffentlichungsweg.

## Ampel

| Bereich | Status | Bedeutung |
|---|---|---|
| Projektregeln | 🟢 | verbindlich definiert |
| Ordnertrennung | 🟢 | Laufzeitdaten, Entwicklung und Protokolle getrennt |
| Sicherungskonzept | 🟢 | Regeln und automatischer Sicherungsweg definiert |
| Prüfablauf | 🟢 | getrennte Laufzeit- und Entwicklerprüfung vorhanden |
| Schnellstart | 🟢 | fünf echte Checkpoints, grafische Ampelanzeige mit Konsolenfallback |
| Paketabgleich | 🟢 | keine unnötigen Downloads, wenn keine externen Pakete benötigt werden |
| Globale UI-Standards | 🟢 | Farben, Abstände, Schriftgrößen und Statusdarstellung zentral definiert |
| Fehlerbericht im Werkzeug | 🟢 | TXT-Bericht und JSON-Zeile mit eindeutiger Kennung |
| Rückfallmanagement | 🟢 | `LOG-FEHLER-001` ist über `REG-LOG-001` als **BEHOBEN** abgesichert |
| Veröffentlichung | 🟢 | nur Manifest-Dateien mit `release: true` gelangen ins Nutzer-ZIP |
| Info-Dateien-Agent | 🟢 | aktualisiert Informationsdateien nur bei belegten Änderungen |
| Werkzeugfunktionen | 🔴 | fachliche Hauptmodule noch nicht festgelegt |

## Einfache Nutzung

1. `schnellstart.sh` doppelklicken oder im Terminal starten.
2. Der Start prüft Python, die abgeschirmte Umgebung, Abhängigkeiten, Projektkern und Anwendung.
3. Wenn eine grafische Oberfläche verfügbar ist, zeigt ein kleines Fenster den echten Stand mit 🟡/🟢/🔴 an.
4. Sind keine externen Pakete nötig, wird der Paketdownload vollständig übersprungen.
5. Erst nach grüner Laufzeitprüfung startet das Dashboard.

```bash
bash schnellstart.sh
```

## Prüfen

Normale Laufzeitprüfung:

```bash
bash scripts/pruefen.sh --runtime
```

Vollständige Entwicklerprüfung:

```bash
bash scripts/pruefen.sh --full
```

## Veröffentlichung

```bash
python3 scripts/veroeffentlichen.py
```

Das Skript validiert alle freigegebenen Pfade, erzeugt das Nutzer-ZIP atomar, prüft dessen Inhalt und schreibt eine SHA-256-Prüfsumme. Dateien ohne `release: true` werden nicht übernommen.

## Wichtige Dateien

- `AGENTS.md` – verbindliche Arbeitsregeln für Entwicklung.
- `agents/INFO_DATEIEN_AGENT.md` – prüft nach Änderungen, welche Infodateien wirklich aktualisiert werden müssen.
- `TODO.md` – offene Arbeit, Priorität und nächste Iteration.
- `CHANGELOG.md` – nachvollziehbare Änderungen.
- `MANIFEST.json` – Projektstand und verbindliche Release-Freigaben.
- `ANLEITUNG_LAIEN.md` – kurze Anleitung ohne unnötige Fachsprache.
- `app/ui_standards.py` – zentrale Farben, Abstände, Schriften und Ampellogik.
- `scripts/start_status.py` – grafische Start-Checkpoints.
- `scripts/veroeffentlichen.py` – manifestgesteuerte Release-Erstellung.
- `tests/regression_registry.json` – bestätigte Rückfallfälle mit Testkennung und Status.
- `scripts/pruefen.sh` – begrenzte Qualitätsprüfung.
- `scripts/backup_erstellen.sh` – lokaler Sicherungspunkt mit Prüfsumme.

## Grundsatz

**Planen → klein ändern → gezielt prüfen → Ergebnis sichern → Infodateien abgleichen → erst dann weiter.**

Keine verdeckten Endlosschleifen, keine unnötigen Komplettumbauten und keine ungeprüften Änderungen an Nutzerdaten.
