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

- 🟢 gesamte produktive GUI von Tkinter auf **PySide6 6.11.2** migriert und durch vollständige CI-/Restore-Abnahme belegt.
- 🟢 Dashboardstruktur an den Provoware-Referenzentwurf angeglichen: kompakter Header, Schnellkacheln, einklappbare Navigation, „Zuletzt bearbeitet“, 2×2-Karten, Statusleiste.
- 🟢 Dark-Orange-Industrial-Farbwelt zentral umgesetzt; Kartenstruktur und Proportionen werden automatisiert gegen Referenzmerkmale geprüft.
- 🟢 Recovery aus der Hauptfläche entfernt und genau einmal unter `Werkzeug → Recovery` geführt.
- 🟢 Songeditor, Songbibliothek, Recovery und Startanzeige auf PySide6 umgestellt; bestehende Datenlogik bleibt unverändert.
- 🟢 39 Logik-/Sicherheitstests, 20 PySide6-GUI-/Referenztests und vollständiges Restore-Gate erfolgreich.

## Iteration 12 – reale Kubuntu/X11-Endabnahme vorbereiten

- 🟢 eigener PySide6-Abnahmeassistent mit Klickstart angelegt.
- 🟢 echte X11-Erkennung; Wayland oder fehlendes `DISPLAY` werden nicht still akzeptiert.
- 🟢 echter SIGTERM-/Prozesswächtertest läuft ausschließlich in Tempdaten.
- 🟢 TXT-/JSON-Abnahmebericht bleibt ohne sichtbare Bestätigung ausdrücklich `NICHT_VOLLSTAENDIG`.
- 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner steht noch aus; sie kann durch GitHub-Offscreen-CI nicht ersetzt werden.

## 2 nächste Schritte

1. 🔴 `bash kubuntu_abnahme.sh` auf dem realen Kubuntu/KDE-X11-Zielrechner ausführen und Layout, Fokus und Zoom sichtbar bestätigen.
2. 🟡 nach dieser realen Abnahme das nächste Fachmodul des Multitools einzeln priorisieren und auf dem einheitlichen PySide6-Dashboard ergänzen.
