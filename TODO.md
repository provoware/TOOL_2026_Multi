# TODO – TOOL_2026_Multi

Stand: 2026-09-09

## Ampel

🟢 erledigt und geprüft · 🟡 umgesetzt, finale Abnahme offen · 🔴 offen · ⚫ blockiert

## Aktueller freigegebener Stand

### Iteration 20 – Repository-Hygiene

- 🟢 versionierten Projektbaum auf Laufzeit-, Sicherungs-, Temp- und lokale Artefakte geprüft.
- 🟢 unreferenziertes 2,05-MB-Root-Bild entfernt.
- 🟢 `.gitignore` und automatischen Repo-Hygiene-Test ergänzt.
- 🟢 Restore-spezifischen Rückfall des Git-Hygienetests ursächlich behoben.
- 🟢 Grundprüfung #337 einschließlich Vollprüfung und Restore-Gate erfolgreich.
- 🟢 veralteten, nicht mergebaren PR #2 geschlossen.
- 🟢 Hygiene-Patch über PR #21 sicher in `main` übernommen.
- 🟢 anschließender Status-Sync über PR #22 ebenfalls vollständig grün geprüft und übernommen.

## Iteration 21 – Laien-UX-Konsistenz

**Hauptziel:** Ein Nutzer ohne technisches Vorwissen muss erkennen können, wo er ist, was funktioniert, was nur geplant ist, was nach einem Klick passiert und was bei einem Fehler geschützt bleibt.

- 🟢 Oberfläche aus Nutzersicht auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft.
- 🟢 Song-Suche, `Programm beenden`, `Projekt-Notiz`, sichtbare Planungszustände und direkte Startwege vereinheitlicht.
- 🟢 Songbibliothek, Songeditor, Todo, Kalender, Profile, Recovery und Startanzeige laienfreundlich gehärtet.
- 🟢 PR #23 in `main` übernommen (`47a6124061268843d05d98ddadcb90066cc0d851`).
- 🟢 drei nachfolgend erkannte GUI-Testannahmen in Iteration 22 ursächlich korrigiert.

## Iteration 22 – Responsive Design und visuelle Härtung

- 🟢 Modern-Dark-/Amber-Design, Sans-Serif-Schrift, Fokus, Abstände, Tabellen, Scrollleisten und Splitter zentral modernisiert.
- 🟢 responsive Breitenstufen und dynamische Songeditor-/Bibliotheksverteilung umgesetzt.
- 🟢 GitHub-Grundprüfung #385: 75 Logiktests + 46 GUI-Tests erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, SHA-256 `c18e1ac25b8b2b43cf7c93d2c9dc8edf8b22dc9a521f3956c1d13d6cfae1d5de`.
- 🟢 PR #24 in `main` übernommen (`1f12951156a7ca86e5533f05a17ade4802c79543`).

## Iteration 23 – Zoom-Härtung 150–200 %

**Hauptziel:** Reale Überlagerungen und Abschneidefehler bei starkem Zoom ursächlich beseitigen.

- 🟢 Schriftzoom und Geometriezoom getrennt; Schrift bleibt vollständig 100/125/150/175/200 % skalierbar.
- 🟢 Geometriewachstum auf maximal 25 % und zusätzliche Breitenreserve auf maximal 10 % begrenzt.
- 🟢 reversiblen Hochzoom-Modus ab 175 % eingeführt; redundante Planungsübersichten werden platzsparend ausgeblendet.
- 🟢 produktive Karten, obere Modulkacheln und Theme-relevante Bedienelemente bleiben im Hochzoom erreichbar.
- 🟢 Regression für vollständigen Schriftzoom, begrenzte Geometrie und Rückkehr in den Normalmodus ergänzt.
- 🟢 Grundprüfung #419 einschließlich Vollprüfung und Restore-Gate erfolgreich.
- 🟢 PR #26 sicher in `main` übernommen (`80544ad8cfd13452f35f9218247570f65beb8b05`).

## Iteration 24 – Barrierefreiheit und Farbthemes

**Hauptziel:** Tastatur-, Screenreader- und Sehzugänglichkeit verbessern und mehrere kontrastgeprüfte Farbthemes anbieten, ohne einen neuen Daten- oder Speicherpfad einzuführen.

### Umsetzung

- 🟢 vier zentrale Themes implementiert: `Amber`, `Türkis`, `Lila`, `Kontrast`.
- 🟢 Theme-Schalter automatisch im Dashboard-Statusbereich integriert.
- 🟢 Theme-Wechsel wirkt sitzungsweit auf alle geöffneten Fenster; später geöffnete Fenster übernehmen das aktive Theme.
- 🟢 Theme-Auswahl ist tastaturbedienbar und explizit als `Farbtheme auswählen` für Screenreader benannt.
- 🟢 interaktive Buttons, Eingaben, Auswahlfelder, Listen und Tabellen erhalten zentral `Qt.StrongFocus`.
- 🟢 fehlende Accessible Names und Descriptions werden aus sichtbaren Beschriftungen, Platzhaltern und Tooltips ergänzt.
- 🟢 Hochkontrast-Theme mit Schwarz/Weiß, gelbem Akzent und 3-px-Fokusrahmen ergänzt.
- 🟢 Zustände bleiben zusätzlich durch Text, Symbole und gestrichelte Konturen erkennbar; Farbe ist nicht das einzige Signal.
- 🟢 vorhandene Zoom-Härtung bleibt erhalten; bei 175/200 % bleibt der Theme-Schalter sichtbar.
- 🟢 automatische WCAG-Kontrastprüfung für Kernfarben aller vier Themes mit mindestens 4,5:1 ergänzt.
- 🟢 keine Theme-Datei und keine Änderung von Nutzerdaten oder Speicherformaten.

### Abnahme

- 🟢 Vorprüfung #428 für den Produktions-/Teststand vollständig erfolgreich.
- 🟢 finaler PR-Head `d750b98e0d98d7abe0441930f9ea52f0e0e85065` in Grundprüfung **#440** vollständig erfolgreich.
- 🟢 **75 Logik-/Regressionstests** erfolgreich.
- 🟢 **50 PySide6-GUI-Tests** einschließlich Theme-, Accessibility-, Zoom- und Responsive-Regressionen erfolgreich.
- 🟢 Release-Manifest mit **36 freigegebenen Betriebsdateien** erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, finale Restore-SHA-256 `ef1fd94f7a3a421416935373a213bba696407c80b441cf5a8108d22ea11c880f`.
- 🟢 PR #27 per Squash-Merge sicher in `main` übernommen.
- 🟢 resultierender Main-Commit: `234f2f5279dc5b6e6d334010da701d3a53ad6ebb`.

## Iteration 25 – Laptop-Kompaktlayout

**Hauptziel:** Die reale 1366×768-Laptopansicht bei 125/150 % entzerren, ohne die bereits gute große Ansicht zu verändern.

### Umsetzung

- 🟢 eigener, reversibler Laptop-Kompaktmodus ausschließlich für das Dashboard ergänzt.
- 🟢 Aktivierung nur bei knapper Höhe, Fensterbreite unter 1450 px und 125/150 % Zoom.
- 🟢 redundante geplante Navigation und die beiden reinen Planungskarten werden nur in diesem Modus ausgeblendet.
- 🟢 Songtexte, Genres/Vorgaben, Todo, Kalender, Fehlerhilfe, alle sieben oberen Modulkacheln, Zoom und Farbtheme bleiben erreichbar.
- 🟢 Profilkopf und Hilfstexte werden auf knapper Fläche verkürzt; die große Ansicht stellt die vollständigen Beschriftungen automatisch wieder her.
- 🟢 zentrale Responsive-/Theme-/Zoom-Engine selbst bleibt unverändert.
- 🟢 Regression für 1366×768 bei 125 % sowie Rückkehr auf 1594×926 ergänzt.
- 🟢 keine Nutzerdaten-, Speicher-, Backup- oder Restore-Logik verändert.

### Abnahme

- 🟡 finaler Branch wird vollständig per Grundprüfung einschließlich GUI-Regression und Vollprojekt-Restore geprüft.
- 🔒 kein Merge vor vollständig grünem finalem Gate.

## Danach

1. 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme mit `bash kubuntu_abnahme.sh` durchführen, besonders 1366×768 bei 125/150 %, zusätzlich 175/200 % und das Theme `Kontrast`.
2. 🔴 verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs ausdrücklich nicht auf Dateiersatz umstellen.
3. 🔴 anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

## Geplante Produktbereiche

Noch nicht freigegeben und deshalb in der Oberfläche sichtbar als `In Planung` markiert:

- Hörspiele
- Blogartikel
- Prompts
- GitHub-Repositories als eigenes Dashboardmodul
- Genre-Zufall
- Reimfinder
- Dateisuche
- Textinhalt-Suche
- Trefferliste
- Duplikatprüfer

Abgeschlossene Detailhistorie steht im `CHANGELOG.md` und in `docs/ITERATION*.md`; sie wird bewusst nicht mehrfach gepflegt.
