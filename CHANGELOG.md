# Änderungsverlauf

## 0.16.1 – 2026-09-10 – Präsentationspolicy und Architekturhärtung

### Geändert
- neue Qt-unabhängige `app/presentation_policy.py` als einzige deterministische Klassifikation für Dashboard-Laptopmodus, breite Ansicht und Hochzoom ergänzt,
- Darstellungsgrenzen als benannte Policy-Konstanten zusammengeführt,
- unveränderlichen `PresentationState` für `wide`, `high_zoom`, `laptop_compact` und `restricted_navigation` eingeführt,
- `app/laptop_layout.py` auf die zentrale Policy umgestellt; bisherige private Helfer bleiben nur als Kompatibilitätsadapter,
- `app/navigation_ux.py` von der privaten Laptop-Hilfsfunktion entkoppelt und die bisher doppelte Hochzoom-Entscheidung entfernt,
- reine Grenzwerttests ohne QApplication/Eventloop für Referenz-Laptop, Großansicht, Breitengrenze, Hochzoom, Mindestgröße und Nicht-Dashboard-Fenster ergänzt,
- Release-Regression erweitert: jedes produktive `app/*.py`-Modul muss mit `release=true` im Manifest erfasst sein,
- Vollprüfung um Präsentationspolicy, neue Tests und Iteration-29-Dokumentation erweitert.

### Fehlerbehebung / Schutz
- erste Grundprüfung #598 deckte durch den neuen Release-Invariant unmittelbar auf, dass `app/presentation_policy.py` noch nicht im Release-Manifest stand,
- der fehlende Runtime-Eintrag wurde vor Freigabe ergänzt; damit kann derselbe Fehler bei späteren `app/*.py`-Modulen nicht mehr unbemerkt bleiben,
- alle 56 GUI-Tests waren bereits im ersten Lauf grün; der gefundene Fehler betraf ausschließlich Release-Vollständigkeit,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Laufzeitabhängigkeit eingeführt,
- sichtbare Nutzerführung und Kubuntu-26.04-/Wayland-Verhalten bleiben funktional unverändert.

### Abnahme
- korrigierter technischer Head `117aa0eee4e3422804506d9bc1c1fc50f75d4591` in Grundprüfung **#600** vollständig erfolgreich,
- **94 Logik-/Regressionstests** und **56 PySide6-GUI-Tests** erfolgreich,
- Release-Manifest mit **39 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start und nativer Qt-Wayland-Smoke erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`,
- der vollständig synchronisierte 0.16.1-Endstand wird vor Merge nochmals durch dasselbe Voll-/Wayland-/Restore-Gate geprüft.

## 0.16.0 – 2026-09-10 – Kubuntu 26.04 / native Wayland-Unterstützung

### Geändert
- Kubuntu 26.04 LTS mit KDE Plasma Wayland als offizielles Linux-Zielsystem für die reale Endabnahme festgelegt,
- bisherige X11-only-Prüfung auf Wayland-Sitzung, `WAYLAND_DISPLAY`, KDE/Plasma und Ubuntu/Kubuntu-Basis 26.04 umgestellt,
- tatsächlichen Qt-Plattformnamen über `QApplication.platformName()` in die Abnahme aufgenommen; `xcb`/XWayland gilt nicht als nativer Wayland-Pass,
- `kubuntu_abnahme.sh` weist ausdrücklich erzwungenes `QT_QPA_PLATFORM=xcb`, `offscreen` und `minimal` für die reale Abnahme ab,
- neuen `scripts/wayland_smoke.py` für einen echten nativen Qt-Wayland-Fensterstart ergänzt,
- GitHub-Grundprüfung um einen isolierten headless Weston-Compositor und echten Qt-Wayland-Smoke erweitert,
- bisherige Offscreen-GUI-Regressionen parallel beibehalten,
- Wayland-/26.04-Regressionen für gültige und blockierte Sitzungen, erzwungenes X11, alten Distributionsstand und Reportstatus ergänzt,
- reale Sichtabnahme um Wayland-spezifisches Fenster-, Menü- und Eingabefokus-Verhalten erweitert.

### Bewusst unverändert / Schutz
- `schnellstart.sh` bleibt backend-neutral und erzwingt weder Wayland noch X11,
- X11 wird nicht künstlich aus der allgemeinen Laufzeit entfernt; es ist lediglich kein gültiger Pass für die offizielle Kubuntu-26.04-Wayland-Endabnahme,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- Weston ist ausschließlich CI-Testinfrastruktur und keine neue Nutzer-Laufzeitabhängigkeit.

### Abnahme
- technischer Head `a7f2c168ecc3f0a2310fbff874cea33d30793d25` in GitHub-Grundprüfung **#567** vollständig erfolgreich,
- finaler 0.16.0-Head `2536bd3183e39ad1566496a067b817dd3ad30b07` in Grundprüfung **#579** erneut vollständig erfolgreich,
- **86 Logik-/Regressionstests** und **56 PySide6-GUI-Tests** erfolgreich,
- nativer Qt-Wayland-Smoke unter isoliertem Weston in beiden vollständigen Abnahmen erfolgreich; Qt meldet Plattform `wayland`,
- Release-Manifest mit **38 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale Feature-SHA-256 `23792d1c96db0b0fd61eaf74630593fbbf37578b64c4f82fd1f6644d2efa103e`,
- GitHub-CI lief auf Ubuntu 24.04.4; die reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt deshalb zusätzlich erforderlich,
- PR #35 anschließend ausschließlich für den geprüften Head per SHA-geschütztem Squash-Merge übernommen; resultierender Produkt-Main-Commit `3b829e799536cc1464e760f77ac7c28295c6ea70`.

## 0.15.3 – 2026-09-10 – Menü-Übersicht und Laiennavigation

### Geändert
- linke Dashboard-Navigation auf eine klare Nutzerhierarchie umgestellt: fertige Wege zuerst unter `Direkt nutzbar`, geplante Wege getrennt unter `Noch nicht fertig`,
- `Songtexte`, `Genres & Vorgaben`, `Todo-Liste`, `Kalender` und `Fehlerhilfe (Recovery)` als direkte fertige Hauptwege priorisiert,
- redundanten sichtbaren Menüpunkt `Alle Bereiche · geplant` entfernt,
- zehn geplante Bereiche standardmäßig eingeklappt und über einen einzigen Schalter ein-/ausblendbar gemacht,
- geplante Bereiche bei Bedarf in `Kreativ & Inhalte`, `Dateien & Werkzeuge` und `Projekte` gruppiert,
- wiederholte `· geplant`-Zusätze aus den einzelnen Planungszeilen entfernt,
- Menütexte in `texte/registry.json` zentralisiert,
- `app/navigation_ux.py` als eigene wiederverwendbare Menüschicht ergänzt und in Start-, Runtime- und Release-Pfad eingebunden,
- gezielte GUI-Regressionen für Standardmenü, Auf-/Zuklappen, Laptopmodus, 175/200-%-Hochzoom, Rückkehr zur großen Ansicht und Accessibility ergänzt.

### Fehlerbehebung / Schutz
- erste CI-Läufe deckten zwei Qt-Synchronisationsrückfälle zwischen Planungsmenü und bestehendem Laptop-/Hochzoom-Layout auf,
- die finale Lösung leitet Einschränkungen direkt aus der aktuellen Geometrieprüfung des Laptopmodus ab und ist damit unabhängig von der Reihenfolge einzelner Qt-Ereignisse,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Abhängigkeit eingeführt,
- große Dashboard-Ansicht außerhalb der Menüstruktur bewusst nicht umgebaut.

### Abnahme
- korrigierter technischer Head `b129b47bb8123fc7ea49680f2fa921f457164c56` in GitHub-Grundprüfung **#540** vollständig erfolgreich,
- finaler 0.15.3-Head `9cd8101ba19c5e28b41fa7793d35860462d38864` in Grundprüfung **#554** erneut vollständig erfolgreich,
- **81 Logik-/Regressionstests**, **56 PySide6-GUI-Tests** und **38 Release-Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale SHA-256 `add4af04204e694427aa2332edea4136c2816e0c196676391a5763e044be3718`,
- PR #34 anschließend per SHA-geschütztem Squash-Merge übernommen; resultierender Main-Commit `e7027e57c3c8709263b73543fd2b01be84e6639d`.

## 0.15.2 – 2026-09-10 – Release- und Bericht-I/O-Härtung

### Geändert
- zentralen `app.atomic_io.atomic_publish_file()`-Schritt für bereits fertig erzeugte Dateien ergänzt: Datei-`fsync`, atomarer Replace, bestmöglicher Verzeichnis-`fsync` und Temp-Cleanup,
- Log-Quarantäne und bereinigte JSONL-Neuschreibung, Rückfall-Lernstatus sowie menschenlesbare Ereignis-/Wächterberichte auf den zentralen atomaren Textschreiber umgestellt,
- Startstatus und Kubuntu-Abnahmeberichte auf denselben zentralen Schreibvertrag umgestellt,
- Release-ZIP von festem `.zip.tmp` auf eindeutige Tempdateien sowie zentralen Prepared-File-Publish umgestellt,
- Release-SHA-256-Begleitdatei atomar geschrieben,
- Diagnose-ZIP auf denselben zentralen Publish-Schritt vereinheitlicht,
- direkt startbare Diagnose-, Startstatus-, Prozesswächter-, Kubuntu-Abnahme- und Release-Skripte gegen fehlenden Projektimport abgesichert,
- Vollständigkeitsprüfung um `app/laptop_layout.py` und Iterationsdokumente 22–26 ergänzt,
- gezielte Regressionen für Replace-Fehler, Altbestandsschutz, Temp-Cleanup und direkte Skriptstarts ergänzt.

### Bewusst unverändert
- Append-only Ereignislog und Projekt-Notiz bleiben Append-only,
- Song-, Profil-, Todo- und Kalenderdatenformate bleiben unverändert,
- vorhandene Backup-/Restore-Fachlogik bleibt unverändert; der bereits gehärtete Restore-ZIP-Pfad wird nicht unnötig refaktoriert,
- keine neue Produktfunktion und keine neue externe Abhängigkeit.

### Abnahme
- technische Grundprüfung **#503** vollständig erfolgreich; Restore-SHA-256 `c7ff7f7e107d815918e9d52a84302bd245baa19f301cb3d4730ee5acff4b0806`,
- finaler Version-/Evidence-Head `d386f9e848237ff400fc60c518f73645b6516cee` in Grundprüfung **#513** erneut vollständig erfolgreich,
- **81 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich,
- Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale SHA-256 `560b9d9ca46ec3e0964f03b385941782e18e892d734c1b5e208dd69c6d4b5bf3`,
- PR #31 anschließend per SHA-geschütztem Squash-Merge übernommen; resultierender Main-Commit `00513bbaaee124da1e04a963aa70ce9e4757108e`.

## 0.15.1 – 2026-09-09 – Laptop-Kompaktlayout

### Geändert
- reversiblen Laptop-Kompaktmodus ausschließlich für das Dashboard ergänzt,
- Aktivierung auf knappe Laptopfläche bei Fensterbreite unter 1450 px und 125/150 % Zoom begrenzt,
- redundante geplante Navigation und die beiden reinen Planungskarten in diesem Modus ausgeblendet,
- produktive Navigation, alle sieben oberen Modulkacheln, Zoom und Farbtheme bleiben erreichbar,
- Profilkopf und entbehrliche Hilfstexte werden platzsparend verkürzt,
- Rückkehr auf große Fenster stellt die vollständige Darstellung automatisch wieder her,
- bestehende zentrale Responsive-/Theme-/Hochzoom-Engine bewusst nicht umgebaut,
- Regression für 1366×768 bei 125 %, Navigationszustand, produktive Erreichbarkeit, 1594×926-Rückkehr und unveränderten 175/200-%-Hochzoom ergänzt.

### Fehlerbehebung / Schutz
- erste Grundprüfung #464 fand ein fehlendes Testdouble für den neuen Startimport und eine ungewollte Wiederherstellung der Planungskarten beim Übergang in den bestehenden Hochzoom,
- beide Ursachen minimal korrigiert, ohne den Funktionsumfang zu erweitern,
- keine Nutzerdaten, Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Abhängigkeit eingeführt.

### Abnahme
- korrigierter Produktions-/Test-Head `d21799baa13562496b5e0821a17b1fb2c6cd89fe` in GitHub-Grundprüfung **#468** vollständig erfolgreich,
- **75 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich,
- Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `9ace0f9d3311dbe98fa4875b9c1ed86ed51ef1d48ad50a41b6527be09c160b01`,
- der nachgezogene Evidence-Sync wird vor Merge nochmals als finaler PR-Head vollständig geprüft.

## 0.15.0 – 2026-09-09 – Barrierefreiheit und Farbthemes

### Hinzugefügt / verbessert
- vier zentrale, sitzungsweite Farbthemes `Amber`, `Türkis`, `Lila` und `Kontrast`,
- kompakter Theme-Schalter im Dashboard-Statusbereich; geöffnete Fenster wechseln gemeinsam und neu geöffnete Fenster übernehmen das aktive Theme,
- Hochkontrast-Theme mit schwarzem Hintergrund, weißem Text, gelbem Akzent und 3-px-Fokusrahmen,
- zentrale `Qt.StrongFocus`-Grundregel für interaktive Buttons, Eingaben, Auswahlfelder, Listen und Tabellen,
- automatische Accessible Names aus sichtbaren Beschriftungen/Platzhaltern und Accessible Descriptions aus Tooltips,
- Screenreader-Bezeichnung `Farbtheme auswählen` für den Theme-Schalter,
- automatische WCAG-Kontrastregression der Kernfarben aller vier Themes mit mindestens 4,5:1,
- Hochzoom-Statusbereich so angepasst, dass bei 175/200 % die entbehrliche Legende ausgeblendet werden kann, der Theme-Schalter aber erreichbar bleibt.

### Schutz / Abnahme
- Theme-Auswahl gilt bewusst nur für die laufende Sitzung und erzeugt keinen neuen Schreibpfad,
- keine Nutzerdaten, Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine externe Font- oder Theme-Abhängigkeit ergänzt,
- Grundprüfung #428 für den Produktions-/Test-Head `cf2d694564909de72dfc65891af23fc525e87cc9` vollständig erfolgreich,
- 75 Logik-/Regressionstests und 50 PySide6-GUI-Tests erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `76a861f4e2e2466906f0eee50f1d19339aa2ea5709c0a540cf0bb51b15a49d20`,
- nach Synchronisierung von Doku/MANIFEST/TODO/CHANGELOG bleibt die Safe-Merge-Regel bestehen: der finale PR-Head wird nochmals vollständig geprüft.

## 0.14.2 – 2026-09-09 – Zoom-Härtung 150–200 %

### Geändert
- Schriftzoom und Geometriezoom getrennt, damit 200 % Schrift nicht gleichzeitig Abstände, Radien und Mindesthöhen verdoppelt,
- Geometriewachstum selbst bei 200 % auf maximal 25 % begrenzt und zusätzliche Breitenreserve auf maximal 10 % reduziert,
- ab 175 % reversiblen Hochzoom-Modus eingeführt,
- redundante geplante Navigationseinträge und reine Planungskarten bei 175/200 % platzsparend ausgeblendet, während obere Modulkacheln und produktive Bereiche erreichbar bleiben,
- Profilsteuerung, Songbereichsliste und Songeditor-Splitter für Hochzoom kompakter verteilt,
- Rückkehr auf 100/125/150 % stellt den vollständigen Normalmodus automatisch wieder her,
- gezielte GUI-Regression für Schriftwachstum, Geometriegrenze, Hochzoom-Sichtbarkeit und Rückkehr in den Normalmodus ergänzt.

### Schutz / Abnahme
- keine Daten- oder Fachlogik verändert,
- Grundprüfung #419 einschließlich Vollprüfung und Restore-Gate erfolgreich,
- PR #26 sicher in `main` übernommen; resultierender Main-Commit `80544ad8cfd13452f35f9218247570f65beb8b05`.

## 0.14.1 – 2026-09-09 – Responsive Design und visuelle Härtung

### Geändert
- reales Dashboard, Songbibliothek und Songeditor anhand der Kubuntu-Screenshots auf Schriftwirkung, Breiten, Abstände, Kontraste und Platznutzung geprüft,
- zentrale Dark-Palette ruhiger aufgebaut und Amber von flächendeckenden Rahmen auf gezielte Akzente, Primäraktionen und Status reduziert,
- systemweite Sans-Serif-Schrift ohne zusätzliche Font-Abhängigkeit festgelegt,
- Schrift-Hierarchie, Innenabstände, Rundungen, Eingabehöhen, Fokusrahmen, Tabs, Scrollleisten und Splitter vereinheitlicht,
- aktive Navigation auf dunkle Auswahlfläche mit linker Akzentlinie umgestellt,
- responsive Breitenstufen für kompakte, normale und breite Fenster eingeführt,
- Sidebar, Dashboard-Suche, Profilfelder und Songbereichsliste passen sich abhängig von Fensterbreite und Zoom an,
- Songeditor-Splitter verteilt Arbeitsbereich und Gesamtvorschau dynamisch,
- Songbibliothek verteilt Tabellenbreite gezielt auf Titel und Tags und hält kurze Spalten inhaltsbezogen,
- drei GUI-Rückfälle aus Grundprüfung #368 korrigiert: Suchplatzhalter-Erwartung, alte Recovery-Beschriftung und zu starre Kartenbreitenannahme,
- Responsive-Regressionen für Dashboardbreiten, Zoom-Breitenreserve und Tabellen-Spaltenmodi ergänzt.

### Schutz / Abnahme
- keine Datenmigration und keine Änderung an Song-, Todo-, Kalender- oder Profildaten,
- atomarer Schreibweg, Backup- und Restore-Fachlogik bleiben unverändert,
- keine externe Schriftart und keine neue Abhängigkeit eingeführt,
- Grundprüfung #368 hatte bereits 75 Logiktests erfolgreich abgeschlossen; das Restore-Gate wurde nur wegen der drei GUI-Rückfälle übersprungen,
- GitHub-Grundprüfung **#385** vollständig erfolgreich: 75 Logik-/Regressionstests und 46 PySide6-GUI-Tests grün,
- Schreibfehler-Simulation, Headless-Start und Release-Manifest mit 36 Betriebsdateien erfolgreich,
- Vollprojekt-Restore erfolgreich mit Status `OK` und SHA-256 `c18e1ac25b8b2b43cf7c93d2c9dc8edf8b22dc9a521f3956c1d13d6cfae1d5de`,
- PR #24 wurde anschließend in `main` übernommen (`1f12951156a7ca86e5533f05a17ade4802c79543`).

## 0.14.0 – 2026-09-09 – Laien-UX-Konsistenz

### Geändert
- gesamtes produktives Projekt aus Sicht eines Nutzers ohne technisches Vorwissen auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft,
- Dashboard-Suche wahrheitsgemäß als Song-Suche bezeichnet und `Logout` durch `Programm beenden` ersetzt,
- technische Oberflächenbezeichnung `Entwicklerinfo` zu `Projekt-Notiz` vereinfacht, ohne das bestehende Speicherformat zu ändern,
- geplante Bereiche sichtbar mit `In Planung` und gestricheltem Zustand von fertigen Bereichen getrennt,
- echte Startwege zu Songtexte, Todo-Liste und Kalender in der Dashboard-Startkarte ergänzt,
- Erstnutzer-Sackgasse in der leeren Songbibliothek durch `＋ Neuen Song schreiben` geschlossen,
- Songbibliothek gegen stille Nicht-Reaktionen bei fehlender Auswahl gehärtet und Datumsanzeige auf deutsches Format umgestellt,
- Songeditor mit Drei-Schritt-Führung, verständlicher Speicheranzeige und Sicherheitsfrage vor dem Entfernen eines Songbereichs ergänzt,
- Wiederherstellung älterer Songversionen zusätzlich nach Vorschau bestätigungspflichtig gemacht; automatische Sicherung des aktuellen Stands bleibt bestehen,
- Todo, Kalender und Profilverwaltung mit eindeutiger Schrittfolge und nächstem sinnvollen Schritt vereinheitlicht,
- Recovery als `Fehlerhilfe (Recovery)` auf einfache Nutzerfragen ausgerichtet; technische Details bleiben standardmäßig verborgen,
- Schnellstart und grafische Startanzeige auf sechs verständliche Prüfschritte umgestellt,
- `ANLEITUNG_LAIEN.md` auf schnellen Einstieg und konkrete Arbeitsabläufe neu strukturiert,
- README auf den aktuellen Stand 0.14.0 synchronisiert und von doppelter Versionshistorie befreit.

### Prüfung / Schutz
- neuer Regressionstest `tests/test_layman_ux_gui.py` prüft wahrheitsgemäße Beschriftungen, sichtbare Planungszustände, Erstnutzer-Songstart, Nicht-Silent-Fail-Verhalten und Sicherheitsbestätigungen,
- Kernkontraste für normalen Text, Hinweistext und Akzent gegen den Hintergrund werden automatisiert auf mindestens 4,5:1 geprüft,
- Laien-UX-Test ist in `bash scripts/pruefen.sh --full` integriert,
- keine Datenmigration, keine Änderung der Song-/Todo-/Kalender-/Profilformate und keine Änderung der atomaren Speicher- oder Restore-Fachlogik,
- PR #23 wurde als Merge-Commit `47a6124061268843d05d98ddadcb90066cc0d851` in `main` übernommen; die anschließend ausgewertete Grundprüfung #368 zeigte drei GUI-Test-Rückfälle, die in 0.14.1 korrigiert wurden.

## 0.13.4 – 2026-09-09 – Repository-Hygiene

### Geändert
- unreferenziertes Root-Artefakt `ChatGPT Image 8. Sept. 2026, 02_16_14.png` mit 2.056.107 Bytes aus dem Repository entfernt,
- `.gitignore` um typische unsortierte ChatGPT-/Screenshot-Bildexporte ausschließlich im Repository-Root ergänzt,
- neuen Regressionstest `tests/test_repo_hygiene.py` ergänzt,
- Vollprüfung um automatische Kontrolle auf versionierte Laufzeit-/Temp-Artefakte, lokale Root-Screenshots und übergroße Root-Dateien erweitert,
- veralteten, nicht mergebaren PR #2 als überholt geschlossen.

### Schutz / Abnahme
- keine Anwendungs-, Speicher-, Backup-, Restore- oder UI-Fachlogik verändert,
- keine Nutzerdaten verändert oder gelöscht,
- reguläre Projektbilder in passenden Unterordnern bleiben weiterhin versionierbar,
- Grundprüfung #335 zeigte einen Restore-spezifischen Rückfall: der Git-Hygienetest erwartete im entpackten Restore irrtümlich `.git`,
- der Test wurde auf seinen tatsächlichen Geltungsbereich begrenzt; das Restore-Gate selbst blieb unverändert aktiv,
- Grundprüfung #337 war anschließend vollständig erfolgreich, einschließlich Vollprüfung und Restore-Gate,
- geprüfter Head `caefca0d51b158ac9a3c8cfedc6fb18e0899a580` wurde als PR #21 per Squash-Merge übernommen; resultierender Main-Commit `aa66dc5ed106e470a533c4dd9f65cf80b726b05c`.

## 0.13.3 – 2026-09-09 – Backup-/Restore-I/O-Konsistenz

### Geändert
- Backup-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- validiertes ZIP wird vor Veröffentlichung per Datei-`fsync` synchronisiert, atomar ersetzt und der Verzeichniseintrag bestmöglich synchronisiert,
- Tempdateien werden auch bei Fehlern bereinigt,
- SHA-256-Begleitdatei und RESTORE-JSON-Bericht verwenden `app.atomic_io.atomic_write_text`,
- Backup-Dateinamen enthalten Mikrosekunden gegen schnelle Mehrfachlauf-Kollisionen,
- `ZipFile.testzip()` wird explizit ausgewertet und meldet beschädigte Einträge,
- Restore-Regressionen für Altbestandsschutz bei Replace-Fehler und Temp-Cleanup ergänzt.

### Schutz / Abnahme
- Restore-Pfadprüfung, Manifestvergleich, Vollprüfung und Headless-Start bleiben unverändert,
- Append-only Ereignislogs und Nutzerdaten wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #315 war erfolgreich; Vollprüfung und Restore-Gate sind grün bestätigt,
- geprüfter PR-Head `ca6ff3a7eb29a6bbf237a81199a8a8764280784a` wurde als PR #19 per Squash-Merge in `main` übernommen; resultierender Main-Commit `72719acbef5be379c1340b5771962a81fb40fc85`.

## 0.13.2 – 2026-09-09 – Diagnose-I/O-Konsistenz

### Geändert
- Diagnose-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- ZIP-Datei wird vor Veröffentlichung per `fsync` synchronisiert und anschließend atomar ersetzt,
- bestmöglicher Verzeichnis-`fsync` und Temp-Cleanup bei Fehlern ergänzt,
- SHA-256-Begleitdatei auf `app.atomic_io.atomic_write_text` umgestellt,
- Diagnose-Dateinamen um Mikrosekunden ergänzt, damit schnelle Mehrfachexporte nicht kollidieren,
- gezielte Regression für eindeutige Exportnamen und Replace-Fehler ergänzt.

### Schutz / Abnahme
- bestehende Datenschutz- und ZIP-Inhaltsprüfungen bleiben unverändert aktiv,
- Append-only Ereignislogs, Nutzerdaten, Restore-Logik, Backup-Skript und sonstige Berichtsschreiber wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #294 war erfolgreich und führte sowohl `bash scripts/pruefen.sh --full` als auch `python3 scripts/iteration_restore.py` aus,
- damit sind Vollprüfung und Restore-Gate für den geprüften Produktionspatch grün nachgewiesen.

## 0.13.1 – 2026-09-08 – Prozess- und Schreibkonsistenz

### Geändert
- zentralen Produktions-Schreibweg `app/atomic_io.py` für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien eingeführt,
- feste `.tmp`-Dateinamen durch eindeutige Tempdateien im jeweiligen Zielordner ersetzt,
- Datei-`fsync`, atomaren `os.replace` und bestmöglichen Verzeichnis-`fsync` vereinheitlicht,
- pro Projektordner einen `QLockFile`-basierten Einzelinstanz-Schutz eingeführt,
- Todo-Termine auf dieselbe lokale, zeitzonenlose ISO-8601-Semantik wie Kalendertermine vereinheitlicht,
- ENOSPC-/EROFS-Simulation auf den echten Produktionsschreiber umgestellt,
- gezielte Prozesskonsistenz-Regressionstests ergänzt.

### Schutz / Fehlerbehebung
- ein zweiter schreibender Dashboard-Prozess wird kontrolliert beendet, bevor er Nutzerdaten oder Laufzeitlogs öffnet,
- der Prozesswächter behandelt den kontrollierten Mehrfachstart-Code 10 nicht als Absturz,
- ein Replace-Fehler erhält den vorherigen Datenbestand und hinterlässt keine Tempdatei,
- unterschiedliche Schreibversuche kollidieren nicht mehr über denselben Tempnamen,
- nicht unterstützter Verzeichnis-`fsync` erzeugt nach bereits erfolgreichem Dateiersatz keinen falschen Speicherfehler,
- beschädigte Profilbestände mit doppelten Werten werden nicht mehr still bereinigt, sondern klar abgewiesen,
- die erste CI-Prüfung deckte drei Rückfälle in Testimport, Qt-Testdouble und direktem Simulationsstart auf; alle wurden ursächlich behoben und in der folgenden Vollprüfung verifiziert.

## 0.13.0 – 2026-09-08 – Kalender und Erinnerungen

### Hinzugefügt
- eigenes PySide6-Kalendermodul unter `Planung → Kalender`,
- echte Tages-, Wochen-, Monats- und Jahresbereiche für den gewählten Kalendertag,
- Termine mit Titel, optionaler Notiz, Beginn und Ende,
- Erinnerungen zum Terminbeginn sowie 5/15/30/60 Minuten oder 1 Tag vorher,
- 30-Sekunden-Erinnerungsprüfung als Kind des laufenden Dashboards, auch bei geschlossenem Kalenderfenster,
- gezielte Logik- und GUI-Rückfalltests für Bereichsgrenzen, Mehrtagestermine, Termineingabe, Einmal-Erinnerung, Dashboardbetrieb und Zoom.

### Schutz
- Beginn und Ende verwenden lokale Rechnerzeit ohne erfundene Zeitzonenumrechnung,
- Ende muss nach Beginn liegen; ungültige Termine werden vor dem Schreiben abgewiesen,
- Kalenderdaten werden atomar unter `daten/kalender/termine.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- eine Erinnerung wird erst nach erfolgreicher Anzeige atomar als erinnert markiert,
- Wiedereintritt während einer geöffneten Erinnerung wird blockiert,
- bei vollständig beendetem Dashboard wird bewusst kein separater Hintergrunddienst gestartet,
- keine destruktive Terminlöschung in dieser Iteration,
- bestehende Todo-, Profil-, Song-, Recovery-, Referenz-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.12.0 – 2026-09-08 – Todo-Liste mit Termin und Archiv

### Hinzugefügt
- eigenes PySide6-Todo-Modul unter `Planung → Todo-Liste`,
- Aufgaben mit Pflicht-Titel, optionaler Notiz und optionalem Datum/Uhrzeit-Termin,
- getrennte Ansichten für aktive Aufgaben und Archiv,
- Abhaken verschiebt die vollständige Aufgabe ins Archiv und setzt einen Abschlusszeitpunkt,
- zentrale Zoom-/Schriftsteuerung gilt auch im Todo-Fenster,
- gezielte Logik- und GUI-Rückfalltests für Terminierung, Abhaken, Archiv und Zoom.

### Schutz
- aktive Aufgaben und Archiv liegen zusammen in `daten/todo/todo.json`, damit beim Abhaken kein Zwischenzustand zwischen zwei Dateien entstehen kann,
- Speicherung erfolgt atomar über Tempdatei, `fsync` und `os.replace`,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- Abhaken löscht keine Aufgabe; der Eintrag wird vollständig ins Archiv verschoben,
- ungültige Termine und leere Titel werden vor dem Schreiben abgewiesen,
- bestehende Song-, Profil-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.11.0 – 2026-09-08 – profilbasierte DB-Eingaben

### Hinzugefügt
- Profile `HardTechno`, `HipHop/Rap` und `Hörspiele` mit Startwerten,
- getrennte Kategorien Genres, Stimmungen, Stil, Stimme und Besonderheiten,
- PySide6-Profilverwaltung zum Anlegen von Profilen und Werten,
- Profilauswahl direkt in der Dashboard-Karte `DB-Eingaben`,
- sofortige Aktualisierung der Dashboard-Auswahlfelder nach Profiländerungen,
- gezielte Logik- und GUI-Rückfalltests für Profilisolation, Duplikate und Dashboardbefüllung.

### Schutz
- Startprofile liegen bis zur ersten eigenen Änderung nur im Programmbestand und schreiben nicht beim Start,
- eigene Profildaten werden atomar unter `daten/profile/db_profile.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen lässt die vorherige Datei unverändert,
- doppelte Werte werden ohne Beachtung der Groß-/Kleinschreibung abgewiesen,
- Entfernen eines Werts verlangt eine ausdrückliche Bestätigung,
- bestehende Song-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.10.2 – 2026-09-08 – Zoom und Schriftgrößensteuerung

### Hinzugefügt
- `Strg + Mausrad` für zentrale Zoom-/Schriftgrößenänderung,
- sichtbare `A−`-/`A+`-Schaltflächen mit Prozentanzeige in der Statusleiste,
- Weitergabe der Zoomstufe an Dashboard, offene Songeditoren, Songbibliothek und Recovery,
- gezielter PySide6-GUI-Rückfalltest für Mausrad, Zoomgrenzen und sichtbare Bedienung.

### Schutz
- bestehende Zoomstufen 100/125/150/175/200 % bleiben unverändert,
- kein zweites Schriftgrößensystem eingeführt,
- keine Nutzerdaten verändert,
- globaler Ereignisfilter wird beim Schließen des Dashboards wieder entfernt.

## 0.10.1 – 2026-09-08 – Kubuntu/X11-Endabnahme vorbereitet

### Hinzugefügt
- neuer Klickstart `kubuntu_abnahme.sh`,
- neuer PySide6-Abnahmeassistent `scripts/kubuntu_abnahme.py`,
- Vorprüfung auf Linux, echte X11-Sitzung und KDE/Plasma,
- echter SIGTERM-/Prozesswächtertest ausschließlich in Tempdaten,
- sichtbare Bestätigung für Referenzlayout, Tastaturfokus und Zoomstufen 100/125/150/175/200 %,
- TXT- und JSON-Abnahmeberichte unter `berichte/`,
- gezielte Tests für X11/KDE-Erkennung, Signalprobe und Berichtsstatus.

### Schutz
- Wayland oder fehlendes `DISPLAY` werden nicht still als X11 akzeptiert,
- der Signaltest verändert keine Song-, Versions- oder sonstigen Nutzerdaten,
- `OK` wird nur vergeben, wenn automatische Prüfungen und alle sichtbaren Bestätigungen erfolgreich sind,
- Offscreen-CI wird ausdrücklich nicht als reale Kubuntu/KDE-X11-Sichtabnahme gewertet.

## 0.10.0 – 2026-09-08 – PySide6-Referenzdashboard

### Geändert
- gesamte produktive Oberfläche einheitlich auf **PySide6 6.11.2** migriert,
- Dashboardtitel auf `Provoware-Datenbank-Dashboard 2026` gesetzt,
- Dashboard nach dem bereitgestellten Dark-Orange-Referenzentwurf neu strukturiert: kompakter Header, Schnellkachelleiste, einklappbare linke Navigation, schmale „Zuletzt bearbeitet“-Zeile, 2×2-Hauptkarten und Statusleiste,
- zentrale Qt/QSS-Standards für Farben, Abstände, Schriftgrößen, Fokus und Zoom eingeführt,
- Songeditor, Songbibliothek, Recovery-Zentrale und Startanzeige ebenfalls auf PySide6 migriert,
- Recovery aus der Startfläche entfernt und **genau einmal** als linker Navigationspunkt geführt.

### Schutz
- bestehendes Song-Textformat und alle Nutzerdatenpfade bleiben unverändert,
- Autosave, Fokusverlust-Speicherung, Versionierung, Restore-Sicherung, Favoriten/Status, Metadaten und Exporte bleiben erhalten,
- geplante noch nicht freigegebenen Dashboardbereiche verändern keine Daten,
- zusätzlicher Referenzlayout-Test prüft Kartenstruktur/-proportionen, Sidebarbreiten, Schnellkacheln, Dark-Orange-Akzent und exakt einen Recovery-Eintrag,
- produktive GUI-Dateien werden auf unerlaubte Tkinter-Reste geprüft,
- bestehende Logik-, Sicherheits-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Gates bleiben verbindlich.

## 0.9.1 – 2026-09-08 – CI-Wartung

### Geändert
- GitHub Actions Checkout von `actions/checkout@v4` auf **`v7.0.1`** aktualisiert.

### Schutz
- keine fachliche Funktion, Songdatei oder Laufzeitlogik verändert,
- vollständige bestehende Logik-, Tk-GUI-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Prüfung bleibt unverändert verbindlich.

## 0.9.0 – 2026-09-08 – Songbibliothek vervollständigt

### Hinzugefügt
- freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags,
- kombinierbare Filter nach Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten,
- Favoritenkennzeichnung im Editor und Favoritenfilter in der Bibliothek,
- Bearbeitungsstatus `Idee`, `Entwurf`, `Überarbeitung`, `Fertig`,
- Sortierung nach letzter Bearbeitung, Titel, Genre, Tags und Status,
- Gruppierung nach Genre, Tags und Status,
- Versionswiederherstellung aus der schreibgeschützten Vorschau heraus,
- gezielte Logik- und Tk-GUI-Tests für Suche, Filter, Gruppierung, Status/Favorit und Restore.

### Schutz
- ältere Songdateien ohne Status/Favorit bleiben lesbar und erhalten nur sichere Standardwerte,
- Filtern, Sortieren und Gruppieren sind reine Ansichtsoperationen,
- vor jeder tatsächlichen Versionswiederherstellung wird der aktuelle Song erneut als Versionsstand gesichert,
- die Restore-Funktion akzeptiert nur die direkte Arbeitsdatei und den zugehörigen `.versionen/<Titel>/`-Pfad,
- fremde Versionspfade werden vor Schreibzugriff abgewiesen,
- Arbeitsdatei und Sicherungsstand werden atomar geschrieben,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.8.0 – 2026-09-08 – Songbibliothek und Versionsverwaltung

### Hinzugefügt
- Songbibliothek mit Titel, Genre, letzter Bearbeitung und Versionsanzahl,
- direktes Öffnen vorhandener Songs per Doppelklick, Enter oder Schaltfläche,
- bis zu fünf zuletzt bearbeitete Songs als Schnellkacheln im Dashboard,
- Song-Metadaten Stimmung, Stil, Stimme, Besonderheiten und Tags,
- automatische Versionsschnappschüsse vor geänderten Überschreibungen,
- schreibgeschützte Vorschau älterer Versionsstände,
- Exporte als TXT, Markdown, JSON und Nur-Songtext-TXT,
- Rückwärtslesen der bisherigen 0.7.0-Textdateien,
- gezielte Logik- und Tk-GUI-Tests für Bibliothek, Metadaten, Versionen, Kacheln und Exporte.

### Schutz
- das bestehende `.txt`-Arbeitsformat bleibt kanonisch; kein paralleles internes Songformat,
- identische Speicherungen erzeugen keinen Versionsmüll,
- Versionsstände werden getrennt unter `.versionen/` gesichert und nicht still überschrieben,
- Versionsansicht ist zunächst schreibgeschützt,
- Exporte verändern weder Arbeitsdatei noch Versionshistorie,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.7.0 – 2026-09-08 – Dashboard-Schnellspeicher und Songtexteditor

### Hinzugefügt
- einzeilige Entwickler-Schnelleingabe im Dashboardheader mit Enter- und Schaltflächenbestätigung,
- append-only Speicherung mit Zeitstempel in `Entwicklerinformation.txt`,
- Songtexteditor mit Titel, optionalem Genre, optionalem Sonstiges und Live-Vorschau,
- auswählbare Bereiche Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken und Instrumental,
- atomare Speicherung unter `daten/songtexte/<Titel>.txt`,
- Autosave alle fünf Minuten sowie bei Fokusverlust und beim Schließen,
- Logout-Schaltfläche mit Speichern aller offenen Songeditoren vor Sitzungsende,
- gezielte Logik- und Tk-GUI-Tests für Schnelleingabe, Speicherpfad, Bereichswechsel, Autosave und Logout.

### Schutz
- Schnellinfos überschreiben vorhandene Informationen nicht,
- Songdateien werden über eine temporäre Datei atomar ersetzt,
- ein Titelwechsel löscht keinen vorherigen Songstand,
- Logout wird gestoppt, wenn ein offener Songtext nicht gespeichert werden kann,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.6.0 – 2026-09-08 – Debug- und Recovery-Zentrale

### Hinzugefügt
- kombinierbare Filter nach Schweregrad und Bereich,
- Ereignisdetails per Doppelklick, Enter oder Schaltfläche,
- Wiederholungszähler und dauerhaft gespeichertes erstes Auftreten,
- zentrale Zoomstufen 100/125/150/175/200 Prozent,
- standardmäßig eingeklappte technische Details,
- gefahrlose `ENOSPC`-/`EROFS`-Simulation ohne echten Datenträgerverbrauch,
- automatisierte Tk-GUI-Prüfung für Tastatur, Fokus, Detailansicht und Zoom.

### Bedienung
- `F5` aktualisiert,
- `Ctrl++` und `Ctrl+-` ändern die Anzeigegröße,
- `Ctrl+0` setzt auf 100 Prozent,
- `Escape` schließt Detailfenster,
- interaktive Filter, Tabelle und Schaltflächen sind in der Fokusreihenfolge.

### Schutz
- Schreibfehlersimulation arbeitet ausschließlich in temporären Testpfaden,
- vorhandener Bestand muss bei simuliertem Fehler unverändert bleiben,
- ohne echte Tk-Sitzung wird die GUI-Prüfung nicht als bestanden gewertet,
- vorhandene Restore-, Diagnose-, Redaktions- und Wächter-Gates bleiben aktiv.

## 0.5.0 – 2026-09-08 – Diagnose- und Logging-Härtung

### Hinzugefügt
- Größen-/Altersrotation für das Ereignislog mit maximal fünf Archiven,
- Quarantäne beschädigter JSONL-Zeilen mit bereinigter Beweiskopie,
- datenschutzgeprüftes Diagnosepaket mit SHA-256,
- eigenes `ENDE`-Ereignis bei kontrolliertem Programmabschluss,
- gezielte Tests für Rotation, Quarantäne, Diagnoseexport und normales Programmende.

### Schutz
- beschädigte Logzeilen werden nicht mehr still verworfen,
- gültige Logzeilen bleiben beim Bereinigen atomar erhalten,
- Diagnosepakete enthalten nur bereinigte Textkopien und keine unveränderten Rohprotokolle,
- Datenschutzprüfung läuft unmittelbar vor ZIP-Übernahme erneut,
- vorhandene Restore-, Headless- und Wächter-Gates bleiben aktiv.

## 0.4.0 – 2026-09-08 – Recovery-Härtung

### Hinzugefügt
- vollständige Iterations-ZIP-/Restore-Kette mit SHA-256, sicherem Entpacken, Manifestvergleich, Vollprüfung und Headless-Start,
- fensterlose Startabnahme über `python3 -m app.main --headless-check`,
- separate Prozesswache `scripts/process_watch.py`,
- zentrale Log-Bereinigung `app/redaction.py`,
- gezielte Sicherheits-, Wächter- und Restore-Tests,
- sechsten Start-Checkpoint für Prozesswache/Headless-Gate,
- CI-Restore-Gate auf jedem Push und Pull Request.

## 0.3.0 – 2026-09-08 – Regression, Start, Standards und Release
- `REG-LOG-001` behebt `recent(0)`.
- globale UI-Standards, Start-Checkpoints und manifestgesteuerter Releasefilter ergänzt.
