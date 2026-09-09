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
- 1594×926 stellt die vollständige große Ansicht wieder her.

## Schutz

Keine Datenmigration, keine Änderung an Song-, Todo-, Kalender- oder Profildaten, keine Änderung am atomaren Schreibweg und keine Änderung an Backup/Restore.

## Abnahme

Finale GitHub-Grundprüfung einschließlich GUI-Regression und Vollprojekt-Restore ist vor Merge verbindlich.
