# Aktueller Projektstand – leicht verständlich

**Stand:** 19. Oktober 2026 · **Programmversion:** 0.18.5 (Entwicklungskandidat)

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
| Link-Schnellstarter (0.18.5) | Namen und Gruppen lokaler Webverknüpfungen verwalten; bewusst im Browser öffnen. |
| Lokales Wiki | Eigene Sammlungen und Artikel anlegen, suchen, verknüpfen und ältere Fassungen aufrufen. |
| Module verwalten | Ideenarchiv, Kontometadaten, Schnellstarter und Wiki im Menü ein- oder ausschalten. |
| Programmsicherung für Updates | Nach Paketprüfung nur Betriebsdateien gesondert sichern und in einen neuen Ordner zurückholen; die laufende Installation bleibt unberührt. |
| Hilfe | Erklärungen und technische Fehlermeldungen in verständlicher Sprache lesen. |
| Anzeige | Zwischen vier Farben und fünf Zoomstufen von 100 bis 200 % wählen. |

Maßgeblich für die vollständige Alt- und Neuplanung ist der [Modulplan](MODULPLAN_2026.md). Die positive Basisabnahme bleibt gültig; eine erneute praktische Gesamt-Kubuntu-Abnahme ist erst nach allen geplanten Modulen vorgesehen. Zwischendurch bleiben sämtliche automatisierten Prüfungen verbindlich.

## Was ist noch nicht fertig?

Die Oberfläche nennt diese Dinge ausdrücklich **„In Planung“**: Reimfinder, Duplikatsuche, automatische GitHub-Verwaltung sowie verschiedene zusätzliche Schreibbereiche. Genre-Zufall und die lokale GitHub-Projektliste sind bereits nutzbar. Hörspiel-Buchvorlagen erzeugen Texte, keine fertige Audioproduktion. Ein geplanter Knopf ist kein fertiges Werkzeug.

## Was wurde zuletzt geprüft?

**Aktueller Bestand:** Die gemeinsame Modul-Integration wurde in [PR #97](https://github.com/provoware/TOOL_2026_Multi/pull/97) nach erfolgreicher [CI #1031](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39288221387) übernommen; der anschließende [main-Prüflauf #1033](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39289592547) war ebenfalls erfolgreich. [PR #98](https://github.com/provoware/TOOL_2026_Multi/pull/98) ergänzt die geprüfte Programmsicherung und echte Zusatzmodulschalter (CI #1035 erfolgreich); der zugehörige neue Hauptzweiglauf #1036 wurde gestartet. Ein automatischer Update-Rollback fehlt weiterhin. Die komplette manuelle Kubuntu-Abnahme erfolgt nur einmal ganz am Projektende.

**Ältere Nachweise (historisch):** Textbuttons/Buchwerkstatt (PR #84) und die freiwillige Leistungsdiagnose (PR #85) sind nach ausdrücklicher Freigabe in `main` enthalten. Der [Main-Lauf #1011](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39132402699) auf `526a423` bestand 200 Logiktests, 148 GUI-Tests, Wayland-Start, Restore und ZIP-Erzeugung. Seine größere Oberflächenmatrix meldete jedoch 24 Fehler und acht Warnungen; ein technisch erfolgreicher Lauf bedeutet deshalb kein fehlerfreies Layout.

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

Neu im 0.18.4-Kandidaten: [statisches Update-Staging](UPDATE_STAGING.md), ohne Codeausführung oder Aktivierung.

Die fünf Folgeaufträge sind im lokalen 0.18.4-Kandidaten umgesetzt: statisches Update-Staging (keine Ausführung/Aktivierung), Ideenarchiv, Kontometadaten ohne Passworttresor, Prozessstartmessung und flüchtige Text-Strukturhilfen. Das Modulmenü liegt am Symbol oben links. Echte dynamische Update-Sandbox, Checkpoint/Aktivierung/Rollback und Zielrechner-Abnahmen bleiben offen.
