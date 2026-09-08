# TODO – TOOL_2026_Multi

Stand: 2026-09-08

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
- 🟢 Zoom gilt gemeinsam für Dashboard, Songeditoren, Songbibliothek und Recovery.

## Iteration 14 – profilbasierte DB-Eingaben

- 🟢 Profile HardTechno, HipHop/Rap und Hörspiele als sofort nutzbare Startprofile.
- 🟢 getrennte Werte für Genres, Stimmungen, Stil, Stimme und Besonderheiten.
- 🟢 Profil- und Kategorienverwaltung in eigener PySide6-Oberfläche.
- 🟢 Profilauswahl direkt in der DB-Karte des Dashboards; Auswahlfelder werden passend befüllt.
- 🟢 neue Profile/Werte speicherbar; Duplikate werden verhindert; Entfernen verlangt Bestätigung.
- 🟢 atomare JSON-Speicherung unter `daten/profile/db_profile.json`; Startprofile erzeugen ohne Änderung keine Nutzerdatendatei.

## Nächste Fachiterationen

1. 🔴 Todo-Liste mit Terminierung, Abhaken und Archiv.
2. 🔴 Kalender mit Tag/Woche/Monat/Jahr, Terminen und Erinnerungen.
3. 🟡 reale Kubuntu/KDE-X11-Sichtabnahme mit `bash kubuntu_abnahme.sh` abschließen.
