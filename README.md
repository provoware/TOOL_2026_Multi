# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern mit Songworkflow · **Version:** 0.8.0 · **Stand:** 2026-09-08

## Iteration 8 – Songbibliothek und Versionsverwaltung

| Bereich | Status | Nachweis |
|---|---|---|
| Songbibliothek | 🟢 | vorhandene Songs werden nach letzter Bearbeitung gelistet und direkt geöffnet |
| Zuletzt bearbeitet | 🟢 | bis zu fünf Songs als Schnellkacheln im Dashboard |
| Song-Metadaten | 🟢 | Genre, Stimmung, Stil, Stimme, Besonderheiten und Tags |
| Versionsstände | 🟢 | vorheriger abweichender Stand wird vor Überschreiben automatisch gesichert |
| Exporte | 🟢 | TXT, Markdown, JSON und Nur-Songtext-TXT |
| Rückwärtskompatibilität | 🟢 | Songdateien aus 0.7.0 bleiben lesbar |
| Recovery/Diagnose | 🟢 | bestehende Schutzketten bleiben aktiv |

## Start

```bash
bash schnellstart.sh
```

Im Dashboard stehen **Neuer Song**, **Songbibliothek**, die letzten bearbeiteten Songs als Schnellkacheln, Entwickler-Schnellinfo und Logout bereit.

## Songbibliothek

Die Bibliothek liest ausschließlich die Arbeitsdateien unter:

```text
daten/songtexte/*.txt
```

Sie zeigt Titel, Genre, letzte Bearbeitungszeit und Anzahl vorhandener Versionsstände. Doppelklick oder `Enter` öffnet den Song im bestehenden Songtexteditor.

## Song-Metadaten

Optional stehen jetzt zur Verfügung:
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Besonderheiten,
- Tags.

Das interne Arbeitsformat bleibt eine parsebare UTF-8-Textdatei. Es wurde kein zweites internes Songformat eingeführt.

## Versionsstände

Vor einem geänderten Überschreiben wird der bisherige Stand automatisch gesichert:

```text
daten/songtexte/.versionen/<Titel>/<Zeitstempel>.txt
```

Identische Speicherungen erzeugen keinen neuen Versionsstand. Die Bibliothek zeigt ältere Stände zunächst nur schreibgeschützt an.

## Exporte

Exporte werden getrennt von der Arbeitsdatei erstellt:

```text
daten/songtexte/export/
```

Unterstützt werden:
- TXT mit Metadaten,
- Markdown,
- JSON,
- Nur Songtext als TXT ohne Metadaten.

## Bestehende Speicherwege

- Autosave alle 5 Minuten,
- Speichern bei Fokusverlust,
- `Ctrl+S`,
- Speichern beim Schließen,
- Speichern vor Logout,
- atomarer Dateiersatz.

## Recovery-Zentrale

Filter nach Schweregrad/Bereich, Ereignisdetails, Wiederholungsinformationen, Zoom 100–200 Prozent, Diagnosepaket, Logquarantäne und Restore-Gates bleiben erhalten.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung umfasst Logiktests, echte Tk-GUI-Tests, Schreibfehler-Simulation, Release-Manifest, Headless-Start und vollständigen Restore.
