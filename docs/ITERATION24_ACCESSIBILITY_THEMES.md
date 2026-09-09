# Iteration 24 – Barrierefreiheit und Farbthemes

## Hauptziel

Die vorhandene Oberfläche wird ohne Eingriff in Nutzerdaten oder Fachlogik besser für Tastatur, Screenreader und unterschiedliche Sehbedürfnisse nutzbar. Gleichzeitig werden mehrere kontrastgeprüfte Farbthemes zentral bereitgestellt.

## Befund

- Die Oberfläche besitzt bereits Zoom 100–200 %, deutliche Fokusrahmen und laienfreundliche Beschriftungen.
- Farbgebung war bisher auf ein einziges Amber-Theme festgelegt.
- Viele interaktive Qt-Elemente hatten zwar sichtbaren Text oder Tooltips, aber nicht systematisch einen expliziten `accessibleName` beziehungsweise eine `accessibleDescription`.
- Ein Farbwechsel sollte nicht in jedem Fenster separat implementiert werden, da dies Wartungs- und Konsistenzrisiken erzeugen würde.

## Umsetzung

- vier zentrale Themes: `Amber`, `Türkis`, `Lila`, `Kontrast`.
- alle Themes verwenden dieselbe Bedienlogik; nur Darstellungsfarben ändern sich.
- Theme-Auswahl wird automatisch im Dashboard-Statusbereich eingeblendet.
- Theme-Auswahl ist per Tastatur erreichbar und für Screenreader als `Farbtheme auswählen` benannt.
- ein Theme-Wechsel gilt sitzungsweit für alle geöffneten Provoware-Fenster; später neu geöffnete Fenster übernehmen das aktive Theme automatisch.
- Theme-Auswahl schreibt bewusst keine Nutzerdaten und keine Projektkonfiguration.
- interaktive Buttons, Eingaben, Kombinationsfelder, Listen und Tabellen erhalten zentral `Qt.StrongFocus`.
- fehlende Accessible Names werden aus sichtbarer Beschriftung, Platzhalter oder Elementtyp ergänzt.
- Tooltips werden, soweit vorhanden, zusätzlich als Accessible Description übernommen.
- das Theme `Kontrast` verwendet Schwarz/Weiß, helles Gelb als Akzent und einen 3-px-Fokusrahmen.
- Status und Planungszustände bleiben zusätzlich durch Symbole, Text und gestrichelte Konturen erkennbar; Farbe ist nicht das einzige Merkmal.
- der vorhandene Hochzoom-Modus bleibt erhalten. Bei 175/200 % wird nur die entbehrliche Statuslegende ausgeblendet, nicht der Theme-Schalter.

## Automatische Prüfung

### Vorprüfung

GitHub-Grundprüfung **#428** für den reinen Produktions-/Teststand war vollständig erfolgreich:

- 75 Logik-/Regressionstests: **OK**
- 50 PySide6-GUI-Tests: **OK**
- Schreibfehler-Simulation: **OK**
- Release-Manifest: 36 freigegebene Betriebsdateien
- Headless-Start: **OK**
- Vollprojekt-Restore: **OK**
- Restore-SHA-256: `76a861f4e2e2466906f0eee50f1d19339aa2ea5709c0a540cf0bb51b15a49d20`
- geprüfter Code-Head: `cf2d694564909de72dfc65891af23fc525e87cc9`

### Finale PR-Abnahme

Nach Synchronisierung von README, Laienanleitung, TODO, MANIFEST, CHANGELOG und Iterationsdokument wurde der endgültige PR-Head nochmals vollständig geprüft:

- GitHub-Grundprüfung **#440**: **SUCCESS**
- geprüfter PR-Head: `d750b98e0d98d7abe0441930f9ea52f0e0e85065`
- 75 Logik-/Regressionstests: **OK**
- 50 PySide6-GUI-Tests: **OK**
- Release-Manifest: **36 Betriebsdateien**
- Headless-Start: **OK**
- Vollprojekt-Restore: **OK**
- finale Restore-SHA-256: `ef1fd94f7a3a421416935373a213bba696407c80b441cf5a8108d22ea11c880f`
- Restore-Version: `0.15.0`

Die GUI-Regression prüft für alle vier Themes die zentralen Text-, Hinweis-, Akzent-, Fokus-, Status- und Fehlerfarben gegen den jeweiligen Hintergrund mit mindestens **4,5:1** Kontrast.

## Safe Merge

PR #27 wurde nach der vollständig grünen finalen Abnahme per Squash-Merge in `main` übernommen.

- Merge-Commit: `234f2f5279dc5b6e6d334010da701d3a53ad6ebb`
- keine nachträgliche Änderung an Produktionslogik oder Nutzerdaten.

## Schutzgrenzen

- keine Datenmigration,
- keine Änderung der Song-, Todo-, Kalender- oder Profilformate,
- keine Änderung am atomaren Schreibweg,
- keine Änderung an Backup-/Restore-Fachlogik,
- keine externe Schrift- oder Theme-Abhängigkeit,
- keine persistente Theme-Datei und damit kein zusätzlicher Schreibpfad.

## Reale Endabnahme

Offscreen-CI kann Tastaturpfade, Qt-Eigenschaften und Kontraste prüfen, ersetzt aber keine reale sichtbare Kubuntu/KDE-X11-Abnahme. Nach Safe Merge bleibt deshalb `bash kubuntu_abnahme.sh` der nächste reale Sichtnachweis – insbesondere für 150/175/200 % und das Kontrast-Theme.
