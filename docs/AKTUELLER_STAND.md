# Aktueller Projektstand – leicht verständlich

**Stand:** 17. Oktober 2026 · **Programmversion:** 0.17.4

## Wozu dient Provoware?

Provoware ist ein Desktopprogramm für kreative Texte und die persönliche Organisation. Es wird auf Linux gestartet. Songtexte, normale Texte, Figuren, Profile, Aufgaben und Termine können in einem Projektordner verwaltet werden.

## Was funktioniert bereits?

| Bereich | Was du damit machen kannst |
|---|---|
| Songtexte | Songs schreiben, speichern, wiederfinden und ältere Versionen ansehen. |
| Allgemeiner Texteditor | Texte und Abschlussnotizen schreiben und speichern. |
| Charakterfibel | Figuren und ihre Eigenschaften verwalten. |
| Profile | Genres, Stimmungen, Stile, Stimmen und weitere Vorgaben sammeln. |
| Todo-Liste | Aufgaben anlegen, erledigen und archivieren. |
| Kalender | Termine verwalten; Erinnerungen erscheinen, solange das Hauptprogramm läuft. |
| Hilfe | Erklärungen und technische Fehlermeldungen in verständlicher Sprache lesen. |
| Anzeige | Zwischen vier Farben und fünf Zoomstufen von 100 bis 200 % wählen. |

## Was ist noch nicht fertig?

Die Oberfläche nennt diese Dinge ausdrücklich **„In Planung“**: automatischer Genre-Zufall, Reimfinder, Dateisuche, umfassende Textsuche, Duplikatsuche, GitHub-Verwaltung sowie verschiedene zusätzliche Schreibbereiche. Ein geplanter Knopf ist kein fertiges Werkzeug.

## Was wurde zuletzt geprüft?

- Die drei Schutzkorrekturen – Warnung vor ungespeichertem Textwechsel, Schutz vor Dateinamen-Kollisionen und Korrektur überlappender Elemente – wurden über [PR #57](https://github.com/provoware/TOOL_2026_Multi/pull/57) integriert.
- Die anschließenden Navigationsverbesserungen wurden über PR #58 bis #61 integriert.
- Die vollständige automatische Oberflächenkontrolle erreichte **60 Fälle**, **180 geprüfte Fenster**, **0 Fehler** und **0 Warnungen**.
- Der zugehörige GitHub-Arbeitsablauf wurde [erfolgreich abgeschlossen](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39065993768).

**Wichtig:** Die GitHub-Prüfung ersetzt **nicht** den Praxistest auf einem echten Kubuntu-26.04-Rechner. Die persönliche Datensicherung ist eine weitere eigenständige Aufgabe.

## Wo fange ich an?

**Nur benutzen:** Zuerst `ANLEITUNG_LAIEN.md` lesen und dann `bash schnellstart.sh` ausführen.

**Fehler beheben:** Im Programm `F1` drücken und **Hilfe & Fehlerhilfe** öffnen.

**Weiterentwickeln:** `TODO.md`, `CHANGELOG.md`, `AGENTS.md` und die technischen Berichte in `docs/` lesen.

**Persönliche Arbeiten schützen:** `daten/` bei geschlossenem Programm regelmäßig auf einen zweiten Datenträger kopieren.

## Was darf beim Aufräumen nicht verloren gehen?

Die Ordner `daten/`, `backups/`, `logs/` und `berichte/` dürfen nicht ohne Prüfung gelöscht werden. Alte Berichte unter `docs/ITERATION*.md` sind absichtlich erhalten: Sie erklären, warum frühere Entscheidungen getroffen wurden.

## Was sollte als Nächstes geschehen?

1. Die Dokumentation durch die vollständige GitHub-Prüfung bestätigen lassen.
2. Echte Bedienprüfung auf Kubuntu 26.04 mit stark vergrößerter Schrift durchführen.
3. Eine unabhängige, erprobte Datensicherung mit sicherer Wiederherstellung entwickeln.

Es gibt keine neue offizielle Versionsnummer, solange keine gesonderte Veröffentlichung freigegeben wurde.
