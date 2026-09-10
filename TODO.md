# TODO – TOOL_2026_Multi

Stand: 2026-09-10

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
- 🟢 reine Grenzwerttests für 1366×768@125 %, 1594×926@125 %, 1450-px-Grenze, 175-%-Hochzoom, Mindestgröße und Nicht-Dashboard-Fenster ergänzt.
- 🟢 Release-Invariant ergänzt: jedes produktive `app/*.py`-Modul muss als `release=true` im Manifest stehen.
- 🟢 neuer Runtime-Pfad ist in Vollprüfung und Release-Manifest aufgenommen.
- 🟢 keine Nutzer-, Speicher-, Backup-, Restore- oder Produktfachlogik verändert.

### Analyse- und Abnahmestand

- 🟠 erste Grundprüfung **#598** blockierte korrekt, weil der neue Release-Invariant `app/presentation_policy.py` als noch fehlenden Release-Manifest-Eintrag erkannte; alle 56 GUI-Tests waren bereits grün.
- 🟢 Manifest-Lücke ursächlich behoben; der Schutztest bleibt dauerhaft aktiv.
- 🟢 korrigierter technischer Head `117aa0eee4e3422804506d9bc1c1fc50f75d4591` in Grundprüfung **#600** vollständig erfolgreich.
- 🟢 **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, SHA-256 `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`.
- 🟡 Version-/Doku-/Manifest-Endstand 0.16.1 wird vor Merge nochmals vollständig durch dasselbe Gate geprüft.

## Danach

1. 🟡 reale sichtbare **Kubuntu 26.04 / KDE Plasma Wayland**-Abnahme mit `bash kubuntu_abnahme.sh` auf dem Zielrechner durchführen, besonders 1366×768 bei 125/150 %, zusätzlich 175/200 % und Theme `Kontrast`.
2. 🔴 anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

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
