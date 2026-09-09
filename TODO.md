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
- 🟡 diese Nachprüfung wird mit Iteration 22 ursächlich korrigiert und vollständig wiederholt.

## Iteration 22 – Responsive Design und visuelle Härtung

**Hauptziel:** Erscheinungsbild, Schrift, Abstände und dynamische Größenanpassung auf Grundlage realer Kubuntu-Screenshots professionell modernisieren, ohne Daten- oder Fachlogik zu verändern.

### Umsetzung

- 🟡 moderne zentrale Dark-/Amber-Palette mit ruhigerer Flächenhierarchie und stärkerem Fokuskontrast umgesetzt.
- 🟡 systemweite Sans-Serif-Schrift ohne externe Font-Abhängigkeit festgelegt.
- 🟡 Schriftgrößen, Innenabstände, Rundungen, Eingabehöhen, Tabs, Scrollleisten und Splitter zentral vereinheitlicht.
- 🟡 orange Vollrahmen auf Karten reduziert; Akzentfarbe gezielt für Primäraktionen, Fokus und Status eingesetzt.
- 🟡 aktive Navigation mit dunkler Auswahlfläche und linker Akzentlinie modernisiert.
- 🟡 responsive Breitenstufen für kompakte, normale und breite Fenster eingeführt.
- 🟡 Sidebar, Dashboard-Suche, Profilfelder und Songbereichsliste passen sich dynamisch an die Fensterbreite an.
- 🟡 Songeditor-Splitter verteilt Arbeitsfläche und Gesamtvorschau dynamisch.
- 🟡 Songbibliothek nutzt verfügbare Tabellenbreite gezielt für Titel und Tags; kurze Spalten bleiben inhaltsbezogen.
- 🟡 drei Rückfälle aus Run #368 ursächlich korrigiert: Suchplatzhalter-Test, Recovery-Beschriftung und starre Kartenbreitenannahme.
- 🟡 Responsive-Regressionen für Dashboardbreiten und Bibliotheksspalten ergänzt.
- 🟢 Datenformate, atomarer Schreibweg, Backup und Restore-Fachlogik unverändert.

### Finale Abnahme

- 🔴 vollständige GitHub-Grundprüfung für Iteration 22 ausführen.
- 🔴 Vollprojekt-Restore-Gate für denselben Head erfolgreich bestätigen.
- 🔴 erst danach per Safe Merge in `main` übernehmen.

## Danach

1. 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme mit `bash kubuntu_abnahme.sh` durchführen.
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
