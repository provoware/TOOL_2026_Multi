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

**Hauptziel:** Ein Nutzer ohne technisches Vorwissen muss jederzeit erkennen können, wo er ist, was bereits funktioniert, was nur geplant ist, was nach einem Klick passiert und was bei einem Fehler geschützt bleibt.

### Umsetzung

- 🟡 gesamtes produktives Projekt aus Nutzersicht auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft.
- 🟡 Dashboard-Suche wahrheitsgemäß als reine Song-Suche bezeichnet.
- 🟡 `Logout` durch `Programm beenden` ersetzt und Speicherwirkung erklärt.
- 🟡 technische `Entwicklerinfo` in der Oberfläche zu verständlicher `Projekt-Notiz` gemacht; bestehendes Dateiformat bleibt kompatibel.
- 🟡 geplante Bereiche deutlich mit `In Planung` und gestricheltem Zustand markiert.
- 🟡 Startkarte mit direkten Wegen zu Songtexte, Todo-Liste und Kalender ergänzt.
- 🟡 Erstnutzer-Sackgasse in leerer Songbibliothek geschlossen: sichtbarer Knopf `＋ Neuen Song schreiben`.
- 🟡 Songbibliothek gegen stille Nicht-Reaktionen gehärtet; fehlende Auswahl und leere Treffer erhalten klare Hinweise.
- 🟡 Songeditor mit Drei-Schritt-Führung, verständlicher Speicheranzeige und Sicherheitsfrage vor Bereichsentfernung verbessert.
- 🟡 Versionswiederherstellung zusätzlich vor dem tatsächlichen Restore bestätigungspflichtig gemacht; bestehende automatische Sicherung bleibt aktiv.
- 🟡 Todo, Kalender und Profilverwaltung sprachlich vereinheitlicht und mit sichtbarem nächsten Schritt versehen.
- 🟡 Recovery als `Fehlerhilfe (Recovery)` auf Nutzerfragen ausgerichtet; technische Details bleiben standardmäßig verborgen.
- 🟡 Schnellstart und grafische Startanzeige auf sechs verständliche Prüfschritte umgestellt.
- 🟡 `ANLEITUNG_LAIEN.md` auf 30-Sekunden-Einstieg und konkrete Arbeitsabläufe neu aufgebaut.
- 🟡 README von historischer Doppelpflege befreit, auf Version 0.14.0 synchronisiert und als aktuelle Projektübersicht neu strukturiert.
- 🟡 neuen GUI-Regressionstest `tests/test_layman_ux_gui.py` ergänzt: Beschriftungswahrheit, geplante Zustände, Erstnutzer-Songstart, Nicht-Silent-Fail, Sicherheitsfrage und Kernkontraste ≥ 4,5:1.
- 🟡 Laien-UX-Test in `bash scripts/pruefen.sh --full` integriert.

### Schutzgrenzen

- 🟢 keine Datenmigration.
- 🟢 keine Änderung der Song-, Todo-, Kalender- oder Profil-Speicherformate.
- 🟢 keine Änderung des zentralen atomaren Schreibwegs.
- 🟢 keine Änderung der Backup-/Restore-Fachlogik.
- 🟢 keine neue Hauptfunktion außerhalb des bestehenden Umfangs; der neue Song-Knopf macht nur den bereits vorhandenen Songeditor erreichbar.

### Finale Abnahme

- 🔴 GitHub-Grundprüfung für den vollständigen Iteration-21-Branch ausführen.
- 🔴 Restore-Gate für denselben geprüften Branch erfolgreich bestätigen.
- 🔴 erst danach per Safe Merge in `main` übernehmen.

## Danach

1. 🟡 reale sichtbare Kubuntu/KDE-X11-Abnahme mit `bash kubuntu_abnahme.sh` durchführen.
2. 🔴 verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs ausdrücklich nicht auf Dateiersatz umstellen.
3. 🔴 anschließend nur noch einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

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

Abgeschlossene Detailhistorie steht im `CHANGELOG.md` und in `docs/ITERATION*.md`; sie wird bewusst nicht mehr im TODO doppelt gepflegt.
