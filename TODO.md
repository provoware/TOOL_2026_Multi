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

### Umsetzung und Abnahme

- 🟢 moderne zentrale Dark-/Amber-Palette, Sans-Serif-Schrift und ruhigere Flächenhierarchie umgesetzt.
- 🟢 Schriftgrößen, Abstände, Rundungen, Eingabehöhen, Tabs, Scrollleisten und Splitter zentral vereinheitlicht.
- 🟢 Sidebar, Dashboard-Suche, Profilfelder, Songbereichsliste, Songeditor-Splitter und Bibliotheksspalten responsiv gemacht.
- 🟢 drei Rückfälle aus Run #368 ursächlich korrigiert.
- 🟢 GitHub-Grundprüfung **Run #385**: 75 Logik-/Regressionstests und 46 PySide6-GUI-Tests erfolgreich.
- 🟢 Vollprojekt-Restore Status `OK`, SHA-256 `c18e1ac25b8b2b43cf7c93d2c9dc8edf8b22dc9a521f3956c1d13d6cfae1d5de`.
- 🟢 PR #24 wurde in `main` übernommen (`1f12951156a7ca86e5533f05a17ade4802c79543`).

## Iteration 23 – Zoom-sichere Layout-Härtung

**Hauptziel:** Die reale 200-%-Darstellung muss ohne überlappende Navigation, kollidierende Formularzeilen oder zusammengedrückte Dashboard-Karten funktionieren.

### Umsetzung

- 🟢 Breakpoints auf zoom-bereinigte effektive Arbeitsbreite umgestellt (`Fensterbreite × 100 / Zoom`).
- 🟢 Schrift bleibt vollständig zoombar; Abstände, Rundungen, Padding und Mindesthöhen wachsen bewusst flacher.
- 🟢 große Überschriften skalieren flacher als Fließtext, damit sie Bedienelemente nicht verdrängen.
- 🟢 Navigation mit eigenem vertikalen Überlauf-/Scrollschutz versehen; Einträge werden nicht mehr in zu geringe Höhe gepresst.
- 🟢 Dashboard-Kartenfläche mit eigenem Überlauf-/Scrollschutz versehen; obere Schnellbereiche und Statusleiste bleiben stabil erreichbar.
- 🟢 unter 960 px zoom-bereinigter Arbeitsbreite automatische Umstellung der vier Hauptkarten von 2×2 auf eine Spalte.
- 🟢 Rückkehr auf 2×2 beim Zurückzoomen implementiert.
- 🟢 Kategorie- und Songbereichsbreiten bei hohem Zoom schriftmetrisch statt pauschal berechnet.
- 🟢 Sidebar-Breite bei 150–200 % an tatsächliche Textbreite angepasst und gegen Fensterbreite begrenzt.
- 🟢 Dashboard-Titel darf bei Bedarf umbrechen; sekundärer Untertitel wird nur bei wirklich schmaler Hochzoom-Darstellung reduziert.
- 🟢 fünf neue GUI-Regressionen gegen den konkreten 200-%-Fehlerzustand ergänzt.
- 🟢 keine Daten-, Speicher-, Backup- oder Restore-Fachlogik verändert.

### Abnahme

- 🟡 erste GitHub-Grundprüfung **Run #401**: 75 Logiktests grün; genau eine veraltete Iteration-22-Testannahme zur zwingend wachsenden Sidebar schlug fehl, Restore deshalb korrekt übersprungen.
- 🟢 veraltete Breitenannahme durch das tatsächliche Abnahmekriterium `Kernbedienung sichtbar + sicherer Überlauf` ersetzt.
- 🟢 GitHub-Grundprüfung **Run #403** vollständig erfolgreich.
- 🟢 **75 Logik-/Regressionstests** erfolgreich.
- 🟢 **50 PySide6-GUI-Tests** einschließlich der neuen 200-%-Überlappungs-, Scroll- und Reflow-Regressionen erfolgreich.
- 🟢 Schreibfehler-Simulation, Headless-Start und Release-Manifest mit 36 Betriebsdateien erfolgreich.
- 🟢 Vollprojekt-Restore Status `OK`.
- 🟢 Restore-SHA-256: `69e6cc8b3b5f3838b4478e3c0373ba0cb46c86942927d5b523f78a0cdb16214a`.
- 🔒 finaler Evidence-/Versions-Sync wird noch einmal auf demselben PR geprüft; erst danach Safe Merge.

## Danach

1. 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme bei **100/125/150/175/200 %** mit `bash kubuntu_abnahme.sh` durchführen.
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
