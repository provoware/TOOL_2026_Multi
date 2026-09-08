# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern · **Version:** 0.5.0 · **Stand:** 2026-09-08

## Iteration 5 – Diagnose- und Logging-Härtung

| Bereich | Status | Nachweis |
|---|---|---|
| Logrotation | 🟢 | Größenlimit 2 MiB, Alterslimit 30 Tage, maximal 5 Archive |
| JSONL-Quarantäne | 🟢 | beschädigte Zeilen werden bereinigt gesichert und aus dem aktiven Log entfernt |
| Diagnosepaket | 🟢 | nur bereinigte Textkopien; abschließende Datenschutzprüfung vor ZIP-Erstellung |
| kontrolliertes Ende | 🟢 | normales Schließen erzeugt eigenes `ENDE`-Ereignis |
| Restore/Headless/Wächter | 🟢 | Schutz aus Iteration 4 bleibt aktiv |

## Start

```bash
bash schnellstart.sh
```

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

## Datenschutzgeprüftes Diagnosepaket

```bash
python3 scripts/diagnosepaket.py
```

Das Paket enthält keine unveränderten Rohprotokolle. Unterstützte Diagnose-Texte werden vor dem ZIP nochmals über `app/redaction.py` bereinigt und anschließend erneut auf verbliebene erkannte Geheimnisse geprüft. Zusätzlich entsteht eine SHA-256-Datei.

## Logpflege

`app/log_maintenance.py` führt begrenzte Rotation und Quarantäne aus. Beschädigte JSONL-Zeilen werden nicht mehr still übersprungen: Eine bereinigte Beweiskopie landet in `logs/quarantaene/`, während gültige Zeilen atomar im aktiven Log erhalten bleiben. Größen- oder altersbedingt rotierte Logs liegen in `logs/archiv/`.

## Verifizierte Iterationssicherung

```bash
bash scripts/backup_erstellen.sh
```

Restore, Headless-Start und Prozesswache aus Iteration 4 bleiben unverändert Teil der Sicherheitskette.
