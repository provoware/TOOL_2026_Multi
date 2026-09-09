# Iteration 23 – Zoom-sichere Layout-Härtung

## Hauptziel

Die Darstellung bei 100–200 % Zoom muss ohne überlappende Texte, zusammengedrückte Karten oder kollidierende Formularzeilen funktionieren. Schwerpunkt ist der reale 200-%-Fehlerzustand aus dem Kubuntu-Screenshot. Daten- und Fachlogik bleiben unverändert.

## Reproduzierter Befund

Der Screenshot bei 200 % zeigt vier strukturelle Fehlerklassen:

1. **Navigation:** Einträge werden vertikal in einen Bereich gepresst, der nicht mehr genug Höhe besitzt; Beschriftungen überlagern sich.
2. **Dashboard-Karten:** Die 2×2-Kartenstruktur bleibt trotz stark vergrößerter Schrift aktiv und zwingt Inhalte in zu kleine Teilflächen.
3. **Daten & Vorgaben:** Kategorien, Auswahlfelder und Kopfzeile kollidieren, weil die verfügbare Breite nicht um den Zoomfaktor bereinigt bewertet wird.
4. **Skalierungsmodell:** 1.594 physische Pixel werden bei 200 % weiterhin als „breites Fenster“ behandelt, obwohl effektiv nur rund 797 Pixel Arbeitsbreite auf 100-%-Basis zur Verfügung stehen.

## Ursache

Iteration 22 kombinierte drei Mechanismen, die einzeln sinnvoll waren, bei hohem Zoom aber gegeneinander arbeiteten:

- Breakpoints wurden anhand der **physischen** Fensterbreite gewählt.
- Schrift wuchs bis 200 % vollständig.
- Abstände, Mindesthöhen und viele Breiten wuchsen ebenfalls nahezu proportional, während kein vertikaler Überlaufcontainer für Navigation und Karten vorhanden war.

Das führte nicht zu einem einzelnen fehlerhaften Widget, sondern zu einem falschen Layoutmodell bei hohem Zoom.

## Umsetzung

- Responsive Breakpoints verwenden jetzt die **zoom-bereinigte effektive Arbeitsbreite** (`Fensterbreite × 100 / Zoom`).
- Schrift bleibt entsprechend der gewählten 100/125/150/175/200-%-Stufe vollständig vergrößert.
- Abstände, Rundungen, Padding und Bedienelement-Mindesthöhen wachsen bewusst flacher und sind bei hohem Zoom begrenzt.
- Große Überschriften wachsen ebenfalls flacher als Fließtext, damit sie Bedienelemente nicht verdrängen.
- Die linke Navigation erhält einen eigenen vertikalen Scrollcontainer, sobald die Einträge physisch nicht mehr gleichzeitig passen.
- Die Kartenfläche erhält einen eigenen vertikalen Scrollcontainer; Kopfzeile, Schnellkacheln, Projekt-Notiz, zuletzt bearbeitete Songs und Statusleiste bleiben außerhalb davon stabil erreichbar.
- Unter 960 px zoom-bereinigter Arbeitsbreite wechseln die vier Dashboard-Karten automatisch von 2×2 auf eine einspaltige Anordnung.
- Beim Zurückzoomen wird die ursprüngliche 2×2-Anordnung automatisch wiederhergestellt.
- Kategorien wie `Besonderheiten` erhalten bei 150–200 % eine schriftmetrisch berechnete Mindestbreite statt einer pauschalen zu kleinen Breite.
- Die Sidebar reserviert bei hohem Zoom anhand der tatsächlich benötigten Textbreite mehr Platz, bleibt aber gegen die Fensterbreite begrenzt.
- Lange Songbereichsnamen werden bei hohem Zoom ebenfalls anhand der Textbreite berücksichtigt.
- Die Dashboard-Überschrift darf umbrechen; der Untertitel wird nur bei sehr schmaler physischer Breite und hohem Zoom ausgeblendet.

## Neue Regressionen

`tests/test_zoom_controls_gui.py` prüft zusätzlich:

- 1.594×900 px bei 200 % erzeugt Scroll-Sicherungen statt vertikaler Kompression,
- alle vier Dashboard-Karten liegen bei diesem effektiven Platz in einer Spalte,
- Navigationseinträge überlappen geometrisch nicht,
- die fünf Profil-Auswahlzeilen überlappen geometrisch nicht,
- Zurückzoomen auf 100 % stellt die 2×2-Kartenstruktur wieder her.

Damit wird nicht nur geprüft, dass der Zoomwert gesetzt wird, sondern erstmals auch, dass der konkrete Fehlerzustand aus dem Screenshot strukturell ausgeschlossen bleibt.

## Schutzgrenzen

- keine Datenmigration,
- keine Änderung an Song-, Todo-, Kalender- oder Profildaten,
- keine Änderung am atomaren Schreibweg,
- keine Änderung der Backup-/Restore-Fachlogik,
- keine neue Produktfunktion,
- keine neue Abhängigkeit,
- keine Änderung der Zoomstufen 100/125/150/175/200 %.

## Automatische Abnahme

### Run #401 – gezielter Rückfall entdeckt

- 75 Logik-/Regressionstests: **grün**.
- GUI-Prüfung: genau **eine** veraltete Iteration-22-Annahme schlug fehl. Der alte Test verlangte, dass die Sidebar bei 125 % zwingend breiter als bei 100 % sein müsse.
- Diese Annahme widersprach dem neuen effektiven Breitenmodell: bei gleichem physischen Fenster kann die Oberfläche durch die zoom-bereinigte Klassifikation bewusst in den kompakten Modus wechseln.
- Restore wurde wegen des fehlgeschlagenen Vollprüfungs-Gates korrekt nicht gestartet.

Die Testannahme wurde nicht „weichgestellt“, sondern auf das eigentliche Nutzungsziel umgestellt: Kernbedienung bleibt sichtbar und Navigation besitzt sicheren Überlauf statt Überlagerung.

### Run #403 – vollständig grün

- **75 Logik-/Regressionstests** erfolgreich.
- **50 PySide6-GUI-Tests** erfolgreich, einschließlich der neuen 200-%-Überlappungs-, Scroll-, Formular- und Reflow-Regressionen.
- Schreibfehler-Simulation erfolgreich.
- Headless-Start erfolgreich.
- Release-Manifest gültig: **36 Betriebsdateien**.
- Vollprojekt-Restore: **OK**.
- Restore-SHA-256: `69e6cc8b3b5f3838b4478e3c0373ba0cb46c86942927d5b523f78a0cdb16214a`.
- geprüfter Branch-Head: `e1dbc977f6bfef97d396ac105ac54a09172d831f`.

Nach dem reinen Versions-/Evidence-Sync wird der endgültige PR-Head nochmals durch dieselbe Vollprüfung und dasselbe Restore-Gate geschickt. Erst danach darf gemergt werden.

## Reale Zielsystem-Abnahme

Die reale Kubuntu/KDE-X11-Sichtprüfung bleibt zusätzlich erforderlich, weil Offscreen-GUI-Tests keine reale Font- und Desktopdarstellung vollständig ersetzen. Dabei werden 100/125/150/175/200 % jeweils in normaler und maximierter Fenstergröße geprüft.
