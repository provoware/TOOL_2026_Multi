# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern mit vervollständigtem Songbibliotheksworkflow · **Version:** 0.9.1 · **Stand:** 2026-09-08

## Iteration 10 – CI-Wartung

- 🟢 `actions/checkout` von `v4` auf **`v7.0.1`** aktualisiert.
- 🟢 keine fachlichen Funktionen, Songdaten oder Laufzeitlogik verändert.
- 🟢 vollständige Grundprüfung und Restore-Gate bleiben verbindliche Abnahme.

## Iteration 9 – Songbibliothek vervollständigen

| Bereich | Status | Nachweis |
|---|---|---|
| Suche | 🟢 | freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags |
| Filter | 🟢 | kombinierbar nach Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten |
| Favoriten | 🟢 | im Editor setzbar; in der Bibliothek sichtbar und filterbar |
| Bearbeitungsstatus | 🟢 | Idee, Entwurf, Überarbeitung, Fertig |
| Sortierung/Gruppierung | 🟢 | zuletzt bearbeitet, Titel, Genre, Tags, Status; Gruppen nach Genre, Tags oder Status |
| Versionswiederherstellung | 🟢 | Vorschau zuerst; aktueller Stand wird vor Restore automatisch neu gesichert |
| Rückwärtskompatibilität | 🟢 | ältere 0.7.0/0.8.0-Songs bleiben lesbar |

## Start

```bash
bash schnellstart.sh
```

Im Dashboard stehen **Neuer Song**, **Songbibliothek**, die letzten bearbeiteten Songs als Schnellkacheln, Entwickler-Schnellinfo und Logout bereit.

## Songbibliothek

Die Bibliothek arbeitet ausschließlich mit den Arbeitsdateien unter:

```text
daten/songtexte/*.txt
```

### Suchen und filtern

Die freie Suche durchsucht:
- Titel,
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags.

Zusätzlich lassen sich Filter kombinieren für:
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags,
- Bearbeitungsstatus,
- nur Favoriten.

Filtern, Sortieren und Gruppieren verändern keine Songdatei.

### Sortierung und Gruppierung

Sortierung:
- zuletzt bearbeitet,
- Titel,
- Genre,
- Tags,
- Status.

Gruppierung:
- keine,
- Genre,
- Tags,
- Status.

## Favoriten und Status

Im Songeditor gibt es:
- **★ Favorit**,
- **Bearbeitungsstatus:** Idee, Entwurf, Überarbeitung oder Fertig.

Beides wird in derselben parsebaren UTF-8-Songdatei gespeichert. Es wurde kein zweites internes Format eingeführt.

## Versionsstände sicher wiederherstellen

Ältere Stände liegen unter:

```text
daten/songtexte/.versionen/<Titel>/<Zeitstempel>.txt
```

Wiederherstellung erfolgt nur aus der Versionsansicht:
1. Version auswählen.
2. Inhalt in der Vorschau prüfen.
3. **Diese Version wiederherstellen** wählen.
4. Der aktuelle Song wird unmittelbar davor automatisch als neuer Versionsstand gesichert.
5. Erst danach wird die gewählte Version atomar als aktueller Song eingesetzt.

Fremde oder nicht zum Song gehörende Versionspfade werden abgewiesen.

## Exporte

Weiterhin verfügbar unter `daten/songtexte/export/`:
- TXT mit Metadaten,
- Markdown,
- JSON,
- Nur-Songtext-TXT.

## Bestehende Schutzwege

- Autosave alle 5 Minuten,
- Speichern bei Fokusverlust,
- `Ctrl+S`,
- Speichern beim Schließen und vor Logout,
- atomarer Dateiersatz,
- automatische Versionsstände nur bei tatsächlichen Änderungen,
- Recovery-/Diagnose-/Restore-Kette.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Sie umfasst Logiktests, echte Tk-GUI-Tests, ENOSPC-/EROFS-Simulation, Release-Manifest, Headless-Start und vollständigen Restore.
