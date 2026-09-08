# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern · **Version:** 0.6.0 · **Stand:** 2026-09-08

## Iteration 6 – Debug- und Recovery-Zentrale

| Bereich | Status | Nachweis |
|---|---|---|
| Filter | 🟢 | Schweregrad und Bereich kombinierbar |
| Ereignisdetails | 🟢 | Doppelklick, Enter oder Schaltfläche |
| Wiederholungen | 🟢 | Zähler plus erstes Auftreten aus dem Rückfallmanager |
| Schreibfehler | 🟢 | gefahrlose ENOSPC-/EROFS-Simulation im temporären Testpfad |
| Tastatur/Fokus | 🟢 | Tk-GUI-Test mit Fokusreihenfolge und Tastaturbindungen |
| Zoom/Schrift | 🟢 | 100, 125, 150, 175 und 200 Prozent zentral |
| technische Details | 🟢 | standardmäßig eingeklappt; gezielt ein-/ausblendbar |
| Restore/Diagnose/Wächter | 🟢 | Schutzketten aus Iteration 4/5 bleiben aktiv |

## Start

```bash
bash schnellstart.sh
```

Die Hauptansicht öffnet als Debug- und Recovery-Zentrale. Filter und Anzeigegröße stehen oberhalb der Ereignistabelle. Ein markiertes Ereignis lässt sich mit **Enter** oder Doppelklick öffnen.

## Tastatur

- `Enter` – markiertes Ereignis öffnen
- `F5` – aktualisieren
- `Ctrl++` / `Ctrl+-` – Anzeige vergrößern/verkleinern
- `Ctrl+0` – 100 Prozent
- `Escape` – Detailfenster schließen
- `Tab` – durch Filter, Tabelle und Schaltflächen wechseln

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung führt zusätzlich zur bisherigen Sicherheitskette eine echte Tk-Oberflächenprüfung aus. Ohne `xvfb-run` oder eine vorhandene grafische Sitzung wird dieser Schritt nicht fälschlich als bestanden markiert.

## Schreibfehler sicher simulieren

```bash
python3 scripts/schreibfehler_simulieren.py
```

Die Simulation füllt keinen Datenträger. Sie erzeugt kontrolliert `ENOSPC` und `EROFS` in einem temporären Testordner und prüft, dass der vorhandene Bestand unverändert bleibt.

## Bestehende Schutzwege

```bash
python3 scripts/diagnosepaket.py
bash scripts/backup_erstellen.sh
```

Datenschutzprüfung, Logrotation/Quarantäne, Headless-Start, Prozesswache und vollständiger Restore bleiben unverändert aktiv.
