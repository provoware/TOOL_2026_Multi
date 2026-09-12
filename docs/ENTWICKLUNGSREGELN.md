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

## Nutzerbeteiligung minimieren

Die Entwicklung trifft reversible technische Entscheidungen autonom. Fehlende reale Geräte-/Oberflächenprüfungen werden klar als externe Abnahme markiert, statt den Nutzer für jeden Zwischenschritt zum Testen einzuspannen.

## Definition „fertig“

Ein Punkt ist erst 🟢, wenn Änderung **und** passende Prüfung nachweisbar abgeschlossen sind. „Implementiert, aber nicht geprüft“ bleibt 🟡.
