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

## Nutzerbeteiligung minimieren

Die Entwicklung trifft reversible technische Entscheidungen autonom. Fehlende reale Geräte-/Oberflächenprüfungen werden klar als externe Abnahme markiert, statt den Nutzer für jeden Zwischenschritt zum Testen einzuspannen.

## Definition „fertig“

Ein Punkt ist erst 🟢, wenn Änderung **und** passende Prüfung nachweisbar abgeschlossen sind. „Implementiert, aber nicht geprüft“ bleibt 🟡.
