# Anleitung für Laien

## Was ist das hier?

Dieses Projekt enthält den ersten ausführbaren Kern von **TOOL_2026_Multi**. Es erklärt Programmereignisse und Fehler, ohne Ihre Basisdaten zu verändern.

## Starten

Öffne im Projektordner ein Terminal und führe aus:

```bash
bash schnellstart.sh
```

Das Skript erledigt die technische Vorbereitung selbst, prüft den Kern und öffnet das Dashboard.

## Debug/Log verstehen

- Im Dashboard stehen immer die letzten fünf Ereignisse.
- Über **Debug/Log → Ereignisse und Fehler öffnen** sehen Sie ausführliche Erklärungen.
- Jede Meldung nennt eine eindeutige Kennung, den Grund, die Schutzmaßnahme und den nächsten sicheren Schritt.
- Wiederholt sich ein Fehlermuster, weist das Programm darauf hin. Es merkt sich dafür nur eine technische Prüfsumme, keine persönlichen Inhalte.
- Maschinenlesbare JSON-Zeilen liegen lokal in `logs/ereignisse.jsonl`; einfache Einzelberichte liegen in `berichte/`.

## Prüfen

```bash
bash scripts/pruefen.sh
```

Die Prüfung läuft einmal durch und endet. Es gibt keine versteckte Dauerschleife.

## Sicherung erstellen

```bash
bash scripts/backup_erstellen.sh
```

Die Sicherung wird im Ordner `backups/` abgelegt. Dazu entsteht eine Prüfsumme, mit der später kontrolliert werden kann, ob die ZIP-Datei unverändert ist.

## Wichtig

- `logs/` enthält spätere Laufzeitprotokolle.
- `backups/` enthält lokale Sicherungen.
- `docs/` enthält Entwicklungsunterlagen.
- `daten/` ist für tatsächliche Basisdaten der Anwendung reserviert.

Diese Bereiche werden bewusst getrennt, damit beim Kopieren oder Veröffentlichen nicht unnötiger Ballast übertragen wird.
