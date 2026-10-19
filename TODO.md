# TODO – TOOL_2026_Multi

Stand: 2026-10-19

## Aktueller Entwicklungsauftrag – einzige verbindliche Kurzliste

Die **[Modulübersicht](docs/MODULPLAN_2026.md)** ist der verbindliche Gesamtplan. Die vielen weiter unten stehenden Kontrollkästchen sind historische Arbeitsprotokolle und dürfen nicht als aktuelle, voneinander unabhängige To-dos addiert werden.

- [x] PR #83 als durch #87 überholte Layoutalternative schließen.
- [x] PR #88 (0.18.3) mit automatischer PR- und Hauptzweigprüfung übernehmen.
- [x] PR #89 (0.18.4) nach Bereinigung des gestapelten Zweigs und grüner PR-Prüfung übernehmen.
- [x] Ursprüngliche und neue Modulplanung in einer verbindlichen Statusmatrix zusammenführen.
- [x] 0.18.5 Link-Schnellstarter mit GUI, Daten-, Browser- und Release-Tests in `main` integriert (PR #90, GitHub-Prüflauf #1019).
- [x] Sicherheitsprototyp der Update-Slots und Rückkehr auf Altversion in PR #100 integriert (CI #1039 grün).
- [ ] Update-Manager produktiv vervollständigen: klassische Installationen sicher migrieren, persönliche Daten trennen und Schnellstart/Startnachprüfung/Rollback vollständig anbinden.
- [x] Grafischen Modulbaukasten mit sicheren Datenvorlagen und Vorschau in PR #101 integriert (CI #1041 grün).
- [ ] Sichere Erweiterungs-API für fremde Plugins, signierte Pakete und wirkliche Module-Funktionen fehlen weiterhin.
- [x] Wikimodul mit Artikeln, Sammlungen, Verweisen, Versionen und GUI über Integrations-PR #97 in main übernommen (CI #1031 und #1033 erfolgreich).
- [x] Entwicklungspool mit Status, Arbeitsordnern, Kopien und ZIP in PR #102 integriert (CI #1043 grün).
- [x] Audioplayer, Bildvorschau und Video-/Slideshow-Basismodule in PR #103 integriert (PR-CI #1046 erfolgreich).
- [ ] Video: FFprobe integriert (PR #105). Videowarteschlange und Ein-/Ausblendeffekte in Iteration 66 an die GUI gekoppelt (Prüfkandidat); echte Bild-zu-Bild-Übergänge, vollständiger Batch-Nachweis und visuelle Ergebnisvergleiche fehlen.
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
