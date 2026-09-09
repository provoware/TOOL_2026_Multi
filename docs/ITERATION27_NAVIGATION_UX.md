# Iteration 27 – Menü-Übersicht und Laiennavigation

Stand: 2026-09-10

## Hauptziel

Die linke Dashboard-Navigation aus realer Nutzersicht ordnen, damit fertige Wege sofort auffindbar sind und geplante Bereiche die Bedienung nicht überladen. Datenlogik, Speicherformate und die bereits gute große Hauptansicht bleiben unverändert.

## Befund aus dem realen Kubuntu-Screenshot

- fertige und geplante Bereiche waren stark vermischt,
- Zwischenüberschriften mit `⌄` wirkten wie anklickbare oder aufklappbare Menüs,
- die fünf Profilkategorien belegten dauerhaft einzelne Menüzeilen,
- zehn geplante Bereiche wiederholten ständig `· geplant`,
- wichtige fertige Wege wie Todo, Kalender und Fehlerhilfe standen unnötig weit unten.

## Umsetzung

- fertige Hauptwege stehen zuerst unter **Direkt nutzbar**: Songtexte, Genres & Vorgaben, Todo-Liste, Kalender und Fehlerhilfe,
- der redundante sichtbare Punkt `Alle Bereiche · geplant` entfällt aus der Nutzeransicht,
- geplante Bereiche stehen getrennt unter **Noch nicht fertig**,
- die zehn geplanten Bereiche sind standardmäßig eingeklappt und lassen sich mit einem einzigen Schalter ein- oder ausblenden,
- bei aufgeklappter Planung werden die Bereiche in **Kreativ & Inhalte**, **Dateien & Werkzeuge** und **Projekte** gruppiert,
- Einzelzeilen wiederholen nicht mehr ständig `· geplant`,
- Laptop-Kompaktmodus sowie 175/200-%-Hochzoom blenden die optionale Planung automatisch aus,
- beim Zurückkehren zur großen Ansicht wird der vorherige Nutzerzustand wieder korrekt hergestellt,
- sichtbare Menütexte kommen aus `texte/registry.json`,
- bestehende Aktionen werden wiederverwendet; keine Fachlogik wurde dupliziert.

## Gefundene und behobene Rückfälle

Die ersten beiden GUI-Gates fanden ausschließlich Synchronisationsprobleme zwischen dem neuen Planungsmenü und dem bestehenden Laptop-/Hochzoom-Layout. Zunächst wurde der neue Planungsschalter im Laptopmodus nicht zuverlässig ausgeblendet; danach blieb beim Zurückwechseln auf die große Ansicht kurz ein veralteter Compact-Zustand wirksam.

Die endgültige Lösung leitet die Einschränkung direkt aus derselben aktuellen Geometrieprüfung wie der bestehende Laptopmodus ab. Damit hängt die Menüsichtbarkeit nicht mehr von der Reihenfolge zweier Qt-Ereignisse ab.

## Schutzgrenzen

- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Datenmigration und keine Änderung von Speicherformaten,
- keine Änderung an atomarem Schreiben, Backup oder Restore,
- keine neue externe Abhängigkeit,
- große Ansicht bleibt außerhalb der Menüstruktur unverändert,
- Änderungen sind vollständig Git-reversibel.

## Technische Abnahme vor Versions-Sync

Der korrigierte technische Head `b129b47bb8123fc7ea49680f2fa921f457164c56` bestand GitHub-Grundprüfung **#540** vollständig:

- **81 Logik-/Regressionstests**: OK,
- **56 PySide6-GUI-Tests**: OK,
- Release-Manifest des vorherigen Versionsstands: **37 Betriebsdateien**,
- Headless-Start: OK,
- Vollprojekt-Restore: `OK`,
- Restore-SHA-256: `42c67e08e419e890c29620ab8e6fef8afeb12a24b1e7006bfc972ab69d87eefc`.

Beim Versions-Sync wird `app/navigation_ux.py` zusätzlich ausdrücklich als Release-Betriebsdatei aufgenommen; damit steigt der erwartete Release-Bestand auf **38 Dateien**. Das ist notwendig, weil `app/main.py` das neue Laufzeitmodul importiert.

## Finales Gate

Nach Synchronisierung auf Version **0.15.3** werden derselbe vollständige Prüfblock und das Vollprojekt-Restore erneut auf dem finalen PR-Head ausgeführt. Merge nur bei vollständig grünem finalem Head-Gate.
