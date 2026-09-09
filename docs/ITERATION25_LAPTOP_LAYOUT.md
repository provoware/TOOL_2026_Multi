# Iteration 25 – Laptop-Kompaktlayout

## Hauptziel

Die vom Nutzer gezeigte reale 1366×768-Laptopansicht bei 125 % wird entzerrt, ohne das bereits gute große Dashboard zu verändern.

## Screenshot-Befund

- Die linke Navigation enthält auf knapper Höhe zu viele redundante geplante Einträge und wird vertikal zusammengedrückt.
- Die beiden unteren reinen Planungskarten nehmen Höhe weg, obwohl die produktiven oberen Karten wichtiger sind.
- Im Profilkopf konkurrieren Kartentitel, `Profil:`, Profilwahl und Bearbeiten-Schaltfläche um dieselbe schmale Zeile.
- Die Statuslegende wiederholt eine Information, die durch gestrichelte Planungselemente bereits sichtbar ist.
- Header und große Ansicht funktionieren bereits gut und sollen nicht neu gestaltet werden.

## Ursächliche Lösung

Ein separater Laptop-Kompaktmodus wird nur für das Dashboard aktiviert, wenn die Breite unter 1450 px liegt, der Zoom 125 oder 150 % beträgt und die reale beziehungsweise zoom-bereinigte Höhe knapp ist.

Im Kompaktmodus werden nur redundante Planungsübersichten ausgeblendet. Produktive Navigation, alle sieben oberen Modulkacheln, Zoom und Farbtheme bleiben erreichbar. Profilkopf und nicht zwingende Hilfstexte werden verkürzt. Beim Vergrößern des Fensters wird der vollständige Zustand automatisch wiederhergestellt.

Die bestehende zentrale Responsive-/Theme-/Zoom-Engine wird nicht umgebaut. Dadurch bleibt die bereits gute große Ansicht geschützt.

## Regression

`tests/test_dashboard_reference_gui.py` prüft zusätzlich:

- 1366×768 bei 125 % aktiviert den Laptop-Kompaktmodus,
- geplante Navigationsduplikate und reine Planungskarten sind ausgeblendet,
- Songtexte, Todo, Kalender, Fehlerhilfe, Theme und sieben Modulkacheln bleiben erreichbar,
- Profilkopf ist platzsparend,
- Ein-/Ausklappen der Navigation zerstört den Kompaktzustand nicht,
- 1594×926 stellt die vollständige große Ansicht wieder her,
- der bestehende 175/200-%-Hochzoom behält seine eigene Ausblendlogik und wird durch den Laptop-Restore nicht überschrieben.

## Gefundene Rückfälle und Korrektur

Die erste GitHub-Grundprüfung **#464** fand zwei klar begrenzte Fehler:

1. Der bestehende Starttest ersetzt GUI-Module durch Test-Doubles. Der neue Laptop-Layout-Import war in diesem Testdouble noch nicht enthalten; dadurch lieferte `app.main.main()` im Test `1` statt `0`.
2. Beim Übergang aus dem Laptop-Kompaktmodus in 175/200 % stellte die Laptop-Schicht die beiden Planungskarten kurz wieder sichtbar und überschritt damit die Zuständigkeit des bereits geprüften Hochzoom-Modus.

Beide Ursachen wurden minimal korrigiert:

- der Starttest enthält das neue Laptop-Modul als neutrales Testdouble,
- die Laptop-Schicht greift außerhalb ihres aktiven oder unmittelbar zu restaurierenden Zustands nicht mehr in normale oder hohe Zoomstufen ein; anschließend übernimmt wieder ausschließlich die zentrale Responsive-Engine.

Keine weitere Produktfunktion wurde in diese Reparatur aufgenommen.

## Automatische Abnahme

Der korrigierte Produktions-/Test-Head `d21799baa13562496b5e0821a17b1fb2c6cd89fe` wurde in GitHub-Grundprüfung **#468** vollständig geprüft:

- 🟢 75 Logik-/Regressionstests,
- 🟢 52 PySide6-GUI-Tests,
- 🟢 37 freigegebene Release-Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `9ace0f9d3311dbe98fa4875b9c1ed86ed51ef1d48ad50a41b6527be09c160b01`.

Der nachgezogene Evidence-Sync in README, TODO, MANIFEST, CHANGELOG und diesem Bericht wird vor Merge nochmals als eigener finaler PR-Head durch dieselbe Voll-/Restore-Prüfung geschickt. Erst ein vollständig grüner Endstand darf gemergt werden.

## Schutz

Keine Datenmigration, keine Änderung an Song-, Todo-, Kalender- oder Profildaten, keine Änderung am atomaren Schreibweg und keine Änderung an Backup/Restore.

## Noch offen

- finale Voll-/Restore-Prüfung des Evidence-Sync-Heads,
- danach Safe Merge von PR #29,
- anschließend reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner, besonders 1366×768 bei 125/150 % sowie 175/200 % und Theme `Kontrast`.
