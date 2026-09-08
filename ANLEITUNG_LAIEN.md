# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Das Startfenster besitzt jetzt sechs echte Schritte. Neu sind die unsichtbare Startprüfung ohne Fenster und die Prozesswache. Erst wenn alles grün ist, öffnet das Dashboard.

## Was schützt die Prozesswache?
Die eigentliche Anwendung läuft unter einem getrennten Wächter. Endet sie fehlerhaft oder durch ein hartes Signal, legt der Wächter einen verständlichen Bericht unter `berichte/` an. Er verändert dabei keine Nutzerdaten.

## Was steht nicht im Protokoll?
Typische Passwörter, Tokens, API-Schlüssel, Bearer-Tokens, Mailadressen und der Benutzername in Linux-Home-Pfaden werden vor dem Schreiben ersetzt.

## Sicherung und echte Wiederherstellungsprüfung
```bash
bash scripts/backup_erstellen.sh
```

Dabei passiert automatisch:
1. vollständiges Projekt-ZIP erstellen,
2. SHA-256 berechnen und erneut vergleichen,
3. ZIP auf unsichere Pfade prüfen,
4. in einen neuen Ordner entpacken,
5. Manifest vergleichen,
6. vollständige Projektprüfung ausführen,
7. Start ohne Fenster prüfen,
8. nur dann Restore-Status `OK` melden.

Ein fehlgeschlagener Schritt wird niemals als erfolgreiche Wiederherstellung ausgegeben.
