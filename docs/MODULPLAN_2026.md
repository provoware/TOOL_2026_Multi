# Verbindlicher Modulplan – TOOL_2026_Multi

**Stand:** 19.10.2026 · **Grundlage:** Hauptzweig 0.18.5 nach PR #100–#103; CI der Entwicklungsstände #1039/#1041/#1043/#1046 erfolgreich. Keine öffentliche Veröffentlichung.

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
| Update-Schutzstufen | Paket-Staging, isolierte Probe, Checkpoint, Rückkehrkopie sowie atomarer Slotwechsel **für vorbereitete Slot-Installationen**; keine Migration gewöhnlicher Bestandsinstallationen. |
| Link-Schnellstarter | Offline gespeicherte Adressen/Gruppen mit bewusstem Browserstart und kompakter rechter Leiste |
| Lokales Wiki | Wissenssammlungen, Artikel, Schlagwortsuche, Querverweise, Textversionen und sicherer Import/Export |
| Modulsteuerung | Sieben bekannte Zusatzmodule mit speicherbarer Ein-/Aus-Schaltung; fremde Plugins werden nicht ausgeführt. |
| Modulbaukasten | Beschreibende eigene Modulvorlagen, 1–12 Eingabefelder, begrenzte Fähigkeiten und sichere GUI-Vorschau. |
| Entwicklungspool | Projektstatus, eigene Arbeitsordner, Kopieren und geprüfte ZIP-Exporte, ohne automatischen Voll-Rückimport. |
| Audioplayer | Persistente Playlist, Play/Pause/Stopp, Vor-/Zurück, Lautstärke, Position. |
| Bildvorschau | Gespeicherte Bildliste, Größenlimit, skalierter Decoder, Navigation. |
| Video/Slideshow – Basis | FFmpeg-Einzelauftrag, bis 20 Bilder, optionaler Ton, Video-Tonmischung, Fortschritt/Abbruch; keine Übergänge/Warteschlange. |
| Leistungsdiagnose | Freiwillige lokale Werte und Benchmarkwerkzeuge |

## B. Begonnene oder unvollständige Bestandteile

| Bereich | Noch fehlender Nachweis / Restumfang |
|---|---|
| Frei belegbares 3×3-Raster | Kachel-/Modulzuordnung, Fokus, persistente Aufteilung, responsive Anzeige |
| Templatesystem mit 30 Buttons | Exakte Funktionsabnahme zum ursprünglichen 30-Button-Vertrag |
| Eigenständige Notizen | Titelgestützter TXT-/MD-Speicher und eigenständiges Notizfenster statt nur Projekt-Kurznotiz |
| Einstellungen | Zentrale persistente Einstellungsverwaltung statt lediglich Zoom/Theme |
| Dateimanager | Ordneransicht, sicheres Umbenennen, Papierkorb, Vorschau, Import/Export |
| Update-Manager | Slotwechsel samt Rückkehr bei Fehlern nur für vorbereitete Slot-Installationen. Bestandsmigration, Datenauslagerung, Schnellstart-Anbindung und produktive Freigabe fehlen. |
| Plugin-Laufzeit | Fremder Code und signierte Drittmodule benötigen erst eine getrennte geschützte Ausführung mit realer Rechteprüfung. |
| Multimedia-Erweiterungen | ffprobe-Ausgangsprüfung, Überblendungseffekte, Intensitäten, Warteschlange und umfangreiche Codec-Tests fehlen. |
| Automatische GitHub-Verwaltung | Erst nach klar definiertem Offline-/Online- und Sicherheitskonzept |
| Hörspiel-, Blog-, Prompt-Produktion | Dedizierte Arbeitsabläufe über vorhandene Schreibvorlagen hinaus |

## C. Fehlende eigenständige Module und Infrastruktur

| Priorität | Modul | Erwartete nächste Iteration |
|---|---|---|
| 1 | Produktive Update-Umschaltung | Atomare Aktivierung erst nach geprüftem Checkpoint, Startnachprüfung und gesichertem automatischem Rollback |
| 2 | Erweiterter Projektmodulbaukasten / Plugin-System | Bestehende Modulverträge und Menüsteuerung um geprüfte Modulbau- und Fremdplugin-Funktionen ergänzen |
| 3 | Video/Slideshow technisch vervollständigen | ffprobe-Validierung, Übergänge, Intensitätssteuerung und Auftragswarteschlange |
| 4 | Entwicklungspool sicher erweitern | Archiv-Rückimport, bestehende Arbeitsordner bei Kollisionen schützen |
| 5 | Reimfinder | Lokales deutsches Nachschlage-/Reimwerkzeug |
| 6 | Duplikatprüfer | Dateihash-/Vorschauprüfung, niemals automatische Löschung |
| 7 | Read-only-Konsole / Entwicklerbereich | Diagnoseanzeige und begrenzte Entwicklerrechte ohne versteckte Schreibwege |
| 8 | Zusätzliche Datei-/Projektwerkzeuge | Vereinbarte Restfunktionen aus B nach getrennten Prüfverträgen |

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

## Iteration 63 – Multimedia-Basismodule (Entwicklungszweig)

Drei eigenständige PySide6-Module mit einheitlicher Tastatur/Zoom/Theme-Steuerung werden ergänzt: ① Audioplayer mit lokaler persistenter Playlist, Play/Pause/Stopp/Sprung und Lautstärke. ② Bildvorschau mit Bildlisten, Größenlimit und skaliertem Leser. ③ FFmpeg-Slideshow (1–20 Bilder, Dauer, optionale Tonspur), Video→Audio-Umsetzung, asynchroner Einzelausführung, Fortschritt/ETA, Abbruch und niemals überschreibender MP4-Veröffentlichung. Bisher **keine konfigurierbaren Überblendeffekte**, keine echte Warteschlange für mehrere Aufträge und keine vollständig garantierte Ergebnisprüfung mit ffprobe. Import/Export bei Playlist, Bildliste und Slideshowvorgaben ist vorhanden. Automatische Logik- und GUI-Prüfungen laufen vor der Übernahme. Die vollständige manuelle Kubuntu-Abnahme erfolgt erst am Projektende.

## Aktuelle Integration – Iterationen 60 bis 63

- PR #100: Verwaltete Update-Slots mit automatischer Rückkehr bei Startproblemen, CI #1039, Hauptzweig #1040.
- PR #101: Modulbaukasten mit sicheren Vorlagen, CI #1041, Hauptzweig #1042.
- PR #102: Entwicklungspool mit Arbeitsordnern und Kopien, CI #1043, Hauptzweig #1044.
- PR #103: Audioplayer, Bildvorschau und FFmpeg-Slideshow-Basis, CI #1046 erfolgreich; Hauptzweig #1047 gestartet.

Die früheren Abschnitte 60 bis 63 mit „Entwicklungszweig“ sind Entstehungsnachweise und keine zweite aktuelle Aufgabenliste. Die Funktionsdefizite stehen weiterhin in Abschnitt B/C. Keine vorgezogene manuelle Kubuntu-Abnahme.

## Iteration 64 – geprüfter Entwicklungskandidat

- **Update:** Nichtverändernde Migrations-Eignungsprüfung bestehender Installation und Zielordner. Eine produktive Migration wird weiterhin ausdrücklich **nicht** freigegeben: externer dauerhafter Datenstart, Sicherung, atomare Migration und Wiederanlauf fehlen.
- **Modulbaukasten:** Modulvorlagen können nun geprüfte lokale Datensätze mit Feld-Typkontrolle speichern und durchsuchen, nur wenn die jeweilige deklarative Fähigkeit erlaubt wurde. Kein dynamisches Laden fremder Plugins, keine Shell- oder Netzwerkrechte.
- **Multimedia:** Vor MP4-Veröffentlichung wird FFprobe zur Prüfung auf Dauer, Videoauflösung und gegebenenfalls Tonspur verwendet. Fehlende oder fehlerhafte FFprobe-Ausgaben verhindern die Veröffentlichung. Übergänge, Effektintensität und Stapelaufträge fehlen noch.
- **Entwicklungspool:** Vollständiger ZIP-Rückimport als separate neue Projektkopie mit Prüfung gegen absolute Pfade, Traversal, Dateiverknüpfungen und Größenüberschreitungen. Kein Überschreiben vorhandener Arbeitsordner.

Dies ist zunächst ein separater Entwicklungszweig. Vor der Übernahme ist die vollständige GitHub-Prüfung verpflichtend. Manuelle Kubuntu-Gesamtabnahme erst am Ende des Gesamtprojekts.

## Iteration 65 – geprüfte Anschlussbausteine (Entwicklungszweig)

Programmdaten: rein lesender Nachweis voneinander unabhängiger Code- und Datenordner; keine automatische Bestandsmigration. Modulbaukasten: ausschließlich fest kodierte Datenoperationen nach expliziter Rechtezustimmung; kein Fremdcode. Video: gespeicherte Auftragsliste mit Zuständen, Absturz-Unterbrechungsmarkierung und Sperre paralleler gestarteter Jobs; Effektparameter mit begrenzter Intensität als **Vorbereitung**, noch keine FFmpeg-/GUI-Einbindung oder fertige Übergangseffekte. Alle Funktionen sind noch CI-pflichtige Kandidaten.

## Iteration 66 – benutzbare Datenmodule (gesonderter Kandidat)

Der vorhandene Modulbaukasten kann gespeicherte Formularentwürfe in einem eigenen Dialog zur tatsächlichen Datenaufnahme öffnen. Vor jedem Schreiben ist eine ausdrückliche Zustimmung erforderlich, die zusätzlich vom Modulrechte-Vertrag geprüft wird. Fremder Python- oder Shellcode bleibt verboten; Module können nur vordefinierte sichere Datenoperationen durchführen. Vollständige GitHub-Prüfung vor Integration erforderlich.
