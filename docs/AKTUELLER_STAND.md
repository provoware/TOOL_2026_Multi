# Aktueller Projektstand – leicht verständlich

**Stand:** 18. Oktober 2026 · **Programmversion:** 0.18.3 (lokaler Prüfkandidat)

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
| Dateisuche | Gespeicherte Namen und Textinhalte mit Trefferliste und Vorschau finden. |
| Hilfe | Erklärungen und technische Fehlermeldungen in verständlicher Sprache lesen. |
| Anzeige | Zwischen vier Farben und fünf Zoomstufen von 100 bis 200 % wählen. |

## Was ist noch nicht fertig?

Die Oberfläche nennt diese Dinge ausdrücklich **„In Planung“**: Reimfinder, Duplikatsuche, automatische GitHub-Verwaltung sowie verschiedene zusätzliche Schreibbereiche. Genre-Zufall und die lokale GitHub-Projektliste sind bereits nutzbar. Hörspiel-Buchvorlagen erzeugen Texte, keine fertige Audioproduktion. Ein geplanter Knopf ist kein fertiges Werkzeug.

## Was wurde zuletzt geprüft?

Textbuttons/Buchwerkstatt (PR #84) und die freiwillige Leistungsdiagnose (PR #85) sind nach ausdrücklicher Freigabe in `main` enthalten. Der [Main-Lauf #1011](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39132402699) auf `526a423` bestand 200 Logiktests, 148 GUI-Tests, Wayland-Start, Restore und ZIP-Erzeugung. Seine größere Oberflächenmatrix meldete jedoch 24 Fehler und acht Warnungen; ein technisch erfolgreicher Lauf bedeutet deshalb kein fehlerfreies Layout.

Version **0.18.2** behebt diese Befunde als eigene Iteration zu [Issue #86](https://github.com/provoware/TOOL_2026_Multi/issues/86). Die lokale Release-Matrix erreicht nun **60 Fälle / 180 Fenster, 0 Fehler, 0 Warnungen**. Die vollständige GitHub-Abnahme muss zum finalen neuen Head gehören; ihr Nachweis wird am zugehörigen Pull Request geführt. Details: [Iteration 42](ITERATION42_LAYOUT.md).

Die folgenden Nachweise betreffen frühere Stände:

- Die drei Schutzkorrekturen – Warnung vor ungespeichertem Textwechsel, Schutz vor Dateinamen-Kollisionen und Korrektur überlappender Elemente – wurden über [PR #57](https://github.com/provoware/TOOL_2026_Multi/pull/57) integriert.
- Die anschließenden Navigationsverbesserungen wurden über PR #58 bis #61 integriert.
- Die vollständige automatische Oberflächenkontrolle erreichte **60 Fälle**, **180 geprüfte Fenster**, **0 Fehler** und **0 Warnungen**.
- Der zugehörige GitHub-Arbeitsablauf wurde [erfolgreich abgeschlossen](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39065993768).

**Wichtig:** Die GitHub-Prüfung ersetzt **nicht** den Praxistest auf einem echten Kubuntu-26.04-Rechner. Die persönliche Datensicherung ist im lokalen 0.18.3-Kandidaten eigenständig umgesetzt; eine automatische Aktivierung zurückgeholter Daten erfolgt nicht.

## Wo fange ich an?

**Nur benutzen:** Zuerst `ANLEITUNG_LAIEN.md` lesen und dann `bash schnellstart.sh` ausführen.

**Fehler beheben:** Im Programm `F1` drücken und **Hilfe & Fehlerhilfe** öffnen.

**Weiterentwickeln:** `TODO.md`, `CHANGELOG.md`, `AGENTS.md` und die technischen Berichte in `docs/` lesen.

**Persönliche Arbeiten schützen:** [Datensicherung](DATENSICHERUNG.md) bei geschlossenem Programm auf einen zweiten Datenträger erstellen.

## Was darf beim Aufräumen nicht verloren gehen?

Die Ordner `daten/`, `backups/`, `logs/` und `berichte/` dürfen nicht ohne Prüfung gelöscht werden. Alte Berichte unter `docs/ITERATION*.md` sind absichtlich erhalten: Sie erklären, warum frühere Entscheidungen getroffen wurden.

## Was sollte als Nächstes geschehen?

1. Gemäß Nutzerpriorität weitere unabhängige Entwicklungsaufgaben bearbeiten.
2. Automatische Prüfungen und isolierte Wiederherstellungsprüfungen beibehalten.
3. Zielrechner-Abnahme und Veröffentlichung später durchführen.

Version 0.18.2 wird als eigener Änderungsantrag geprüft. Frühere CI-Nachweise gelten für den damaligen Stand.

Die Bewertung der Entwicklung mit gemessenen Laufzeiten und Verbesserungsregeln steht im [Entwicklungsreview](ENTWICKLUNGSREVIEW_2026_10_18.md). Das Konzept zusätzlicher Leistungsdaten steht im [Messplan](DIAGNOSE_MESSPLAN.md); die erste ausdrücklich einschaltbare Ausbaustufe ist nun in 0.18.1 implementiert.


Neu im lokalen Kandidaten 0.18.3: eigenständige Daten-ZIPs mit geprüftem Rückholen, Prüfung defekter Startumgebungen, Ladebenchmark mit Datenklassen und Auswertung gespeicherter UI-Kalibrierungsnachweise. Details und Freigabegrenzen: [Versionsunterlagen](FREIGABE_0_18_3.md). Keine Aussage, dass dieser Stand bereits in GitHub/main veröffentlicht wurde.

Die zentrale Text-/Dateisuche ist im lokalen Kandidaten umgesetzt; Grenzen stehen in [Dateisuche](DATEISUCHE.md). Repository-/CI-Nachweise gehören zum zugehörigen neuen Pull Request.
