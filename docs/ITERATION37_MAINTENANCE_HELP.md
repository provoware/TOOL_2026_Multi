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

- der Einmal-Helfer `scripts/_iter33_docs_apply.py` wurde entfernt.
- der Hygiene-Test blockiert künftig `scripts/_iter*`, `scripts/finalize_*` und temporäre `finalize-*`-Workflows.
- temporäre Iteration-37-Syncskripte und Sync-Workflows entfernen sich im gleichen Commit wieder und gehören nicht zum freizugebenden Projektstand.
- alte Remote-Branches werden nur nach Vergleich gelöscht; divergierte Branches werden nicht blind entfernt.

### Hilfe im Tool

- die Navigation heißt jetzt **Hilfe & Fehlerhilfe**.
- `F1` öffnet direkt die Schnellhilfe. `Strg+R` bleibt als kompatibler Recovery-Schnellweg erhalten.
- **Schnellhilfe** enthält acht durchsuchbare, UI-unabhängig definierte Themen mit konkreten Schritten.
- **Fehlermeldungen** behalten Filter, Wiederholungsanzeige, sichere nächste Schritte und optionale technische Details.
- Hilfetexte liegen zentral in `app/help_content.py` statt verteilt in Widget-Code.

## Sicherheitsgrenzen

- keine Nutzerdaten oder Datenformate werden migriert,
- keine Systemkonfiguration wird geändert,
- keine Passwörter oder neuen sensiblen Daten werden eingeführt,
- kein divergierter Branch wird automatisch gelöscht,
- reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme bleibt ein separater Zielrechner-Schritt.

## Abnahme

Der erste technische PR-Gate **#764** hat 113 Logik-/Regressionstests und 77 GUI-Tests ausgeführt. Alle GUI-Tests waren grün; genau ein Logiktest blockierte korrekt, weil das neue Runtime-Modul `app/help_content.py` noch nicht im Release-Manifest eingetragen war. Zusätzlich erkannte die neue Entwickler-Grundausstattung diese Iterationsdokumentation als fehlend. Die beiden Metadatenlücken wurden korrigiert, ohne Tests oder Schutzmechanismen abzuschwächen.

Der korrigierte technische Head `7368488c601160506a7b95a057c3e340bef64e8f` wurde in Grundprüfung **#769 vollständig grün** bestätigt:

- **113 Logik-/Regressionstests** erfolgreich,
- **77 PySide6-GUI-Tests** erfolgreich,
- **47 Release-Betriebsdateien** vollständig,
- Headless-Start erfolgreich,
- nativer Qt-Wayland-Smoke erfolgreich,
- Vollprojekt-Restore `OK`,
- Restore-SHA-256 `000b03420cb2a7cddc4ce80885e27aa9f96bdf62aa43a571116f099c16fbb177`,
- Runtime-Release-SHA-256 `993786558ce564dfbd5deee90ac9b7f1fe0067a321d5e12a7c0859f97cb6f28a`,
- Release- und Vollprojekt-ZIP wurden erzeugt und als CI-Artefakte hochgeladen.

Anschließend wurden Manifest und Dokumentation auf **Version 0.17.2 / Schema 30 / Iteration 37** synchronisiert. Die dafür verwendeten einmaligen Sync-Helfer wurden im selben Commit wieder entfernt. Dieser Dokumentationsabschluss löst den verbindlichen finalen PR-Gate auf exakt dem vollständig versionierten Freigabestand aus. Erst nach dessen Erfolg darf PR #50 gemergt werden; anschließend muss derselbe Gate noch einmal auf `main` vollständig grün sein.
