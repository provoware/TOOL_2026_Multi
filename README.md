# TOOL_2026_Multi

> **Status:** 🟡 Ausführbarer Kern mit PySide6-Referenzdashboard und vorbereiteter realer Kubuntu/X11-Endabnahme · **Version:** 0.13.1 · **Stand:** 2026-09-08

## Iteration 17 – Prozess- und Schreibkonsistenz

- 🟢 Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien verwenden denselben zentralen atomaren Schreibweg.
- 🟢 eindeutige Tempdateien verhindern Kollisionen zwischen parallelen Schreibversuchen.
- 🟢 Dateiinhalt wird vor dem Ersetzen synchronisiert; der Verzeichniseintrag wird auf unterstützten Dateisystemen zusätzlich synchronisiert.
- 🟢 pro Projektordner ist nur eine schreibende Dashboard-Instanz erlaubt; ein zweiter Start wird verständlich und ohne falschen Absturzbericht beendet.
- 🟢 Todo und Kalender verwenden dieselbe lokale, zeitzonenlose Datum/Zeit-Semantik.
- 🟢 beschädigte Profilbestände mit doppelten Werten werden nicht still verändert, sondern als Fehler gemeldet.
- 🟢 ENOSPC-/EROFS-Simulation prüft jetzt direkt den produktiven Schreibweg.

## Iteration 16 – Kalender

- 🟢 Tages-, Wochen-, Monats- und Jahresansicht mit echten Zeitbereichen.
- 🟢 Termine mit Titel, optionaler Notiz, Beginn und Ende anlegen.
- 🟢 Erinnerungen zum Beginn sowie 5/15/30/60 Minuten oder 1 Tag vorher.
- 🟢 Erinnerungsprüfung alle 30 Sekunden, solange das Dashboard läuft – auch wenn das Kalenderfenster geschlossen ist.
- 🟢 Erinnerung wird erst nach Anzeige als erledigt markiert und dadurch nicht wiederholt.
- 🟢 atomare Speicherung unter `daten/kalender/termine.json`; keine destruktive Terminlöschung in dieser Iteration.
- 🟢 Kalender folgt derselben zentralen Zoom-/Schriftsteuerung wie die übrigen Module.

## Iteration 15 – Todo-Liste

- 🟢 Aufgaben mit Titel und optionaler Notiz anlegen.
- 🟢 optionalen Termin mit Datum und Uhrzeit speichern.
- 🟢 aktive Aufgaben nach Termin sortiert anzeigen.
- 🟢 Abhaken verschiebt die vollständige Aufgabe atomar ins getrennte Archiv; nichts wird gelöscht.
- 🟢 aktive und archivierte Aufgaben liegen zusammen unter `daten/todo/todo.json`, damit beim Verschieben kein Zwischenzustand zwischen zwei Dateien entstehen kann.
- 🟢 Todo folgt derselben zentralen Zoom-/Schriftsteuerung wie das restliche Dashboard.

## Iteration 14 – profilbasierte DB-Eingaben

- 🟢 Profile **HardTechno**, **HipHop/Rap** und **Hörspiele** als Startbestand.
- 🟢 profilweise Werte für Genres, Stimmungen, Stil, Stimme und Besonderheiten.
- 🟢 eigene Profile und Werte anlegbar, Duplikate werden abgefangen.
- 🟢 Werte werden erst nach Bestätigung entfernt.
- 🟢 Dashboard-Auswahl wird nach Profilwechsel direkt neu befüllt.
- 🟢 Speicherung atomar unter `daten/profile/db_profile.json`; Startprofile bleiben bis zur ersten Änderung nur im Speicher.

## Iteration 13 – Zoom und Schriftgröße

- 🟢 `Strg + Mausrad` ändert Zoom und Schriftgröße zentral.
- 🟢 `Strg++`, `Strg+-` und `Strg+0` bleiben verfügbar.
- 🟢 die Statusleiste bietet zusätzlich `A−`, Prozentanzeige und `A+`.
- 🟢 Dashboard, offene Songeditoren, Songbibliothek, Recovery, Profilverwaltung, Todo und Kalender folgen derselben Zoomstufe.
- 🟢 keine parallele Schriftgrößenkonfiguration; alles läuft weiter über die zentralen PySide6-QSS-Standards.

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

Der Schnellstart legt bei Bedarf `.venv` an, installiert exakt `PySide6==6.11.2`, prüft den Startunterbau und öffnet anschließend die Anwendung unter Prozesswache. Wird derselbe Projektordner versehentlich ein zweites Mal gestartet, verhindert der Einzelinstanz-Schutz den zweiten schreibenden Prozess.

## Dashboard

Die Hauptansicht orientiert sich am Provoware-Referenzentwurf:
- Schnellkacheln für Songtexte und geplante Module,
- einklappbare linke Navigation,
- Entwickler-Schnellinfo,
- letzte bearbeitete Songs,
- 2×2-Hauptfläche mit **Workflow Übersicht**, **DB-Eingaben**, **Funktionen**, **Systemanwendungen**,
- Planung mit **Todo-Liste** und **Kalender**,
- Recovery nur unter `Werkzeug → Recovery`.

### Zoom und Schrift

- `Strg + Mausrad hoch/runter` vergrößert/verkleinert.
- `A−` und `A+` in der Statusleiste machen dasselbe per Klick.
- `Strg+0` setzt auf 100 % zurück.
- verfügbare Stufen: 100, 125, 150, 175 und 200 %.

Geplante, noch nicht freigegebene Module werden sichtbar dargestellt, führen aber nur zu einem verständlichen Hinweis und verändern keine Daten.

## Kalender

Aufruf über `Planung → Kalender`.

Links wählen Sie ein Datum und legen Termine an. Rechts wechseln Sie zwischen:
- **Tag**,
- **Woche**,
- **Monat**,
- **Jahr**.

Die Bereiche werden tatsächlich neu berechnet. Ein Termin über Mitternacht erscheint deshalb in beiden betroffenen Tagesbereichen.

### Termin anlegen

Pflicht:
- Titel,
- Beginn,
- Ende.

Optional:
- Notiz,
- Erinnerung.

Das Ende muss nach dem Beginn liegen. Als Erinnerungsabstand stehen keine Erinnerung, Terminbeginn, 5/15/30/60 Minuten oder 1 Tag vorher zur Verfügung.

Datenpfad:

```text
daten/kalender/termine.json
```

### Erinnerungen

Solange das Provoware-Dashboard läuft, prüft es alle 30 Sekunden auf fällige Erinnerungen. Das funktioniert auch bei geschlossenem Kalenderfenster. Nach der angezeigten Erinnerung wird der Termin atomar als bereits erinnert markiert.

Wenn das gesamte Dashboard geschlossen ist, läuft bewusst kein separater Linux-Hintergrunddienst. Erinnerungen bei vollständig geschlossenem Programm gehören nicht zum Umfang dieser Iteration.

## Todo-Liste

Aufruf über `Planung → Todo-Liste`.

- Titel ist Pflicht.
- Notiz ist optional.
- Termin kann über „Termin verwenden“ zugeschaltet werden.
- Aktive Aufgaben werden getrennt vom Archiv angezeigt.
- Beim Abhaken wird die Aufgabe nicht gelöscht, sondern vollständig in den Archivbereich derselben atomar geschriebenen JSON-Datei verschoben.

Datenpfad:

```text
daten/todo/todo.json
```

## Profil-DB

Aufruf über die DB-Navigation oder die Genres-Kachel. Die Dashboard-Karte besitzt eine Profilauswahl; profilabhängig werden Genres, Stimmungen, Stil, Stimme und Besonderheiten geladen.

Datenpfad:

```text
daten/profile/db_profile.json
```

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
- zentraler atomarer Dateiersatz für Profil, Todo, Kalender, Songs, Versionen und Exporte,
- eindeutige Tempdateien und Einzelinstanz-Schutz,
- automatische Versionsstände nur bei tatsächlichen Änderungen,
- Recovery-/Diagnose-/Restore-Kette.

## Vollprüfung

```bash
bash scripts/pruefen.sh --full
```

Sie umfasst Logiktests, Prozesskonsistenz- und Schreibfehlerprüfungen, echte PySide6-Offscreen-GUI-Tests einschließlich Zoom-, Profil-, Todo- und Kalender-Regressionsprüfung, Referenzlayoutprüfung, Kubuntu-Abnahmelogik einschließlich echtem Temp-SIGTERM-Wächtertest, ENOSPC-/EROFS-Simulation gegen den Produktionsschreiber, Release-Manifest, Headless-Start und vollständigen Restore.
