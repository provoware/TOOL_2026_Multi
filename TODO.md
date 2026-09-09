# TODO – TOOL_2026_Multi

Stand: 2026-09-09

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

### Umsetzung

- 🟢 gesamtes produktives Projekt aus Nutzersicht auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft.
- 🟢 Dashboard-Suche als reine Song-Suche bezeichnet; `Logout` durch `Programm beenden` ersetzt.
- 🟢 technische `Entwicklerinfo` in der Oberfläche zur verständlichen `Projekt-Notiz` gemacht; Dateiformat kompatibel belassen.
- 🟢 geplante Bereiche deutlich mit `In Planung` und gestricheltem Zustand markiert.
- 🟢 Startkarte mit direkten Wegen zu Songtexte, Todo-Liste und Kalender ergänzt.
- 🟢 Erstnutzer-Sackgasse in leerer Songbibliothek mit `＋ Neuen Song schreiben` geschlossen.
- 🟢 Songbibliothek gegen stille Nicht-Reaktionen gehärtet.
- 🟢 Songeditor mit Drei-Schritt-Führung, verständlicher Speicheranzeige und Sicherheitsfrage vor Bereichsentfernung verbessert.
- 🟢 Versionswiederherstellung zusätzlich bestätigungspflichtig gemacht; automatische Sicherung bleibt aktiv.
- 🟢 Todo, Kalender, Profilverwaltung, Recovery und Startanzeige laienfreundlich vereinheitlicht.
- 🟢 `ANLEITUNG_LAIEN.md`, README, MANIFEST und CHANGELOG auf den neuen Bedienstand synchronisiert.
- 🟢 PR #23 wurde in `main` übernommen (`47a6124061268843d05d98ddadcb90066cc0d851`).

### Nachprüfung

- 🟡 GitHub-Grundprüfung Run #368: **75 Logiktests grün**, aber drei GUI-Regressionen durch veraltete Testannahmen beziehungsweise zu starre Kartenbreitenprüfung.
- 🟡 Restore-Gate von Run #368 wurde deshalb nicht gestartet.
- 🟢 die drei Nachprüfungsfehler wurden in Iteration 22 ursächlich korrigiert und erneut vollständig geprüft.

## Iteration 22 – Responsive Design und visuelle Härtung

**Hauptziel:** Erscheinungsbild, Schrift, Abstände und dynamische Größenanpassung auf Grundlage realer Kubuntu-Screenshots professionell modernisieren, ohne Daten- oder Fachlogik zu verändern.

### Umsetzung

- 🟢 moderne zentrale Dark-/Amber-Palette mit ruhigerer Flächenhierarchie und stärkerem Fokuskontrast umgesetzt.
- 🟢 systemweite Sans-Serif-Schrift ohne externe Font-Abhängigkeit festgelegt.
- 🟢 Schriftgrößen, Innenabstände, Rundungen, Eingabehöhen, Tabs, Scrollleisten und Splitter zentral vereinheitlicht.
- 🟢 orange Vollrahmen auf Karten reduziert; Akzentfarbe gezielt für Primäraktionen, Fokus und Status eingesetzt.
- 🟢 aktive Navigation mit dunkler Auswahlfläche und linker Akzentlinie modernisiert.
- 🟢 responsive Breitenstufen für kompakte, normale und breite Fenster eingeführt.
- 🟢 Sidebar, Dashboard-Suche, Profilfelder und Songbereichsliste passen sich dynamisch an Fensterbreite und Zoom an.
- 🟢 Songeditor-Splitter verteilt Arbeitsfläche und Gesamtvorschau dynamisch.
- 🟢 Songbibliothek nutzt verfügbare Tabellenbreite gezielt für Titel und Tags; kurze Spalten bleiben inhaltsbezogen.
- 🟢 drei Rückfälle aus Run #368 ursächlich korrigiert: Suchplatzhalter-Test, Recovery-Beschriftung und starre Kartenbreitenannahme.
- 🟢 Responsive-Regressionen für Dashboardbreiten, Zoom-Breitenreserve und Bibliotheksspalten ergänzt.
- 🟢 Datenformate, atomarer Schreibweg, Backup und Restore-Fachlogik unverändert.

### Abnahme

- 🟢 GitHub-Grundprüfung **Run #385** vollständig erfolgreich.
- 🟢 **75 Logik-/Regressionstests** erfolgreich.
- 🟢 **46 PySide6-GUI-Tests** einschließlich Laien-, Responsive-, Zoom- und Tabellenprüfung erfolgreich.
- 🟢 Schreibfehler-Simulation und Release-Manifestprüfung erfolgreich; 36 freigegebene Betriebsdateien.
- 🟢 Vollprojekt-Restore erfolgreich, Restore-Status `OK`.
- 🟢 Restore-SHA-256: `c18e1ac25b8b2b43cf7c93d2c9dc8edf8b22dc9a521f3956c1d13d6cfae1d5de`.
- 🟢 PR #24 wurde in `main` übernommen (`1f12951156a7ca86e5533f05a17ade4802c79543`).

## Iteration 23 – Zoom-Härtung 150–200 %

**Hauptziel:** Die real sichtbaren Überlagerungen und Abschneidefehler bei starkem Zoom ursächlich beseitigen, ohne Nutzerdaten oder Fachlogik anzufassen.

### Umsetzung

- 🟢 Schriftzoom und Geometriezoom technisch getrennt.
- 🟢 Schrift bleibt vollständig bei 100/125/150/175/200 % skalierbar.
- 🟢 Abstände, Radien, Mindesthöhen und andere Geometriewerte wachsen selbst bei 200 % nur noch moderat und maximal um 25 %.
- 🟢 Breitenreserve bei Hochzoom von früher bis 25 % auf maximal 10 % begrenzt.
- 🟢 ab 175 % reversiblen Hochzoom-Modus eingeführt.
- 🟢 redundante geplante Navigationseinträge bei 175/200 % ausgeblendet; dieselben Module bleiben oben als Kacheln sichtbar.
- 🟢 untere reine Planungs-Karten bei 175/200 % ausgeblendet, damit die produktiven Karten genügend Höhe behalten.
- 🟢 beim Zurückzoomen auf 100/125/150 % wird der vollständige Normalmodus automatisch wiederhergestellt.
- 🟢 Profilsteuerung und Songbereichsliste im Hochzoom kompakter dimensioniert.
- 🟢 Songeditor-Splitter priorisiert im Hochzoom den eigentlichen Arbeitsbereich stärker.
- 🟢 gezielte Regression für vollständigen Schriftzoom, begrenztes Geometriewachstum, Hochzoom-Sichtbarkeit und Rückkehr in den Normalmodus ergänzt.
- 🟢 Datenformate, atomarer Schreibweg, Backup und Restore-Fachlogik unverändert.

### Abnahme

- 🟢 GitHub-Grundprüfung **Run #412** vollständig erfolgreich.
- 🟢 vollständige Grundprüfung erfolgreich.
- 🟢 Vollprojekt-Restore erfolgreich.
- 🟡 aktueller Dokumentations-/Manifest-Sync wird nach derselben Safe-Merge-Regel nochmals vollständig geprüft.
- 🔒 PR #26 erst nach grünem finalem Head mergen.

## Danach

1. 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme mit `bash kubuntu_abnahme.sh` durchführen, besonders 150/175/200 % sowie normales und maximiertes Fenster.
2. 🔴 verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs ausdrücklich nicht auf Dateiersatz umstellen.
3. 🔴 anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

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
