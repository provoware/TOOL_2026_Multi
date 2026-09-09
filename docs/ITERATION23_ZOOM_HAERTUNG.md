# Iteration 23 – Zoom-Härtung

## Hauptziel

Darstellungsfehler bei 150–200 % Zoom ursächlich beheben, ohne Daten-, Speicher- oder Fachlogik zu verändern.

## Befund aus dem realen 200-%-Screenshot

- Schrift, Abstände, Radien, Mindesthöhen und Breiten wurden bisher gleichzeitig nahezu linear vergrößert.
- Dadurch wuchs die Oberfläche stärker als der verfügbare Bildschirmplatz.
- Linke Navigationseinträge überlagerten sich vertikal.
- Die beiden unteren Planungs-Karten kollidierten mit den oberen Arbeitskarten.
- Profilzeilen und Schaltflächen wurden zu breit und schnitten Inhalte ab.
- Mehrzeilige Elemente verloren nutzbare Höhe.

## Korrektur

- Schriftzoom bleibt vollständig bei 100/125/150/175/200 % erhalten.
- Geometrie erhält eine getrennte Skalierung und wächst selbst bei 200 % höchstens um 25 %.
- Breitenreserve wächst bei Hochzoom nur moderat statt bis 25 %.
- Ab 175 % aktiviert das Dashboard einen Hochzoom-Modus.
- Redundante geplante Einträge werden in der langen Navigation ausgeblendet; die gleichen Module bleiben oben als sichtbare Kacheln erhalten.
- Die beiden unteren reinen Planungsübersichten werden bei 175/200 % ausgeblendet, damit die produktiven Start- und Datenkarten genügend Höhe erhalten.
- Bei Rückkehr auf 100/125/150 % erscheinen alle Planungsübersichten automatisch wieder.
- Profilsteuerung und Songbereichsliste verwenden im Hochzoom kompaktere Breiten.
- Songeditor-Splitter priorisiert bei Hochzoom den eigentlichen Arbeitsbereich stärker.

## Schutzgrenzen

- keine Datenmigration,
- keine Änderung an Song-, Todo-, Kalender- oder Profildaten,
- keine Änderung am atomaren Schreibweg,
- keine Änderung an Backup oder Restore,
- keine neue Produktfunktion,
- keine neue Abhängigkeit.

## Regression

Der Dashboard-GUI-Test prüft zusätzlich:

- 200-%-Schriftzoom bleibt vollständig erhalten,
- Geometrie wächst nicht mehr linear mit,
- redundante Planungsnavigation ist bei 200 % verborgen,
- die produktiven zwei Hauptkarten bleiben sichtbar,
- alle sieben Modul-Kacheln bleiben sichtbar,
- beim Zurückzoomen auf 100 % wird der vollständige Normalmodus wiederhergestellt.

Die vollständige GitHub-Grundprüfung einschließlich Restore-Gate bleibt vor Merge verbindlich.
