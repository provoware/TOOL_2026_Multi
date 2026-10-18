# Aktueller Projektstand – leicht verständlich

**Stand:** 18. Oktober 2026 · **Programmversion:** 0.18.1

## Wozu dient Provoware?

Provoware ist ein Desktopprogramm für kreative Texte und die persönliche Organisation. Es wird auf Linux gestartet. Songtexte, normale Texte, Figuren, Profile, Aufgaben und Termine können in einem Projektordner verwaltet werden.

## Was funktioniert bereits?

| Bereich | Was du damit machen kannst |
|---|---|
| Songtexte | Songs schreiben, speichern, wiederfinden und ältere Versionen ansehen. |
| Textbuttons | Häufige Texte, Platzhalter und Unterversionen auf Knopfdruck kopieren. |
| Buchwerkstatt | Kapitel, Unterkapitel und Vorlagen für Hörspiel, Satire, Sachtext und Tutorial. |
| Allgemeiner Texteditor | Texte und Abschlussnotizen schreiben und speichern. |
| Charakterfibel | Figuren und ihre Eigenschaften verwalten. |
| Genre-Zufall | Stiltexte aus vorhandenen Profilen erzeugen; Favoriten und Monatsbericht nutzen. |
| GitHub-Projekte | Offene und fertige Projekte lokal mit Notizen verwalten. |
| Profile | Genres, Stimmungen, Stile, Stimmen und weitere Vorgaben sammeln. |
| Todo-Liste | Aufgaben anlegen, erledigen und archivieren. |
| Kalender | Termine verwalten; Erinnerungen erscheinen, solange das Hauptprogramm läuft. |
| Leistungsdiagnose | Zusätzliche lokale Messung einschalten, ausgewählte Tagesdaten ansehen, exportieren und löschen. |
| Hilfe | Erklärungen und technische Fehlermeldungen in verständlicher Sprache lesen. |
| Anzeige | Zwischen vier Farben und fünf Zoomstufen von 100 bis 200 % wählen. |

## Was ist noch nicht fertig?

Die Oberfläche nennt diese Dinge ausdrücklich **„In Planung“**: Reimfinder, Dateisuche, umfassende Textsuche, Duplikatsuche, automatische GitHub-Verwaltung sowie verschiedene zusätzliche Schreibbereiche. Genre-Zufall und die lokale GitHub-Projektliste sind bereits nutzbar. Hörspiel-Buchvorlagen erzeugen Texte, keine fertige Audioproduktion. Ein geplanter Knopf ist kein fertiges Werkzeug.

## Was wurde zuletzt geprüft?

Der Code-/Layoutstand `cfc7353` von [PR #84](https://github.com/provoware/TOOL_2026_Multi/pull/84) bestand [Lauf #1007](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39127077853): 188 Logiktests, 144 GUI-Tests, nativer Wayland-Start, Wiederherstellung und ZIP-Erzeugung. Die UI-Analyse erreichte acht Matrixfälle / 24 Fensterinstanzen mit null Fehlern und null Warnungen. Die nachfolgende Informationsrunde hat ihren eigenen Prüfnachweis am aktuellen PR-Head. **0.18.0 wurde nach ausdrücklicher Freigabe über PR #84 mit main zusammengeführt. Der Hauptzweig-Lauf nach dem Merge ist erfolgreich. 0.18.1 ergänzt als nächste Iteration die lokale Leistungsdiagnose.**

Die folgenden Nachweise betreffen frühere Stände:

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

1. Den aktuellen PR-Head einschließlich Informationsrunde durch die vollständige GitHub-Prüfung bestätigen lassen.
2. Echte Bedienprüfung auf Kubuntu 26.04 mit stark vergrößerter Schrift durchführen.
3. Eine unabhängige, erprobte Datensicherung mit sicherer Wiederherstellung entwickeln.

Version 0.18.0 wird als eigener Änderungsantrag geprüft. Frühere CI-Nachweise oben gelten für den damaligen Stand. Die neue Prüfung muss zum neuen Commit gehören.

Die Bewertung der Entwicklung mit gemessenen Laufzeiten und Verbesserungsregeln steht im [Entwicklungsreview](ENTWICKLUNGSREVIEW_2026_10_18.md). Das Konzept zusätzlicher Leistungsdaten steht im [Messplan](DIAGNOSE_MESSPLAN.md); die erste ausdrücklich einschaltbare Ausbaustufe ist nun in 0.18.1 implementiert.
