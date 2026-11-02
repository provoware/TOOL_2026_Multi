# TODO – TOOL_2026_Multi

**Verbindliche Abschlussreihenfolge:** Erst sämtliche vereinbarten Funktionen entwickeln, Fehler beheben, optimieren, erweitern und vollständig technisch prüfen; die **persönliche Nutzer-Endabnahme erfolgt als letzter Schritt**. [Aktive Abschluss-Gates am Dateiende](#verbindliche-abschluss-gates--nutzer-endabnahme-ist-letzter-schritt-01112026). Ältere offene Kästchen nicht als 1:1 fehlende Funktionen zählen; Status am aktuellen `main` gegen Code und Tests verifizieren.


<!-- PV_UX26_SCREENSHOT_AUDIT_20261101 -->
## Screenshot-Anforderungen 01.11.2026 – verbindliche nächste Umsetzungspakete

**Quelle und Akzeptanz:** [Issue #161](https://github.com/provoware/TOOL_2026_Multi/issues/161) · [ausführlicher ausführbarer Auftrag](docs/PROVOWARE_UI_AUFTRAG_2026_11_01.md). **Noch nicht abgenommen:** Ein Entwicklungszweig und vorbereitete Tests zählen nicht als erfolgreiche Integration.

- [x] 2026-11-01 | P0 Navigation PV-UX26-01 | Untere Links vollständig scrollbar machen, festen Kopf erhalten | prüfen: Regression in tests/test_navigation_scroll_gui.py, alle Zoom- und Kompaktzustände, PR- und main-CI | fertig wenn: kein Menüpunkt bei kleiner Fensterhöhe abgeschnitten und Test auf freigegebenem main erfolgreich.
- [ ] 2026-11-01 | P1 Kacheln PV-UX26-02 | Hohe sieben Kacheln kompakter und dynamisch umbrechend auslegen | prüfen: Textbreite und Klickflächen bei 100–200 % | fertig wenn: alle Einstiege ohne Überlagerung erreichbar.
- [ ] 2026-11-01 | P1 Kopf/Notiz PV-UX26-03 | Projektnotiz aus eigener Hauptzeile in gegliederten Header verlegen | prüfen: sichere Speicherung, lange Notiz, 200 %, Navigation per Tab | fertig wenn: Notizen ohne Datenverlust und übergroße Mindestbreite bearbeitbar.
- [ ] 2026-11-01 | P1 Bereichsgrößen PV-UX26-04 | Horizontale und vertikale Griffe, Reset und dynamische Mindestgrößen ergänzen | prüfen: 800×600, 1366×768, 1600×900, Tastatur und Zoom | fertig wenn: alle Pflichtfunktionen erreichbar bleiben.
- [ ] 2026-11-01 | P1 Daten-Schnelleingabe PV-UX26-05 | Profil → Kategorie → kommagetrennte Werte → Dubletten-Vorschau → atomar speichern | prüfen: vorhandene Namen, Unicode, ungültige Eingabe, unveränderte Altprofile, gemeinsame Zufallsquelle | fertig wenn: jeder neue Wert in bestehenden Modulen sichtbar und vor Dopplungen geschützt.
- [ ] 2026-11-01 | P1 Themes PV-UX26-06 | Unterschiedliche Flächenfarben, Text/Input/Placeholder/Aktion/Fokus getrennt gestalten | prüfen: WCAG-2.2-Kontraste automatisch pro Theme und Zustand | fertig wenn: Texte, Grenzen und Status auch ohne Farbe erkennbar sind.
- [ ] 2026-11-01 | P1 Einstellungen PV-UX26-07 | Menüleiste und eigenen, verständlichen Oberflächeneinstellungen-Dialog anlegen | prüfen: Speicherweg separat von Nutzerdaten, Zurücksetzen, Zoom, Tastatur | fertig wenn: alle UI-Optionen zentral und laienverständlich erreichbar.
- [ ] 2026-11-01 | P1 rechte Leiste PV-UX26-08 | Schnellaktionen oben und Favoriten darunter ein-/ausklappbar anzeigen | prüfen: kompakte Ansicht, Tastatur, optional automatische Buttongröße | fertig wenn: Bedienung in jeder Größe ohne verdeckten Hauptbereich möglich.
- [ ] 2026-11-01 | P1 Textbuttons PV-UX26-09 | Karten kompakt farblich gruppieren und Sterne/Favoriten ohne Datenverlust ergänzen | prüfen: Altbestand, Kopieren, Variante, Import/Export, Farbkontraste | fertig wenn: Favoriten aus derselben Datenquelle in rechter Leiste erscheinen.
- [ ] 2026-11-01 | P1 Tastatur PV-UX26-10 | Tab-Folge, sichtbaren Fokus, eindeutige Nutzereingabe/Platzhalter sichern | prüfen: nur Tastatur, 150/200 %, Escape/Enter und Screenreader-Labels | fertig wenn: alle Kernwege ohne Maus funktionieren.
- [ ] 2026-11-01 | P1 Ereignisse PV-UX26-11 | Mindestens fünf letzte Ereignisse mit Uhrzeit und Schweregrad anzeigen | prüfen: nur bestehendes EventLogger-API, Datenschutz, leere und sehr lange Meldungen | fertig wenn: letzte fünf Einträge ohne Abdeckung lesbar.
- [ ] 2026-11-01 | P2 Katalog PV-UX26-12 | Breite fachlich geprüfte Profilstruktur und Ziel 100 eindeutige Werte je Kategorie/Profil | prüfen: Quellen, Taxonomie, Duplikate, Import-Freigabe, atomare Sicherung | fertig wenn: Zielzahl mit echten geprüften Begriffen erfüllt, andernfalls belegter Fehlbestand.
- [ ] 2026-11-01 | P1 Gesamtqualität PV-UX26-13 | Messbare UI-/Daten-/Recovery-/CI-Nachweise für jede Teilfreigabe sammeln | prüfen: aktueller SHA, PR und main getrennt, CI, Changelog/Manifest | fertig wenn: keine offenen Sicherheits- oder Bedientests vor Freigabe.

**Nachweise 01.11.2026:** PV-UX26-01 via PR #162 auf main `4748363403bbc4f459fb3eca74dc82abbc9e42d1`; PR-CI #41305351643 und separate main-CI #41305861757 erfolgreich, vier neue GUI-Tests; die praktische Kubuntu-Endabnahme bleibt später. PV-UX26-06: Eingabefeldrand-Kontrastkorrektur als eigener Prüfzweig vorbereitet, noch **nicht** als Gesamt-Theme-Überarbeitung erledigt; übrige Farbzustände und Themes folgen.

**Abhängigkeit:** vorhandene PV-UI-01/02, übriger Modulplan und Freeze unverändert gültig; Aufgaben werden pro Iteration priorisiert, nicht in einem unprüfbaren Gesamtpatch zusammengeführt.

---


Stand: 2026-10-19 · Ergänzung 2026-11-01

<!-- README_AUDIT_20261101 -->
## 📌 Aktueller Dokumentations- und Integrationsstand · 01.11.2026

**Verbindlicher Modulplan bleibt unverändert.** Die folgenden Punkte dokumentieren die Repository-Prüfung; sie eröffnen **keine** neuen Funktionsaufträge.

- [x] 2026-11-01 | Dokumentation | README um dreistufigen Linux-Kurzstart mit echten Kopierbefehlen und Fehlerhilfe ergänzt | prüfen: `README.md`, Commit `79f690ef52a8` | fertig wenn: vollständiger alter README-Inhalt erhalten und neue Anleitung am Anfang sichtbar.
- [ ] 2026-11-01 | Qualität | Hauptzweig nach reiner Dokumentationsänderung prüfen | prüfen: GitHub-Qualitätslauf für den endgültigen main-Commit; bestehende dokumentationsbezogene Prüfungen | fertig wenn: Prüfläufe auf genau diesem Stand erfolgreich.
- [ ] 2026-11-01 | Bestehender Plan | Noch offene Funktionen nach `docs/MODULPLAN_2026.md` und realem Teststand priorisieren | prüfen: Source, CI, bisherige Nachweise | fertig wenn: jedes noch offene Modul nachvollziehbar als offen, geprüft oder blockiert ausgewiesen ist.
- [ ] 2026-11-01 | Abschluss | Die einmalige vollständige Kubuntu-Sichtabnahme ausschließlich am finalen, unveränderten Kandidaten durchführen | prüfen: native Wayland-Oberfläche, 800×600, 200 %, Datenrückkehr | fertig wenn: echte Endabnahme protokolliert; keine vorgezogene Release-Freigabe.

---


> **Neu (22.10.2026):** [Priorisierter Architektur-, Sicherheits- und Interoperabilitätsaudit mit 30 Befunden, Wiederverwendung, Nutzerabläufen, Tests und Next Queue](#neuer-prüf--und-entwicklungsbedarf--nutzerinteroperabilität-audit-vom-22102026). Der bestehende Plan bleibt eingefroren; neue Punkte stehen **am Ende** dieser Datei und sind noch nicht umgesetzt.

## Aktueller Entwicklungsauftrag – einzige verbindliche Kurzliste

Die **[Modulübersicht](docs/MODULPLAN_2026.md)** ist der verbindliche Gesamtplan. Die vielen weiter unten stehenden Kontrollkästchen sind historische Arbeitsprotokolle und dürfen nicht als aktuelle, voneinander unabhängige To-dos addiert werden.

- [ ] **PV-UI-01/02 und Songeditor 200 %:** Lokaler Umsetzungskandidat vom 26.10.2026 mit gemessenen Label-/Auswahlbreiten, einblendbaren Nebenbereichen und erweitertem UI-Shadow-Gate. 70 Offscreen-Fälle ohne Textüberlauf, 59 gezielte GUI-Tests erfolgreich; vollständige GitHub-CI und Integration noch nicht erfolgt. Keine Datenmigration.
- [x] PR #83 als durch #87 überholte Layoutalternative schließen.
- [x] PR #88 (0.18.3) mit automatischer PR- und Hauptzweigprüfung übernehmen.
- [x] PR #89 (0.18.4) nach Bereinigung des gestapelten Zweigs und grüner PR-Prüfung übernehmen.
- [x] Ursprüngliche und neue Modulplanung in einer verbindlichen Statusmatrix zusammenführen.
- [x] 0.18.5 Link-Schnellstarter mit GUI, Daten-, Browser- und Release-Tests in `main` integriert (PR #90, GitHub-Prüflauf #1019).
- [x] Sicherheitsprototyp der Update-Slots und Rückkehr auf Altversion in PR #100 integriert (CI #1039 grün).
- [ ] Update-Manager produktiv vervollständigen: separate Kopierprobe für alte Programm-/Benutzerdaten als CI-Kandidat vorhanden, aber Schnellstart, Aktivierung und vollständiger Rückfall einer realen Altinstallation weiterhin gesperrt.
- [x] Grafischen Modulbaukasten mit sicheren Datenvorlagen und Vorschau in PR #101 integriert (CI #1041 grün).
- [ ] Formularmodule können mit Einwilligung bereits eigene Datensätze im Modulbaukasten öffnen (CI-Kandidat); sichere Ausführung fremder Plugins und signierte Pakete fehlen weiterhin.
- [x] Wikimodul mit Artikeln, Sammlungen, Verweisen, Versionen und GUI über Integrations-PR #97 in main übernommen (CI #1031 und #1033 erfolgreich).
- [x] Entwicklungspool mit Status, Arbeitsordnern, Kopien und ZIP in PR #102 integriert (CI #1043 grün).
- [x] Audioplayer, Bildvorschau und Video-/Slideshow-Basismodule in PR #103 integriert (PR-CI #1046 erfolgreich).
- [ ] Video: FFprobe integriert (PR #105). Videowarteschlange und Ein-/Ausblendeffekte in Iteration 66 an die GUI gekoppelt (Prüfkandidat); echte Bild-zu-Bild-Übergänge als CI-Kandidat ergänzt; für die Stapelwarteschlange sind Übergangstypen weiterhin nicht speicherbar. Mehrfach-Batch-Nachweis und visuelle Ergebnisvergleiche folgen.
- [x] PR #94/#95/#96 konfliktfrei über PR #97 integriert; PR-CI #1031 und main-CI #1033 erfolgreich, Vorläufer-PRs geschlossen.
- [x] Programmsicherung samt isolierter Rückkehrkopie und die echte Modulsteuerung über PR #98 integriert; PR-CI #1035 erfolgreich.
- [ ] Erst nach Abschluss **aller** vereinbarten Module: vollständige praktische Kubuntu-/Plasma-Gesamtabnahme und Veröffentlichung.

**Grundregel:** Während des Modulaufbaus bleiben die automatisierten Vollprüfungen aktiv. Die bereits erfolgte positive Basisabnahme wird nicht ständig wiederholt; die nächste vollständige **manuelle** Kubuntu-Abnahme ist ein Abschlussmeilenstein.

## Aktuelle Übersicht – zuerst lesen

**Nutzerpriorität:** Entwicklungsarbeit ohne manuelle Abnahme zuerst. Zielrechner-Abnahmen und Veröffentlichung bleiben bis zum Ende aller Module offen; automatische Schutzprüfungen laufen weiter. PR #88/#89, #97 (Update-Probe, Modulverträge, Wiki) und #98 (Checkpoint, Modulschalter) sind in `main` integriert. Dies ist weiterhin kein öffentliches Release.

**Erledigt und durch GitHub geprüft**
- [x] Texteditor: vor dem Verlassen eines veränderten Textes Speichern, Verwerfen oder Abbrechen anbieten (PR #57).
- [x] Dateinamen-Kollisionen bei Song- und allgemeinen Textdateien absichern (PR #57).
- [x] Profilwahl und Bearbeitung im Dashboard ohne Überlagerung anordnen (PR #57).
- [x] Navigation bei starker Vergrößerung korrigieren (PR #58–61).
- [x] Automatische Oberfläche: 60 Kombinationen / 180 Fenster, 0 Fehler, 0 Warnungen (GitHub #39065993768).

**Noch offen – vor einer breiten Veröffentlichung**
- [ ] Die Anzeige und Bedienung auf einem echten Kubuntu-26.04-/Plasma-Wayland-Rechner vollständig durchgehen.
- [x] Eigenständige Sicherung und isoliert geprüfte Wiederherstellung persönlicher Daten umgesetzt; siehe `docs/DATENSICHERUNG.md` (lokale Tests, kein automatisches Ersetzen des Arbeitsbestands).
- [ ] UI-Schattenprüfung erst nach bewusster Kalibrierung als blockierende Pflichtprüfung schalten.
- [x] Startprogramm bei beschädigter Umgebung und fehlenden Paketen trotz gültigem Marker absichern; sechs isolierte Starttests erfolgreich.
- [x] Versionskennung 0.18.3 im Manifest und Fenstertitel sowie Freigabeunterlagen als lokalen Kandidaten vorbereiten.
- [ ] Kandidaten nach späteren Abnahmen tatsächlich veröffentlichen.

**Später geplante Funktionen**
- [x] Genre-Zufallsgenerator bereits umgesetzt; bisherigen Übersichtsstatus mit vorhandener Anwendung und Tests abgeglichen.
- [x] Zentrale Text-/Dateisuche mit Trefferliste, Vorschau, Abbruch und festen Schutzgrenzen umgesetzt; `docs/DATEISUCHE.md`.
- [ ] Sicherer Update-Manager mit Rückkehr zur vorherigen Version.

**Lesetipp:** Die längeren Iterationsabschnitte weiter unten sind historische Entwicklungsprotokolle. Dort noch offene Aufgaben können inzwischen durch die aktuelle Übersicht erledigt sein.


## Iteration 39 – Autonomous UI Quality Gate PRO (Shadow Mode)

- [x] zentrale Qt-unabhängige UI-Verträge für Raster, Geometrie, Kontrast und Mindestgrößen anlegen
- [x] kritische PR-Matrix mit 8 reproduzierbaren Fällen definieren
- [x] vollständige Main-/Release-Matrix mit 60 Kombinationen definieren
- [x] deterministisches Window-State-Fuzzing für Monitor-/Skalierungswechsel ergänzen
- [x] echte Dashboard-/Songbibliothek-/Songeditor-Prüfung im Offscreen-Shadow-Gate ergänzen
- [x] maschinenlesbare JSON-Evidenz, Markdown-Zusammenfassung und Raster-Diagnosebilder erzeugen
- [x] Shadow-Gate so integrieren, dass bestehende harte Release-Gates nicht blockiert werden
- [ ] Shadow-Ergebnisse über mehrere CI-Läufe kalibrieren und bestätigte Fehlalarme beseitigen
- [ ] nach mindestens drei sauberen Läufen ausgewählte Regeln zum Pflicht-Gate hochstufen

## Iteration 38 – Fensterführung und kleine Displays

- [x] Bibliothek→Editor→Bibliothek ohne gleichzeitigen Fensterstapel
- [x] Bildschirmbegrenzung und sichere Zentrierung für Songeditor/Songbibliothek
- [x] neutraler Eingaberand, Akzent nur im Fokus, Rot/Grün als Zustände
- [x] Platzhalterkontrast erhöhen
- [x] sichtbares `&` in Hilfe & Fehlerhilfe reparieren
- [x] Songeditor: einklappbare optionale Angaben und Kompaktmodus
- [x] Songbibliothek: einklappbare Filter/Sortierung/Gruppierung
- [x] portable, validierte Fensterzustände ergänzen
- [x] technischer Iteration-38-Gate #799: 113 Logiktests, 83 GUI-Tests, 48 Release-Dateien, nativer Wayland-Smoke, Restore und ZIP-Artefakte vollständig grün
- [ ] reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme bei 1366×768 und 125/150/175/200 % durchführen


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

- 🟠 erste Grundprüfung #464 deckte zwei begrenzte Rückfälle auf: fehlendes Testdouble für den neuen Startimport sowie eine ungewollte Wiederherstellung der Planungskarten beim Übergang in den bestehenden 175/200-%-Hochzoom.
- 🟢 beide Ursachen minimal korrigiert; keine Erweiterung des Funktionsumfangs.
- 🟢 korrigierter Produktions-/Test-Head `d21799baa13562496b5e0821a17b1fb2c6cd89fe` in Grundprüfung #468 vollständig erfolgreich.
- 🟢 finaler Evidence-Sync-Head `d8f07560d4974708d8fa38ae57de4b1910bc536f` in Grundprüfung **#478** vollständig erfolgreich.
- 🟢 **75 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich.
- 🟢 Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich.
- 🟢 Headless-Start erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, finale SHA-256 `5ac25bbd0499d30ad1ace80f1b6ffa0faa6db70e24fec6e30a0d9095420ce825`.
- 🟢 PR #29 per Squash-Merge sicher in `main` übernommen.
- 🟢 resultierender Main-Commit: `1a64810fd2e202045666538f57054951e5099257`.

## Iteration 26 – Release- und Bericht-I/O-Härtung

**Hauptziel:** Verbleibende nicht-append Schreibwege vor dem nächsten vollständigen ZIP auf denselben atomaren Schutzvertrag bringen, ohne Nutzerdaten- oder Produktlogik zu verändern.

### Umsetzung

- 🟢 zentralen `atomic_publish_file()`-Schritt für fertig erzeugte Dateien ergänzt: Datei-`fsync`, atomarer Replace, bestmöglicher Verzeichnis-`fsync`, Temp-Cleanup.
- 🟢 Log-Quarantäne, Regressionstatus, menschenlesbare Ereignis-/Wächterberichte, Startstatus und Kubuntu-Abnahmeberichte auf den zentralen atomaren Textschreiber umgestellt.
- 🟢 Release-ZIP verwendet eindeutige Tempdateien und den zentralen Publish-Schritt; SHA-256-Begleitdatei wird atomar geschrieben.
- 🟢 Diagnose-ZIP verwendet denselben zentralen Publish-Schritt.
- 🟢 direkte Skriptstarts für Diagnose, Startstatus, Prozesswächter und Kubuntu-Abnahme gegen fehlenden Projektimport abgesichert.
- 🟢 `app/laptop_layout.py` und Iterationsdokumente 22–26 in der Vollständigkeitsprüfung nachgezogen.
- 🟢 Append-only Ereignislog und Projekt-Notiz bewusst nicht auf Dateiersatz umgestellt.
- 🟢 bestehende Restore-ZIP-Implementierung bewusst unverändert gelassen, da sie bereits denselben Schutz nachweist und gezielt regressionsgeprüft ist.

### Abnahme

- 🟢 erste vollständige Grundprüfung **#503** erfolgreich; Restore-SHA-256 `c7ff7f7e107d815918e9d52a84302bd245baa19f301cb3d4730ee5acff4b0806`.
- 🟢 finaler Version-/Evidence-Head `d386f9e848237ff400fc60c518f73645b6516cee` in Grundprüfung **#513** vollständig erfolgreich.
- 🟢 **81 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich.
- 🟢 Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich.
- 🟢 Headless-Start erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, finale SHA-256 `560b9d9ca46ec3e0964f03b385941782e18e892d734c1b5e208dd69c6d4b5bf3`.
- 🟢 PR #31 per SHA-geschütztem Squash-Merge in `main` übernommen.
- 🟢 resultierender Main-Commit: `00513bbaaee124da1e04a963aa70ce9e4757108e`.

## Iteration 27 – Menü-Übersicht und Laiennavigation

**Hauptziel:** Fertige Wege in der linken Navigation zuerst sichtbar machen und geplante Bereiche platzsparend bündeln, ohne Fachlogik oder Nutzerdaten zu verändern.

### Umsetzung

- 🟢 fertige Hauptwege unter **Direkt nutzbar** priorisiert: Songtexte, Genres & Vorgaben, Todo-Liste, Kalender, Fehlerhilfe.
- 🟢 redundanten sichtbaren Punkt `Alle Bereiche · geplant` aus der Nutzeransicht entfernt.
- 🟢 zehn geplante Bereiche unter **Noch nicht fertig** zusammengeführt und standardmäßig eingeklappt.
- 🟢 ein einziger Schalter blendet geplante Bereiche ein oder aus; bei geöffneter Planung werden sie in Kreativ & Inhalte, Dateien & Werkzeuge und Projekte gruppiert.
- 🟢 unnötige wiederholte `· geplant`-Texte in den Einzelzeilen entfernt.
- 🟢 Laptop-Kompaktmodus und 175/200-%-Hochzoom blenden die optionale Planung automatisch aus.
- 🟢 Menütexte in der zentralen Textregistrierung gepflegt; bestehende Aktionen werden wiederverwendet.
- 🟢 gezielte GUI-Regressionen für Standardansicht, Auf-/Zuklappen, Laptopmodus, Hochzoom, Rückkehr zur großen Ansicht und Accessibility ergänzt.
- 🟢 zwei während der CI aufgedeckte Qt-Synchronisationsrückfälle ursächlich behoben; Sichtbarkeit wird jetzt aus der aktuellen Geometrie statt aus einem veralteten Zwischenzustand abgeleitet.

### Abnahme

- 🟢 technischer Head `b129b47bb8123fc7ea49680f2fa921f457164c56` in Grundprüfung **#540** vollständig erfolgreich.
- 🟢 finaler 0.15.3-Head `9cd8101ba19c5e28b41fa7793d35860462d38864` in Grundprüfung **#554** erneut vollständig erfolgreich.
- 🟢 **81 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **38 Release-Betriebsdateien** und Headless-Start erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, finale SHA-256 `add4af04204e694427aa2332edea4136c2816e0c196676391a5763e044be3718`.
- 🟢 PR #34 per SHA-geschütztem Squash-Merge in `main` übernommen; Main-Commit `e7027e57c3c8709263b73543fd2b01be84e6639d`.

## Iteration 28 – Kubuntu 26.04 / native Wayland-Unterstützung

**Hauptziel:** Kubuntu 26.04 LTS mit KDE Plasma Wayland als offizielles Zielsystem prüfen und absichern, ohne den normalen Start künstlich auf ein einzelnes Qt-Backend festzunageln.

### Umsetzung

- 🟢 X11-only-Endabnahme auf Kubuntu 26.04 / Plasma Wayland umgestellt.
- 🟢 Abnahme prüft Linux, Ubuntu/Kubuntu-Basis 26.04, KDE/Plasma, `XDG_SESSION_TYPE=wayland` und `WAYLAND_DISPLAY`.
- 🟢 erzwungenes `QT_QPA_PLATFORM=xcb`/XWayland wird für die offizielle Wayland-Abnahme blockiert.
- 🟢 tatsächlicher Qt-Plattformname wird über `QApplication.platformName()` kontrolliert; nur natives `wayland*` gilt als Pass.
- 🟢 nativen Qt-Wayland-Smoke-Test `scripts/wayland_smoke.py` ergänzt.
- 🟢 CI startet dafür einen isolierten headless Weston-Compositor; bestehende Offscreen-GUI-Regressionsprüfung bleibt zusätzlich erhalten.
- 🟢 `schnellstart.sh` bleibt backend-neutral und setzt weder Wayland noch X11 künstlich.
- 🟢 reale Sichtabnahme prüft zusätzlich Laptoplayout 125/150 %, Hochzoom 175/200 %, Tastaturfokus, Kontrasttheme sowie Fenster-/Menü-/Eingabeverhalten unter Wayland.
- 🟢 keine Nutzerdaten-, Speicher-, Backup- oder Restore-Fachlogik verändert.

### Abnahme

- 🟢 technischer Head `a7f2c168ecc3f0a2310fbff874cea33d30793d25` in Grundprüfung **#567** vollständig erfolgreich.
- 🟢 finaler 0.16.0-Head `2536bd3183e39ad1566496a067b817dd3ad30b07` in Grundprüfung **#579** erneut vollständig erfolgreich.
- 🟢 **86 Logik-/Regressionstests** und **56 PySide6-GUI-Tests** erfolgreich.
- 🟢 nativer Qt-Wayland-Start unter isoliertem Weston in beiden vollständigen Abnahmen erfolgreich; Qt meldet Plattform `wayland`.
- 🟢 Release-Manifest mit **38 freigegebenen Betriebsdateien** erfolgreich.
- 🟢 Headless-Start erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, finale Feature-SHA-256 `23792d1c96db0b0fd61eaf74630593fbbf37578b64c4f82fd1f6644d2efa103e`.
- 🟢 PR #35 ausschließlich für den geprüften Head per SHA-geschütztem Squash-Merge in `main` übernommen.
- 🟢 resultierender Produkt-Main-Commit: `3b829e799536cc1464e760f77ac7c28295c6ea70`.
- 🟢 finaler Evidence-Sync über PR #36 vollständig mit Vollprüfung, nativem Wayland-Smoke und Restore geprüft und übernommen; resultierender Main `aeb4086e1d20f68a753e9a204ee8bf0d29ddf746`.

## Iteration 29 – Präsentationspolicy und Architekturhärtung

**Hauptziel:** Darstellungszustände zentral, deterministisch und Qt-unabhängig klassifizieren und die Vollständigkeit produktiver Runtime-Module im Release automatisch erzwingen.

### Umsetzung

- 🟢 neues reines Modul `app/presentation_policy.py` ohne Qt-Abhängigkeit eingeführt.
- 🟢 Laptop-, Breit- und Hochzoomzustand über unveränderlichen `PresentationState` zentralisiert.
- 🟢 Schwellenwerte für 125/150 %, 175 %, 1450 px, 820 px und 700 px als benannte Policy-Konstanten gebündelt.
- 🟢 `app/laptop_layout.py` verwendet die zentrale Policy; private Helfer bleiben nur als Kompatibilitätsadapter.
- 🟢 `app/navigation_ux.py` importiert keine private Laptopfunktion mehr und dupliziert `zoom >= 175` nicht mehr.
- 🟢 `app/ui_standards.py` verwendet nach der strengen Konsistenzrunde dieselben Policy-Konstanten für 1450 px und 175 % sowie die gemeinsame Zoomnormalisierung; keine Schwelle und keine Geometrie wurde verändert.
- 🟢 `compact < 1100 px` bleibt bewusst als eigene Responsive-Klasse lokal, weil er nicht dieselbe Semantik wie der Laptop-Kompaktmodus hat.
- 🟢 reine Grenzwerttests für 1366×768@125 %, 1594×926@125 %, 1450-px-Grenze, 175-%-Hochzoom, Mindestgröße und Nicht-Dashboard-Fenster ergänzt.
- 🟢 Release-Invariant ergänzt: jedes produktive `app/*.py`-Modul muss als `release=true` im Manifest stehen.
- 🟢 neuer Runtime-Pfad ist in Vollprüfung und Release-Manifest aufgenommen.
- 🟢 keine Nutzer-, Speicher-, Backup-, Restore- oder Produktfachlogik verändert.

### Analyse- und Abnahmestand

- 🟠 erste Grundprüfung **#598** blockierte korrekt, weil der neue Release-Invariant `app/presentation_policy.py` als noch fehlenden Release-Manifest-Eintrag erkannte; alle 56 GUI-Tests waren bereits grün.
- 🟢 Manifest-Lücke ursächlich behoben; der Schutztest bleibt dauerhaft aktiv.
- 🟢 korrigierter technischer Head `117aa0eee4e3422804506d9bc1c1fc50f75d4591` in Grundprüfung **#600** vollständig erfolgreich; Restore `OK`, SHA-256 `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`.
- 🟢 vollständig synchronisierter 0.16.1-Head `306eb551234882401d98114182b51c2ecdbdfdcb` in Grundprüfung **#612** vollständig erfolgreich: **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `78813816a492133dab8687112f80479bd7eff7309577ab2853833b9baf5b479f`.
- 🟢 PR #37 ausschließlich für den geprüften Head per SHA-geschütztem Squash-Merge übernommen; resultierender Produkt-Main `608f7236f68161436b5d77e6e4c907ff6c1aa1a0`.
- 🟢 anschließende strenge Single-Source-of-Truth-Prüfung fand noch zwei rohe gemeinsame Grenzen (`1450`, `175`) in `app/ui_standards.py`; isolierter Konsistenzhead `5d0eb33165bfe721a380912cd528981c51a88042` beseitigte nur diese Duplikation und vereinheitlichte die Zoomnormalisierung.
- 🟢 Grundprüfung **#616** für genau diesen isolierten Head vollständig erfolgreich: erneut **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start, nativer Qt-Wayland-Smoke und Vollprojekt-Restore `OK`; Restore-SHA-256 `f745cfd8ae287ecfe7b34340f695959317f7a19901dae3cee9131133d5f90c82`.
- 🟢 PR #38 mit exaktem Head-SHA-Schutz per Squash-Merge übernommen; resultierender Main `e74d0ddc45258dc51926c94662ab23303f80e5f2`.
- 🟢 Iteration 29 ist damit unter der strengeren Architekturdefinition technisch abgeschlossen; die reale sichtbare Zielsystemabnahme bleibt bewusst ein separates Projektgate.

## Iteration 30 – Codequalität der Log-Wartung

**Hauptziel:** Log-Wartung deterministischer, kohärenter und besser testbar machen, ohne Produkt- oder Nutzerdatenlogik zu verändern.

- 🟢 Zeitlogik pro Wartungsoperation auf einen UTC-Snapshot begrenzt.
- 🟢 Rotationsentscheidung als reine, dateisystemunabhängige Funktion getrennt.
- 🟢 Quarantäne-JSON auf den zentralen atomaren JSON-Schreiber umgestellt.
- 🟢 Archivsortierung gegen parallel verschwundene Dateien robuster gemacht.
- 🟢 Grundprüfung **#628**: 96 Logiktests, 56 GUI-Tests, 39 Release-Dateien, Headless-Start, nativer Wayland-Smoke und Restore `OK`.
- 🟢 Restore-SHA-256 `c45fa475055dfb1b5d3e5904321f4d967c96a3ea5d3f82bba46bdb6538ad574c`.
- 🟢 PR #40 gemergt; Main-Commit `20a9106616e4f32677c271906f345f02652b7cdd`.

## Iteration 31 – Fenster-Lebenszyklus zentralisieren

**Hauptziel:** Wiederholte Öffnen-/Aktivieren-/Aktualisieren-Logik der Dashboard-Nebenfenster in einen typisierten Helfer überführen.

- 🟢 generischen `_open_managed_window()`-Helfer eingeführt.
- 🟢 sichtbare Fenster werden zentral vorbereitet, aktiviert und aktualisiert.
- 🟢 bisherige Unterschiede bleiben erhalten: Kalender darf verborgenen Zustand wiederverwenden; Profile, Todo, Songbibliothek und Recovery behalten ihre bisherige Neuerzeugungssemantik.
- 🟢 drei deterministische Lebenszyklus-Regressionen ergänzt.
- 🟢 Grundprüfung **#633**: 96 Logiktests, 59 GUI-Tests, 39 Release-Dateien, Headless-Start, nativer Wayland-Smoke und Restore `OK`.
- 🟢 Restore-SHA-256 `8d6f15df599d92ad60be71fab18c171243cbdfbf5fb55e4d236d23cbec79819a`.
- 🟢 PR #41 gemergt; Main-Commit `c4df362e8518acab07d4aac987ce08b5ff7e60b6`.

## Iteration 32 – Managed-Window-Registry zentralisieren

**Hauptziel:** Alle aktuell verwalteten Dashboard-Fenster als gemeinsame Quelle für Erkennung, Zoom-Verteilung und selektiven Refresh führen.

- 🟢 `_managed_window_registry()` als Single Source of Truth eingeführt.
- 🟢 Ctrl+Mausrad-/Fenstererkennung und Zoom-Verteilung verwenden dieselbe Registry.
- 🟢 Dashboard-Refresh verwendet die Registry mit explizitem `refresh_when_visible`; automatisch aktualisiert werden unverändert Recovery, Todo und Kalender.
- 🟢 Songeditor-Sonderbehandlung bleibt als eigener Zoom-Adapter erhalten.
- 🟢 drei neue GUI-Regressionen prüfen Registry-Vollständigkeit, Zoom-Verteilung und unveränderten Refresh-Scope.
- 🟢 Grundprüfung **#638**: 96 Logiktests, 62 GUI-Tests, 39 Release-Dateien, Headless-Start, nativer Wayland-Smoke und Restore `OK`.
- 🟢 Restore-SHA-256 `64c3d081f652abcb29623375336c4d71b5ffd55ebce72e2c33cae64e83cef51b`.
- 🟢 PR #42 gemergt; technischer Main-Commit vor diesem Evidence-Sync: `a0032bc7977e21d830297828610d9b6d3ac68ea3`.

## Iteration 34 – Charakterfibel, Texteditor und gemeinsame Standards

**Hauptziel:** Zwei produktiv nutzbare Module hinzufügen und gemeinsame Daten-/UI-/Import-/Startstandards vereinheitlichen.

### Umsetzung

- 🟢 Charakterfibel mit atomarem Datenbestand, stabilen IDs, Suche/Bearbeitung und wiederverwendbaren Charakterreferenzen.
- 🟢 universeller Texteditor mit Titel→Dateiname, Haupttext, Abschlussnotizen, Versionierung, Autosave und Charakterbezug.
- 🟢 Genres, Stimmungen, Stil, Stimme und Besonderheiten akzeptieren Komma-Listen und speichern jeden bereinigten Wert einzeln; Dubletten werden verhindert.
- 🟢 Songtexteditor erlaubt eigene validierte Bereichsnamen zusätzlich zu den Standardbereichen.
- 🟢 Hilfe enthält eine kopierbare exakte JSON-Importvorlage; zusätzliche Datei `vorlagen/songtext_import_vorlage.json`.
- 🟢 Startvalidierung fragt vor dem Erstellen fehlender Arbeitsordner nach Zustimmung und prüft anschließend Schreibbarkeit.
- 🟢 Eingabe-/Auswahlfelder erhalten zentral einen kontrastierenden Theme-Hintergrund mit kontrastgeprüfter Schrift.
- 🟢 neue Module sind eigenständige Top-Level-Fenster und verwenden die vorhandenen Zoom-/Theme-/Accessibility-Standards.
- 🟢 Projekt-Todo ergänzt die neun Modulvorhaben idempotent als 9 Hauptaufgaben plus 48 separat abhakbare Unteraufgaben.

### Finale technische Abnahme und Release

- 🟢 synchronisierter PR-Head `9d9b608b55a72311d65d627dbe274ab400a2c79d` in Grundprüfung **#696** vollständig erfolgreich.
- 🟢 **104 Logik-/Regressionstests**, **74 PySide6-GUI-Tests** und **46 Release-Betriebsdateien** erfolgreich; Headless-Start und nativer Qt-Wayland-Smoke ebenfalls grün.
- 🟢 PR #45 SHA-geschützt gemergt; Produkt-Main `f3fafe411f48a67e8eff83c07f7caf9e2ea753c7`.
- 🟢 gemergter Main in Grundprüfung **#697** erneut vollständig erfolgreich: 104 Logiktests, 74 GUI-Tests, 46 Release-Dateien, nativer Wayland-Smoke und Restore `OK`.
- 🟢 Main-Restore-SHA-256 `25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04`.
- 🟢 Version **0.17.0** freigegeben; reale sichtbare Kubuntu-/Plasma-Wayland-Abnahme bleibt als separater manueller Schritt bestehen.

## Iteration 35 – Standardisierter Charakterzugriff in Schreibmodulen

**Hauptziel:** Den letzten offenen Charakterfibel-Punkt aus 0.17.0 klein und rückfallarm abschließen, ohne Song- oder Textdatenformat zu migrieren.

- 🟢 zentrale, UI-unabhängige Charakterauswahl mit stabilen IDs und einheitlicher Beschriftung eingeführt.
- 🟢 allgemeiner Texteditor auf dieselbe Referenzlogik umgestellt.
- 🟢 Songtexteditor kann Charaktere aus der Fibel direkt an der aktuellen Schreibposition einsetzen.
- 🟢 Referenzmarker auf `«Charakter: Name (Rolle)»` festgelegt; dadurch keine Kollision mit `[Strophe]`, `[Refrain]` oder eigenen Songbereichen.
- 🟢 erster Prüflauf #716 hat die ursprüngliche Kollision mit eckigen Klammern korrekt blockiert.
- 🟢 korrigierter technischer Head `907e65df46ba31d2d5e7df03d137baf1448742b8` in Grundprüfung #722 vollständig grün: 106 Logiktests, 76 GUI-Tests, 46 Release-Dateien, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`.
- 🟢 Restore-SHA-256: `2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a`.
- 🟢 CI stellt nach erfolgreichem Restore zusätzlich Runtime- und vollständiges Projekt-ZIP samt SHA-256 als Artefakt bereit.
- 🟡 reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt weiterhin ein separater Zielrechner-Schritt.

## Iteration 36 – Klick-&-Start-/Restore-Härtung

- 🟢 `kubuntu_abnahme.sh` direkt ausführbar (`0755`).
- 🟢 Restore erhält normale Unix-Ausführungsrechte und blockiert Symlink-/Sonderbit-Übernahme.
- 🟢 Main-Grundprüfung #750 auf `d34e5fd643d086f6737eb42448a9a126a6bd3214`: 111 Logiktests, 76 GUI-Tests, 46 Release-Dateien, Wayland und Restore `OK`.
- 🟡 reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt separat offen.

## Iteration 37 – Wartbarkeit, Entwicklungseffizienz, Repo-Hygiene und Hilfe

- 🟢 `scripts/pruefen.sh` auf Manifest-basierte Dateiprüfung und automatische Testentdeckung umgestellt.
- 🟢 `--quick` als kurze Entwicklungsprüfung ergänzt; `--full` bleibt verbindliches Release-Gate.
- 🟢 `scripts/_iter33_docs_apply.py` als bestätigten Einmal-Überrest entfernt.
- 🟢 Hygiene-Test blockiert künftig Einmal-Patch-/Finalizer-Helfer.
- 🟢 Hilfe & Fehlerhilfe mit zentralen, durchsuchbaren Hilfethemen und F1-Zugriff umgesetzt; Recovery bleibt getrennt als Fehlermeldungs-Reiter erhalten.
- 🟢 technischer PR-Gate #769 vollständig grün: 113 Logiktests, 77 GUI-Tests, 47 Release-Dateien, nativer Wayland-Smoke, Restore `OK` und ZIP-Artefakte; finaler 0.17.2-Metadatenstand wird vor Merge erneut voll geprüft.

## Detaillierter Modul-Backlog zum Abhaken

### 1. Charakterfibel
- [x] atomarer Charakterdatenbestand und stabile IDs
- [x] Such-/Bearbeitungsoberfläche
- [x] Kernfelder für Rolle, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen
- [x] Zugriffsmöglichkeit aus dem Texteditor
- [x] Zugriff aus weiteren Schreibmodulen standardisieren

### 2. Profil- & Accountmanager
- [x] Webseite/URL, Profilname optional, verwendete E-Mail-Adresse, Passworthinweis und Sonstiges
- [x] frei ergänzbare Felder
- [x] Gruppen, Suche, Filter und Schnellwiederfinden
- [x] Schutzkonzept: kein Passwortfeld, keine Zugangsdaten-URLs; bekannte Geheimnisfeldnamen abweisen. Metadaten bleiben unverschlüsselt.
- [x] Modulimport/-export mit Datenschutzhinweis; reguläre Datenablage durch vorhandene Datensicherung erfasst.

### 3. Universeller Texteditor
- [x] Titel bestimmt sicheren Dateinamen
- [x] große Schreibfläche und Abschlussnotizenfeld
- [x] atomare Speicherung, Versionierung und Autosave
- [x] Charakterfibel-Zugriff
- [x] Flüchtige Strukturfarben, Codeblöcke und begrenzte Gliederung mit Sprungfunktion ergänzen

### 4. Textfragment- und Ideenarchiv
- [x] einzelne oder mehrere Verse, Sätze, Fragmente und Schlagworte speichern
- [x] Tags, Herkunft und Volltextsuche
- [x] übersichtliche Karten-/Listenansicht
- [x] Drag-and-drop in einen seitlichen Kompositionsbereich
- [x] neue Texte aus Fragmenten erzeugen, ohne Originale zu löschen

### 5. Autonomes Updatemodul
- [x] Runtime-ZIPs begrenzt prüfen und ausschließlich in neues getrenntes Staging entpacken
- [x] Manifest, Versionsfortschritt, Paket-/Basis-/Dateihashes und Integrität vor weiterer Nutzung validieren
- [ ] vollständigen Checkpoint/Backup vor jedem Update erzeugen
- [ ] Update zuerst isoliert im Staging testen
- [ ] automatisierte Tests vor Aktivierung erzwingen
- [ ] atomare Aktivierung und Nachprüfung
- [ ] automatischen Rollback bei Fehlern
- [ ] Rechte-/Bestätigungsdialoge für riskante Änderungen; kein blindes Überschreiben

### 6. Projektmodulbaukasten / Plugin-System
- [ ] standardisierte Projektvorlagen
- [ ] Modul-/Plugin-Manifest definieren
- [ ] stabile Plugin-Schnittstellen statt Direktzugriff auf Kerninternas
- [ ] Plugins aktivieren/deaktivieren, ohne Kerncode zu beschädigen
- [ ] Abhängigkeits-, Versions- und Kompatibilitätsprüfung
- [ ] Test-/Stagingbereich für neue Module

### 7. Rechte Schnellstarter-Symbolleiste
- [ ] schmale persistente rechte Symbolleiste
- [ ] URL-Starter hinzufügen, bearbeiten und entfernen
- [ ] URL validieren und sicher im Standardbrowser öffnen
- [ ] Name, Symbol und Gruppe speichern
- [ ] Beispiele für YouTube, Suno und eigene Seiten
- [ ] Tastatur-, Tooltip- und Screenreader-Unterstützung

### 8. Wikimodul
- [ ] mehrere getrennte Wissensbasen
- [ ] Artikel mit Titel, Text, Tags und Verknüpfungen
- [ ] Volltextsuche und Querverweise
- [ ] dokumentierter Import/Export
- [ ] Versionierung, Backup und Zugriff anderer Module

### 9. Arbeitsverzeichnis- und Entwicklungspool
- [ ] mehrere Arbeits-/Poolordner persistent speichern und direkt öffnen
- [ ] dateimanagerartige Übersicht
- [ ] Status Entwicklung/Beta/stabil/archiviert
- [ ] funktionierende Beta-/Release-Stände sicher ins Archiv duplizieren
- [ ] niemals bestehende Archive überschreiben; eindeutige Namen/Versionen
- [ ] organisieren, umbenennen und Metadaten bearbeiten
- [ ] Vor-/Nachprüfung und nachvollziehbares Protokoll

## Danach

1. 🟡 reale sichtbare **Kubuntu 26.04 / KDE Plasma Wayland**-Abnahme mit `bash kubuntu_abnahme.sh` auf dem Zielrechner durchführen, besonders 1366×768 bei 125/150 %, zusätzlich 175/200 % und Theme `Kontrast`.
2. 🔴 anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

## Geplante Produktbereiche

Noch nicht freigegeben und deshalb in der Oberfläche sichtbar als `In Planung` markiert:

- Hörspiele
- Blogartikel
- Prompts
- Automatische GitHub-Verwaltung über die vorhandene lokale Projektliste hinaus
- Reimfinder
- Duplikatprüfer

Abgeschlossene Detailhistorie steht im `CHANGELOG.md` und in `docs/ITERATION*.md`; sie wird bewusst nicht mehrfach gepflegt.


## Iteration 40 – Textbuttons und Buchwerkstatt

- [x] Acht Funktionspakete der beiden neuen Module umgesetzt (siehe Abnahmebericht).
- [x] Gemeinsame Modularchive, atomare Speicherung, Hilfe und Entwurfsschutz.
- [x] 25 neue isolierte Daten-/GUI-Tests.
- [ ] Sichtbare Kubuntu-/Plasma-Wayland-Abnahme einschließlich Zwischenablage und deutschem Wörterbuch.
- [x] Erste datensparsame Qualitätskennzahlen in bestehende Diagnose integriert; keine automatische Übertragung.


## Fortführung: Informationsstand und Entwicklungsreview · 18.10.2026

- [x] Code-/Layoutstand cfc7353: CI #1007 einschließlich Wayland, Restore, ZIP und UI-Shadow 0/0 bestätigt.
- [x] Infotexte zu PR-/main-Status, verfügbaren Modulen und geplantem Messkonzept berichtigt.
- [x] Qualität, Effizienz, Fehlerursachen und unnötige Aktionen anhand der vorhandenen Nachweise bewertet.
- [x] Eine belegte Formular-Doppelung durch vorhandene Resetfunktion ersetzt (vier Codezeilen weniger; kein neues Framework).
- [x] Entwicklungsregeln und Info-Dateien-Checkliste um konkrete Lehren ergänzt.
- [x] Konsolidierter PR-Head 3954320: CI #1008 vollständig erfolgreich; Nachweis in PR-Metadaten gepflegt.
- [ ] Echte Kubuntu-/Plasma-Abnahme durchführen.
- [x] PR #84 nach ausdrücklicher Nutzerfreigabe mit main zusammengeführt (45c2496); Hauptzweig-Prüfung erfolgreich.
- [x] Erste Messkonzept-Ausbaustufe umgesetzt: freiwillige lokale Lade-/Schreibmessung, unveränderte gültige Speicherversuche, Tagesübersicht und Exportvorschau.
- [ ] Wirkung der neuen Entwicklungsregeln nach vergleichbaren Iterationen prüfen; keine Effizienzverbesserung ohne Messung behaupten.


## Iteration 41 – lokale Leistungsdiagnose

- [x] Opt-in, feste Messnamen und inhaltsfreie begrenzte Tagesaggregate.
- [x] Dashboard-/Modulladezeit und Text-/JSON-Schreibzugriffe instrumentiert.
- [x] Unveränderte gültige Speicherversuche in drei Schreibmodulen ohne zusätzliche Datei-Lesezugriffe zählen.
- [x] Bestehende Hilfe mit Übersicht, Exportauswahl, TXT/JSON-Vorschau und Löschfunktion ergänzt.
- [x] Rekursionsschutz, Aufbewahrung, Größenlimit und Fehlerisolierung ergänzt.
- [x] Vollständige lokale Prüfung: 200 Logiktests, 148 GUI-Tests, 67 Release-Dateien und Headless-Start; UI-Shadow 8 Fälle / 24 Fenster, 0 Fehler / 0 Warnungen.
- [x] GitHub-Prüfung und genehmigter Merge von PR #85 abgeschlossen; main 526a423, Lauf #1011: 200 Logiktests, 148 GUI-Tests, Wayland/Restore/ZIP erfolgreich. Größere Release-UI meldete dabei 24 Fehler / 8 Warnungen; Folgeauftrag #86.
- [ ] Zusatzaufwand auf realem Zielrechner mit vergleichbaren Arbeitsmengen messen; 1%-Ziel ist noch nicht belegt.
- [ ] Kalt-/Warmstart, Datenmengengruppen sowie echte app-eigene Cachekennzahlen in einer späteren abgegrenzten Iteration ergänzen.

Externe Abhängigkeiten bleiben unverändert: echte Kubuntu-/Plasma-Abnahme und Wirksamkeitsbewertung nach mehreren vergleichbaren Entwicklungsiterationen. Sie werden nicht durch einzelne Entwicklungsprüfungen als erledigt markiert.

## Iteration 42 – Release-UI-Befunde aus Issue #86

- [x] Ursache der 24 Überlappungen nachgewiesen: Vorgabenkarte benötigte 300 px, erhielt 234 px; leere Planungszeile reservierte weiterhin Höhe.
- [x] Acht GitHub-Warnungen anhand des originalen Artefakts geklärt: Textbaustein-Menü bei 150 % zu breit.
- [x] Kleine Korrektur mit vorhandenem Kompaktmodus und kurzem Textbutton-Label; keine gelockerten Prüfgrenzen.
- [x] Lokale Release-Matrix mit 60 Fällen / 180 Fenstern: 0 Fehler / 0 Warnungen.
- [x] Vollprüfung und GitHub-Prüfung abgeschlossen (PR #87, Main-Lauf #1013); historischer Haken nachgezogen.
- [ ] Reale Kubuntu-/Plasma-Bedienung bleibt als externer Zielrechner-Schritt offen.

Nächste Queue: vergleichbaren Overhead-Benchmark der freiwilligen Leistungsdiagnose erstellen; weiterführende Messgrößen bleiben nachrangig. Dieser Layoutauftrag ersetzt keine reale Bildschirmabnahme.

## Iteration 43 – reproduzierbarer Diagnose-Benchmark

- [x] Isoliertes Entwicklerscript mit drei Varianten, rotierter Reihenfolge, Rohwerten und separater Flush-Zeit.
- [x] Identische synthetische Arbeitsmenge, geprüfte Inhalte/Zähler und begrenzte Argumente; keine persönlichen Daten.
- [x] Lokale Vergleichsmessung durchgeführt; 1%-Ziel ausdrücklich nicht bestätigt.
- [ ] Vergleich auf echtem Zielrechner durchführen und danach Optimierungsziel festlegen.

Details und nächster Schritt: `docs/LEISTUNGSBENCHMARK.md`. Die externe Sichtabnahme und die finale GitHub-Abnahme der Layoutiteration bleiben unabhängig offen.

## Iteration 44 – unabhängige Datensicherung

- [x] Vollständige reguläre Dateien aus `daten/` mit Index und SHA-256 sichern.
- [x] Sicherung automatisch isoliert zurückholen und Inhalte vergleichen.
- [x] Vorhandene Ziele, Links, unsichere Archive und geänderte Quellen abweisen; zehn Schutztests erfolgreich.
- [x] Anleitung und Release-Manifest ergänzen.

Basis: 56528eb; Scope: Sicherungswerkzeug, Tests und Informationsdateien. Keine aktive Rückübernahme, keine Nutzerdatenmigration.

## Iteration 45 – beschädigte Startumgebung

- [x] Defekte/unvollständige vorhandene `.venv` erkennen und unverändert mit sicherer Anleitung abbrechen.
- [x] Tatsächliche Paketversionen und Qt-Import zusätzlich zum Hash prüfen.
- [x] Fehlende/defekte Pakete begrenzt neu installieren; Marker erst nach erfolgreicher Prüfung schreiben.
- [x] Fehlerfälle ohne Netz in isolierter Startumgebung prüfen; keine Oberfläche nach fehlgeschlagener Prüfung öffnen.

Basis f1c83f7. Scope: Startscript, Paketprüfung, Tests und Informationsdateien. Keine automatische Löschung oder Umbenennung einer Umgebung. Zeitgrenzen: Umgebung 60 s, Python 15 s, Paketprüfung 20 s, Installation 180 s, Vorprüfung 30 s.

## Iteration 46 – getrennte Lademessungen

- [x] Echten Bucharchiv-Lader mit festen synthetischen Datenklassen 1/25/100 Bücher prüfen.
- [x] Neue Python-Prozesse, erstes Lesen und wiederholtes Lesen getrennt erfassen.
- [x] Cachebestand prüfen: im gemessenen Buch-/Archivlader existiert kein app-eigener Cache; Kennzahlen nicht anwendbar.
- [ ] Vollständigen Dashboard-/Betriebssystem-Kaltstart später getrennt messen; dieser Benchmark behauptet ihn nicht.

Basis 6e60749. Nur Entwicklerwerkzeug und Schutztests, keine zusätzliche Datenerhebung in der Anwendung. Zwei isolierte Tests und eine vollständige lokale Messung erfolgreich.

## Iteration 47 – Kalibrierungsnachweise vorbereiten

- [x] Gespeicherte Shadow-Evidenz mit bestehender Infrastrukturprüfung und strengeren Eignungskriterien auswerten.
- [x] Doppelte/lokale/PR-Nachweise nicht als drei saubere Release-Läufe zählen.
- [x] Ohne Evidenz keine Empfehlung und niemals automatische Gate-Aktivierung; drei Schutztests erfolgreich.
- [ ] Drei saubere Original-CI-Läufe belegen und einzelne Regeln fachlich kalibrieren; anschließend Pflicht-Gate getrennt entscheiden.

REQUIRES: echte CI-Artefakte. Die Abnahme-/Aktivierungsentscheidung ist gemäß Nutzerpriorität zurückgestellt.

## Iteration 48 – Versionsunterlagen ohne Veröffentlichung

- [x] Versionskennung aus bestehender Manifest-/Logger-Kette im Fenstertitel anzeigen.
- [x] Kandidatenstatus, Änderungen, Lieferumfang, Prüfwege und offene Freigaben dokumentieren.
- [x] Informationsdateien und überholten Genre-Zufall-Übersichtsstatus abgleichen.
- [ ] Kandidaten veröffentlichen; gemäß Nutzerpriorität nach den übrigen Entwicklungsarbeiten.

Basis 6b823d4. Kein automatischer Merge und keine Veröffentlichung. Der Stand wird vor Abschluss vollständig automatisiert geprüft und isoliert wiederhergestellt.

## Iteration 49 – zentrale Text-/Dateisuche

- [x] Namen und UTF-8-Textinhalte unter `daten/` rein lesend suchen; keine Links oder versteckten Versionen.
- [x] Trefferliste, Zeilennummer, Klartextvorschau, Abbruch und Fensterwiederverwendung.
- [x] Dashboard-Kachel, Kopfsuche, vorhandene Kartenaktionen und Tastaturzugriff anbinden.
- [x] Schutz- und GUI-Regressionen einschließlich 100/150/200 % ergänzen.
- [ ] Finale Vollprüfung und Repository-Übertragung am identischen Quellbaum bestätigen; Nachweis am Pull Request.

Basis 230f562, isolierter Branch central-search. Scope: Suchkern, Suchfenster, vorhandene Einstiege, Hilfe, Tests und Informationsdateien. Nutzerdaten, Suchindexdateien und Prüfgrenzen werden nicht verändert. Manuelle Abnahme bleibt auf Nutzerwunsch zurückgestellt.

## Iteration 50 – statisches Update-Staging

- [x] Runtime-ZIP-Prüfung, Pfad-/Größen-/Identitäts-/Versionsschutz und Ausgangs-SHA.
- [x] Eigenen privaten Kandidatenordner außerhalb des aktiven Projekts erzeugen; bei Fehler nur diesen aufräumen.
- [x] Statische Python-/JSON-/Abhängigkeitsprüfung und nicht aktivierbaren Bericht ergänzen; elf Schutztests bestanden.
- [ ] Kandidat in echter Sandbox dynamisch testen; kein Code aus Kandidaten auf dem Host ausführen.
- [ ] Checkpoint, atomare Aktivierung und Rollback später separat umsetzen.

Nutzerreihenfolge nach diesem Staging-Schritt: Ideenarchiv → Accountmanager → Kaltstartmessung → Text-Strukturhilfen.

## Iteration 51 – Ideenarchiv

- [x] Atomare Fragmente mit Tags/Herkunft, Suche, Liste, Bearbeitung und Modulimport/-export.
- [x] Drag-and-drop als Klartextkopie in die Komposition; neue allgemeine Texte ohne Löschen/Überschreiben der Quellen.
- [x] Entwurfs-/Kompositionsschutz, gemeinsamer Zoom/Theme-Standard und zwei Daten-/zwei GUI-Schutztests.

Basis 95f184c. Zugriff über das Modulmenü am bisherigen Logo und Strg+Alt+I. Kein zusätzlicher Sidebar-Eintrag.

## Iteration 52 – Accountmetadaten

- [x] URL, optionaler Profilname, E-Mail, Merkhilfe, Notizen, Gruppen und freie Textfelder in einer Tabelle.
- [x] Suche/Gruppe, geprüfter Browseraufruf und Datenschutzhinweis vor Export.
- [x] Kein Passwortfeld; bekannte Geheimnisfelder und Zugangsdaten-URLs abweisen. Drei Daten- und zwei GUI-Schutztests.

Kein verschlüsselter Tresor und keine semantische Erkennung beliebiger Geheimnisse in Freitext. Diese Grenze ist direkt im Modul sichtbar. Tatsächliche Passwörter gehören in einen Passwortmanager.

## Iteration 53 – Prozess-Kaltstart und wiederholter Start

- [x] Echten Einstieg `app.main.main()` in neuen Prozessen bis zur ersten Ereignisschleife messen.
- [x] Synthetische Datenklassen mit 1/100 Songs; erster und wiederholter Start derselben Testinstallation getrennt.
- [x] Eigene temporäre Messbereiche, feste Arbeits-/Prozesszeitgrenzen und zwei Schutztests.
- [ ] Betriebssystem-Kaltstart und echte Zielrechnerwerte separat messen; keine kontrollierte OS-Cache-Leerung behaupten.

## Iteration 54 – Text-Strukturhilfen

- [x] Überschriften, eigene Bereiche, Aufgaben und Codeblöcke flüchtig hervorheben.
- [x] Theme-Kontrast, Abschalten und begrenzte Gliederung mit Sprungfunktion.
- [x] Zwei GUI-Tests: Klartextbytes und Änderungsstatus bleiben durch die Hilfen unverändert.

Validierungsfolgen: Formularbezeichnungen umbrechen; Verwerfen einer Komposition leert auch deren sichtbaren Entwurf. Account-URL-Schutz umfasst Query und Fragment.

- [ ] Opt-in-Datentrennung und verwalteter Programmstart als Entwicklungsprüfkandidat: alter Standardstart unverändert; vollständige Produktivmigration und Umschaltung bestehender Startsymbole noch gesperrt.

- [ ] Bildübergänge in der Video-Warteschlange aus der Iteration 68 nach CI und Hauptzweigprüfung freigeben; langfristig Batch-Statistik, Fortschritt pro Auftrag und weitere reale Videoqualitätsvergleiche ergänzen.

- [ ] Unabhängigen Kopie-Start (Iteration 68) nach vollständiger CI integrieren; bestehende Desktop-Verknüpfungen und alte Standardinstallation bis zur Schlussabnahme nicht umstellen.

<!-- PROVOWARE_2026_AUDIT_2026-10-22_BEGIN -->
## Neuer Prüf- und Entwicklungsbedarf – Nutzerinteroperabilität (Audit vom 22.10.2026)

> **Status:** Neuaufnahme in die `Next Queue`, **keine Implementierung und keine Freigabe** durch dieses Dokument. Ausgangspunkt: Quellcode- und GitHub-Prüfung von `main` (Grundstand `dca61e9` / aktualisierter Stand `536902e95c`). Alle historischen Aufgaben und der bisher freigegebene Modulplan bleiben erhalten. Dies ist **kein zweiter konkurrierender Ist-Stand**. Vor jeder Umsetzung aktuellen HEAD, `AGENTS.md`, `docs/MODULPLAN_2026.md`, bereits laufende PRs und Tests erneut abgleichen. Die hier erfassten neuen Produktkonzepte werden ausschließlich in eigenständig freigegebenen Folgeiterationen umgesetzt.

**Verbindliches Ziel:** Aus eigenständigen Werkzeugen ein projektorientiertes, durchgängig verknüpftes Offline-Kreativsystem entwickeln: **Projekt → einmal erfasste Daten → kontrolliert wiederverwenden → Ergebnis zuordnen → wiederfinden → vollständig sichern**. Vorhandene Module, Datenformate, Prüfungen, die positive Basisabnahme und die spätere **einmalige** Kubuntu-Gesamtabnahme bleiben geschützt.

**Nachweis- und Statussprache:** `Bestand` = im überprüften Code sichtbar; `Offen: PR` = Patch vorhanden, nicht als `main`-Funktion zählen; `Prüfbedarf` = Risiko oder historischer Befund, erneute Bestätigung erforderlich; `Teilweise` = Grundfunktion vorhanden, Abschluss fehlt. Die Prio bewertet zuerst Datenbewahrung/Sicherheit, dann Nutzerwirkung. **Checkbox [ ] bedeutet Auftrag, nicht nachgewiesenen Fehler.** Ein `[x]` wird erst nach implementiertem Code, Tests und passender GitHub-Evidenz gesetzt.

**Umfang:** 30 nummerierte Befunde (2× P0 / 20× P1 / 8× P2), 19 fachliche Modulverbindungen, 14 Wiederverwendungsdienste, 8 Umsetzungsphasen, 6 echte Nutzerszenarien und 16 Ende-zu-Ende-Abnahmetests. Alle Punkte haben eine stabile Kennung und sind nur einmal in dieser Next Queue führend.

### A. Detaillierter Maßnahmenkatalog – 30 Befunde

| ID | Prio | Nachweisstatus | Ist / Schwachstelle | Maßnahme / Warum | Abnahme | Bezug |
|---|---|---|---|---|---|---|
| PV-AUD-01 | P0 | Umsetzung vollständig geprüft in PR #130 | Neue Notizen liegen unter `daten/notizen/`; Altbestände werden nur bestätigt bytegenau kopiert, Original bleibt erhalten. | Atomare Speicherung, exklusive Altkopien, unveränderter persönlicher Sicherungsvertrag. | 80 lokale Prüfungen und vollständige GitHub-Prüfung #1112 erfolgreich; finale Statusrevision separat vor Merge prüfen. | PR #130, `app/quick_note.py`, `docs/DATENSICHERUNG.md`; Abschlussnachweis unten |
| PV-AUD-02 | P0 | Erledigt; am 24.10.2026 abgeglichen | PR #121 ist bereits in `main` integriert; die frühere Offen-Aussage war veraltet. | Vorhandenen Schutz wiederverwenden; keine Doppelimplementierung. | Drei Rückfalltests zu unveränderten Originalbytes, lesender Diagnose und weiterem Schreiben mit TXT-Bericht erfolgreich. | `tests/test_log_invalid_utf8.py`, PR #121; Details im Abschlussnachtrag unten |
| PV-AUD-03 | P1 | Bestand | Keine stabile modulübergreifende Projektzuordnung für Songs, Bücher, Bilder, Videoaufträge und Aufgaben. | Projektobjekt mit beständiger Kennung und getrenntem Referenzindex ergänzen; Originaldaten zunächst unverändert lassen. | Alle erfassten Projektbestandteile auffindbar; Wechsel der Projektbezeichnung erhält Beziehungen. | `app/development_pool.py`, `app/song_document.py`, `app/media_queue.py` |
| PV-AUD-04 | P1 | Bestand | Todo-Fälligkeit und Kalendereintrag sind eigenständige Datensätze. | Verknüpfte Fälligkeiten und Termine über IDs und definierte Änderungsregeln anbieten; keine automatische Dublette. | Terminkorrektur und Aufgabenerledigung bleiben in beiden Ansichten widerspruchsfrei. | `app/todo_store.py`, `app/calendar_store.py` |
| PV-AUD-05 | P1 | Umsetzung vollständig geprüft in PR #131 | Persönliche Aufgaben und Entwicklungsaltbestand sind über feste Kennungen getrennt; Öffnen erzeugt keine Aufgaben. | Rein lesende Ansichten, bewusste persönliche Kopie mit neuer Kennung, Originale erhalten. | 87 lokale Tests und vollständige GitHub-Prüfung #1115 erfolgreich; finale Statusrevision vor Merge separat prüfen. | PR #131; Abschlussnachweis unten |
| PV-AUD-06 | P1 | Bestand | GitHub-Projekte speichern eigene `todos`, getrennt von zentralen Aufgaben. | Ein gemeinsames Aufgabenmodell bzw. explizite Referenzierung einführen; bestehende Projektaufgaben erhalten. | Doppelte Anzeige ohne doppelte Speicherung; Erledigt-Status und Herkunft nachvollziehbar. | `app/github_projects.py`, `app/todo_store.py` |
| PV-AUD-07 | P1 | Bestand | Songidentität basiert auf Titel/Dateiname; keine dauerhafte Song-ID im `SongDocument`. | Persistente Song-ID über kompatible Metadaten/Index einführen, mit Altdatei-Einlesung und Titelwechsel. | Umbenannter Song behält Cover-, Audio- und Projektverknüpfungen; Text-Export bleibt lesbar. | `app/song_document.py`, `app/song_library.py` |
| PV-AUD-08 | P1 | Bestand | Texteditor speichert Charakter-IDs; Song/Buch verwenden sichtbar eingefügte Namensmarker. | Strukturierte Charakterrelation separat zum unveränderten Text speichern; historische Formulierungen nie unaufgefordert umschreiben. | Figurenumbenennung bricht keine Beziehung und ändert keinen veröffentlichten Text. | `app/text_editor_store.py`, `app/character_store.py`, `app/song_editor.py`, `app/book_window.py` |
| PV-AUD-09 | P1 | Bestand | Buchkapitel, Wikiartikel und Songtexte haben keine allgemeine modulübergreifende Quellen-/Werksrelation. | Typisierte Beziehungen `source`, `references`, `contains`, `variant_of`, `derived_from` zentral prüfen und speichern. | Quellen im Zielmodul öffnen; Löschen/Import von Zielobjekten behandelt verwaiste Referenzen sicher. | `app/wiki_store.py`, `app/book_store.py`, `app/song_document.py` |
| PV-AUD-10 | P1 | Bestand | Dateisuche listet Dateizeilen, öffnet aber nicht zielgenau den zugehörigen Facheditor. | Sicheren Treffer-Router Datei/Datensatz → zugehöriges Modul inklusive Fehlerhinweis ergänzen. | Ein Treffer führt zum richtigen bearbeitbaren Datensatz; ungültiger Pfad führt zu sicherem Hinweis. | `app/data_search.py`, `app/search_window.py` |
| PV-AUD-11 | P1 | Bestand | Suche erfasst nur gespeicherte erlaubte Dateien unter `daten/`, nicht ungespeicherte Entwürfe, Versionen oder externe Medien. | Suchumfang ausdrücklich kennzeichnen; fachlichen Index für registrierte Datensätze mit auswählbaren Scopes konzipieren. | Benutzer erkennt fehlende Suchbereiche; Suchtreffer und Sichtbarkeit sind reproduzierbar. | `app/data_search.py`, `docs/DATEISUCHE.md` |
| PV-AUD-12 | P1 | Bestand | Textbuttons-Platzhalter werden nicht allgemein aus Projekt, Genreprofil und Figurenzuordnung gespeist. | Gemeinsamen, lesenden Kontextdienst mit ausdrücklich gewählter Platzhalterquelle und Vorschau aufbauen. | Platzhalterauflösung ist deterministisch; Originalbausteine bleiben unverändert. | `app/snippet_store.py`, `app/profile_store.py` |
| PV-AUD-13 | P1 | Bestand | Datenformate/Validierung variieren zwischen TXT-Songs, JSON-Dokumenten und Modularchiven. | Gemeinsame IDs, Schema-Metadaten, Fehlerverträge und sichere Import-/Export-Schnittstellen ohne sofortige Datenbankmigration definieren. | Altdaten laden unverändert; unbekannte Versionen werden geschützt abgewiesen. | `app/module_archive.py`, `app/atomic_io.py`, `app/song_document.py` |
| PV-AUD-14 | P1 | Bestand | Playlists und Videoaufträge speichern absolute Dateipfade. | Projekt-relative Pfade bzw. Medien-ID mit sicheren Auflösungsregeln und Nachverknüpfen fehlender Quellen ergänzen. | Ordnerumzug gelingt ohne Datenänderung an Originalmedien; fehlende Medien werden klar markiert. | `app/media_files.py`, `app/media_queue.py` |
| PV-AUD-15 | P1 | Bestand | Persönliches Daten-ZIP enthält nicht automatisch extern referenzierte Audio-/Bild-/Videodateien. | Von normaler Datensicherung getrenntes vollständiges Projektpaket mit optionalen, geprüften Mediendateien entwickeln. | Wiederherstellung auf anderem Rechner enthält Quellen/Prüfsummen; keine fremden Pfade werden überschrieben. | `docs/DATENSICHERUNG.md`, `app/media_files.py` |
| PV-AUD-16 | P1 | Bestand | `module_contracts.describe()` meldet bei fehlendem Katalogeintrag deaktiviert; `is_module_enabled()` liefert aktiviert. | Eine zentrale Statusfunktion mit identischer Voreinstellung für Anzeige, Menü und Laufzeit etablieren. | Kaltstart, De-/Aktivierung, Menü und Beschreibung stimmen für alle sieben optionalen Module überein. | `app/module_contracts.py` |
| PV-AUD-17 | P1 | Prüfbedarf | Link-/Pfadschutz im allgemeinen Modularchiv ist nicht mit allen spezialisierten Datenablagen gleich stark. | Datei-/Verzeichnis-Links sowie Austausch zwischen Prüfung und Schreiben systematisch prüfen; gemeinsame sichere Speicher-API verwenden. | Negativtests zu Links, Umbenennung, Pfadwechsel, Symlink-Race und abgewiesenen Exportzielen bestehen. | `app/module_archive.py`, `app/module_runtime.py`, `app/data_search.py` |
| PV-AUD-18 | P1 | Bestand | `app/ui.py` ist zentral für zahlreiche Fenster und Navigation verantwortlich und überschreitet den Richtwert von 500 Zeilen. | Modul-Routing registrieren und schrittweise auslagern; funktionierende UI ohne Komplettneubau beibehalten. | Module werden aus Registry geöffnet; bestehende Tastenkürzel und Fensterzustände funktionieren. | `app/ui.py`, `app/window_lifecycle.py`, `app/module_contracts.py` |
| PV-AUD-19 | P1 | Bestand | README, TODO und Modulplan enthalten historische Aussagen, die neueren `main`-Funktionen widersprechen. | Eine aus Code/Tests abgeleitete, aktuelle Statusmatrix als einzige Quelle pflegen; Historie als Historie kennzeichnen. | ffprobe, echte Übergänge und gespeicherte Warteschlange werden entsprechend HEAD beschrieben. | `README.md`, `TODO.md`, `docs/MODULPLAN_2026.md` |
| PV-AUD-20 | P1 | Bestand | UI-Shadow ist bei fachlichen Bildbefunden weiterhin teilweise nicht blockierend. | Bekannte echte Befunde beheben, Fehlalarme kalibrieren und ausgewählte Regeln erst danach als harte Prüfung verwenden. | Mindestens drei sauber geprüfte Läufe und reproduzierbare Schwellen vor Pflicht-Gate; echter GUI-Befund blockiert. | `.github/workflows/qualitaet.yml`, `scripts/ui_shadow_entry.py` |
| PV-AUD-21 | P1 | Prüfbedarf: Issue #92 | Späte `QTimer`-Navigationsrückrufe verursachten früher einen Qt-Objektlebenszyklusfehler; `isValid`-Schutz steht im Hauptzweig. | Issue #92 gegen aktuelle Codeversion und gezielten Zerstörungs-Regressionsfall prüfen, erst dann schließen. | Nach Fensterzerstörung und ausstehenden Timerereignissen keine Ausnahme; Zoom und Navigation unverändert. | `app/navigation_ux.py`, Issue #92 |
| PV-AUD-22 | P1 | Bestand | Song/Audioplayer/Bildvorschau/Video verfügen über keine durchgängige Ergebnisweitergabe mit Projektbezug. | Direkte Übernahme als referenzierter Medien-/Produktionsauftrag samt Quelle, Typ und Version anbieten. | Vom Song aus Audio/Cover wählen, Video erzeugen und Ergebnis dem Songprojekt zuordnen. | `app/song_document.py`, `app/slideshow_window.py`, `app/media_queue.py` |
| PV-AUD-23 | P2 | Bestand | Hauptfläche nutzt feste 2×2-Karten statt frei belegbarer 3×3-Modulplätze. | Frei belegbares 3×3-Raster mit Fokus, Fensterzustand und zurücksetzbarer Belegung nach Modulrouter planen. | Kleine Auflösungen, 100–200 % Zoom, Tastaturbedienung und Persistenz getestet. | `app/ui.py`, `docs/MODULPLAN_2026.md` |
| PV-AUD-24 | P2 | Teilweise erledigt | PR #123 für frei verschiebbare Navigation wurde in `main` übernommen; verstellbare Dashboard-Karten folgen separat in PR #124. | PR #124 nur nach grüner Prüfung integrieren; persistente Einstellungen und Rücksetzen anschließend konsistent prüfen. | Mausverschiebung und Reset stabil, kein Regression bei Kompaktmodus/Zoom; kein Doppelpatch für #123. | PR #123, PR #124, `app/ui.py` |
| PV-AUD-25 | P2 | Bestand | Dashboard-Mindestgröße ist etwa 1020×650; Unterstützung kleinerer Flächen bleibt begrenzt. | 800×600 als zusätzlichem Testprofil nur nach Layoutkonzept nachgehen; Bedienwege in Kompaktansicht priorisieren. | Auf Zielgrößen kein abgeschnittener kritischer Ablauf und keine horizontale Pflichtscrollleiste. | `app/ui.py`, `app/presentation_policy.py` |
| PV-AUD-26 | P2 | Teilweise | Zoom/Themes und modulspezifische Optionen haben kein vollständiges gemeinsames Einstellungszentrum. | Persistenten Einstellungsdienst mit klaren Geltungsbereichen (Programm/Projekt/Modul) ergänzen. | Neustart, Export, ungültiger Zustand und Rücksetzen geprüft. | `app/ui.py`, `app/module_contracts.py` |
| PV-AUD-27 | P2 | Teilweise | Plugin-Ausführung ist nur kontrollierte isolierte Probe, keine produktiv freigegebene Erweiterungsplattform. | Signatur, Berechtigungen, Isolation, Ressourcenlimits, Lebenszyklus und Rücknahme getrennt nachweisen. | Ohne Freigabe nie ausführen; Negativtests für Netzwerk, Nutzerdatenzugang und Zeit-/Speicherlimits. | `app/plugin_sandbox.py`, `app/module_extension.py` |
| PV-AUD-28 | P2 | Bestand | Textbuttons, Ideenarchiv und Buchvorlagen überschneiden sich bei Textfragmenten. | Gemeinsame Baustein-Referenzfunktion prüfen; getrennte Fachoberflächen erhalten. | Vorlage einmal pflegen und bewusst in mehrere Projekte übernehmen, ohne Ursprungsinhalt zu verändern. | `app/snippet_store.py`, `app/idea_store.py`, `app/book_store.py` |
| PV-AUD-29 | P2 | Bestand | Einzelmodul-Import/Export ist nicht gleich einem vollständigen Austausch zusammengehöriger Projektdaten. | Ein Projekt-Austauschformat mit Version, Beziehungsindex, Konfliktvorschau, ID-Remapping und optionalen Medien definieren. | Hin-/Rückimport erhält Beziehungen, Originale und Versionsstände; Kollisionen sind transparent. | `app/module_archive.py`, `app/wiki_store.py`, `app/book_store.py` |
| PV-AUD-30 | P2 | Teilweise | Slot-Updates und Altinstallations-Migration besitzen geprüfte Bausteine, aber keine allgemeine produktive Altinstallation-Umstellung. | Vorhandene Sicherheitsgates konsolidieren; echter Schnellstart-/Rollbackpfad nur nach isolierter und nachvollziehbarer Freigabe. | Fehler-Injektionen, Code-/Datentrennung, Checkpoint und Rückfall auf unveränderte Altdaten geprüft. | `app/update_slots.py`, `app/runtime_roots.py`, `app/managed_launcher_switch.py` |

#### A1. Umsetzbare Aufgaben (jede Kennung ist ein eigenständiger, zu prüfender Auftrag)

- [x] **PV-AUD-01 [P0]** – Neue Projekt-Notizen im Datenordner gespeichert; bestehende Altdatei nur nach Zustimmung bytegenau kopiert und nie überschrieben. Sicherungs-/Restore-Roundtrip, Fehlerfälle und vollständige GitHub-Prüfung erfolgreich; Abschlussnachweis in PR #130 und unten. Keine Doppelzählung.
- [x] **PV-AUD-02 [P0]** – Bereits über PR #121 integrierten UTF-8-Logschutz mit drei Rückfalltests erneut bestätigt. Originalbytes bleiben erhalten; Lesen und weitere Diagnoseschritte bleiben kontrolliert. Nachweise im Statusabgleich unten; keine Doppelimplementierung.
- [ ] **PV-AUD-03 [P1]** – Projektobjekt mit beständiger Kennung und getrenntem Referenzindex ergänzen; Originaldaten zunächst unverändert lassen. **Fertig erst wenn:** Alle erfassten Projektbestandteile auffindbar; Wechsel der Projektbezeichnung erhält Beziehungen. (Bestand; Bezug: `app/development_pool.py`, `app/song_document.py`, `app/media_queue.py`).
- [ ] **PV-AUD-04 [P1]** – Verknüpfte Fälligkeiten und Termine über IDs und definierte Änderungsregeln anbieten; keine automatische Dublette. **Fertig erst wenn:** Terminkorrektur und Aufgabenerledigung bleiben in beiden Ansichten widerspruchsfrei. (Bestand; Bezug: `app/todo_store.py`, `app/calendar_store.py`).
- [x] **PV-AUD-05 [P1]** – Persönliche Aufgaben von historischem Entwicklungsaltbestand getrennt. Öffnen/Aktualisieren erzeugt und verändert keine Aufgaben; Altaufgaben bleiben vollständig sichtbar und erhalten. Persönliche Kopie nur nach Bestätigung mit neuer Kennung. 87 lokale Tests und vollständige GitHub-Prüfung #1115 erfolgreich; Abschlussnachweis in PR #131 und unten.
- [ ] **PV-AUD-06 [P1]** – Ein gemeinsames Aufgabenmodell bzw. explizite Referenzierung einführen; bestehende Projektaufgaben erhalten. **Fertig erst wenn:** Doppelte Anzeige ohne doppelte Speicherung; Erledigt-Status und Herkunft nachvollziehbar. (Bestand; Bezug: `app/github_projects.py`, `app/todo_store.py`).
- [ ] **PV-AUD-07 [P1]** – Persistente Song-ID über kompatible Metadaten/Index einführen, mit Altdatei-Einlesung und Titelwechsel. **Fertig erst wenn:** Umbenannter Song behält Cover-, Audio- und Projektverknüpfungen; Text-Export bleibt lesbar. (Bestand; Bezug: `app/song_document.py`, `app/song_library.py`).
- [ ] **PV-AUD-08 [P1]** – Strukturierte Charakterrelation separat zum unveränderten Text speichern; historische Formulierungen nie unaufgefordert umschreiben. **Fertig erst wenn:** Figurenumbenennung bricht keine Beziehung und ändert keinen veröffentlichten Text. (Bestand; Bezug: `app/text_editor_store.py`, `app/character_store.py`, `app/song_editor.py`, `app/book_window.py`).
- [ ] **PV-AUD-09 [P1]** – Typisierte Beziehungen `source`, `references`, `contains`, `variant_of`, `derived_from` zentral prüfen und speichern. **Fertig erst wenn:** Quellen im Zielmodul öffnen; Löschen/Import von Zielobjekten behandelt verwaiste Referenzen sicher. (Bestand; Bezug: `app/wiki_store.py`, `app/book_store.py`, `app/song_document.py`).
- [ ] **PV-AUD-10 [P1]** – Sicheren Treffer-Router Datei/Datensatz → zugehöriges Modul inklusive Fehlerhinweis ergänzen. **Fertig erst wenn:** Ein Treffer führt zum richtigen bearbeitbaren Datensatz; ungültiger Pfad führt zu sicherem Hinweis. (Bestand; Bezug: `app/data_search.py`, `app/search_window.py`).
- [ ] **PV-AUD-11 [P1]** – Suchumfang ausdrücklich kennzeichnen; fachlichen Index für registrierte Datensätze mit auswählbaren Scopes konzipieren. **Fertig erst wenn:** Benutzer erkennt fehlende Suchbereiche; Suchtreffer und Sichtbarkeit sind reproduzierbar. (Bestand; Bezug: `app/data_search.py`, `docs/DATEISUCHE.md`).
- [ ] **PV-AUD-12 [P1]** – Gemeinsamen, lesenden Kontextdienst mit ausdrücklich gewählter Platzhalterquelle und Vorschau aufbauen. **Fertig erst wenn:** Platzhalterauflösung ist deterministisch; Originalbausteine bleiben unverändert. (Bestand; Bezug: `app/snippet_store.py`, `app/profile_store.py`).
- [ ] **PV-AUD-13 [P1]** – Gemeinsame IDs, Schema-Metadaten, Fehlerverträge und sichere Import-/Export-Schnittstellen ohne sofortige Datenbankmigration definieren. **Fertig erst wenn:** Altdaten laden unverändert; unbekannte Versionen werden geschützt abgewiesen. (Bestand; Bezug: `app/module_archive.py`, `app/atomic_io.py`, `app/song_document.py`).
- [ ] **PV-AUD-14 [P1]** – Projekt-relative Pfade bzw. Medien-ID mit sicheren Auflösungsregeln und Nachverknüpfen fehlender Quellen ergänzen. **Fertig erst wenn:** Ordnerumzug gelingt ohne Datenänderung an Originalmedien; fehlende Medien werden klar markiert. (Bestand; Bezug: `app/media_files.py`, `app/media_queue.py`).
- [ ] **PV-AUD-15 [P1]** – Von normaler Datensicherung getrenntes vollständiges Projektpaket mit optionalen, geprüften Mediendateien entwickeln. **Fertig erst wenn:** Wiederherstellung auf anderem Rechner enthält Quellen/Prüfsummen; keine fremden Pfade werden überschrieben. (Bestand; Bezug: `docs/DATENSICHERUNG.md`, `app/media_files.py`).
- [ ] **PV-AUD-16 [P1]** – Eine zentrale Statusfunktion mit identischer Voreinstellung für Anzeige, Menü und Laufzeit etablieren. **Fertig erst wenn:** Kaltstart, De-/Aktivierung, Menü und Beschreibung stimmen für alle sieben optionalen Module überein. (Bestand; Bezug: `app/module_contracts.py`).
- [ ] **PV-AUD-17 [P1]** – Datei-/Verzeichnis-Links sowie Austausch zwischen Prüfung und Schreiben systematisch prüfen; gemeinsame sichere Speicher-API verwenden. **Fertig erst wenn:** Negativtests zu Links, Umbenennung, Pfadwechsel, Symlink-Race und abgewiesenen Exportzielen bestehen. (Prüfbedarf; Bezug: `app/module_archive.py`, `app/module_runtime.py`, `app/data_search.py`).
- [ ] **PV-AUD-18 [P1]** – Modul-Routing registrieren und schrittweise auslagern; funktionierende UI ohne Komplettneubau beibehalten. **Fertig erst wenn:** Module werden aus Registry geöffnet; bestehende Tastenkürzel und Fensterzustände funktionieren. (Bestand; Bezug: `app/ui.py`, `app/window_lifecycle.py`, `app/module_contracts.py`).
- [ ] **PV-AUD-19 [P1]** – Eine aus Code/Tests abgeleitete, aktuelle Statusmatrix als einzige Quelle pflegen; Historie als Historie kennzeichnen. **Fertig erst wenn:** ffprobe, echte Übergänge und gespeicherte Warteschlange werden entsprechend HEAD beschrieben. (Bestand; Bezug: `README.md`, `TODO.md`, `docs/MODULPLAN_2026.md`).
- [ ] **PV-AUD-20 [P1]** – Bekannte echte Befunde beheben, Fehlalarme kalibrieren und ausgewählte Regeln erst danach als harte Prüfung verwenden. **Fertig erst wenn:** Mindestens drei sauber geprüfte Läufe und reproduzierbare Schwellen vor Pflicht-Gate; echter GUI-Befund blockiert. (Bestand; Bezug: `.github/workflows/qualitaet.yml`, `scripts/ui_shadow_entry.py`).
- [ ] **PV-AUD-21 [P1]** – Issue #92 gegen aktuelle Codeversion und gezielten Zerstörungs-Regressionsfall prüfen, erst dann schließen. **Fertig erst wenn:** Nach Fensterzerstörung und ausstehenden Timerereignissen keine Ausnahme; Zoom und Navigation unverändert. (Prüfbedarf: Issue #92; Bezug: `app/navigation_ux.py`, Issue #92).
- [ ] **PV-AUD-22 [P1]** – Direkte Übernahme als referenzierter Medien-/Produktionsauftrag samt Quelle, Typ und Version anbieten. **Fertig erst wenn:** Vom Song aus Audio/Cover wählen, Video erzeugen und Ergebnis dem Songprojekt zuordnen. (Bestand; Bezug: `app/song_document.py`, `app/slideshow_window.py`, `app/media_queue.py`).
- [ ] **PV-AUD-23 [P2]** – Frei belegbares 3×3-Raster mit Fokus, Fensterzustand und zurücksetzbarer Belegung nach Modulrouter planen. **Fertig erst wenn:** Kleine Auflösungen, 100–200 % Zoom, Tastaturbedienung und Persistenz getestet. (Bestand; Bezug: `app/ui.py`, `docs/MODULPLAN_2026.md`).
- [ ] **PV-AUD-24 [P2]** – PR #124 nur nach grüner Prüfung integrieren; persistente Einstellungen und Rücksetzen anschließend konsistent prüfen. **Fertig erst wenn:** Mausverschiebung und Reset stabil, kein Regression bei Kompaktmodus/Zoom; kein Doppelpatch für #123. (Teilweise erledigt; Bezug: PR #123, PR #124, `app/ui.py`).
- [ ] **PV-AUD-25 [P2]** – 800×600 als zusätzlichem Testprofil nur nach Layoutkonzept nachgehen; Bedienwege in Kompaktansicht priorisieren. **Fertig erst wenn:** Auf Zielgrößen kein abgeschnittener kritischer Ablauf und keine horizontale Pflichtscrollleiste. (Bestand; Bezug: `app/ui.py`, `app/presentation_policy.py`).
- [ ] **PV-AUD-26 [P2]** – Persistenten Einstellungsdienst mit klaren Geltungsbereichen (Programm/Projekt/Modul) ergänzen. **Fertig erst wenn:** Neustart, Export, ungültiger Zustand und Rücksetzen geprüft. (Teilweise; Bezug: `app/ui.py`, `app/module_contracts.py`).
- [ ] **PV-AUD-27 [P2]** – Signatur, Berechtigungen, Isolation, Ressourcenlimits, Lebenszyklus und Rücknahme getrennt nachweisen. **Fertig erst wenn:** Ohne Freigabe nie ausführen; Negativtests für Netzwerk, Nutzerdatenzugang und Zeit-/Speicherlimits. (Teilweise; Bezug: `app/plugin_sandbox.py`, `app/module_extension.py`).
- [ ] **PV-AUD-28 [P2]** – Gemeinsame Baustein-Referenzfunktion prüfen; getrennte Fachoberflächen erhalten. **Fertig erst wenn:** Vorlage einmal pflegen und bewusst in mehrere Projekte übernehmen, ohne Ursprungsinhalt zu verändern. (Bestand; Bezug: `app/snippet_store.py`, `app/idea_store.py`, `app/book_store.py`).
- [ ] **PV-AUD-29 [P2]** – Ein Projekt-Austauschformat mit Version, Beziehungsindex, Konfliktvorschau, ID-Remapping und optionalen Medien definieren. **Fertig erst wenn:** Hin-/Rückimport erhält Beziehungen, Originale und Versionsstände; Kollisionen sind transparent. (Bestand; Bezug: `app/module_archive.py`, `app/wiki_store.py`, `app/book_store.py`).
- [ ] **PV-AUD-30 [P2]** – Vorhandene Sicherheitsgates konsolidieren; echter Schnellstart-/Rollbackpfad nur nach isolierter und nachvollziehbarer Freigabe. **Fertig erst wenn:** Fehler-Injektionen, Code-/Datentrennung, Checkpoint und Rückfall auf unveränderte Altdaten geprüft. (Teilweise; Bezug: `app/update_slots.py`, `app/runtime_roots.py`, `app/managed_launcher_switch.py`).

### B. Wiederverwendung technischer Funktionen statt Doppelimplementierung

| Baustein | Aktueller Bezug | Entscheidung für Folgearbeit |
|---|---|---|
| Atomar speichern | `app/atomic_io.py` | Bestand; auf alle relevanten Nutzerdatenwege ausdehnen |
| Modularchive/Validierung | `app/module_archive.py`, `app/record_store.py` | Bestand; gleiche Pfad-/Fehlerverträge durchsetzen |
| Modulverträge/-rechte | `app/module_contracts.py`, `app/module_permissions.py` | Bestand; Aktivierungsstatus und Fähigkeiten aus einer Quelle |
| Fensterlebenszyklus | `app/window_lifecycle.py` | Bestand; Modulrouter statt weiterer direkter Dashboard-Verweise |
| Theme/Zoom/Geometrie | `app/ui_standards.py`, `app/presentation_policy.py` | Bestand; Entflechtung ohne Funktionsverlust |
| Charakterauswahl | `app/character_combo.py` | Bestand; im Text strukturiert referenzieren |
| Genreprofile | `app/profile_store.py` | Bestand; gemeinsame Profil-IDs für neue Übergaben |
| Webadressen prüfen | `app/account_store.py` | Bestand; auch Schnellstarter nutzt Validierung |
| Medienpfade | `app/media_files.py` | Bestand; um portable Referenzen ergänzen |
| Protokolle/Diagnose | `app/event_log.py` | Bestand; abgesicherte UTF-8-Fehlerwege fertigstellen |
| Objektregister (neu) | noch nicht vorhanden | Stabile fachliche IDs plus Datensatzauflösung ohne Vollmigration |
| Beziehungsdienst (neu) | noch nicht vorhanden | Typisierte, validierte Verweise mit Lösch-/Importregeln |
| Modul-Aktionsvermittlung (neu) | aus bestehender Modulregistry ableiten | Sichere Übergabe und Öffnen von Datensätzen |
| Fachsuche/Medienkatalog (neu) | aus Dateisuche/Medienwegen ableiten | Quelle, Objekt-ID, Filter, sichere Treffer-Navigation |

**Vorgehensregel:** Gemeinsame Speicherung ≠ gemeinsame Inhalte. Unterschiedliche Fachoberflächen (Songeditor, Buchwerkstatt, Wiki) **nicht** zu einem überladenen Fenster zusammenschmelzen. Stattdessen sichere Kernfunktionen einmal anbieten und aus den fachlichen Modulen aufrufen. Abweichende Kunsttexte und historische Fassungen niemals automatisch umschreiben.

### C. Fachliche Modul- und Dateninteroperabilität

| Quelle | Ziel | Ist / Übergabe | Erforderlicher Sollzustand | Befunde |
|---|---|---|---|---|
| Charakterfibel | Allgemeiner Texteditor | IDs vorhanden | Namens-/Rollenänderung kontrolliert anzeigen, Texte unverändert lassen | 08 |
| Charakterfibel | Songeditor | lesbarer Textmarker | stabile Figuren-ID getrennt vom Liedtext speichern | 08 |
| Charakterfibel | Buchwerkstatt | lesbarer Textmarker | Figur mit Buch/Kapitel dauerhaft verknüpfen | 08–09 |
| Genrearchiv | Genre-Zufall | gemeinsamer Profilbestand | bestehende zentrale Datenquelle erhalten | 12 |
| Genre-Zufall | Songeditor | Stilausgabe nutzbar, Herkunft nicht dauerhaft gebunden | Profil und Generationslauf referenzieren | 07,12 |
| Ideenarchiv | Songeditor | Copy-/Fragmentworkflow, kein universeller Objektbezug | Fragment als bewusst gewählte Kopie/Referenz übernehmen | 09,28 |
| Textbuttons | Songeditor | Platzhalter auf Textwerte begrenzt | Projekt-, Profil- und Figurenwerte anbieten | 12,28 |
| Textbuttons | Buchwerkstatt | getrennte Baustein- und Vorlagendaten | gemeinsame Bausteinquelle ohne Originalüberschreibung | 28 |
| Wiki | Buchwerkstatt | separate Wissens-/Buchbestände | Artikel als Quelle pro Kapitel referenzieren | 09 |
| Songbibliothek | Audioplayer | kein gemeinsames Song-/Audioobjekt | Audiodatei einem Song zuordnen | 07,22 |
| Songbibliothek | Bildvorschau | keine gemeinsame Coverzuordnung | Bild als Covervariante referenzieren | 07,22 |
| Audioplayer | Video/Slideshow | Pfad manuell auswählbar | Medien-ID und Projektkontext direkt übergeben | 14,22 |
| Bildvorschau | Video/Slideshow | separate Bildliste | reihenfolgestabile Bildsammlung übernehmen | 14,22 |
| Videogenerator | Projektbestand | Auftrags-ID, aber kein Kreativprojektbezug | Ausgabe, Quellen und Parameter registrieren | 03,22 |
| Todo-Liste | Kalender | getrennte Ereignisse | Fälligkeit und Kalendertermin verknüpfen | 04 |
| GitHub-Projekte | Todo-Liste | separate Aufgabenlisten | ein Aufgabenobjekt mit Projektansicht | 05–06 |
| Entwicklungspool | GitHub-Projekte | getrennte Projektobjekte | gemeinsame Projektkennung und Statusansichten | 03,06 |
| Dateisuche | Datenmodule | Text-/Dateitreffer | fachlich korrektes Fenster und Originaldatensatz öffnen | 10–11 |
| Datensicherung | Medien-/Projektbereich | nur definierter Datenbestand | vollständiges, optional medienhaltiges Projektpaket | 01,14–15,29 |

**Verbindliche Datenbeziehungen:** `project_id`, `object_id`, `source` (Quelle), `references` (Verweis), `contains` (Bestandteil), `variant_of` (Variante), `derived_from` (abgeleitetes Werk) und `media_id`. Nur geprüfte Beziehungen erlauben; ungültige/gelöschte Ziele werden kontrolliert behandelt. Sichtbarer Figurenname bleibt Darstellung, nicht Identität. Ein Textfragment darf **Kopie oder Referenz** sein, je nach ausdrücklicher Nutzerentscheidung.

### D. Nutzerzentrierte Ende-zu-Ende-Szenarien (fachliche Abnahme)

| Szenario | Bedienkette | Erfolg aus Nutzersicht | Befunde |
|---|---|---|---|
| Kreativprojekt von Idee bis Veröffentlichung | Projekt anlegen → Idee/Textbaustein nutzen → Song schreiben → Profil/Charakter referenzieren → Audio/Cover zuordnen → Video berechnen → Exportstatus/Aufgabe/Termin verbinden. | Jeder Schritt bewahrt Quellen-/Projektbezug; keine erneute Stammdateneingabe; keine ungefragte Veröffentlichung. | 03,07–09,12,14,22 |
| Figur in mehreren Werken | Figur in Charakterfibel speichern → Song, Text und Buch referenzieren → Figur umbenennen → alte Fassungen erneut öffnen. | Stabile Figurenbeziehung, unveränderte künstlerische Textfassungen, verständliche Konfliktanzeige. | 08–09 |
| Recherche zur Sachausarbeitung | Wikiartikel anlegen → Buchkapitel als Quelle verknüpfen → Quelle über Suche öffnen → Kapitel exportieren. | Herkunft/Quelle maschinenlesbar, keine verdeckte Überschreibung des Wikiartikels. | 09–11 |
| Projektplanung ohne Dubletten | Projektaufgabe anlegen → Fälligkeit setzen → Kalender öffnen → Termin anpassen → Aufgabe abhaken. | Ein verbundenes Aufgabenobjekt, konsistenter Terminbezug, getrennte Entwicklungs- und persönliche Aufgaben. | 04–06 |
| Portabler Umzug eines Medienprojekts | Projekt mit Song, Videoauftrag und externen Quelldateien sichern → Paket in neuem Verzeichnis wiederherstellen → betroffene Module öffnen. | Alle eingebetteten Medien geprüft, fehlende externe Quellen nachvollziehbar; bestehende Dateien nicht überschrieben. | 01,14–15,29 |
| Update und Wiederherstellung bei Fehler | Bestandsinstallation sichern → Update isoliert prüfen → Startfehler simulieren → altes Programm mit Originaldaten nutzen. | Rückfall nachweisbar; keine ungefragte Altdatenmigration oder Datenveränderung. | 17,27,30 |

**UX-Entscheidungsregel:** Der Nutzer denkt in Songs, Projekten und Veröffentlichungen statt in Dateitypen und Fenstern. Ein zentraler Projektkontext zeigt verknüpfte Texte, Vorlagen, Figuren, Audio, Bilder, Videos, Aufgaben und Termine; die Originale verbleiben in ihren spezialisierten Modulen. Standardschritte sollen ohne wiederholte Eingabe erreichbar sein, riskante Aktionen mit Bestätigung und verständlichem Rückfall.

### E. Zielarchitektur und Grenzen der Umstellung

1. **Objektregister:** Stabile Kennung → Typ, Projekt, aktueller Speicherort, Schema-/Versionsangabe. Beim Umbenennen bleiben IDs gleich.
2. **Beziehungsdienst:** Typisierte Verweise zwischen registrierten Objekten, Prüfung auf fehlende Ziele, sichere Lösch-/Importfolgen.
3. **Modulrouter / Aktionsvermittlung:** Ein `Öffne Datensatz X in Modul Y`-Vertrag für Suchtreffer, Projektansicht und Modulwechsel statt Direktverweisen aus `app/ui.py`.
4. **Gemeinsamer Kontextdienst:** Nur ausdrücklich gewählte Projekt-, Genre-, Figuren- und Bausteininformationen als schreibgeschützte Vorlagenwerte.
5. **Fachsuche und Medienkatalog:** Suchtreffer mit Typ/ID/Originalquelle; Medieneinträge möglichst portabel, absolute Pfade als kompatible Altwerte.
6. **Getrennte Sicherungsarten:** Persönliche Programmdaten gegenüber **vollständiger Projektsicherung mit optional eingebetteten Medien** klar unterscheiden.
7. **Gemeinsame Einstellungen:** Dauerhafte Projekt-, Modul- und Anzeigeeinstellungen mit belastbarer Gültigkeits-/Rückfallprüfung.
8. **Keine riskante Big-Bang-Migration:** Erst additive, getestete Metadaten-/Beziehungsregistrierung. TXT-/JSON-Originaldateien bleiben erhalten; SQLite nur bei späterem nachgewiesenem Mehrwert und eigener Entscheidung. Keine automatische Überschreibung, kein Kopierverlust, keine stillen Änderungen am künstlerischen Original.

### F. Abhängige Umsetzungsreihenfolge (keine parallelen Konfliktänderungen)

| Phase | Abhängige Befunde | Arbeitsauftrag | Freigabe/Prüfkriterium |
|---|---|---|---|
| 0 – Sicherung/Status | 01,02,16,17,19,21,24 | Bestandsdaten sichern; offene Fix-PRs statusgenau integrieren, aktuelle Dokumentation/Wahrheitsmatrix und Negativtests; PR #123 nicht erneut bearbeiten. | Keine bekannten ungeschützten Datenwege; CI grün; offene Probleme nachvollziehbar. |
| 1 – Identitäten | 03,07,08,13 | Kompatible IDs für Projekte/Songs; Objektregister und sichere Auflösung, bestehende Dateien nicht blind migrieren. | Roundtrip/Umbenennung/Restore erhalten IDs und Daten. |
| 2 – Beziehungen | 09,12,22,28 | Typisierte Beziehungen, Kontextplatzhalter, bewusstes Kopieren/Referenzieren, Song→Medien. | Referenzen bleiben bei Umbenennen/Import valide; keine stillen Textänderungen. |
| 3 – Suche & Öffnen | 10,11,18 | Einheitliche fachliche Suchresultate und Modulrouter; vorhandene Suchschutzgrenzen bewahren. | Suche führt korrekt zum Originaldatensatz, keine Dateien ausgeführt/überschrieben. |
| 4 – Aufgaben & Termine | 04,05,06 | Persönliche Aufgaben von Entwicklerbacklog trennen; Projektaufgaben und Kalender referenziert zusammenführen. | Keine automatische Übernahme alter Entwicklungsaufgaben; Erledigungs-/Terminstatus konsistent. |
| 5 – Medien & Projekttransport | 14,15,29 | Portabler Medienkatalog, Projektsicherung mit optionalen Medien, sichere Konflikt-/Importprüfung. | Projektkopie nach Umzug auch mit Audio, Bildern und Videobezügen lauffähig. |
| 6 – Oberfläche/Erweiterungen | 20,23,25,26,27,30 | Registry-basiertes Raster, Fokus, Einstellungen, UI-Kalibrierung, geprüfte Modul-/Update-Laufzeit. | 100–200-%-Zoom, Tastenweg, Restore, Wayland, keine fremde Codeausführung ohne Freigabe. |
| 7 – Abschluss | alle offenen | Durchgängige Integrations-, Sicherheits-, Medien- und Releaseprüfungen; reale Kubuntu-Gesamtabnahme ausschließlich zum Schluss. | Keine offenen releaseblockierenden Befunde; Nutzer-Endabnahme erst nach Vollständigkeit. |

**Abhängigkeitskette:** `Sicherer Bestand` **BLOCKS** `Objektidentität` → **BLOCKS** `Beziehungen` → **REQUIRES** `Router und globale Suche` → **REQUIRES** `medienhaltige Projektsicherung` → **REQUIRES** `vollständige Release-Abnahme`. Einzelne unabhängige Reparaturen dürfen in eigenen PRs stattfinden; gemeinsamer Schreibscope bleibt durch `Single Writer` geschützt.

**Abgrenzung zu bestehenden Aufträgen:**
- `PV-AUD-02` **DUPLICATE/REQUIRES** PR #121: Patch nicht ein zweites Mal implementieren; stattdessen Prüf-/Mergezustand klären.
- `PV-AUD-21` **REQUIRES** Issue #92: aktuelle `isValid`-Absicherung durch passenden Regressionstest belegen, bevor das Issue geschlossen wird.
- `PV-AUD-24` **SUPERSEDES** die frühere Aussage, Navigation liege nur in PR #123: **PR #123 ist in `main` integriert**; PR #124 betrifft nur die darüber hinausgehende Kartenverstellung und bleibt bis zur Prüfung getrennt.
- `PV-AUD-19` **REQUIRES** Vergleich mit PR-/main-Stand: Alte Textbehauptungen über fehlende Übergänge/Warteschlangen nicht ungeprüft als aktuelle Wahrheit behandeln.
- `PV-AUD-18` **BLOCKS** freie dynamische Modulbelegung: erst stabile Modulansprache, dann 3×3 statt zusätzlicher fester Fensterlogik.
- `PV-AUD-29` **REQUIRES** `03/07/09/14/15`: Projektarchiv erst, wenn IDs, Beziehungen und Medienauflösung definiert sind.

### G. Risikobasierte Ende-zu-Ende- und Negativprüfungen

| Test | Eingriff/Ablauf | Erwartetes nachweisbares Ergebnis | Befunde |
|---|---|---|---|
| UAT-01 | Song umbenennen | Verknüpfte Audio-, Cover-, Aufgaben- und Projekt-IDs bleiben gültig. | 03,07 |
| UAT-02 | Figur umbenennen | Referenzen bleiben gültig; historische Song-/Buchtexte bleiben wortgleich. | 08 |
| UAT-03 | Aufgabe mit Termin ändern | Kalender und Aufgabenansicht zeigen keine widersprüchlichen Einträge. | 04–06 |
| UAT-04 | Persönliche Sicherung | Kurznotizen, Texte und Archivdaten vollständig nach Restore vorhanden. | 01 |
| UAT-05 | Projekt medienhaltig exportieren | Unabhängige Wiederherstellung auf anderem Pfad mit Prüfsummen. | 14–15,29 |
| UAT-06 | Videoquelle fehlt | Keine irrtümliche Erfolgsmarkierung oder Überschreibung, verständlicher Fehler. | 14,22 |
| UAT-07 | Videoquelle während Berechnung wechselt | Fehler/Warnung, kein stillschweigend falsches Ergebnis. | 14,22 |
| UAT-08 | Modul ausschalten | Menü, Tastenkürzel, Beschreibung und Laufzeitentscheidung stimmen überein. | 16 |
| UAT-09 | Beschädigten Import testen | Ursprüngliche Daten und Dateien unverändert; eindeutige Fehlerkennung. | 13,17,29 |
| UAT-10 | Dashboard mit ausstehenden Timern schließen | Kein Qt-Lebenszyklusfehler; Zoom/Navigation weiter korrekt. | 21 |
| UAT-11 | Song/Figur/Wiki über Suche finden | Öffnet richtigen Datensatz im zuständigen Editor; kein blindes Dateiausführen. | 10–11,18 |
| UAT-12 | Altdaten wiederherstellen | Kein stilles Überschreiben; Altformate bleiben lesbar. | 13,29–30 |
| UAT-13 | Großer Zoom/kleiner Monitor | Kernbedienung unter 100/125/150/175/200 % erreichbar. | 20,23–25 |
| UAT-14 | Update mit Startfehler | Automatischer Rückfall auf geprüften alten Stand, Nutzerdaten unverändert. | 30 |
| UAT-15 | Fehlerhaftes Ereignislog | Fehler in Diagnose sichtbar; Logbytes erhalten, Folgeereignis sicher protokollierbar. | 02 |
| UAT-16 | Kreativprojekt importieren | ID-Neuzuordnung erhält Beziehungen zwischen Werken, Quellen und Medien. | 03,09,29 |

**Pflichtnachweis je Umsetzung:** Scope und ursprünglicher Commit-SHA, referenzierte Befund-ID, betroffene Funktionen/Dateien, sichere Rückfallstrategie, passende positive und negative Tests, Veränderung an Altdaten nur in isolierten Prüfordnern, GitHub-PR-Prüfung auf exakt dem geprüften HEAD, anschließend main-Prüfung nach Merge. Nicht ausführbare Prüfungen **nicht** als erfolgreich ausgeben. UI-Shadow-Befunde getrennt vom grünen Infrastruktur-Job beurteilen. Kein manuelles Nutzer- oder Kubuntu-Zwischengate während des Modulaufbaus.

### H. Kontinuität und Arbeitsübergabe

- **Frozen Current Plan:** Bestehenden Modulplan und laufende Implementierungen nicht durch dieses Audit ersetzen. Neue Anforderungen sind bis zur priorisierten Freigabe ausschließlich `Next Queue`.
- **Recovery Key:** Audit `2026-10-22`, Repo `provoware/TOOL_2026_Multi`, geprüfter Ausgangs-HEAD `536902e95c188f9082462f980f022e9fc5a9965f`, einzig beabsichtigter Schreibscope dieses Dokumentationsauftrags `TODO.md`, keine Laufzeitdatei geändert, keine Tests als selbst ausgeführt behauptet. Nächster erlaubter Schritt nach Übernahme: `PV-AUD-01` auf Basis aktueller Datenpfade in eigenem Patch untersuchen und isolierte Sicherungs-/Restore-Tests definieren; PR #121 unabhängig kontrollieren.
- **Traceability:** Jede Umsetzung verlinkt `PV-AUD-ID → konkrete Änderung → Test → GitHub-Evidenz → Abschlussstatus`. Gleiche Anforderungen aus historischen TODO-Abschnitten dürfen nicht doppelt gezählt werden.
- **Begrenzung:** Sicherheits- und Datenbewahrungsaufgaben zuerst; keine automatische Plugin-Freigabe, keine Migration produktiver Altdaten, keine automatische Veröffentlichung, keine vorgezogene visuelle Nutzerabnahme.
- **Dokumentationsgenauigkeit:** Die vorgenannten Befunde sind ein Entwicklungsauftrag aus Quellcodeanalyse, keine Aussage, dass alle zukünftigen Funktionen bereits erstellt oder die reale Kubuntu-Abnahme durchgeführt wurden.

<!-- PROVOWARE_2026_AUDIT_2026-10-22_END -->
- [x] **PV-UX-01 [P1]** – Tätigkeitsorientierten Einstieg und hilfreiche Leerzustände gestalten. **Abnahme:** Erster Inhalt lässt sich ohne Erklärung erstellen, speichern und wieder öffnen. **Bezug:** ui.py; Buch-, Text- und Song-Einstiege.
- [ ] **PV-UX-02 [P1]** – Beschrifteten Zugang „Alle Werkzeuge“ und nachvollziehbare Gruppen anbieten. **Abnahme:** Alle fertigen Werkzeuge bleiben per Tastatur und bei Zoom erreichbar; Status stimmt mit Laufzeit überein. **Bezug:** REQUIRES PV-AUD-16/18.
- [x] **PV-UX-03 [P1]** – Einheitliche Speicherzustände und sichtbare Grenzen unbetitelter Entwürfe definieren. **Abnahme:** Bearbeitung, automatisches Speichern, Fehler und Schließen zeigen den tatsächlichen Zustand. **Bezug:** song_editor.py, text_editor_window.py, book_window.py.
- [ ] **PV-UX-04 [P1]** – Ja/Nein-Rückfragen durch eindeutige aktionsbezogene Entscheidungen ersetzen. **Abnahme:** Speichern/Verwerfen/Weiterarbeiten haben bei Wechsel und Schließen die angekündigte Wirkung; Fehler verhindert Verlassen. **Bezug:** module_widgets.py, module_controls_window.py, text_editor_window.py.
- [ ] **PV-UX-05 [P2]** – Letzte Arbeiten über unterstützte Inhaltstypen hinweg anzeigen. **Abnahme:** Typ und Öffnen-Aktion stimmen; fehlende und umbenannte Ziele werden kontrolliert behandelt. **Bezug:** REQUIRES sichere Datensatzauflösung aus PV-AUD-18.
- [ ] **PV-UX-06 [P1]** – Grafischen Ablauf für persönliche Sicherung und isolierte Wiederherstellung anbieten. **Abnahme:** Ziel, Umfang, Ausschlüsse, Abbruch und Ergebnis verständlich; vorhandene Ziele werden nicht überschrieben. **Bezug:** REQUIRES PV-AUD-01; Medienpaket bleibt PV-AUD-15/29.
- [ ] **PV-UX-07 [P2]** – Sichtbare Begriffe, Hilfe und barrierefreie Namen gemeinsam vereinfachen. **Abnahme:** Bezeichnungen bleiben eindeutig; Kontenübersicht erzeugt keine Passworttresor-Erwartung; zentrale Texte verwenden. **Bezug:** texte/registry.json und betroffene Direkttexte.
- [ ] **PV-UX-08 [P1]** – Kurzen aktuellen Alltagseinstieg von Entwicklerprüfung und Systemabnahme trennen. **Abnahme:** Beschriebene Wege entsprechen aktuellem Code; zentrale Suche korrekt beschrieben; Historie erhalten. **Bezug:** REQUIRES PV-AUD-19; ergänzt dessen Statuspflege.
- [ ] **PV-UX-09 [P1]** – Fehlermeldungen mit konkreten sicheren Folgeaktionen und wahrheitsgetreuer Schutzwirkung ausstatten. **Abnahme:** Wiederholter Autosave-Fehler erzeugt keinen falschen Erfolg und keine unkontrollierte Dialogfolge. **Bezug:** Moduloberflächen und Speicherwege.
- [ ] **PV-UX-10 [P1]** – Aufgabenbezogene Tastatur-, Zoom- und Screenreader-Prüfung vorbereiten. **Abnahme:** Kernabläufe gemäß UX-UAT-09/10 tatsächlich geprüft; offene Nachweise sichtbar; Gesamtabnahme erst am Ende. **Bezug:** REQUIRES PV-AUD-20/25; kein neues manuelles Zwischengate.

**Zählregel:** Zehn UX-Aufträge: zwei technisch abgeschlossen, acht offen; keine bestehenden PV-AUD-Aufträge doppelt zählen. Die Dokumentation des Konzepts bedeutet keine fachliche Erledigung.

**Empfehlung:** Zuerst PV-AUD-01 am aktuellen HEAD mit isolierten Sicherungs-/Restore-Fällen bearbeiten; anschließend Einstieg und Werkzeugnavigation. Dies ist eine Folgeempfehlung, keine Umpriorisierung laufender freigegebener Arbeit. Zuordnung und zwölf geplante UX-Abnahmeszenarien stehen im Konzept.


## UX-Folgeplanung – Nutzerfreundlichkeit und Laientauglichkeit (24.10.2026)

**Konzept:** [UX-Analyse und Verbesserungskonzept](docs/UX_KONZEPT_LAIENTAUGLICHKEIT.md). Status: dokumentiert, Produktmaßnahmen offen. Der eingefrorene Modulplan bleibt erhalten. Ausgangsstand: `5c143fe87a1890017829580987b3c1776f184c40`.

**Bestehende Anforderungen bleiben führend:** Notizsicherung `PV-AUD-01`, persönliche Aufgaben `05`, Suchöffnung/-umfang `10/11/18`, Medien-/Projektpaket `14/15/29`, Inhaltsbeziehungen `03/07/08/09/12/22/28`, Dokumentationsstatus `19`, Darstellung/Einstellungen `20/23/24/25/26`. Diese Punkte sind Beziehungen vom Typ **DUPLICATE** zum bestehenden Auftrag und werden nicht nochmals als neue Aufgaben gezählt.

### Ergänzende UX-Aufträge


## Präzisierter Suchauftrag – lokales Dateisystem (24.10.2026)

- [ ] **PV-SEARCH-01 [P1]** – Datei-/Textinhaltssuche mit frei wählbarem lokalen Suchpfad, ausdrücklicher Bestätigung zusätzlicher Suchbereiche und transparenter Behandlung fehlender OS-Leserechte. **Status:** Implementierungskandidat; lokale und GitHub-Nachweise im zugehörigen PR führen. **Abnahme:** Auswahl/Eingabe externer Ordner, Ablehnung ohne Scan oder Trefferverlust, Pfadwechsel mit erneuter Zustimmung, reine Lesezugriffe, keine Linkverfolgung, erhaltene Suchgrenzen und sichtbar unvollständige Ergebnisse bei Berechtigungsfehlern. Keine automatische Root-Suche oder Rechteänderung. **SUPERSEDES:** `daten/` als ausschließliches Produktziel; **REQUIRES:** bestehende Suchschutzverträge; ergänzt `PV-AUD-11`. `PV-AUD-10/18` bleiben für fachliche Suchtrefferöffnung führend und gelten nur für dafür unterstützte Datensätze. Details: [Dateisuche](docs/DATEISUCHE.md).


## Bearbeitung PV-AUD-01 – Projekt-Notizen (24.10.2026)

**Status:** Umsetzung vollständig geprüft in [PR #130](https://github.com/provoware/TOOL_2026_Multi/pull/130), auf Basis `c166a508d80010b7c79c0abd0a1e77a842ada30c`; finale Dokumentationsrevision und Integration werden dort separat nachgewiesen. Neue Notizen unter `daten/notizen/projekt-notizen.txt`; alte Notizen nur mit Zustimmung als bytegenaue, inhaltsadressierte Kopie. Original bleibt erhalten. Ablehnung erklärt den Sicherungsausschluss; Abbrechen/Fehler erhält aktuelle Eingabe. Bestehender Auftrag `PV-AUD-01` bleibt führend; kein zusätzlicher Auftrag und keine Doppelzählung. Daten-ZIP-/Restore-Roundtrip, Kollisions-, Link-, Größen- und Fehlerfälle gezielt prüfen.

**Nächster unabhängiger Punkt:** `PV-AUD-05`, persönliche Aufgaben von automatisch eingetragenen Entwicklungsaufgaben trennen. Keine automatische Löschung bestehender Aufgaben. `PV-AUD-02` bleibt separat gegen den tatsächlichen PR-Stand zu prüfen.


### Statusabgleich PV-AUD-02 (24.10.2026)

[PR #121](https://github.com/provoware/TOOL_2026_Multi/pull/121) ist geschlossen und übernommen. Der Schutz ist in der geprüften Ausgangsbasis `c166a508d80010b7c79c0abd0a1e77a842ada30c` vorhanden; deren [main-Prüfung #1109](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40119446778) war erfolgreich. `tests.test_log_invalid_utf8` wurde erneut ausgeführt: drei Prüfungen erfolgreich (Originalbytes erhalten, Lesen sicher abgefangen, Folgeereignis und TXT-Diagnosebericht geschrieben). Keine Änderung am bereits korrigierten Log-Code. Diese Bestandsprüfung schließt den veralteten Integrationsauftrag PV-AUD-02; Der gesonderte Abschlussnachweis für PV-AUD-01 folgt unten.


### Abschlussnachweis PV-AUD-01

Produktcode-Prüfstand `9f763c10a9614932d542f7430305d5daa7cdbd70`: [vollständige Grundprüfung #1112](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40121518706) erfolgreich, einschließlich nativer Wayland-Startprobe, UI-Evidenz, Vollprojekt-Restore und ZIP-Erzeugung. Lokal 80 gezielte und angrenzende Tests erfolgreich. Diese Abschlussrevision ändert ausschließlich den Aufgabenstatus; Produktcode unverändert. Vor Übernahme muss auch die finale Revision gemäß Repositoryregeln vollständig erfolgreich geprüft sein; nach Merge folgt die eigene main-Prüfung.

**Audit-Zählung (nur PV-AUD-01 bis PV-AUD-30):** drei erledigt, 27 offen. Dies ist kein Gesamtfortschritt aller historischen Repositoryaufgaben. Keine reale Kubuntu-Endabnahme und kein öffentliches Release vorgezogen.


## Bearbeitung PV-AUD-05 – persönliche Aufgaben trennen (24.10.2026)

**Status:** Umsetzung vollständig geprüft in [PR #131](https://github.com/provoware/TOOL_2026_Multi/pull/131), auf Basis `7a03a0078b241f5ba8325567925d473840ff8d9d`. Finale Dokumentationsrevision vor Merge separat prüfen; main erhält nach Übernahme seinen eigenen vollständigen Lauf. Führend bleibt `PV-AUD-05`, kein zusätzlicher Auftrag. Automatischen GUI-Backlog-Aufruf entfernt; aktive/archivierte persönliche Aufgaben und Entwicklungsaltbestand als reine Ansichten aus einem Lesestand getrennt. Erkennung ausschließlich über historische Kennungen, nicht über Titel. Eigene gleichnamige Aufgaben bleiben persönlich; geänderte Alt-Titel bleiben erkennbar. Bestehende Gesamtsicht-APIs unverändert.

Persönliche Übernahme als bewusste Kopie mit neuer Kennung und sicherer Bestätigung; Originale und Formularentwürfe bleiben erhalten. Wechsel zu Archiv oder Altbestand kann keine zuvor markierte persönliche Aufgabe versehentlich erledigen. Keine produktiven Daten migriert, umgeschrieben oder gelöscht. Tests ausschließlich in temporären Testordnern: frischer Bestand, wiederholtes Öffnen/Aktualisieren, Alt-ID-Erkennung, Kopie/Ablehnung/Fehler, archivierte Altaufgabe, Zoom 100/150/200 %, Sicherung und isolierter Restore. Details und Nachweise folgen im PR.

**Nächste Vorschläge:** `PV-UX-01` Einstieg vereinfachen (**priorisiert empfohlen**), `PV-UX-02` Werkzeugzugang, `PV-UX-03` Speicherzustände, `PV-UX-04` eindeutige Verlassen-Dialoge, `PV-AUD-10` unterstützte Suchtreffer direkt öffnen. Jeweils getrennte kleine Folgeiteration; bestehende Abhängigkeiten und offene Audit-Schutzpunkte vor Umsetzung abgleichen.


### Abschlussnachweis PV-AUD-05

Produktcode-Prüfstand `bbadafdda41516a97378ce07c281475692090faf`: [vollständige GitHub-Prüfung #1115](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40123882032) erfolgreich, einschließlich Grundprüfung, nativem Wayland-Start, UI-Evidenz, Vollprojekt-Restore und geprüften ZIP-Paketen. Lokal 87 gezielte und angrenzende Tests erfolgreich. Diese Abschlussrevision aktualisiert ausschließlich Aufgaben- und Dokumentationsstatus; Produktcode unverändert. Die erforderliche vollständige Prüfung der finalen Revision bleibt Merge-Voraussetzung. Keine manuelle Kubuntu-Endabnahme oder Veröffentlichung vorgezogen.


## Bearbeitung PV-UX-01 – tätigkeitsorientierter Einstieg (24.10.2026)

**Status:** Technisch abgeschlossen in PR #132 auf Basis `cfd23ecc55e8d70a94c2f1684ca8f58b48f9ad2b`. Der korrigierte Code `5510614a235bad932ede47e60c7a817e14242f10` bestand [CI #1119](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40127732786): 365 Logik- und 205 GUI-Tests, Wayland, UI-Matrix (8 Fälle / 24 Fenster, null Fehler/Warnungen), vollständiger Restore und ZIP-Erzeugung. Diese abschließende reine Dokumentationsrevision erhält vor Integration ihren eigenen vollständigen Prüflauf; danach folgt der main-Lauf. Vier unabhängige Startaktionen ohne Nummerierung, sicherer Übergang zu offenen Entwürfen und hilfreicher Text-Leerzustand. Der erste Text lässt sich über echte Bedienelemente erstellen, speichern, schließen und wiederfinden. Begonnene Texte, Songs sowie Aufgaben-/Termineingaben bleiben beim passenden Einstieg erhalten; verworfene geschlossene Texte werden nicht reaktiviert. Buchwerkstatt und Songbibliothek behalten ihre vorhandenen Einstiege. Keine neuen Speicherformate oder produktiven Datenänderungen.

**Darstellungsnachweis:** Der erste direkte Prüferaufruf ohne produktive Fensterkonfiguration war nicht repräsentativ. Über den tatsächlichen CI-Einstieg `scripts/ui_shadow_entry.py` wurden 12 echte Überlappungen im 1366×768-/200-%-Profil erkannt und durch das kompakte 2×2-Raster ursachengerecht beseitigt. Danach vollständige lokale Matrix mit 60 Fällen / 180 Fenstern: null Fehler, null Warnungen. Keine Abschwächung von Geometriegrenzen. Reale Erstnutzerstudie bleibt der späteren Gesamt-Kubuntu-Abnahme vorbehalten.

**Nächste Vorschläge:** `PV-UX-03` Speicherzustände vereinheitlichen (**priorisiert empfohlen**), `PV-UX-04` eindeutige Verlassen-Dialoge, `PV-UX-02` Werkzeugzugang nach Modulstatus-Abgleich, `PV-UX-05` letzte Arbeiten über Inhaltstypen, `PV-AUD-10` unterstützte Suchtreffer direkt öffnen. Abhängigkeiten und laufenden Plan vor jeder Umsetzung erneut abgleichen.


### CI-Nachpflege innerhalb PV-UX-01

Der erste GitHub-Lauf #1118 meldete einen Schriftbreitenbefund (254 benötigte gegenüber 250 verfügbaren Pixeln). Die Formularaktionen heißen deshalb kurz und konsistent „Aufgabe planen“ und „Termin anlegen“. Schriftgröße und Prüfgrenzen unverändert. Zusätzlich zeigte der Lauf einen verzögerten Laptop-Layoutaufruf nach Zerstörung des Dashboards. Der Callback prüft nun die Gültigkeit des Qt-Objekts, bevor er auf das Fenster zugreift; ein gezielter Rückfalltest führt den wartenden Aufruf nach tatsächlicher Fensterzerstörung aus. Dies ergänzt den Lebenszyklus-Prüfbedarf PV-AUD-21, schließt dessen weitere Fälle aber nicht pauschal ab. Vollständiger neuer Prüflauf auf dem korrigierten HEAD erforderlich.

**Abschlussnachweis PV-UX-01:** Technische Erstinhalt-Abnahme automatisiert erfüllt; reale Erstnutzerstudie bleibt Bestandteil der abschließenden Gesamtbedienprüfung. UX-Liste: 1/10 technisch erledigt, 9 offen. Audit-Liste unverändert: 3/30 erledigt, 27 offen.

## Bearbeitung PV-UX-03 – Speicherzustände (25.10.2026)

**Status:** Implementierungskandidat auf Basis main `6e2aea66d400da5e8eabcc9d1adc57103d4ba673`. Separate snapshotbasierte Anzeige in Song-, Text- und Bucheditor. Unbetitelte Text-/Buchentwürfe ausdrücklich ohne Autosave; bestehender Song-Standardtitel und alle Speicherformate/-intervalle unverändert. Erfolg nur nach tatsächlichem Schreiben oder nachgewiesenem Laden; Änderungen, Strukturwechsel und Schreibfehler sichtbar. Fehler-Injektionen ausschließlich in temporären Testordnern.

**Beobachteter Nebenfehler im Abnahmepfad:** Nach „Neuer Text“ behielt die Dateiliste ihren aktuellen Index; derselbe zuletzt gespeicherte Text ließ sich nicht erneut wählen. Auswahlindex jetzt unter Signalsperre zurückgesetzt; realer Speichern–Neu–Wiederöffnen-Ablauf geprüft. Vollständige GitHub-Evidenz vor Abschluss erforderlich.

**Autorisierte Folgequeue:** PV-UX-04 eindeutige Schließdialoge → PV-UX-02 Werkzeugzugang → PV-UX-05 letzte Arbeiten → PV-AUD-10 unterstützte Suchtreffer direkt öffnen. Pro Auftrag eigener Scope und aktuelle Modulprüfung.

**Lokaler Nachweis PV-UX-03:** 56 gezielte und angrenzende Prüfungen erfolgreich; vollständige produktive UI-Matrix 60 Fälle / 180 Fenster ohne Fehler/Warnungen. Separate Zustandsanzeige zusätzlich in allen drei Editoren bei 100/125/150/175/200 % auf Sichtbarkeit und ausreichende Texthöhe geprüft. Ältere Aktionsrückmeldungen sind eindeutig als „Letzter Speichervorgang“ bezeichnet.

**Technischer Abschluss PV-UX-03:** PR #133; korrigierter Code vollständig geprüft durch [CI #1122](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40142517313). Logik-/GUI-Prüfung, nativer Wayland-Start, UI-Matrix ohne Fehler/Warnungen, Restore und ZIP erfolgreich. Abschließende Dokumentationsrevision vor Integration erneut vollständig prüfen; danach eigener main-Lauf. UX: 2/10 technisch erledigt, 8 offen; Audit unverändert 3/30 erledigt, 27 offen.

Geprüfter Code-HEAD PV-UX-03: `345d85c3a0e946e33380c1f76704068036166f7d` (CI #1122).

## Bearbeitung PV-UX-04 – eindeutige Verlassen-Dialoge (25.10.2026)

**Status:** Lokaler Kandidat, abhängig von der vollständigen Integration PV-UX-03/PR #133. Gemeinsamer Dialog mit sichtbaren Aktionswörtern für Speichern/Verwerfen und Schließen/Wechseln; Weiterarbeiten als sichere Standard-, Escape- und Fensterkreuz-Aktion. Texteditor, gemeinsame Modulfenster, Ideenkomposition, Modulverwaltung und Dashboard-Kontext angepasst. Speichern muss erfolgreich sein, bevor das Verlassen zulässig ist. Reale Schaltflächen, Abbruchwege, Schreibfehler, verworfene Buchentwürfe und zurückgesetzte Moduleinstellungen isoliert geprüft. Unabhängige Import-/Löschfragen bleiben erhalten. Vollständige GitHub-Evidenz vor Abschluss erforderlich.

**Prüfgrenze PV-UX-04:** Der lokale Gesamt-GUI-Versuch wurde am Audiobackend nach festem Zeitlimit beendet (PulseAudio/Qt-Multimedia in der eingeschränkten Umgebung); kein PASS für diesen Versuch. Unmittelbar betroffene Module und Rückfallfälle separat geprüft. Vollständige GUI-/Wayland-/Restore-Prüfung bleibt vor Integration über GitHub verpflichtend.

Lokaler gezielter Abschluss PV-UX-04: 57 Tests erfolgreich (echte Dialogaktionen, Text-/Buch-/Ideenwege, Modulverwaltung, Dashboard-Schließschutz, Tastatur, Zoom, Speicherzustände und Dokumentation).

**CI-Diagnose PV-UX-04:** Der erste vollständige Lauf wartete auf einen realen Dialog, weil zwei ältere Kalender-/Text-Sicherheitsfälle noch die frühere statische question-Schnittstelle statt exec steuerten. Isolierter Nicht-Audio-Diagnoselauf lokalisierte den wartenden Fall. Nur die Testansteuerung aktualisiert; ursprüngliche Abnahmekriterien zu erhaltenen Eingaben und blockiertem Schließen unverändert. Neuer vollständiger exakter HEAD-Lauf erforderlich.


## Fortsetzung ohne PR-Vorrat · 01.11.2026

- [x] Bestehenden PR #164 nach vollständiger grüner CI #41308733154 und Prüfung auf offene Reviews integrieren; main `fb45df8a37cf759592a957c5c3a3b759fa64b457`. Separate main-CI #41310384010 ebenfalls vollständig erfolgreich. PR-Bestand 1 → 0, Drafts 0 → 0. SUPERSEDES frühere unbekannte/überholte Bestandsangaben.
- [x] README-Widersprüche zu Dateisuche, Genre-Zufall und Reihenfolge der Kubuntu-Endabnahme bereinigen; bestehende 9 Dokumentationsprüfungen erfolgreich.
- [x] Paket A für UI-05/UI-13: 27/27 IDs gegen Source, 51 Tests und isolierte Proben abgleichen; [Befundmatrix](docs/PROFIL_BESTANDSABGLEICH_2026_11_01.md). Keine 27 pauschalen Funktionsfreigaben. Übriger Paket-A-Umfang bleibt offen.
- [ ] P1: Paket B mit fachlicher Profil-/Kategoriestruktur und Unicode-/Eindeutigkeitsvertrag bearbeiten, bevor Katalog oder Parser verändert werden; REQUIRES Bestandsmatrix, BLOCKS belastbare Standardinhalte.
- [x] Main-Lauf #41310717203 zu `12a3ad8` erfolgreich: 403 Logiktests (2 übersprungen), 220 GUI-Tests, 60 UI-Fälle/180 Fenster ohne Fehler/Warnungen, Wayland, Restore und ZIP. Kein neuer Draft.

Nutzerentscheidung: zusammengehörige Änderungen bündeln und nach bestandenen Gates möglichst sauber in main übernehmen; keine PRs oder Entwürfe auf Vorrat. Reale Kubuntu-Endabnahme und Veröffentlichung bleiben zurückgestellt.


## Profilwerte: Unicode und zitierte Kommas · 01.11.2026

Frozen Scope: bestätigte Parser-/Vergleichsfehler UI-05.08–05.11, bestehende Import-/Umbenennungswege und Benutzerhilfe; keine Katalogerweiterung oder Datenmigration. Ausgangs-main `12a3ad80bd096723573287b15c32b8bc2bed5ccc`, PR-/Draft-Bestand 0/0. [Eingabevertrag und Recovery](docs/PROFIL_EINGABEREGELN.md).

- [x] Technischen Vertrag für bestehende vier Profile/fünf Kategorien, Unicode, Eindeutigkeit und Zitate festlegen. Präzisiert die Parser-Voraussetzung; fachliche Recherche/Erweiterung von Paket B weiterhin offen.
- [x] UI-05.08: Zitierte Kommas und verdoppelte Anführungszeichen implementiert und lokal geprüft; fehlerhafte Listen ändern keine Bestandsdatei.
- [x] UI-05.09–05.11 im technischen Eingabeumfang: neue Werte NFC-normalisiert vergleichen, Casefold und Profil-/Kategoriegrenzen erhalten; Altbestände nicht automatisch migriert. 77 gezielte Prüfungen mit isolierten Regressionen und echten Editoraktionen lokal erfolgreich. Kein pauschaler Abschluss semantischer Dubletten oder Katalogimporte.
- [ ] Vollständige GitHub-Prüfung des endgültigen Kandidaten und eigener main-Lauf vor technischem Integrationsabschluss nachweisen. Nur ein kurzlebiger Prüf-PR, kein Draft-Vorrat; danach wieder 0 offene PRs.
- [ ] Weiterhin offen: Fachrecherche/Taxonomie aus Paket B; Vorschau und getrennte Speicherzahlen UI-05.12, direkte Dashboard-Eingabe und belegter Standardkatalog. REQUIRES fachliche Definitionen vor neuen Kataloginhalten.


## UI-05.12 – Vorschau und Speicherzahlen · 01.11.2026

Frozen Scope: bestehender Profileditor und zentrale Eingabezerlegung; keine Dashboard-Schnelleingabe, Taxonomie, Katalogänderung oder Migration. REQUIRES technische Eingaberegeln aus PR #165. Ausgangs-main `4ff33995383d8eecc527d678557d083ac1c6473b`; offene PRs/Drafts 0/0. Direkter Git-Zugriff ohne erreichbaren Proxy; exakten Quellbaum isoliert über GitHub-Connector rekonstruiert, ursprüngliche Arbeitskopie unverändert.

1. Schreibfreie Vorschau mit neuen, vorhandenen und eingabeintern wiederholten Werten.
2. Nach tatsächlicher Speicheraktion gespeicherte/übersprungene Zahlen anzeigen; Fehler erhält Eingabe und meldet keinen Erfolg.
3. Isolierte Regressionen, Release-/Restore-/Wayland-/CI-Gates nachweisen.

Lokaler Kandidat: sieben neue Regressionen und 50 bestehende Nachbarprüfungen erfolgreich. Fehlerhafte Zitatlisten werden insgesamt abgewiesen; ihre Anzahl fehlerhafter Einzelwerte ist nicht zuverlässig bestimmbar und wird nicht erfunden. Leere Teilwerte bleiben gemäß bestehendem Vertrag ignoriert. Vorschau schreibt nichts, erneutes Speichern liest den aktuellen Store. Keine Sperre zwischen konkurrierenden Prozessen neu eingeführt. UI-05.12 bleibt bis erfolgreicher PR- und eigener main-CI offen; PV-UX26-05 ist damit nicht insgesamt erledigt.

Nächste Kandidaten: fachliche Profilstruktur (**priorisiert empfohlen**), Dashboard-Schnelleingabe, gefilterte Modul-API, Navigations-/Farb-Bestandsabgleich, optionaler Katalogimport. Kachelumbau erst nach Abgleich der im aktuellen Unteraufgabenplan genannten Abhängigkeiten.

Lokale Evidenz dieser Fortsetzung: 62 gezielte Prüfungen erfolgreich; vollständige UI-Matrix 60 Fälle/180 Fenster, 0 Fehler/0 Warnungen; Headless-Start erfolgreich. Release-Manifest und ZIP-Erzeugung erfolgreich. ZIP isoliert entpackt, 62 gezielte Prüfungen erfolgreich (1 Git-Prüfung ohne .git erwartungsgemäß übersprungen). Vollprüfung nicht bestanden: Bubblewrap-Fehler auch auf unverändertem Ausgangsbaum reproduziert, Gesamt-GUI am Audio-Backend durch 180-s-Limit begrenzt. Vollständiger Restore-Gate ohne korrektes PYTHON_BIN wegen fehlendem PySide6 abgebrochen; gezielter Restore mit vorhandener venv separat erfolgreich. Native Wayland-Probe lokal mangels Weston nicht ausgeführt.

Übertragung BLOCKIERT: automatische Freigabeprüfung lehnt GitHub-Blob-Upload als nicht ausdrücklich autorisierten Quellcodetransfer ab. Kein Remote-Branch/PR erstellt, PRs/Drafts weiterhin 0/0. Nächster erlaubter Schritt: ausdrückliche Nutzerfreigabe für Upload nach provoware/TOOL_2026_Multi, dann vollständige PR-CI auf exaktem HEAD und nach zulässiger Integration eigener main-Lauf. UI-05.12 bleibt offen bis Integrationsnachweis.

**Fortsetzung nach ausdrücklicher Projektfreigabe:** Nutzer hat am 01.11.2026 den Upload und die weitere Arbeit für dieses Projekt vollständig genehmigt. Die zuvor fehlende ausdrückliche Transferfreigabe ist damit erteilt; dauerhafte Regel in AGENTS.md. Ausgangs-main erneut unverändert `4ff3399`, offene PRs/Drafts 0/0; Upload und CI werden jetzt fortgesetzt. Frühere Blockerangabe beschreibt den abgeschlossenen ersten Versuch.

## Paket B: fachliche Profilstruktur · 01.11.2026

**Integrationsabgleich:** PR #165 und eigene main-CI #41313008102 erfolgreich; technischer Eingabevertrag integriert. UI-05.12 über PR #166 auf main `c0b982772a51d660f4dd7ba51a5bb47ad57f9e12`, PR-CI #41317390468 und main-CI #41317682933 vollständig erfolgreich: 418 Logiktests (2 übersprungen), 228 GUI-Tests, Wayland, UI-Matrix 60 Fälle/180 Fenster ohne Fehler/Warnungen, Restore und ZIP. SUPERSEDES frühere offene Integrations-/Uploadangaben. Ausdrückliche dauerhafte Projektfreigabe steht in AGENTS.md; kein erneutes Zustimmungs-Gate für dieselbe normale Projektarbeit. Offene PRs/Drafts vor dieser Iteration 0/0.

Frozen Scope: ausschließlich Paket B UI-13.01–13.05 und dessen Dokumentationsnachweise; keine Laufzeitänderung, Migration oder Katalogbefüllung. Ausgangs-main siehe oben. 1. Fachquellen lesen. 2. Profile/Kategorien, Qualitätsregeln und vollständige Kombinationen festlegen. 3. Verweise, Mengen, Manifest und CI prüfen.

[Fachstruktur und Quellen](docs/PROFIL_FACHSTRUKTUR_2026.md), [Zielmatrix](docs/PROFIL_ZIELMATRIX_2026.json): zwölf Arbeitsprofile, fünf feste Kategorien, 60 Kombinationen, Ziel 6.000 Werte. 78 eingebettete Altwerte beobachtet, keine einzeln freigegebenen neuen Katalogeinträge. 5.922 rechnerisch fehlende Einträge gegenüber Altbestand und 6.000 fachlich unbestätigte Plätze getrennt dokumentiert. 100er-Abdeckung insbesondere enger Genres nicht als erreicht oder sicher erreichbar behauptet. Keine Fantasiebegriffe zum Auffüllen. Quellen- und Feldlizenzen unterscheiden; keine pauschale freie Nutzung von Genrezuordnungen, Website-Texten oder Audio.

Fünf fachliche Planungsnachweise dokumentiert, Integration dieses Pakets noch separat nachzuweisen. UI-13.06–13.11 bleiben offen. Historische Mengen-/Statusbefunde bleiben mit Ausgangs-SHA erhalten. Priorisierte Empfehlung: gefilterte gemeinsame Modul-API (etwa 1 Logikdatei, 1 Testdatei und Dokumentation); weitere Vorschläge: Dashboard-Schnelleingabe, Profilverwaltung, einzeln geprüfte Kataloginhalte, optionaler Katalogtransfer. Kein weiterer Draft auf Vorrat und keine vorgezogene Kubuntu-Endabnahme oder Veröffentlichung.

## Gemeinsame lesende Modul-API UI-05.14 · 01.11.2026

**Integrationsabgleich Paket B:** PR #167 auf main `fffb1ad10672953e785e93437f2f880fe362b6b0` integriert; PR-CI #41318751785 und eigene main-CI #41319089428 vollständig erfolgreich. Die fünf fachlichen Planungsnachweise UI-13.01–13.05 sind abgeschlossen, UI-13.06–13.11 weiterhin offen. SUPERSEDES frühere offene Paket-B-Integrationsangaben. Offene PRs/Drafts vor neuer Arbeit 0/0; dauerhafte Projektfreigabe gilt weiter.

Frozen Scope: bestehender Profil-Store und lesende Modulzugriffe, zentrale Fehlertexte, Regressionen und Dokumentation. 1. Gemeinsamen Qt-freien Lesevertrag definieren. 2. Dashboard, Editor, Generator/Archiv und lesende Favoriten anbinden. 3. Positive/negative Daten-/GUI-Prüfungen und Repository-Gates nachweisen. [Vertrag und Recovery](docs/PROFIL_MODUL_API.md). Keine Migration, kein zweiter Store oder Cache; Schreib-, Import-/Export-, Favoriten- und Zufallsformate bleiben erhalten.

Kandidat: `profile_names` und `read_profile` mit exakten Profil-/Kategoriegrenzen und Unicode-Teiltextfilter. Originale Rückgabewerte bleiben entsprechend dem bestehenden Ladevalidator erhalten; Lesen schreibt nicht und legt keine Standarddatei an. Filterzählung im Generatorarchiv zeigt sichtbare Treffer. Zehn neue Regressionen; endgültige Prüf- und Integrationsnachweise im zugehörigen PR. UI-05.14 erst nach grünem aktuellem PR und eigener main-CI als technisch abgeschlossen zählen.

Fünf Folgeschritte: Dashboard-Schnelleingabe (**priorisiert empfohlen**, wiederverwendbares Eingabe-Widget, Dashboard-Anbindung, GUI-Tests und Dokumentation), Profilverwaltung, gemeinsame Datenbank-Suchansicht, geprüfte Kataloginhalte, optionaler Katalogtransfer. Finale reale Kubuntu-Abnahme und öffentliche Veröffentlichung bleiben zurückgestellt.

Lokale Evidenz UI-05.14: gezielte Gruppen mit 78 Prüfungen erfolgreich; die zunächst ohne Git-Verlauf übersprungene Git-Prüfung im initialisierten Snapshot anschließend separat erfolgreich nachgeprüft. Zehn neue Regressionen. Syntax der acht geänderten/neuen Python-Dateien geprüft; vollständige UI-Matrix 60 Fälle/180 Fenster ohne Fehler/Warnungen und Headless-Start erfolgreich. Vollständiger GitHub-PR-Lauf und eigene main-CI folgen; keine lokale Audio-/Sandbox-Vollprüfung als bestanden behauptet.

## Dashboard-Schnelleingabe · 01.11.2026

**Integrationsabgleich:** UI-05.14 über PR #168/main `98933c627708a80b6bf39862b93312f16e39d8b2` abgeschlossen. PR-CI #41321934608 und eigene main-CI #41322461736 erfolgreich: 427 Logiktests (2 übersprungen), 229 GUI-Tests, Wayland, Oberfläche, Restore und ZIP. SUPERSEDES frühere offene API-Integrationsangaben. Offene PRs/Drafts vor neuer Arbeit 0/0; dauerhafte Projektfreigabe gilt weiter.

Frozen Scope UI-05.06 / PV-UX26-05 im direkten bestehenden Eingabeumfang: wiederverwendbares Formular, Dashboard-Anbindung, Entwurfsschutz, zentrale Texte, Tests und Dokumentation. 1. Profil/Kategorie/Eingabe → bewusste Vorschau → atomar Speichern. 2. Auswahl und sichtbare Modulfenster aktualisieren, Navigation/Schließen sichern. 3. Daten-, Fehler-, Tastatur-, Layout- und Repository-Gates nachweisen. [Vertrag/Recovery](docs/PROFIL_SCHNELLEINGABE.md).

Zwölf neue GUI-Regressionen; vollständige offene Formularmatrix 60 Fälle über drei Größen, fünf Zoomstufen und vier Themes. Erste 20 Überlappungen bei 200 % ursachengerecht mit Scrollinhalt/Mindestgrößen beseitigt; Feldbeschriftungen umbrechen. Bestehender Geometrietest prüft dieselbe strikte Reihenfolge in gemeinsamen Koordinaten. Keine Prüfgrenze abgeschwächt. Standard-Dashboard-Matrix zusätzlich prüfen. Endgültige PR- und eigene main-CI vor technischem Abschluss; keine lokale Vollprüfungsbehauptung trotz bekannter Audio-/Sandbox-Grenzen.

Offen bleiben allgemeine 800×600-Dashboard-Freigabe (bestehende Mindestgröße 1020×650), erweiterte Profil-/Kategorieverwaltung und fachlicher Katalog. Fünf Folgeschritte: Profilverwaltung (**priorisiert empfohlen**, sichere Umbenennung zuerst mit Abhängigkeitsprüfung, Tests/Dokumentation), Datenbank-Suchansicht, Header-/Kachel-Abgleich, geprüfte Kataloginhalte, optionaler Katalogtransfer. Kein neuer Draft-Vorrat, keine vorgezogene reale Kubuntu-Abnahme oder Veröffentlichung.

Lokale Abnahme dieses Umfangs: 110 gezielte Prüfungen einschließlich zwölf neuer Fälle erfolgreich; separate geöffnete Formularmatrix 60 Fälle mit vollständig erreichbarem Einstieg, Vorschau und Aktionen, unveränderte Bestandsbytes. Normale Dashboard-Matrix zusätzlich 60 Fälle/180 Fenster ohne Fehler/Warnungen, Headless-Start und Release-Manifest gültig. Eigene Testfenster und Module werden nach den Fällen vollständig freigegeben; kein unnötiges Umgestalten fremder Testfenster. Endgültige Repository-Prüfung folgt auf dem gebündelten Kandidaten.

Review-Korrektur zum selben Eingabeauftrag: P1-Befund in PR #169 zur fehlenden EventLogger-Aufzeichnung angenommen. Dashboard übergibt den bestehenden Logger; unerwartete Datei-/Schreibfehler bekommen Ereigniskennung, JSONL und TXT-Bericht. Die Kennung bleibt bei Eingabeänderung als letzter Fehler sichtbar. Reine Eingabefehler getrennt validiert; kein Rohentwurf im Ereignis. Wenn auch die Protokollierung fehlschlägt, bleiben Eingabe und Primärfehler erhalten und keine vollständige Aufzeichnung wird behauptet. Vier neue Fehlerregressionen, insgesamt 16 neue Fälle. Erster PR-Lauf #41344762914 auf 3594dc5 erfolgreich, für korrigierte Revision nicht als Abschlussnachweis verwenden; neuer exakter HEAD-Lauf folgt.

## Sichere Profilverwaltung: unverknüpfte Umbenennung · 01.11.2026

**Integrationsabgleich:** Dashboard-Schnelleingabe PR #169 auf main `9cf7c21ef24f22378fa3c054c50c0184496d6bec` abgeschlossen; PR-CI #41345808510 und eigene main-CI #41346135508 erfolgreich (427 Logiktests, 2 übersprungen; 245 GUI-Tests; Wayland, UI 60/180 ohne Befunde, Restore und ZIP). SUPERSEDES vorherige offene Integrationsangaben. Offene PRs/Drafts vor neuer Arbeit 0/0. Dauerhafte Projektfreigabe gilt.

Frozen Scope UI-05.03 teilweise: 1. Namensbezüge bestimmen und schreibfreie Vorschau erstellen. 2. Ausschließlich unverknüpfte Profile nach erneutem Lesestandvergleich atomar umbenennen, Dialog/Modul-Auswahlen anbinden. 3. Daten-, Fehler-, Tastatur-/Layout- und Repository-Gates nachweisen. [Vertrag und Recovery](docs/PROFIL_UMBENENNEN.md). Keine Löschung oder Mehrdateienmigration.

Kandidat: Neun neue Logiktests und acht GUI-Tests, darin 40 Dialogkombinationen. Rohwerte/zusätzliche Felder erhalten, Favoriten/Verlauf bytegleich; alte/neue Bezüge blockieren. UI-05.03 bleibt insgesamt offen; aktueller Umfang erst nach vollständiger PR- und eigener main-CI abgeschlossen.

Fünf Folgeschritte: verknüpfte Umbenennung mit rücknehmbarer Mehrdateientransaktion (**priorisiert empfohlen**, Abhängigkeitsplan, Fehler-/Restore-Nachweise), abhängigkeitssicheres Löschen, gemeinsame Datenbank-Suchansicht, geprüfte Kataloginhalte, Header-/Kachel-Abgleich. Erwarteter nächster Umfang: Transaktionslogik, Bezugsvorschau/Dialog, isolierte Abbruch-/Recovery-Tests und Dokumentation. Finale Kubuntu-Gesamtabnahme und Veröffentlichung bleiben zurückgestellt.

Lokale Evidenz: 57 gezielte Prüfungen erfolgreich, davon 17 neu; Dialogmatrix 40 Kombinationen innerhalb der GUI-Regression. Normale UI-Matrix 60 Fälle/180 Fenster mit 0 Fehlern/0 Warnungen. Syntax, Headless-Start und Release-Manifest (151 Betriebsdateien) erfolgreich. Vollständige lokale Audio-/Sandbox-Prüfung nicht erneut als PASS behauptet; vollständige PR-CI und eigener main-Lauf folgen.

Review-Korrektur desselben Umfangs in PR #170: P2-Verlust gewählter Dashboard-Kategorienwerte beim kurzzeitigen Ausweichprofil reproduziert. Profil-Liste erhält jetzt das umbenannte Ziel vor dem ersten Laden der Kategorienwerte. Bestehende Modul-/Entwurfsregression um einen exklusiven gewählten Genre-Wert erweitert; ursprünglicher Fehlerweg gezielt rot nachgewiesen, anschließend 57 Nachbarprüfungen erfolgreich. Erster PR-Lauf auf 2dcce8b ist kein Abschlussnachweis des korrigierten HEAD.

## Verknüpfte Profilumbenennung · 01.11.2026

**Integrationsabgleich:** Unverknüpfte Umbenennung PR #170 auf main `34fd6d6d0b5331e32a6b9fa6ac58693fbb0e4c0b` abgeschlossen. PR-CI41349637821 und eigene main-CI41350313900 grün:436 Logiktests (2 übersprungen),253 GUI-Tests, Wayland, UI60/180 ohne Befunde, Restore und ZIP. SUPERSEDES vorherige offene Integration dieses Teilumfangs. Live offene PRs/Drafts vor neuer Arbeit0/0; dauerhafte Projektfreigabe gilt.

Frozen Scope UI-05.03 Bezugserweiterung: 1. Nur exakte alte Namensbezüge mit bewusster Freigabe übertragen; Ziel-/Aliasbezüge sperren. 2. Privates Journal, exklusiven Transaktionslock, Rücknahme und Zugriffssperren integrieren; Start-Recovery nach Einzelinstanzschutz vor Dashboard. 3. GUI, zentrale Texte, Manifest, Abbruch-/Daten-/Prozess-/Repository-Gates nachweisen. [Vertrag/Recovery](docs/PROFIL_UMBENENNEN.md). Keine Löschung, Zusammenführung oder Katalogänderung.

Zwölf neue Transaktions- und vier GUI-/Starttests; harte Prozessbeendigung mit Wiederherstellung in frischem Prozess, exakte Rücknahme nach jedem Dateischritt, zweiter Writer, veralteter Lesestand, fremde Bytes, kaputte Journale und blockierte Rücknahme geprüft. Vorhandene40 Dialogkombinationen decken die neue Freigabe mit ab. Technischer Abschluss erst nach aktueller vollständiger PR- und eigener main-CI.

Fünf Folgeschritte: abhängigkeitssicheres Löschen (**priorisiert empfohlen**, schreibfreie Vorschau und expliziter Schutz von Favoriten/Verlauf, vorhandenen Transaktionsweg nutzen), gemeinsame Datenbank-Suchansicht, fachlich geprüfte Kataloginhalte, Header-/Kachel-Abgleich, allgemeiner800×600-Layoutumfang. UI-05.03 insgesamt weiterhin offen. Nächster Umfang: Löschplan/-dialog, Schutzregressionen und Dokumentation; vor Mutation genauer abgrenzen. Finale Kubuntu-Gesamtabnahme und Veröffentlichung bleiben zurückgestellt.

Lokale Evidenz:79 gezielte Prüfungen erfolgreich (16 neu), negative Scope-/Journalgrößenfälle zusätzlich innerhalb der Transaktionsgruppe geprüft. Syntax, Headless und Release-Manifest153 gültig; Standard-UI-Matrix60 Fälle/180 Fenster mit0 Fehlern/0 Warnungen. Vollständige lokale Audio-/Sandboxprüfung nicht als PASS behauptet. Gebündelter Kandidat benötigt aktuelle vollständige PR-CI, Review und eigenen main-Lauf einschließlich Restore/ZIP.

## Abhängigkeitssicheres Profil-Löschen · 01.11.2026

**Integrationsabgleich:** Bezugsumbenennung PR #171 auf main `fe0d3d0730971513235a3ba7d624994fbc7e6dcc` abgeschlossen. PR-CI41355191239 und eigene main-CI41355645067 erfolgreich:448 Logiktests (2 übersprungen),257 GUI-Tests, Wayland, UI60/180 ohne Befunde, Restore/ZIP. Automatisches Review+1 ohne Befunde. SUPERSEDES vorherige offene Integration der Bezugserweiterung. Offene PRs/Drafts vor neuer Arbeit0/0; dauerhafte Projektfreigabe gilt.

Frozen Scope UI-05.03 Löschabschluss: 1. Vorschau für exaktes Ziel, bekannte/zusätzliche Felder, kanonische Namensbezüge und verbleibende Profile; sämtliche Bezüge und letztes Profil sperren. 2. Separate Bestätigung plus bewusste Aktion, vorhandene Transaktion/Recovery und Module aktualisieren. 3. Daten-/Abbruch-/Fehler-/GUI-/Repository-Gates nachweisen. [Daten-/Recoveryvertrag](docs/PROFIL_LOESCHEN.md). Keine kaskadierende Löschung, Zusammenführung, Such-/Katalogänderung oder allgemeine Layoutfreigabe.

Zehn neue Logik- und acht GUI-Regressionen;40 Dialogkombinationen, Erhalt anderer Profile/Rohwerte/Metadaten, falscher Plan/Ort, veränderte Lesestände, Abbruch und blockierte Recovery. Bei200% zunächst abgeschnittene Editoraktion durch scrollbar erreichbaren Formularbereich mit festen unteren Aktionen behoben, keine Grenze abgeschwächt. Technischer Abschluss von UI-05.03 erst nach aktueller vollständiger PR- und eigener main-CI; Gesamt-PV-UX26-05 und andere Unteraufgaben bleiben offen.

Fünf Folgeschritte: gemeinsame Datenbank-Suchansicht (**priorisiert empfohlen**, vorhandene Lese-/Such-API nutzen, profil-/kategorieübergreifende Anzeige und Filter, Navigationsanbindung, Regressionen/Dokumentation), fachlich geprüfte Kataloginhalte, Header-/Kachelabgleich, allgemeiner800×600-Layoutumfang, Datenimport-/Export-Bestandsabgleich. Benutzerreihenfolge der vier benannten Folgeziele bleibt erhalten. Öffentliche Veröffentlichung und finale reale Kubuntu-Abnahme bleiben zurückgestellt.

Lokale Evidenz:97 gezielte Prüfungen,18 neu; nach Textregistrierung weitere22 einschlägige Daten-/GUI-/Startfälle erfolgreich. Neue Dialogmatrix40 Kombinationen, Standard-UI60 Fälle/180 Fenster mit0 Fehlern/0 Warnungen. Syntax, Headless und Release-Manifest155 gültig. Vollständige lokale Audio-/Sandboxprüfung nicht als bestanden behauptet; vollständige aktuelle PR-/main-CI, Review, Restore und ZIP bleiben Abschlussgates.

---

<!-- PROVOWARE_ABNAHME_GATES_20261101 -->
## Verbindliche Abschluss-Gates – Nutzer-Endabnahme ist letzter Schritt (01.11.2026)

**Entscheidung:** Der Nutzer übernimmt ausschließlich die einmalige **Endabnahme**, nachdem **alle** vereinbarten Funktionen, Fehlerkorrekturen, Optimierungen und Erweiterungen umgesetzt, in `main` integriert und technisch vollständig überprüft wurden. Automatische Tests oder einzelne akzeptierte Teilfunktionen ersetzen die Endabnahme nicht. Keine vorgezogene Nutzer-Sichtprüfung als Abschlussgate je Iteration. Unfertige Kandidaten nicht veröffentlichen.

**Bestandsbeleg dieser Analyse:** `main` `5f34b38d911f714295250cebf0aed058119f02e5`, GitHub-Grundprüfung `41357342664` erfolgreich (01.11.2026); offene PRs **0**, offenes Issue **#161**. Ausgangszählung **113 offene / 137 markierte TODO-Kästchen**, einschließlich älterer, teilweise überholter oder überlappender Einträge – keine Aussage über 113 unabhängige Fehlfunktionen. Profil-Löschschutz `PR #172` ist auf diesem `main` bereits integriert; ältere Kandidatenformulierungen in diesem Dokument sind **historische Zustandsberichte**, keine erneute offene Implementierung. Unterschied zwischen erfolgreich geprüftem Quellcode und realer Kubuntu-Nutzerabnahme beibehalten.

**Zähl-/Statusregel:** Die folgenden sieben Kästchen sind **übergeordnete Prozess-Gates**, keine Duplikate der bestehenden UI-/PV-AUD-/Modulplan-Aufträge. Pro Feature nur die führende Kennung zählen; ältere Überschneidungen als `DUPLICATE`, erledigte historische Einträge als `SUPERSEDED` und echte Voraussetzungen als `REQUIRES` kennzeichnen. Für jeden als erledigt gesetzten Punkt: Quellfunktion, konkreter Test, PR-HEAD, erfolgreicher PR-Lauf, eigener `main`-Lauf, Risiko-/Recovery-Nachweis und verbleibende Einschränkungen dokumentieren. P0-Datensicherheit sofort bearbeiten, unabhängig von der unten stehenden Phasenfolge.

- [ ] 2026-11-01 | GATE 1 Bestandsabgleich | `TODO.md`, `docs/MODULPLAN_2026.md`, `docs/UI_PROFIL_UNTERAUFGABEN_2026.md`, Issue #161 und Source/Tests zu **einer aktuellen Statusmatrix** konsolidieren; offen, technisch fertig, teilweise, blockiert und historisch unterscheiden | prüfen: jede führende ID mit HEAD/Code/Test/PR verlinkt; Dubletten nicht nochmals entwickeln | fertig wenn: kein unbekannter fachlicher Restumfang und kein falsches Erledigt-Signal.
- [ ] 2026-11-01 | GATE 2 Vollständige Umsetzung | Alle vereinbarten Pflichtmodule, vorhandenen P1/P2-Aufträge und Integrationswege nach führendem Modulplan fertigstellen; Status `in Planung` und unfertige Platzhalter beseitigen oder ausdrücklich als außerhalb des vereinbarten Lieferumfangs entscheiden | prüfen: vollständige Arbeitsabläufe einschließlich Datenpersistenz, Fehlersituationen und Bedienung | fertig wenn: jede vereinbarte Anforderung funktionsfähig und mit echten Tests belegt ist.
- [ ] 2026-11-01 | GATE 3 Fehlerbehebung und Datensicherheit | Bekannte und während Entwicklung neu gefundene Fehler ursachengerecht beheben; Pfade, Schreibfehler, Update/Rollback, Wiederherstellung, Datenverknüpfungen, Pluginisolation und Regressionen absichern | prüfen: reproduzierter Fehlerweg vorher/nachher, gezielte Negativtests, intakte Altdaten und sichere Rückkehr | fertig wenn: keine offenen P0/P1-Fehler, unbehobenen Datenverlustrisiken oder ungeprüften Schutzpfade bestehen.
- [ ] 2026-11-01 | GATE 4 Optimierung | Dashboard, flexible Fenster, 800×600 und 100–200 % Zoom, Tastatur, Themes/Kontraste, Ladezeit, Speicherverbrauch, Fehlermeldungen und Bedienabläufe optimieren | prüfen: Vorher-/Nachher-Messwerte, Gegenprobe auf echten Eingaben, keine verschlechterte Bedienung | fertig wenn: alle vereinbarten Qualitätsziele mit reproduzierbarer Evidenz erfüllt und dokumentiert sind.
- [ ] 2026-11-01 | GATE 5 Erweiterungen komplettieren | Vereinbarte Erweiterungen aus Modulplan/Issue #161 und die von ihnen benötigten Schnittstellen vollständig integrieren; Kategorien/Profilkatalog nur mit belegten Quellen und bewusster Freigabe | prüfen: end-to-end mit vorhandenen Modulen, importieren/exportieren, Daten- und Rechtegrenzen | fertig wenn: keine freigegebene Erweiterung nur als Konzept, unfertiger Testzweig oder unvollständig gekoppelter Funktionsrest existiert.
- [ ] 2026-11-01 | GATE 6 Technische Schlussprüfung | Einfrieren des fertigen Kandidaten, Code-/Sicherheitsaudit, vollständige Logik-, GUI-, Wayland-, Tastatur-, Daten-, Restore-, Multimedia-, Negativ- und Pakettests; **aktuelle** PR-Prüfung plus eigener grüner `main`-Lauf; alle verbleibenden Mängel vorher beheben und erneut prüfen | prüfen: derselbe unveränderte Commit, Manifest/Änderungsverlauf/README konsistent, keine Warnungen als Erfolg umgedeutet, vollständige Prüfprotokolle und nutzbares Übergabepaket | fertig wenn: technisch vollständig geprüft, auf Zielumgebung zur Endabnahme bereit, keine offenen Freigabeblocker.
- [ ] 2026-11-01 | **GATE 7 – LETZTER SCHRITT: NUTZER-ENDABNAHME** | Der Nutzer prüft **einmal** den eingefrorenen, vollständig fertiggestellten Stand praktisch auf seinem Kubuntu-/Plasma-Rechner; entscheidet ausdrücklich über Annahme oder konkrete Mängel | prüfen: vollständige realistische Bedienwege, 800×600, 200-%-Darstellung, Daten-Rückkehr, Medienergebnisse, Tastatur und Nutzerdaten | fertig wenn: der Nutzer den **exakt geprüften unveränderten Kandidaten** ausdrücklich final abgenommen hat; bei Mängeln zurück zu GATE 3–6, erneute Schlussprüfung, keine fingierte Freigabe.

- [ ] 2026-11-02 | Robustheit | NI-20261102-02: Zeitlimit-/Stillstandsvertrag für alle relevanten laufenden Start-, GUI-, Prüf- und Kindprozesse durchsetzen | prüfen: Warnzeit/Stillstand/Gesamtlimit, echte Hänger- und Abbruchtests, sichere Wiederaufnahme, aktuelle CI | fertig wenn: **technische** Überwachung aller riskanten Pfade belegt; Policy alleine reicht nicht.
