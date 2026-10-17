# Entwicklungsverfahren

Version 1.0 · 2026-09-08

## Ziel

Jede Änderung soll klein, begründet, rücknehmbar und prüfbar sein. Die Entwicklung soll ohne unnötige Nutzerbeteiligung vorankommen.

## Nummerierte Arbeitsweise

1. **Befund:** aktuellen Stand und konkretes Problem bestimmen.
2. **Abnahme:** messbar festlegen, wann der Schritt fertig ist.
3. **Sicherung:** vor riskanten Änderungen einen Sicherungspunkt erzeugen.
4. **Position:** betroffene Dateien und möglichst genaue Funktionen/Abschnitte bestimmen.
5. **Patch:** nur den kleinsten ursächlichen Änderungsblock anwenden.
6. **Direktprüfung:** genau das geänderte Verhalten prüfen.
7. **Nachbarprüfung:** nur angrenzende, real gefährdete Wege prüfen.
8. **Rückfallprüfung:** für behobene Fehler dauerhaft absichern.
9. **Dokumentation:** TODO, CHANGELOG und MANIFEST aktualisieren.
10. **Abschluss:** ZIP, Repository-Stand, offene Punkte und nächste Iteration ausgeben.

## Prüfstopp

Ein Prüfblock darf nicht ohne Anlass wiederholt werden. Er wird erneut ausgeführt, wenn:
- sich seitdem relevanter Code geändert hat,
- eine vorherige Prüfung fehlgeschlagen ist und die Ursache verändert wurde,
- neue Evidenz einen zusätzlichen Fehlerweg zeigt.

## Zweistufige Prüfung für schnellere Entwicklung

- Nach kleinen Codeänderungen zuerst `bash scripts/pruefen.sh --quick`: Syntax, Manifest/JSON, automatisch erkannte Logiktests, Schreibfehler-Simulation und Headless-Start.
- `bash scripts/pruefen.sh --full` bleibt Pflicht vor PR-Merge, Release und nach Änderungen an GUI, Release, Restore oder CI.
- Neue `tests/test_*.py` und `tests/*_gui.py` werden automatisch entdeckt. Sie dürfen nicht zusätzlich in manuellen Shell-Testlisten gepflegt werden.
- Freigegebene Betriebsdateien werden aus `MANIFEST.json` gelesen; parallele manuelle Runtime-Dateilisten sind zu vermeiden.
- Einmalige Patch-/Finalisierungshilfen müssen sich entfernen oder dürfen gar nicht erst committed werden; der Hygiene-Test blockiert bekannte Einmal-Helfer-Präfixe.

## Schlanke Entwicklung – weniger Code und weniger GitHub-Verkehr

Diese Regeln betreffen nur die Entwicklung und ändern **keine Bedienung** des Programms:

1. **Ein Hauptziel pro Änderungsantrag.** Vorher betroffene Stellen eingrenzen. Bestehende Funktionen benutzen, bevor neue Hilfsdateien oder zusätzliche Abhängigkeiten entstehen.
2. **Erst eine gezielte Prüfung, danach eine volle.** Lokal bzw. isoliert zunächst den betroffenen Test und `bash scripts/pruefen.sh --quick` verwenden. Vor Freigabe muss die vollständige GitHub-Prüfung erfolgreich sein. Das vollständige Prüfsystem, native Wayland-Startprüfung, Restore und Freigabepakete dürfen nicht übersprungen werden.
3. **Dateiänderungen gesammelt bereitstellen.** Inhaltlich zusammengehörende geprüfte Änderungen möglichst in *einem* Commit übertragen; nicht jede Textzeile über GitHub einzeln veröffentlichen. Dadurch entfallen unnötige Prüfstarts und Datenübertragungen.
4. **Ein PR löst einen Prüflauf aus.** Direkte Zweig-Pushes werden nicht mehr zusätzlich zum Pull-Request-Ereignis vollständig geprüft. Jeder Merge nach `main` startet unverändert die volle Prüfung; überholte PR-Läufe werden abgebrochen, nicht jedoch die Hauptzweig-Abnahme.
5. **Abhängigkeiten zwischenspeichern.** GitHub merkt bereits heruntergeladene Python-Pakete anhand von `requirements.txt`. Ändert sich diese Liste, erstellt GitHub einen neuen passenden Zwischenspeicher. Sicherheit und Versionsbindung bleiben unverändert.
6. **Gezielt lesen statt alles herunterladen.** Vor Änderungen zuerst Dateibaum/Dateinamen, dann nur die tatsächlich betroffenen Dateiausschnitte laden. Große ZIP-Pakete und Oberflächenbilder nur bei konkretem Prüfbedarf abrufen.
7. **Code nicht um jeden Preis verkürzen.** Eine verständliche Funktion ist wertvoller als ein schwer lesbarer Einzeiler. Gemeinsame Logik nur zusammenfassen, wenn dasselbe Verhalten mehrfach existiert. Keine zusätzlichen Werkzeuge, Pakete oder Steuerungsebenen ohne belegten Nutzen.
8. **Prüfnachweise zu genau einem Commit.** Erfolg, Version, Prüfergebnis und Freigabe müssen zum identischen Git-Stand gehören. Ein neuer Commit braucht die erforderlichen Prüfungen erneut.
9. **Keine Nutzerabnahme ohne Oberflächenänderung.** Reine Prüf-, Wartungs- und Dokumentationsverbesserungen automatisch absichern. Sichtbare Bedienänderungen bleiben eine eigene, getrennt zu bewertende Aufgabe.

**Wichtig:** Gespart werden doppelte *Ausführungen* und unnötige Übertragungen, nicht sicherheitsrelevante *Prüfschritte*.

## Entwicklungsarbeit gezielt messen

Diese rein internen Werkzeuge sind **optional**. Sie verändern keine persönlichen Dateien und benötigen keine neuen Pakete.

- **Code-Doppelungen finden:** `python3 scripts/code_doppelungen.py`. Zeigt identische Anweisungsfolgen mit Datei und Zeilennummer. Die Treffer sind Hinweise und dürfen nicht automatisch zusammengelegt werden.
- **Prüfläufe messen:** `python3 scripts/entwicklungsmessung.py --online`. Fragt die letzten 100 GitHub-Prüfläufe in einer einzigen Anfrage ab. Für die Entwicklung ohne Internet: `python3 scripts/entwicklungsmessung.py --datei laeufe.json`.
- **Zwischenspeicher belegen:** Optional `--protokoll job.txt` mit einem bereits gespeicherten GitHub-Protokoll angeben. Ohne Nachweis wird kein erfolgreicher Zwischenspeicher-Treffer behauptet.
- **Änderungsumfang belegen:** Optional `--pr-datei pull-request.json` für Zahl der Dateien sowie ergänzte und entfernte Zeilen.
- **Messwerte richtig lesen:** Laufzeiten sind Näherungswerte, mehrfach geprüfte Commits sind nicht zwingend verschwendete Prüfungen. Vorher-/Nachher-Vergleiche sollen gleichartige Prüfungen gegenüberstellen. Diese Messung zählt **keine tatsächlichen übertragenen Bytes**.

Die bisherige allgemeine Fensterverwaltung wurde ohne Verhaltensänderung aus `app/ui.py` in das kürzere, einzeln wartbare `app/window_lifecycle.py` ausgelagert. Die bisherigen Importnamen bleiben erhalten.

## Nutzerbeteiligung minimieren

Die Entwicklung trifft reversible technische Entscheidungen autonom. Fehlende reale Geräte-/Oberflächenprüfungen werden klar als externe Abnahme markiert, statt den Nutzer für jeden Zwischenschritt zum Testen einzuspannen.

## Definition „fertig“

Ein Punkt ist erst 🟢, wenn Änderung **und** passende Prüfung nachweisbar abgeschlossen sind. „Implementiert, aber nicht geprüft“ bleibt 🟡.
