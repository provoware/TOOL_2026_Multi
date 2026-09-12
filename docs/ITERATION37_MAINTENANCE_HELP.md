# Iteration 37 – Wartbarkeit, Entwicklungseffizienz, Repo-Hygiene und Hilfe

## Ausgangslage

Version 0.17.1 / Iteration 36 wurde auf `main` in Grundprüfung #750 vollständig bestätigt: 111 Logik-/Regressionstests, 76 GUI-Tests, 46 Release-Dateien, nativer Qt-Wayland-Start und Restore `OK`. Dieses Ergebnis bleibt der unveränderte Referenzstand vor der Wartungsiteration.

Beim anschließenden Wartbarkeits-Audit wurden drei konkrete Reibungspunkte gefunden:

1. `scripts/pruefen.sh` enthielt lange manuell gepflegte Listen für Runtime-Dateien und Tests. Neue Tests mussten dadurch an mehreren Stellen nachgetragen werden.
2. `scripts/_iter33_docs_apply.py` war ein nicht mehr benötigter Einmal-Helfer im Projektbaum.
3. Die bisherige „Fehlerhilfe (Recovery)“ half gut bei Fehlern, bot aber keine allgemeine, durchsuchbare Bedienhilfe.

## Umsetzung

### Schnellere und wartbarere Prüfungen

- `MANIFEST.json` ist die einzige Quelle für freigegebene Betriebsdateien.
- Logiktests werden automatisch aus `tests/test_*.py` erkannt.
- GUI-Tests werden automatisch aus `tests/*_gui.py` erkannt.
- `scripts/pruefen.sh --quick` dient als schnelle Entwicklungsprüfung ohne den langsameren GUI-/Release-Block.
- `--full` bleibt das verbindliche Freigabe-Gate.

### Repository-Hygiene

- der Einmal-Helfer `scripts/_iter33_docs_apply.py` wird entfernt.
- der Hygiene-Test blockiert künftig `scripts/_iter*`, `scripts/finalize_*` und temporäre `finalize-*`-Workflows.
- alte Remote-Branches werden nur nach Vergleich gelöscht; divergierte Branches werden nicht blind entfernt.

### Hilfe im Tool

- die Navigation heißt jetzt **Hilfe & Fehlerhilfe**.
- `F1` öffnet direkt die Schnellhilfe. `Strg+R` bleibt als kompatibler Recovery-Schnellweg erhalten.
- **Schnellhilfe** enthält durchsuchbare, UI-unabhängig definierte Themen mit konkreten Schritten.
- **Fehlermeldungen** behalten Filter, Wiederholungsanzeige, sichere nächste Schritte und optionale technische Details.
- Hilfetexte liegen zentral in `app/help_content.py` statt verteilt in Widget-Code.

## Sicherheitsgrenzen

- keine Nutzerdaten oder Datenformate werden migriert,
- keine Systemkonfiguration wird geändert,
- keine Passwörter oder neuen sensiblen Daten werden eingeführt,
- kein divergierter Branch wird automatisch gelöscht,
- reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme bleibt ein separater Zielrechner-Schritt.

## Abnahme

Der erste technische PR-Gate #764 hat **113 Logik-/Regressionstests** und **77 GUI-Tests** ausgeführt. Alle GUI-Tests waren grün; genau ein Logiktest blockierte korrekt, weil das neue Runtime-Modul `app/help_content.py` noch nicht im Release-Manifest eingetragen war. Zusätzlich erkannte die neue Entwickler-Grundausstattung diese Iterationsdokumentation als fehlend. Beide Metadatenlücken werden korrigiert, ohne Tests oder Schutzmechanismen abzuschwächen.

Vor Freigabe müssen anschließend `--quick`, die vollständige CI-Grundprüfung, GUI-Tests, nativer Wayland-Smoke, Restore und beide ZIP-Artefakte vollständig grün sein. Die endgültigen Freigabewerte werden danach in MANIFEST/TODO/CHANGELOG synchronisiert.
