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
| Module verwalten | Ideenarchiv, Kontometadaten, Schnellstarter, Wiki, Audioplayer, Bildvorschau und Slideshow ein- oder ausschalten. |
| Modulbaukasten | Eigene Modulvorlagen, Feldbezeichnungen und eine harmlose Formularvorschau entwerfen. |
| Entwicklungspool | Projektordner und Bearbeitungsstände verwalten, Kopien und ZIP-Archive erstellen. |
| Audioplayer | Playlist speichern, Musik abspielen, pausieren, Titel wechseln und Lautstärke ändern. |
| Bildvorschau | Lokale Bilder skalieren, anzeigen und per Liste auswählen. |
| Slideshow & Video | Bilder als MP4 erzeugen, optional Ton hinzufügen oder die Audiospur eines Videos ersetzen. |
| Programmsicherung für Updates | Nach Paketprüfung nur Betriebsdateien gesondert sichern und in einen neuen Ordner zurückholen; die laufende Installation bleibt unberührt. |
| Hilfe | Erklärungen und technische Fehlermeldungen in verständlicher Sprache lesen. |
| Anzeige | Zwischen vier Farben und fünf Zoomstufen von 100 bis 200 % wählen. |

Maßgeblich für die vollständige Alt- und Neuplanung ist der [Modulplan](MODULPLAN_2026.md). Die positive Basisabnahme bleibt gültig; eine erneute praktische Gesamt-Kubuntu-Abnahme ist erst nach allen geplanten Modulen vorgesehen. Zwischendurch bleiben sämtliche automatisierten Prüfungen verbindlich.

## Was ist noch nicht fertig?

Die Oberfläche nennt diese Dinge ausdrücklich **„In Planung“**: Reimfinder, Duplikatsuche, automatische GitHub-Verwaltung sowie verschiedene zusätzliche Schreibbereiche. Genre-Zufall und die lokale GitHub-Projektliste sind bereits nutzbar. Hörspiel-Buchvorlagen erzeugen Texte, keine fertige Audioproduktion. Ein geplanter Knopf ist kein fertiges Werkzeug.

## Was wurde zuletzt geprüft?

**Neue Entwicklungsrunde:** Update-Slotmechanismus PR #100 (CI #1039, main #1040), Modulbaukasten PR #101 (CI #1041, main #1042), Entwicklungspool PR #102 (CI #1043, main #1044), Multimedia PR #103 (CI #1046 grün, Hauptzweigprüfung #1047 gestartet). Alle vier Pull Requests wurden in `main` übernommen. Diese Nachweise sind automatische Prüfungen, keine erneute manuelle Kubuntu-Abnahme. Es fehlen unter anderem produktive Altinstallations-Migration, echte Fremdplugin-Sandbox, ZIP-Rückimport und erweiterte Videofunktionen.

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


## Nachpflege: Projekt-Notizen (PV-AUD-01, 24.10.2026)

Neue Projekt-Notizen werden im Datenordner gespeichert. Alte Notizen können nach ausdrücklicher Zustimmung bytegenau dorthin kopiert werden; die ursprüngliche Datei bleibt erhalten. Bei Ablehnung sind die alten Notizen weiterhin nicht Bestandteil des persönlichen Daten-ZIPs. Details und Grenzen: [Datensicherung](DATENSICHERUNG.md). Status und aktuelle CI-Evidenz werden am zugehörigen Änderungsantrag geführt; die historische Übersicht oben bleibt auf ihren damaligen Stand bezogen.


## Nachpflege: persönliche Aufgaben und Entwicklungsaltbestand (PV-AUD-05)

Technisch geprüfter Produktstand vom 24.10.2026 in [PR #131](https://github.com/provoware/TOOL_2026_Multi/pull/131), auf Basis `7a03a0078b241f5ba8325567925d473840ff8d9d`: Beim Öffnen der persönlichen Aufgabenliste werden keine Entwicklungsaufgaben mehr erzeugt. Bereits vorhandene Entwicklungsaufgaben bleiben erhalten und werden anhand ihrer historischen festen Kennungen getrennt angezeigt. Eine persönliche Kopie benötigt eine ausdrückliche Bestätigung und eine neue Kennung. Öffnen, Aktualisieren und Zoom schreiben den Aufgabenbestand nicht um; Sicherung und isolierter Restore verwenden unverändert dieselbe Datei und dasselbe Format. Bedienung: [einfache Anleitung](../ANLEITUNG_LAIEN.md#persönliche-aufgaben-und-ältere-entwicklungsplanung).

Technischer Vertrag: `task_groups()` leitet die Ansichten aus einem einzigen gelesenen Bestand ab. Die vorhandenen APIs `active_tasks()` und `archived_tasks()` behalten ihre Gesamtsicht; nur die persönliche GUI verwendet die getrennten Gruppen. Historische Titelkataloge in `todo_store.py` sind Bestandteil der Alt-ID-Erkennung und dürfen künftig nicht für neue Planungsnamen umgeschrieben werden. Der explizite alte Entwicklerhelfer bleibt aus Kompatibilitätsgründen erhalten und wird von der GUI nicht aufgerufen. Der Formularaufbau bleibt als zusammenhängende Anordnung erhalten; Tabellen-/Altbestandsaufbau sind separat gekapselt.

Die vollständige GitHub-Prüfung und Integration werden am zugehörigen PR geführt. Keine produktiven Dateien migriert oder gelöscht, keine zusätzliche manuelle Kubuntu-Zwischenabnahme, kein öffentliches Release.

Lokaler Nachweis dieses Kandidaten: 87 gezielte und angrenzende Prüfungen erfolgreich (Aufgabenlogik/-GUI, historische Entwicklerhelfer, Modulnachbarn, Laienführung, Dashboard, Dokumentation und Datensicherung). 147 freigegebene Betriebsdateien im Release-Manifest gültig; `git diff --check` ohne Befund. Bei 1280×740 und 100/150/200 % Zoom sind die Altbestandsaktionen erreichbar; eine neue persönliche Kopie verdrängt keine Hauptaktion. Dateiänderungen der Tests ausschließlich in temporären Ordnern. Vollständige PR-/main-CI-Evidenz bleibt davon getrennt.

GitHub-Nachweis des Produktcodes: [Prüfung #1115](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40123882032) auf `bbadafdda41516a97378ce07c281475692090faf` vollständig erfolgreich. Finale Statusrevision und anschließende main-Prüfung werden am PR separat nachgewiesen.


## Nachpflege: tätigkeitsorientierter Einstieg (PV-UX-01)

Implementierungskandidat vom 24.10.2026 auf Basis `cfd23ecc55e8d70a94c2f1684ca8f58b48f9ad2b`: Die Startkarte bietet vier unabhängige Aktionen in einem kompakten 2×2-Raster. Song schreiben öffnet einen neuen Editor; Text schreiben aktiviert einen sichtbaren Texteditor ohne Refresh und bewahrt dessen Entwurf. Ein zuvor geschlossenes Fenster wird über den bestehenden Manager neu geöffnet, damit bewusst verworfene Texte nicht wieder erscheinen. Aufgaben-/Terminaktionen fokussieren vorhandene Formulare, ohne sie zu leeren. Die leere Textliste erklärt den ersten Speicherschritt. Bestehende Song- und Buch-Einstiege bleiben verfügbar. Bedienung: [einfache Anleitung](../ANLEITUNG_LAIEN.md#karte-was-möchtest-du-tun).

Der vorhandene Texteditor-Neu-/Schließen-Dialog bleibt maßgeblich für bewusste Dokumentwechsel; die Startkarte löst bei einem bereits sichtbaren Entwurf keinen impliziten Wechsel aus. Keine Speicherformatänderung oder Datenmigration. Reale Erstnutzertests bleiben Bestandteil der abschließenden Gesamtbedienprüfung; automatisierte Abläufe werden nicht als Nutzerstudie ausgegeben.


Lokaler Prüfnachweis: 97 gezielte und angrenzende Tests erfolgreich. Produktive UI-Matrix über `scripts/ui_shadow_entry.py`: 60 Fälle, 180 Fenster, null Fehler und null Warnungen. Die vier vertikalen Aktionen wurden wegen nachgewiesener Überlappungen bei 200 % Zoom auf das 2×2-Raster umgestellt; Grenzwerte unverändert. Release-Manifest gültig mit 147 Betriebsdateien; diff-Prüfung ohne Befund. Die Startkarte ist als eigener Builder im bestehenden Dashboard gekapselt; eine umfassende Aufteilung der bereits großen `ui.py` bleibt dem separaten Auftrag PV-AUD-18 vorbehalten. GitHub-Prüfung, endgültiger Aufgabenabschluss und Integration folgen am zugehörigen PR.

CI-Nachpflege: Kurze Formularaktionen „Aufgabe planen“ und „Termin anlegen“ erhalten zusätzliche Breitenreserve bei abweichenden Systemfonts. Ein verzögerter Laptop-Layoutaufruf ignoriert zerstörte Qt-Fenster; der neue Rückfalltest reproduziert diesen Zustand mit einem tatsächlich zerstörten Fenster. Nach den Korrekturen erneut 97 lokale Tests und 60 UI-Matrixfälle / 180 Fenster erfolgreich, null Fehler und null Warnungen. Die weitergehende Lebenszyklusprüfung PV-AUD-21 bleibt offen.

GitHub-Codeprüfung PV-UX-01: Commit `5510614a235bad932ede47e60c7a817e14242f10` in [PR #132](https://github.com/provoware/TOOL_2026_Multi/pull/132) bestand [Lauf #1119](https://github.com/provoware/TOOL_2026_Multi/actions/runs/40127732786): 365 Logiktests, 205 GUI-Tests, nativer Wayland-Start, UI-Matrix 8 Fälle / 24 Fenster ohne Fehler/Warnungen, vollständiger Restore und Paketbau. Technischer UX-Auftrag abgeschlossen; diese abschließende Dokumentationsrevision sowie der spätere main-Stand werden separat vollständig geprüft. Reale Erstnutzerstudie weiterhin ausstehend.

## Nachpflege: Speicherzustände (PV-UX-03, 25.10.2026)

Lokaler Kandidat: Song-, Text- und Bucheditor besitzen eine separate gemeinsame Speicheranzeige. Sie vergleicht den sichtbaren Entwurf mit dem tatsächlich gespeicherten/geladenen Stand; Erfolgshinweise anderer Aktionen ersetzen sie nicht. Unbetitelte Text-/Buchentwürfe werden ausdrücklich als ungespeichert ohne Autosave angezeigt. Die bestehende Song-Automatik mit Standardtitel bleibt erhalten und wird erklärt. Speicherformate, Datenpfade und Intervalle unverändert. Schreibfehler mit unverändertem Bestandsinhalt und erhaltenem Entwurf sowie Neu-/Ladewege sind in isolierten GUI-Tests geprüft. GitHub-/main-Nachweise folgen separat; keine reale Nutzerstudie behauptet.
