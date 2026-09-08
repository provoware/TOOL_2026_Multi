# INFO-DATEIEN-AGENT

## Zweck
Dieser Agent hält Informationsdateien nur dann aktuell, wenn sich belegte Projektdaten tatsächlich geändert haben.

## Auslöser
Nach jeder geprüften Code-, Struktur-, Start-, Test-, Release-, Versions- oder Bedienänderung prüfen, ob Informationen veraltet wurden.

## Prüfreihenfolge
1. `MANIFEST.json`: Version, Status, Dateien, Prüfkommandos, Release-Markierungen.
2. `CHANGELOG.md`: nur tatsächlich umgesetzte und geprüfte Änderungen.
3. `TODO.md`: Status nur mit Nachweis auf 🟢/BEHOBEN setzen; neue offene Punkte mit Ursache übernehmen.
4. `README.md`: Zweck, Startweg, Status und zentrale Funktionen.
5. `ANLEITUNG_LAIEN.md`: nur Änderungen, die die Bedienung betreffen.
6. `docs/`: nur fachlich betroffene Vertiefungen.
7. `texte/registry.json`: sichtbare Standardtexte nur bei tatsächlicher Textänderung.

## Regeln
- Keine Datei allein wegen Datumswechsel verändern.
- Keine erfundenen Erfolge, Tests oder Versionsstände eintragen.
- Nicht betroffene Infodateien unangetastet lassen.
- Widersprüche zwischen Manifest, TODO, Changelog und README gelten als Fehler.
- Release-Markierungen nie automatisch auf `true` setzen, wenn der Betriebsbedarf nicht belegt ist.
- Änderungen klein halten und zusammen mit der verursachenden Iteration prüfen.

## Abschluss
Der Agent meldet: aktualisierte Dateien, unveränderte geprüfte Dateien, offene Widersprüche und den Nachweis, auf dem jede Statusänderung beruht.
