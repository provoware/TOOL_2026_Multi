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

Die freie Suche durchsucht Titel, Genre, Stimmung, Stil, Stimme und Tags. Zusätzlich lassen sich Filter für Genre, Stimmung, Stil, Stimme, Tags, Bearbeitungsstatus und nur Favoriten kombinieren.

Filtern, Sortieren und Gruppieren verändern keine Songdatei.

### Sortierung und Gruppierung

Sortierung: zuletzt bearbeitet, Titel, Genre, Tags oder Status. Gruppierung: keine, Genre, Tags oder Status.

## Favoriten und Status

Im Songeditor gibt es **★ Favorit** sowie **Bearbeitungsstatus**: Idee, Entwurf, Überarbeitung oder Fertig. Beides bleibt Teil derselben parsebaren UTF-8-Songdatei.

## Versionsstände sicher wiederherstellen

Ältere Stände liegen unter `daten/songtexte/.versionen/<Titel>/<Zeitstempel>.txt`. Vor einer Wiederherstellung wird der aktuelle Song automatisch als neuer Versionsstand gesichert. Fremde Versionspfade werden abgewiesen.

## Exporte

Weiterhin verfügbar unter `daten/songtexte/export/`: TXT mit Metadaten, Markdown, JSON und Nur-Songtext-TXT.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Sie umfasst Logiktests, echte Tk-GUI-Tests, ENOSPC-/EROFS-Simulation, Release-Manifest, Headless-Start und vollständigen Restore.
