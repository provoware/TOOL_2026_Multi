# TODO – TOOL_2026_Multi

Stand: 2026-09-09

## Ampel
🟢 erledigt und geprüft · 🟡 teilweise · 🔴 offen · ⚫ blockiert

## Iteration 9 – Songbibliothek vervollständigen

- 🟢 freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags.
- 🟢 kombinierbare Filter für Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten.
- 🟢 Favoriten im Songeditor speicherbar und in der Bibliothek filterbar.
- 🟢 Bearbeitungsstatus Idee, Entwurf, Überarbeitung, Fertig integriert.
- 🟢 Sortierung nach zuletzt bearbeitet, Titel, Genre, Tags und Status; Gruppierung nach Genre, Tags und Status.
- 🟢 Versionswiederherstellung nur nach Vorschau; aktueller Stand wird unmittelbar davor automatisch als neuer Versionsstand gesichert.
- 🟢 fremde Versionspfade werden abgewiesen; ältere 0.7.0/0.8.0-Songs bleiben lesbar.

## Iteration 10 – CI-Wartung

- 🟢 `actions/checkout` von `v4` auf `v7.0.1` aktualisiert; keine fachliche Laufzeitfunktion verändert.

## Iteration 11 – PySide6-Referenzdashboard

- 🟢 gesamte produktive GUI auf PySide6 6.11.2 migriert.
- 🟢 Referenzdashboard, einzelne Recovery-Navigation und vollständige CI-/Restore-Abnahme.

## Iteration 12 – reale Kubuntu/X11-Endabnahme vorbereiten

- 🟢 eigener PySide6-Abnahmeassistent mit Klickstart, X11-Erkennung und isoliertem SIGTERM-Test.
- 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner steht weiterhin aus.

## Iteration 13 – Zoom und Schriftgröße

- 🟢 `Strg + Mausrad`, `Strg++`, `Strg+-`, `Strg+0` sowie A−/A+ umgesetzt.
- 🟢 Zoom gilt gemeinsam für Dashboard, Songeditoren, Songbibliothek, Recovery, Profilverwaltung, Todo und Kalender.

## Iteration 14 – profilbasierte DB-Eingaben

- 🟢 Profile HardTechno, HipHop/Rap und Hörspiele als sofort nutzbare Startprofile.
- 🟢 getrennte Werte für Genres, Stimmungen, Stil, Stimme und Besonderheiten.
- 🟢 Profil- und Kategorienverwaltung in eigener PySide6-Oberfläche.
- 🟢 Profilauswahl direkt in der DB-Karte des Dashboards; Auswahlfelder werden passend befüllt.
- 🟢 neue Profile/Werte speicherbar; Duplikate werden verhindert; Entfernen verlangt Bestätigung.
- 🟢 atomare JSON-Speicherung unter `daten/profile/db_profile.json`; Startprofile erzeugen ohne Änderung keine Nutzerdatendatei.

## Iteration 15 – Todo-Liste

- 🟢 Aufgabe mit Pflicht-Titel und optionaler Notiz anlegbar.
- 🟢 optionaler Termin mit Datum und Uhrzeit.
- 🟢 aktive Aufgaben nach Termin sortiert in eigener Ansicht.
- 🟢 Abhaken verschiebt die vollständige Aufgabe in derselben atomaren Transaktion ins Archiv.
- 🟢 Archiv ist getrennt sichtbar; beim Abhaken wird nichts gelöscht.
- 🟢 gemeinsamer Bestand unter `daten/todo/todo.json`, atomar mit Tempdatei, `fsync` und `os.replace`.
- 🟢 Todo ist unter `Planung → Todo-Liste` erreichbar und folgt der zentralen Zoomsteuerung.

## Iteration 16 – Kalender

- 🟢 echte Tagesansicht für den gewählten Kalendertag.
- 🟢 Wochenansicht von Montag bis zum folgenden Montag.
- 🟢 Monatsansicht vom ersten Tag bis zum ersten Tag des Folgemonats.
- 🟢 Jahresansicht vom 1. Januar bis zum 1. Januar des Folgejahres.
- 🟢 Termine mit Titel, optionaler Notiz, Beginn und Ende anlegbar; Ende muss nach Beginn liegen.
- 🟢 optionale Erinnerungen: Terminbeginn, 5/15/30/60 Minuten oder 1 Tag vorher.
- 🟢 Erinnerungsprüfung alle 30 Sekunden, solange das Dashboard läuft, auch bei geschlossenem Kalenderfenster.
- 🟢 Erinnerung wird erst nach Anzeige atomar als erledigt markiert; keine Wiederholungsmeldung desselben Termins.
- 🟢 Kalenderdaten atomar unter `daten/kalender/termine.json`; in dieser Iteration keine destruktive Terminlöschung.
- 🟢 Kalender ist unter `Planung → Kalender` erreichbar und folgt der zentralen Zoomsteuerung.

## Iteration 17 – Prozess- und Schreibkonsistenz

- 🟢 Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien verwenden denselben zentralen atomaren Schreibweg.
- 🟢 eindeutige Tempdateien statt fester `.tmp`-Namen verhindern Kollisionen paralleler Schreibversuche.
- 🟢 Dateiinhalt wird vor dem Ersetzen synchronisiert; Verzeichniseintrag wird auf unterstützten Dateisystemen zusätzlich synchronisiert.
- 🟢 zweite schreibende Dashboard-Instanz pro Projektordner wird mit `QLockFile` kontrolliert blockiert.
- 🟢 kontrollierter Mehrfachstart erzeugt keinen falschen Absturzbericht des Prozesswächters.
- 🟢 Todo- und Kalendertermine verwenden dieselbe lokale, zeitzonenlose Datum/Zeit-Semantik.
- 🟢 beschädigte Profilbestände mit doppelten Werten werden nicht mehr still verändert, sondern als Fehler gemeldet.
- 🟢 ENOSPC-/EROFS-Simulation prüft den echten Produktionsschreiber.

## Iteration 18 – Diagnose-I/O-Konsistenz

- 🟢 Diagnose-ZIP verwendet eindeutige Tempdatei, Datei-`fsync`, atomaren Replace und bestmöglichen Verzeichnis-`fsync`.
- 🟢 SHA-256-Begleitdatei nutzt den zentralen atomaren Textschreiber.
- 🟢 schneller Mehrfachexport erhält durch Mikrosekunden eindeutige Zielnamen.
- 🟢 Regression für eindeutige Dateinamen und Replace-Fehler ergänzt.
- 🟢 GitHub-Grundprüfung inklusive `scripts/pruefen.sh --full` und Restore-Gate erfolgreich bestätigt.

## Nächste Freigabepunkte

1. 🟡 reale Kubuntu/KDE-X11-Sichtabnahme mit `bash kubuntu_abnahme.sh` abschließen.
2. 🔴 nächster separater Konsistenz-Slice: Backup- und Berichtsschreiber auf dieselben Temp-/fsync-/Fehlerregeln prüfen; Append-Logs nicht fälschlich auf Dateiersatz umstellen.
