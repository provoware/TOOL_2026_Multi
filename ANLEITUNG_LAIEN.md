# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Die sechs Startschritte, die unsichtbare Startprüfung und die Prozesswache bleiben aktiv.

## Debug- und Recovery-Zentrale
Oben können Sie Ereignisse einfach eingrenzen:
- **Schweregrad** – zum Beispiel nur Fehler,
- **Bereich** – zum Beispiel nur START oder IMPORT,
- **Anzeigegröße** – 100, 125, 150, 175 oder 200 Prozent.

Ein Ereignis öffnen Sie durch:
- Doppelklick auf die Zeile,
- `Enter`,
- oder **Ausgewähltes Ereignis öffnen**.

## Was zeigt die Detailansicht?
Zuerst nur die verständlichen Angaben:
- Was ist passiert?
- Wann ist es passiert?
- Wie oft trat es auf?
- Wann trat es zum ersten Mal auf?
- Was wurde geschützt?
- Was ist der nächste Schritt?

Technische Angaben bleiben zuerst **eingeklappt**. Sie erscheinen nur nach **Technische Details anzeigen**.

## Tastatur
- `Tab` – zum nächsten bedienbaren Element,
- `Enter` – markiertes Ereignis öffnen,
- `F5` – aktualisieren,
- `Ctrl++` / `Ctrl+-` – Anzeige größer/kleiner,
- `Ctrl+0` – zurück auf 100 Prozent,
- `Escape` – Detailfenster schließen.

## Schreibfehler sicher prüfen
```bash
python3 scripts/schreibfehler_simulieren.py
```

Dabei wird **kein Datenträger gefüllt**. Das Projekt simuliert nur in einem temporären Testordner:
- kein Speicherplatz mehr (`ENOSPC`),
- Datenträger nur lesbar (`EROFS`).

Der Test ist nur grün, wenn ein vorhandener Bestand unverändert bleibt und keine unvollständige Temp-Datei zurückbleibt.

## Vollprüfung
```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung prüft zusätzlich eine echte Tk-Oberfläche für Tastatur, Fokus, Detailansicht und Zoom. Ohne virtuelle oder echte grafische Sitzung wird dieser Teil nicht als bestanden ausgegeben.

## Bestehende Schutzfunktionen
- Logrotation und Quarantäne beschädigter Zeilen,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- vollständige ZIP-/SHA-/Restore-Prüfung.
