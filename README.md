# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern mit PySide6-Referenzdashboard und vorbereiteter realer Kubuntu/X11-Endabnahme · **Version:** 0.10.1 · **Stand:** 2026-09-08

## Iteration 12 – Kubuntu/X11-Endabnahme

- 🟢 `kubuntu_abnahme.sh` startet einen eigenen PySide6-Abnahmeassistenten.
- 🟢 echte X11-Sitzung und KDE/Plasma werden vorgeprüft; Wayland wird nicht als X11 durchgewunken.
- 🟢 echter SIGTERM-/Prozesswächtertest läuft ausschließlich in einem temporären Verzeichnis.
- 🟢 TXT- und JSON-Bericht werden unter `berichte/` erstellt.
- 🟢 ein Bericht erhält nur dann `OK`, wenn automatische Prüfungen und alle sichtbaren Bestätigungen für Referenzlayout, Tastaturfokus und Zoom grün sind.
- 🟡 die tatsächliche sichtbare Abnahme muss weiterhin auf dem realen Kubuntu/KDE-X11-Zielrechner erfolgen; Offscreen-CI ersetzt sie bewusst nicht.

Start der realen Endabnahme:

```bash
bash kubuntu_abnahme.sh
```

## Iteration 11 – PySide6-Referenzdashboard

- 🟢 gesamte produktive GUI auf **PySide6 6.11.2** umgestellt; PyQt6/PySide6 werden nicht gemischt.
- 🟢 Dashboardtitel: **Provoware-Datenbank-Dashboard 2026**.
- 🟢 Layout an den Referenzentwurf angeglichen: kompakter Header, Schnellkacheln, einklappbare linke Navigation, schmale „Zuletzt bearbeitet“-Zeile, 2×2-Hauptkarten, Statusleiste.
- 🟢 **Dark Orange Industrial** mit dunklem Blau/Schwarz, Orange `#FF9800`, feinen Konturen und kompakten Abständen zentral definiert.
- 🟢 Recovery aus der Startfläche entfernt und **genau einmal** als linker Navigationspunkt geführt.
- 🟢 Songeditor, Songbibliothek, Recovery und Startanzeige ebenfalls auf PySide6 migriert.
- 🟢 Referenzlayout wird zusätzlich mit Qt-Offscreen-GUI-Tests auf Struktur, Proportionen und „kein Tkinter in produktiver GUI“ geprüft.

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

Der Schnellstart legt bei Bedarf `.venv` an, installiert exakt `PySide6==6.11.2`, prüft den Startunterbau und öffnet anschließend die Anwendung unter Prozesswache.

## Dashboard

Die Hauptansicht orientiert sich am Provoware-Referenzentwurf:
- Schnellkacheln für Songtexte und geplante Module,
- einklappbare linke Navigation,
- Entwickler-Schnellinfo,
- letzte bearbeitete Songs,
- 2×2-Hauptfläche mit **Workflow Übersicht**, **DB-Eingaben**, **Funktionen**, **Systemanwendungen**,
- Recovery nur unter `Werkzeug → Recovery`.

Geplante, noch nicht freigegebene Module werden sichtbar dargestellt, führen aber nur zu einem verständlichen Hinweis und verändern keine Daten.

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

Sie umfasst Logiktests, echte PySide6-Offscreen-GUI-Tests, Referenzlayoutprüfung, Kubuntu-Abnahmelogik einschließlich echtem Temp-SIGTERM-Wächtertest, ENOSPC-/EROFS-Simulation, Release-Manifest, Headless-Start und vollständigen Restore.
