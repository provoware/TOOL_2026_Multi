# Verbindlicher Modulplan – TOOL_2026_Multi

**Stand:** 19.10.2026 · **Grundlage:** Hauptzweig 0.18.5 nach PR #97 und #98, erfolgreich geprüft mit CI #1033 bzw. PR-CI #1035. Noch kein öffentliches Release.

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
| Update-Schutzstufen | Paket-ZIP/Manifest/Hash prüfen; optionale abgeschirmte Laufzeitprobe, geprüfter Programm-Checkpoint und isolierte Rückkehrkopie. **Keine Produktivaktivierung/automatischer Rollback.** |
| Link-Schnellstarter | Offline gespeicherte Adressen/Gruppen mit bewusstem Browserstart und kompakter rechter Leiste |
| Lokales Wiki | Wissenssammlungen, Artikel, Schlagwortsuche, Querverweise, Textversionen und sicherer Import/Export |
| Modulsteuerung | Vier fest bekannte Zusatzmodule (Ideen, Kontometadaten, Schnellstarter, Wiki) mit speicherbarer Ein-/Aus-Schaltung, ohne Fremdcode |
| Leistungsdiagnose | Freiwillige lokale Werte und Benchmarkwerkzeuge |

## B. Begonnene oder unvollständige Bestandteile

| Bereich | Noch fehlender Nachweis / Restumfang |
|---|---|
| Frei belegbares 3×3-Raster | Kachel-/Modulzuordnung, Fokus, persistente Aufteilung, responsive Anzeige |
| Templatesystem mit 30 Buttons | Exakte Funktionsabnahme zum ursprünglichen 30-Button-Vertrag |
| Eigenständige Notizen | Titelgestützter TXT-/MD-Speicher und eigenständiges Notizfenster statt nur Projekt-Kurznotiz |
| Einstellungen | Zentrale persistente Einstellungsverwaltung statt lediglich Zoom/Theme |
| Dateimanager | Ordneransicht, sicheres Umbenennen, Papierkorb, Vorschau, Import/Export |
| Update-Manager | Isolierte Probe und Checkpoint/Rückkehrkopie vorhanden; noch ausstehend: atomare Aktivierung, Startnachprüfung und automatischer Rollback |
| Automatische GitHub-Verwaltung | Erst nach klar definiertem Offline-/Online- und Sicherheitskonzept |
| Hörspiel-, Blog-, Prompt-Produktion | Dedizierte Arbeitsabläufe über vorhandene Schreibvorlagen hinaus |

## C. Fehlende eigenständige Module und Infrastruktur

| Priorität | Modul | Erwartete nächste Iteration |
|---|---|---|
| 1 | Produktive Update-Umschaltung | Atomare Aktivierung erst nach geprüftem Checkpoint, Startnachprüfung und gesichertem automatischem Rollback |
| 2 | Erweiterter Projektmodulbaukasten / Plugin-System | Bestehende Modulverträge und Menüsteuerung um geprüfte Modulbau- und Fremdplugin-Funktionen ergänzen |
| 3 | Arbeitsverzeichnis-/Entwicklungspool | Ordner, Status, sichere Kopien, Archive und nachvollziehbare Organisation |
| 4 | Audioplayer | Playlist mit Speicherung, Wiedergabe, Sprung und Lautstärke |
| 5 | Bildvorschau | Dateiauswahl, skalierbare Ansicht und Bildnavigation |
| 6 | Video- und Slideshow-Generator | FFmpeg-Verarbeitung, Auftragsschlange, Fortschritt, Abbruch, Ausgabeprüfung |
| 7 | Reimfinder | Lokales deutsches Nachschlage-/Reimwerkzeug |
| 8 | Duplikatprüfer | Dateihash-/Vorschauprüfung, niemals automatische Löschung |
| 9 | Read-only-Konsole / Entwicklerbereich | Diagnoseanzeige und begrenzte Entwicklerrechte ohne versteckte Schreibwege |
| 10 | Zusätzliche Datei-/Projektwerkzeuge | Vereinbarte Restfunktionen aus B nach getrennten Prüfverträgen |

## Iterationsregel
Pro Iteration ein abgegrenzter Umfang: **Vertrag → Datenformat → sichere Logik → Oberfläche → Tests → Dokumentation → PR → grüne GitHub-Prüfung → Integration**. Das gemeinsame `MANIFEST.json`, die Texte, Hilfe, Fensterverwaltung, Zoom/Themes, Atomarspeicherung, Import-/Export- und Fehlerwege werden konsequent wiederverwendet.

**Nie doppelt zählen:** Die historische Checklisten-Sammlung in `TODO.md` und die alten Iterationsberichte dienen nur als Nachweis; neuer maßgeblicher Stand steht in diesem Modulplan und im kurzen aktuellen Abschnitt oben in `TODO.md`. Offen heißt nicht automatisch, dass eine komplette Funktion fehlt (z. B. Update-Staging).

**Freigabe:** Versionskandidaten dürfen automatisch geprüft und in `main` integriert werden. Die sichtbare Gesamt-Kubuntu-Abnahme und die öffentliche Release-Veröffentlichung bleiben bis zum vollständigen Projektabschluss zurückgestellt.

## Qualitätsnachpflege zu 0.18.5
GitHub-Main #1020 bestand 254 Logik- und 164 GUI-Tests, Wayland, Restore und ZIP. Das nicht blockierende 60-Fall/180-Fenster-UI-Profil meldete **0 harte Fehler, aber 16 Warnungen** (zu langes „Bearbeiten“-Label in der rechten Leiste). Der Folgepatch verkürzt den Text und schützt späte Qt-Theme-Rückrufe. Der neue Patch benötigt eine eigene vollständige Prüfung; diese historische Aussage bleibt unverändert.

## Iteration 58 – lokales Wiki (Entwicklungszweig)

Das Wiki wurde als separater Umsetzungskandidat mit mehreren Sammlungen, Artikeln, Schlagwortsuche, geprüften Querverweisen, bis zu 20 früheren Fassungen und sicherem Kopierimport vorbereitet. Es nutzt die bestehenden Fenster-, Theme-/Zoom- und Modularchiv-Standards. Noch nicht in `main`, automatische PR-Prüfung vor Integration erforderlich. Vollständige praktische Kubuntu-Abnahme erst am Ende der Modulentwicklung.


## Iteration 56 – Update-Laufzeitprobe (Entwicklungszweig)

Eine streng verweigernde Bubblewrap-Prüfung wird als separater Kandidat vorbereitet. Ohne wirksame Isolation darf keinerlei Paketcode ausgeführt werden. Die Probe ist ohne automatische Aktivierung und ohne Rückfallfunktion; vollständiger Update-Manager weiterhin **teilweise**. Die GUI- und Praxisabnahme bleibt bis zum Ende zurückgestellt, die GitHub-Vollprüfung ist für die Übernahme erforderlich.


## Iteration 57 – Modulkatalog-Verträge (Entwicklungszweig)

Stabile Schnittstellenbeschreibung und atomarer Modul-Katalog für geprüfte Kennungen werden aufgebaut. **Nur Metadatenregistrierung, kein dynamisches Laden und keine Produktaktivierung**. Die Navigation wird erst nach separater geprüfter Integration an diese Vertragsquelle gebunden. Dies ist ein Anfang des Plugin-Systems, noch keine vollständige Plugin-Plattform.

## Integrationsgrenze (PR #94, #95, #96)

Alle drei Einzelzweige bestanden vollständige GitHub-Automatik auf unveränderten Commits; die gemeinsame Integration benötigt einen eigenen erfolgreichen Prüfstand vor dem Hauptzweig. Die isolierte Probe ersetzt keine produktive Update-Aktivierung. Der Modulkatalog ist noch ohne wirksame Navigation. Die manuelle Kubuntu-/Plasma-Gesamtabnahme bleibt bis nach Fertigstellung aller Module ausgesetzt.

## Iteration 59 – Programmsicherung und Modulsteuerung (Folgeentwicklungszweig)

- Update: Nach validiertem Staging können nur die im Release-Manifest freigegebenen Betriebsdateien in einen eigenen, schreibgeschützten Sicherungsbestand kopiert, erneut geprüft und in ein neues Rückkehrverzeichnis wiederhergestellt werden. **Das laufende Programm wird nicht ersetzt.** Ein automatischer Rückwechsel erfordert später eine getrennte atomare Slot-Umschaltung mit Rückfallvertrag. Die bestehende persönliche Datensicherung bleibt eigenständig.
- Modulkatalog: Nutzer können die bereits fest einkompilierten Zusatzmodule **Ideen, Kontometadaten, Schnellstarter und Wiki** mit realen Menü- und Tastenkürzel-Sperren aktivieren/deaktivieren. Voreinstellung: alle zugänglich. Die Daten werden beim Abschalten nicht gelöscht; ein derzeit offenes Modulfenster verhindert die Deaktivierung. Kernmodule bleiben unangetastet. **Drittmodule können weiterhin nicht ausgeführt werden**.
- Beide Bereiche werden im eigenen Pull Request vollständig automatisch geprüft. Kein manueller Kubuntu-Test vor Abschluss aller Module.

## Verbindlicher Hauptzweig-Nachweis – Iteration 59

- PR #97: Vereinigung von Update-Sandbox, Modulvertrag und Wiki, vollständige Integrations-CI #1031 erfolgreich; danach Hauptzweig-CI #1033 erfolgreich.
- PR #98: unabhängige Checkpoint- und echte Modulsteuerungs-Erweiterung, PR-CI #1035 erfolgreich und danach in `main` integriert. Ein gesonderter Hauptzweig-Prüflauf #1036 wurde gestartet.
- Alle bis dahin als „Entwicklungszweig“ bezeichneten Iterationsabschnitte 56 bis 59 sind **historische Entstehungsberichte**. Maßgeblich ist die aktuelle Statusmatrix oben.
- Automatische Produktivaktivierung und Rollback fehlen weiterhin. Reale manuelle Kubuntu-Abnahme bleibt ausschließlich für den Abschluss aller Module vorgesehen.

## Iteration 60 – atomarer Slotwechsel (Entwicklungszweig)

Ein getrennter Sicherheitsprototyp kann bei **explizit vorbereiteten verwalteten Slot-Installationen** eine neue Version in einen zweiten Programmordner kopieren, isoliert prüfen und den relativen Zeiger atomar umschalten. Bei fehlgeschlagener Nachprüfung oder unterbrochenem Wechsel bleibt die alte Version verfügbar beziehungsweise wird sie wieder aktiviert. **Normale bestehende Kubuntu-Installationen können damit noch nicht automatisch aktualisiert werden.** Dafür fehlen die geprüfte einmalige Migration, Trennung persönlicher Daten und der sichere Aufruf aus dem normalen Schnellstart. Siehe `docs/UPDATE_SLOTS.md`; derzeit keine praktische Kubuntu-Abnahme.

## Iteration 61 – Sicherer grafischer Modulbaukasten

Der neue Modulbaukasten verwaltet ausschließlich **beschreibende** lokale Modulvorlagen (Name, Felder, erlaubte Fähigkeiten, Formularvorschau). Die eingebaute API gibt nur geprüfte Daten zurück, führt keine externen Python-Module aus und enthält keine Shell-, Netz- oder Dateilösch-Berechtigung. Module können als JSON mit bestehenden Import-/Export-Grenzen kopiert werden. Noch fehlen generierte ausführbare Funktionen, Berechtigungssandboxes und Plugin-Signaturprüfung; diese werden nicht als erledigt verbucht. Menü: „Modulbaukasten · Entwürfe“, Strg+Alt+E. GitHub-Vollprüfung verpflichtend, manuelle Kubuntu-Abnahme am Ende.

## Iteration 62 – Entwicklungspool (eigener Kandidat)

Der lokale Projektpool erhält Status, projektbezogene Arbeitsordner, geprüfte sichere Verzeichniskopien und einen ZIP-Export. Keine automatische Löschung. Links, Spezialdateien, große Einzeldateien, zu große Archivbestände und bestehende Exportdateien werden abgewehrt. Der sichere Rückimport gesamter Verzeichnisse fehlt noch; das wird offen ausgewiesen. Menü- und Tastaturzugang Strg+Alt+P, Nutzung der bekannten Fenster-/Zoom- und Speicherstandards. Automatische GitHub-Prüfungen vor Integration; keine wiederholte manuelle Kubuntu-Abnahme.
