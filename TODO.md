# TODO – TOOL_2026_Multi

Stand: 2026-09-12

## Iteration 38 – Fensterführung und kleine Displays

- [x] Bibliothek→Editor→Bibliothek ohne gleichzeitigen Fensterstapel
- [x] Bildschirmbegrenzung und sichere Zentrierung für Songeditor/Songbibliothek
- [x] neutraler Eingaberand, Akzent nur im Fokus, Rot/Grün als Zustände
- [x] Platzhalterkontrast erhöhen
- [x] sichtbares `&` in Hilfe & Fehlerhilfe reparieren
- [x] Songeditor: einklappbare optionale Angaben und Kompaktmodus
- [x] Songbibliothek: einklappbare Filter/Sortierung/Gruppierung
- [x] portable, validierte Fensterzustände ergänzen
- [ ] Iteration-38-CI, nativer Wayland-Smoke, Restore und ZIP-Artefakte vollständig grün bestätigen
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
- [ ] Webseite/URL, Profilname optional, verwendete E-Mail-Adresse, Passworthinweis und Sonstiges
- [ ] frei ergänzbare Felder
- [ ] Gruppen, Suche, Filter und Schnellwiederfinden
- [ ] Schutzkonzept: keine Passwörter unverschlüsselt speichern
- [ ] Import/Export, Backup, Restore und Datenschutzprüfung

### 3. Universeller Texteditor
- [x] Titel bestimmt sicheren Dateinamen
- [x] große Schreibfläche und Abschlussnotizenfeld
- [x] atomare Speicherung, Versionierung und Autosave
- [x] Charakterfibel-Zugriff
- [ ] farbliche Text-/Strukturhilfen weiter ausbauen

### 4. Textfragment- und Ideenarchiv
- [ ] einzelne oder mehrere Verse, Sätze, Fragmente und Schlagworte speichern
- [ ] Tags, Herkunft und Volltextsuche
- [ ] übersichtliche Karten-/Listenansicht
- [ ] Drag-and-drop in einen seitlichen Kompositionsbereich
- [ ] neue Texte aus Fragmenten erzeugen, ohne Originale zu löschen

### 5. Autonomes Updatemodul
- [ ] ZIP-Dateien sicher prüfen und entpacken
- [ ] Manifest, Version, Prüfsummen und Integrität vor Änderung validieren
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
- GitHub-Repositories als eigenes Dashboardmodul
- Genre-Zufall
- Reimfinder
- Dateisuche
- Textinhalt-Suche
- Trefferliste
- Duplikatprüfer

Abgeschlossene Detailhistorie steht im `CHANGELOG.md` und in `docs/ITERATION*.md`; sie wird bewusst nicht mehrfach gepflegt.
