# Verbindlicher Modulplan – TOOL_2026_Multi

**Stand:** 19.10.2026 · **Grundlage:** Hauptzweig 0.18.5 nach PR #88/#89/#90. Keine öffentliche Veröffentlichung.

## Maßgebliche Entwicklungsentscheidung
Die bereits vom Nutzer bestätigte Kubuntu-Basis dient als Entwicklungsfundament. **Die erneute vollständige praktische Kubuntu-/Plasma-Abnahme erfolgt ausschließlich am Ende des gesamten Modulaufbaus**, wenn alle vereinbarten Funktionen integriert und die Oberfläche weitgehend stabil ist. Zwischendurch bleiben Quellcodeprüfung, Logik-/GUI-Tests, Wayland-Startprobe, Daten- und Wiederherstellungstests sowie ZIP-Prüfung verbindlich. Ein automatisches Testergebnis ist keine erneute manuelle Abnahme.

## Statusbegriffe
- **Bestand:** ausführbarer Code auf `main`; die vorhandenen automatischen Prüfungen sind erfolgreich, die spätere Gesamtbedienabnahme bleibt getrennt.
- **Kandidat:** Code im eigenen Entwicklungszweig, noch nicht auf `main` übernommen.
- **Teilweise:** es gibt geeignete Grundfunktionen, jedoch nicht den gesamten ursprünglich geplanten Leistungsumfang.
- **Fehlt:** keine fertige eigenständige Funktion nachgewiesen.
- **Historisch:** frühere Iterations-Kästchen sind kein zweites paralleles Aufgabenregister.

## A. Derzeit nutzbarer Bestand in main (0.18.5)

| Fachbereich | Tatsächlich vorhandener Umfang |
|---|---|
| Dashboard | Hauptnavigation, 2×2-Karten, Status, Zoom, Themes, Startwege; noch kein frei belegbares 3×3-Modulraster |
| Songbibliothek und Songeditor | Texte, Metadaten, Versionen, Sicherung gegen Datenverlust |
| Profile/Genres | fünf Kategorien mit Archiv und Vorgaben |
| Genre-Zufall | Suno-kompatible Ausgabe, Favoriten, Monatsbericht, Verlauf |
| Charakterfibel | Suche, Datensatzverwaltung und Referenzen in Schreibmodulen |
| Allgemeiner Texteditor | Titel, Text, Notizen, Versionierung und flüchtige Strukturhilfen |
| Textbuttons | Archiv, Varianten, Platzhalter, Monatsstatistik; genaue alte Vorgabe 30 Buttons gesondert prüfen |
| Buchwerkstatt | Kapitel, Vorlagen und Export; keine fertige Audio-/Hörspielproduktion |
| Ideenarchiv | Fragmente, Tags, Suche und kopierende Komposition |
| Accountmetadaten | Gruppierte Adressen/Notizen; **kein** verschlüsselter Passwortspeicher |
| GitHub-Projekte | Lokale Offline-Übersicht; keine automatische GitHub-Verwaltung |
| Aufgabenliste | Aufgaben, Termine und Archiv |
| Kalender | Tages-, Wochen-, Monats- und Jahresansicht, Erinnerungen bei laufendem Programm |
| Zentrale Dateisuche | Gespeicherte Namen und Textinhalte mit Vorschau und Schutzgrenzen; kein vollwertiger Dateimanager |
| Hilfe, Fehlerlog, Recovery | Anleitung, Ereignisse, Diagnose und Fehlerbehandlung |
| Persönliche Datensicherung | Separates Daten-ZIP, Integritätsprüfung, isolierte Wiederherstellung |
| Update-Vorprüfung | ZIP/Manifest/Hash im getrennten Staging prüfen; **keine** Aktivierung oder Rückkehr |
| Link-Schnellstarter | Offline gespeicherte Adressen/Gruppen mit bewusstem Browserstart und kompakter rechter Leiste |
| Leistungsdiagnose | Freiwillige lokale Werte und Benchmarkwerkzeuge |

## B. Begonnene oder unvollständige Bestandteile

| Bereich | Noch fehlender Nachweis / Restumfang |
|---|---|
| Frei belegbares 3×3-Raster | Kachel-/Modulzuordnung, Fokus, persistente Aufteilung, responsive Anzeige |
| Templatesystem mit 30 Buttons | Exakte Funktionsabnahme zum ursprünglichen 30-Button-Vertrag |
| Eigenständige Notizen | Titelgestützter TXT-/MD-Speicher und eigenständiges Notizfenster statt nur Projekt-Kurznotiz |
| Einstellungen | Zentrale persistente Einstellungsverwaltung statt lediglich Zoom/Theme |
| Dateimanager | Ordneransicht, sicheres Umbenennen, Papierkorb, Vorschau, Import/Export |
| Update-Manager | Isolierte Laufzeitprobe, vollständiger Checkpoint, atomare Aktivierung, Nachprüfung und Rollback |
| Automatische GitHub-Verwaltung | Erst nach klar definiertem Offline-/Online- und Sicherheitskonzept |
| Hörspiel-, Blog-, Prompt-Produktion | Dedizierte Arbeitsabläufe über vorhandene Schreibvorlagen hinaus |

## C. Fehlende eigenständige Module und Infrastruktur

| Priorität | Modul | Erwartete nächste Iteration |
|---|---|---|
| 1 | Sicherer Update-Manager, nächste Ausbaustufe | Isolierte Prüfung vor Aktivierung, danach Checkpoint/Rollback in gesonderten Iterationen |
| 2 | Projektmodulbaukasten / Plugin-System | Verträge, Modulmanifest, stabile Schnittstellen und Testbereich vor dynamischem Laden |
| 3 | Wiki / lokale Wissensbasen | Mehrere Sammlungen, Artikel, Tags, Querverweise, Suche, Versionsschutz, Import/Export |
| 4 | Arbeitsverzeichnis-/Entwicklungspool | Ordner, Status, sichere Kopien, Archive und nachvollziehbare Organisation |
| 5 | Audioplayer | Playlist mit Speicherung, Wiedergabe, Sprung und Lautstärke |
| 6 | Bildvorschau | Dateiauswahl, skalierbare Ansicht und Bildnavigation |
| 7 | Video- und Slideshow-Generator | FFmpeg-Verarbeitung, Auftragsschlange, Fortschritt, Abbruch, Ausgabeprüfung |
| 8 | Reimfinder | Lokales deutsches Nachschlage-/Reimwerkzeug |
| 9 | Duplikatprüfer | Dateihash-/Vorschauprüfung, niemals automatische Löschung |
| 10 | Read-only-Konsole / Entwicklerbereich | Diagnoseanzeige und begrenzte Entwicklerrechte ohne versteckte Schreibwege |
| 11 | Zusätzliche Datei-/Projektwerkzeuge | Vereinbarte Restfunktionen aus B nach getrennten Prüfverträgen |

## Iterationsregel
Pro Iteration ein abgegrenzter Umfang: **Vertrag → Datenformat → sichere Logik → Oberfläche → Tests → Dokumentation → PR → grüne GitHub-Prüfung → Integration**. Das gemeinsame `MANIFEST.json`, die Texte, Hilfe, Fensterverwaltung, Zoom/Themes, Atomarspeicherung, Import-/Export- und Fehlerwege werden konsequent wiederverwendet.

**Nie doppelt zählen:** Die historische Checklisten-Sammlung in `TODO.md` und die alten Iterationsberichte dienen nur als Nachweis; neuer maßgeblicher Stand steht in diesem Modulplan und im kurzen aktuellen Abschnitt oben in `TODO.md`. Offen heißt nicht automatisch, dass eine komplette Funktion fehlt (z. B. Update-Staging).

**Freigabe:** Versionskandidaten dürfen automatisch geprüft und in `main` integriert werden. Die sichtbare Gesamt-Kubuntu-Abnahme und die öffentliche Release-Veröffentlichung bleiben bis zum vollständigen Projektabschluss zurückgestellt.

## Qualitätsnachpflege zu 0.18.5
GitHub-Main #1020 bestand 254 Logik- und 164 GUI-Tests, Wayland, Restore und ZIP. Das nicht blockierende 60-Fall/180-Fenster-UI-Profil meldete **0 harte Fehler, aber 16 Warnungen** (zu langes „Bearbeiten“-Label in der rechten Leiste). Der Folgepatch verkürzt den Text und schützt späte Qt-Theme-Rückrufe. Der neue Patch benötigt eine eigene vollständige Prüfung; diese historische Aussage bleibt unverändert.

## Iteration 56 – Update-Laufzeitprobe (Entwicklungszweig)

Eine streng verweigernde Bubblewrap-Prüfung wird als separater Kandidat vorbereitet. Ohne wirksame Isolation darf keinerlei Paketcode ausgeführt werden. Die Probe ist ohne automatische Aktivierung und ohne Rückfallfunktion; vollständiger Update-Manager weiterhin **teilweise**. Die GUI- und Praxisabnahme bleibt bis zum Ende zurückgestellt, die GitHub-Vollprüfung ist für die Übernahme erforderlich.
