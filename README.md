# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern mit erstem Fachworkflow · **Version:** 0.7.0 · **Stand:** 2026-09-08

## Iteration 7 – Dashboard-Schnellspeicher und Songtexteditor

| Bereich | Status | Nachweis |
|---|---|---|
| Entwickler-Schnellinfo | 🟢 | einzeilig im Dashboardheader; Enter oder Schaltfläche; append-only mit Zeitstempel |
| Songtexteditor | 🟢 | Titel, optionale Genre-/Sonstiges-Felder, strukturierte Songbereiche und Live-Vorschau |
| Songbereiche | 🟢 | Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken, Instrumental |
| Autosave | 🟢 | alle 5 Minuten, bei Fokusverlust und beim Schließen |
| Titelspeicherung | 🟢 | atomar unter `daten/songtexte/<Titel>.txt` |
| Logout | 🟢 | speichert offene Songeditoren und beendet die Sitzung nur bei erfolgreichem Speichern |
| Recovery/Diagnose | 🟢 | bestehende Schutzketten bleiben aktiv |

## Start

```bash
bash schnellstart.sh
```

Im Dashboardheader befinden sich jetzt:
- das einzeilige Feld **Entwickler-Schnellinfo**,
- **Songtexteditor**,
- **Logout**.

Eine Schnellinfo wird mit Zeitstempel an `Entwicklerinformation.txt` angehängt. Vorhandener Inhalt wird nicht überschrieben.

## Songtexteditor

Der Editor arbeitet in einem eigenen Fenster. Songbereiche können einzeln hinzugefügt oder entfernt werden. Rechts wird der aktuelle Song fortlaufend als Vorschau angezeigt.

Speicherung:

```text
daten/songtexte/<Titel>.txt
```

Wenn der Titel geändert wird, wird der neue Stand unter dem neuen Titel gespeichert. Eine vorherige Datei wird nicht automatisch gelöscht.

Speicherwege:
- automatisch alle 5 Minuten,
- beim Verlassen von Titel, Genre, Songtext oder Sonstiges,
- mit `Ctrl+S`,
- beim Schließen des Editors,
- vor Logout.

## Recovery-Zentrale

Filter nach Schweregrad/Bereich, direkte Ereignisdetails, Wiederholungsinformationen, Zoom 100–200 Prozent und eingeklappte Technikdetails aus Iteration 6 bleiben unverändert erhalten.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung umfasst Logiktests, echte Tk-GUI-Tests, Schreibfehler-Simulation, Release-Manifest, Headless-Start und das vollständige Restore-Gate.
