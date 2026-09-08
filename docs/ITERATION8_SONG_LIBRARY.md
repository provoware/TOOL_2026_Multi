# Iteration 8 – Songbibliothek und Versionsverwaltung

## Ziel
Den vorhandenen Songtexteditor zu einem zusammenhängenden Songworkflow erweitern, ohne ein zweites internes Datenformat einzuführen.

## Arbeitsformat
Kanonisch bleibt:

```text
daten/songtexte/<Titel>.txt
```

Die Datei enthält parsebare UTF-8-Kopfzeilen für Metadaten und danach die Songbereiche. Dateien aus 0.7.0 bleiben lesbar.

## Metadaten
Optional:
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Besonderheiten,
- Tags.

## Bibliothek
`app/song_library.py` liest nur `daten/songtexte/*.txt`, sortiert nach Änderungszeit absteigend und öffnet vorhandene Dateien im normalen `SongEditor`.

Dashboard: maximal fünf zuletzt bearbeitete Songs als Schnellkacheln. Auch diese öffnen denselben Editorpfad.

## Versionsstände
Vor einem atomaren Überschreiben wird der vorherige Inhalt nur dann nach

```text
daten/songtexte/.versionen/<Titel>/<UTC-Zeitstempel>.txt
```

gesichert, wenn er sich vom neuen Inhalt unterscheidet. Identische Saves erzeugen keine Version. Die Bibliothek zeigt ältere Stände schreibgeschützt an; eine automatische Rücksetzung ist bewusst nicht Teil dieser Iteration.

## Exporte
Getrennt unter `daten/songtexte/export/`:
- TXT mit Metadaten,
- Markdown,
- JSON,
- TXT nur mit Songbereichen und Songtext.

Exporte dürfen weder die Arbeitsdatei noch Versionsstände verändern.

## Schutz
- atomare Writes über temporäre Datei + `fsync` + `os.replace`,
- kein stilles Löschen alter Songdateien bei Titelwechsel,
- kein Versionsschnappschuss ohne Inhaltsänderung,
- Versionsvorschau nur lesbar,
- Laufzeitdaten bleiben außerhalb von Git und Release-Quellbestand,
- Recovery-, Diagnose-, Datenschutz- und Restore-Gates bleiben unverändert aktiv.

## Abnahme
1. 0.7.0-Datei wird korrekt geladen.
2. Erweiterte Metadaten überstehen Render/Parse-Rundtrip.
3. Erstes Save erzeugt keine Version; identisches Save ebenfalls nicht; geändertes Save genau einen vorherigen Stand.
4. Bibliothek sortiert nach letzter Bearbeitung und öffnet vorhandene Songs.
5. Dashboard zeigt bis zu fünf aktuelle Songkacheln.
6. TXT/Markdown/JSON/Nur-Songtext-Export erzeugen getrennte Dateien.
7. Alte Song-, Recovery-, Diagnose- und Restore-Tests bleiben grün.
