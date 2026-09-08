# Anleitung für Laien

## Was ist das hier?

Dieses Projekt enthält den ausführbaren Kern von **TOOL_2026_Multi**. Es erklärt Programmereignisse und Fehler, ohne Ihre Basisdaten zu verändern.

## Starten

```bash
bash schnellstart.sh
```

Der Start erledigt die technische Vorbereitung selbst. Wenn eine grafische Oberfläche verfügbar ist, erscheint ein kleines Startfenster mit fünf echten Checkpoints:

- 🟡 Vorgang läuft,
- 🟢 Schritt erfolgreich,
- 🔴 sicher abgebrochen.

Ohne grafische Oberfläche werden dieselben Zustände im Terminal angezeigt.

Der Start prüft nacheinander Python, die abgeschirmte Umgebung, nötige Zusatzpakete, den Laufzeitkern und danach die Anwendung. Sind in `requirements.txt` keine externen Pakete eingetragen, wird kein unnötiger Paketdownload gestartet.

## Dashboard verstehen

- Im Dashboard stehen immer die letzten fünf Ereignisse.
- Die Schweregrade erhalten zusätzlich ein Ampelsymbol.
- Über **Debug/Log → Ereignisse und Fehler öffnen** sehen Sie ausführliche Erklärungen.
- Jede Meldung nennt eine eindeutige Kennung, den Grund, die Schutzmaßnahme und den nächsten sicheren Schritt.
- Wiederholt sich ein Fehlermuster, weist das Programm darauf hin.

## Prüfen

Der Schnellstart nutzt automatisch die kurze Laufzeitprüfung:

```bash
bash scripts/pruefen.sh --runtime
```

Für Entwicklung und Veröffentlichung gibt es die vollständige Prüfung:

```bash
bash scripts/pruefen.sh --full
```

Beide Wege laufen einmal durch und enden. Es gibt keine versteckte Dauerschleife.

## Nutzer-ZIP erzeugen

Für Entwickler:

```bash
python3 scripts/veroeffentlichen.py
```

Das Veröffentlichungs-Skript übernimmt ausschließlich Dateien, die in `MANIFEST.json` mit `release: true` freigegeben wurden. Tests, interne Agent-Dateien und Entwicklerdokumentation bleiben draußen. Das ZIP wird anschließend geprüft und erhält eine SHA-256-Prüfsumme.

## Wichtig

- `logs/` enthält Laufzeitprotokolle und Start-Checkpoints.
- `backups/` enthält lokale Sicherungen.
- `docs/` enthält Entwicklungsunterlagen.
- `daten/` ist für tatsächliche Basisdaten der Anwendung reserviert.
- `release/` enthält lokale Veröffentlichungs-ZIPs und wird nicht in Git übernommen.
