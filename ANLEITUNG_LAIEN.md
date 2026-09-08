# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Die vorhandenen sechs Startschritte, die Headless-Prüfung und die Prozesswache bleiben aktiv.

## Was passiert beim normalen Beenden?
Wenn das Programm regulär geschlossen wird, schreibt es jetzt ein eigenes `ENDE`-Ereignis. So lässt sich später unterscheiden, ob das Programm sauber beendet wurde oder unerwartet verschwunden ist.

## Was passiert mit zu großen oder alten Logs?
Das Ereignislog wird automatisch begrenzt:
- ab mehr als 2 MiB wird es archiviert,
- nach mehr als 30 Tagen wird es archiviert,
- höchstens 5 ältere Archive bleiben erhalten.

Die Archive liegen unter `logs/archiv/`.

## Was passiert mit beschädigten Logzeilen?
Eine ungültige JSONL-Zeile wird nicht mehr still ignoriert. Das Programm:
1. sichert eine bereinigte Beweiskopie unter `logs/quarantaene/`,
2. entfernt nur die beschädigte Zeile aus dem aktiven Log,
3. erhält alle gültigen Zeilen atomar.

## Datenschutzgeprüftes Diagnosepaket
```bash
python3 scripts/diagnosepaket.py
```

Das Diagnosepaket übernimmt keine unveränderten Rohprotokolle. Textdaten werden zuerst bereinigt und danach nochmals geprüft. Erkannte Passwörter, Tokens, API-Schlüssel, Bearer-Tokens, Mailadressen und Linux-Home-Benutzernamen werden ersetzt. Erst nach dieser zweiten Prüfung wird das ZIP fertiggestellt. Dazu entsteht eine SHA-256-Prüfsumme.

## Sicherung und echte Wiederherstellungsprüfung
```bash
bash scripts/backup_erstellen.sh
```

Der bestehende Restore-Weg bleibt unverändert: ZIP, SHA-256, sicherer neuer Ordner, Manifestvergleich, Vollprüfung und Headless-Start müssen vollständig grün sein, bevor der Restore-Status `OK` lautet.
