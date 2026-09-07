# Anleitung für Laien

## Was ist das hier?

Dieses Projekt ist derzeit die vorbereitete Grundlage für das spätere Werkzeug **TOOL_2026_Multi**. Die Entwicklungsregeln, Sicherungen und Prüfungen sind bereits vorbereitet. Die eigentliche Werkzeugfunktion folgt in der nächsten Entwicklungsstufe.

## Starten

Öffne im Projektordner ein Terminal und führe aus:

```bash
bash schnellstart.sh
```

Das Skript erledigt die technische Vorbereitung selbst. Wenn die eigentliche Anwendung noch fehlt, zeigt es eine klare Meldung und beendet sich ohne etwas zu beschädigen.

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
