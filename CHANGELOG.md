# Änderungsverlauf

<!-- PV_UX26_INPUT_CONTRAST_20261101 -->
## Eingabefelder in drei Themes klarer begrenzen (01.11.2026; Prüfzweig)

- Reproduzierbarer Farb-Befund: Eingabefeldrand gegen Eingabehintergrund Amber 2,86:1, Türkis 2,22:1, Lila 2,39:1.
- Farbwerte gezielt auf Amber `#7291A7`, Türkis `#6FA5AB` und Lila `#AA89BA` erhöht. Erwartete Kontrastverhältnisse mindestens 3,42:1, 3,52:1 und 3,60:1.
- Neue automatische Prüfung kontrolliert alle Farbthemes auf Eingaberand-Kontrast, Platzhalter-/Textlesbarkeit und die zentrale Styleverwendung.
- Keine Änderungen an Profilen, Daten, Farben der Nutzereingabe, Fensterlogik oder Bedienfunktionen; **vollständiger Theme-Umbau bleibt eine offene gesonderte Aufgabe PV-UX26-06**.
- Erste Dashboard-Navigationskorrektur PR #162 wurde nach grüner PR-Prüfung integriert; eigenständiger main-Prüflauf #41305861757 ist ebenfalls erfolgreich.

<!-- PV_UX26_NAV_SCROLL_20261101 -->
## Navigation bei kleinen Fensterhöhen scrollbar (01.11.2026; Prüfzweig, noch keine Freigabe)

- Screenshot-Befund #161: Menüeinträge am unteren Rand waren nicht zuverlässig zugänglich, weil die Navigation keinen vertikal scrollenden Inhaltsbereich hatte.
- Gezielter PySide6-Patch: Menükopf bleibt fest; vorhandene Einträge einschließlich erweiterter Planungsgruppen liegen in einer `QScrollArea`; beim Einklappen verschwindet die Liste vollständig.
- Bestehende Aktionsverknüpfungen, zentraler Profilbestand und Navigationsbreiten bleiben unverändert. Keine Datenmigration.
- **Prüfstatus:** Automatisierter GUI-Rückfalltest im Prüfzweig ergänzt; PR-CI und main-CI vor einem Haken in TODO abwarten. Die allgemeine Dashboard-Neugestaltung bleibt als Folgeauftrag in #161.


## Issue #126 – Dashboard-Karten im bestehenden Raster verstellen (31.10.2026; Prüfkandidat)

- Statt der fehlerhaften verschachtelten QSplitter aus PR #124 bleiben die vier Karten im nativen Qt-Raster. Zwei senkrechte und ein waagerechter Griff verändern die Spalten-/Zeilenanteile per Maus oder Pfeiltasten.
- Die bisherigen Mindestbreiten bleiben unverändert. Bei knapper Fensterhöhe bleiben die beiden Planungskarten und zugehörige Griffe verborgen; die gewählte Zeilenverteilung wird beim Rückwechsel wiederhergestellt.
- Keine Nutzerdatenänderung und keine zusätzliche Bibliothek. Automatisierte Layout-, Zoom- und Tastaturtests sind vorgesehen; vollständige GitHub-Prüfung bleibt Pflicht.


## README: farbiger Projektstatus und Schnellnavigation (31.10.2026)

- Farbig beschriftete Statuskennzeichen für Entwicklungsstand, Version und Zielsystem ergänzt; der Hauptzweig-Prüfstatus wird direkt aus GitHub Actions angezeigt.
- Schnellzugriffe auf Start, Bedienung, Datensicherung, Modulplan und offene Aufgaben ergänzt. Statusfarben werden zusätzlich ausgeschrieben und bleiben ohne Farberkennung verständlich.
- Dokumentationsstand aktualisiert und die veraltete Angabe zu den zuletzt verbesserten Funktionen durch einen neutralen Verweis auf Sicherheitskorrekturen und den Änderungsverlauf ersetzt. **Keine Code-, Nutzerdaten- oder Versionsänderung.**

## Lesbare Eingabefelder und Song-Arbeitsfläche bei 200 % (PV-UI-01/02, 26.10.2026; Umsetzungskandidat)

- Dashboard-Beschriftungen, Profil- und Theme-Auswahl erhalten gemessene Mindestbreiten statt abgeschnittener Texte; der Laptop-Kompaktmodus verwendet einen kurzen, vollständig benannten Titel.
- UI-Shadow-Gate prüft zusätzlich einfache sichtbare Beschriftungen und aktuelle Auswahlwerte auf Textüberlauf; entsprechende Negativproben und eine sieben Fälle umfassende Referenzmatrix ergänzt.
- Songeditor hält bei 175/200 % die Schreibfläche und Gesamtvorschau frei. Charakterauswahl und optionale Notizen sind bei Bedarf über erreichbare Schalter einblendbar; vorhandene Werte bleiben unverändert.
- Lange Statusmeldungen in Songbibliothek und Aufgabenliste können umbrechen. Datenformate, Speicherintervalle, Modulzugänge und Version bleiben unverändert.
- Lokale Qt-Offscreen-Messung: 70 Fälle ohne Textbreitenbefund; PR-Shadow: acht Matrixfälle, 0 Fehler/0 Warnungen. Vollständige GitHub-Prüfung und finale reale Kubuntu-Abnahme bleiben getrennt.

## Eindeutige Verlassen-Dialoge (PV-UX-04, 25.10.2026)

- Aktionsbezogene Schaltflächen statt sichtbarer Ja/Nein-Rückfragen bei Text-/Modulwechsel und Fenster-/Dashboard-Schließen.
- Weiterarbeiten als Vorauswahl, Escape- und Fensterschließen-Aktion; fehlgeschlagenes Speichern verhindert das Verlassen.
- Gemeinsamer Dialog auch für Ideenkomposition und Modulverwaltung; sonstige Import-/Löschbestätigungen und Song-Automatik unverändert.

## Einheitliche Speicherzustände (PV-UX-03, 25.10.2026)

- Eigene gemeinsame Speicheranzeige für Songs, Texte und Bücher; Erfolg an tatsächlichen sichtbaren Snapshot gebunden und bei Änderungen sofort ungültig.
- Titelgrenze ungespeicherter Text-/Buchentwürfe und bestehende Song-Automatik ausdrücklich erklärt. Schreibfehler erhalten Eingaben und bisherigen Datenbestand.
- Textauswahl beim Neuanfang vollständig zurücksetzen, damit der zuvor gewählte Text erneut geöffnet werden kann. Speicherformate und Intervalle unverändert.

## Tätigkeitsorientierter Einstieg (PV-UX-01, 24.10.2026)

- Startkarte „Was möchtest du tun?“ mit vier gleichwertigen Aktionen ohne nummerierte Reihenfolge: Song schreiben, Text schreiben, Aufgabe planen, Termin anlegen.
- Neue Songs direkt beginnen; sichtbaren Texteditor ohne Neuladen aktivieren und offene Entwürfe erhalten. Geschlossene verworfene Texte werden nicht wiederbelebt.
- Leere Textliste erklärt Titel, Inhalt und Speichern. Aufgaben-/Termineingaben bleiben beim erneuten Öffnen erhalten.
- Verzögerten Laptop-Layoutaufruf auf bereits zerstörte Fenster kontrolliert beenden; gezielter Rückfalltest.
- Kompaktes 2×2-Aktionsraster schützt Lesbarkeit und getrennte Bedienung bei starkem Zoom; bestehende UI-Grenzen unverändert.
- Zentrale Texte, Hilfe, Anleitung, Manifest und Aufgabenplanung aktualisiert.

## Persönliche Aufgaben von Entwicklungsaltbestand trennen (PV-AUD-05, 24.10.2026)

- Beim Öffnen keine Entwicklungsaufgaben mehr in den persönlichen Bestand eintragen.
- Alte Entwicklungsaufgaben anhand ihrer festen Kennungen rein lesend separat anzeigen; eigene Aufgaben mit gleichen Titeln bleiben persönlich.
- Persönliche Kopie nur nach Bestätigung und mit neuer Kennung; ursprüngliche offene/erledigte Aufgaben und noch nicht angelegte Formulareingaben erhalten.
- Erledigen-Aktion auf die persönliche Aktiv-Ansicht begrenzen; Fehler bei Kopien mit geschützter Diagnose behandeln.
- Datenformat, Sicherungsumfang und bisherige Gesamtsicht-APIs unverändert; Anleitung, Hilfe und Manifest aktualisiert.

## Projekt-Notizen und persönliche Sicherung (24.10.2026; PV-AUD-01)

- Aufgabenstatus PV-AUD-02 berichtigt: PR #121 war bereits übernommen; drei vorhandene UTF-8-Log-Rückfalltests erneut erfolgreich, keine Doppelimplementierung.
- Neue Notizen atomar unter `daten/notizen/projekt-notizen.txt` speichern; bestehende Einträge erhalten.
- Alte `Entwicklerinformation.txt` nur nach ausdrücklicher Zustimmung als bytegenaue Altkopie in den Datenordner übernehmen; Original nie löschen oder überschreiben.
- Wiederholte Übernahme ohne Dubletten, geänderte Altbestände als neue Kopie, Ablehnung mit Hinweis auf Sicherungsausschluss.
- Kollisions-, Link-, Größen- und Schreibfehler schützen vorhandene Dateien und aktuelle Eingaben; Daten-ZIP-Roundtrip mit Alt- und Neunotizen geprüft.

## Lokale Dateisystemsuche – Implementierungskandidat (24.10.2026)

- Suchordner frei eingeben oder über die native Ordnerauswahl wählen; Unterordner werden mit durchsucht.
- Lesenden Suchbereich außerhalb des Standarddatenordners vor dem ersten Lauf ausdrücklich bestätigen; Pfadwechsel hebt die Freigabe auf.
- Fehlende Betriebssystem-Leserechte zählen und unvollständige Ergebnisse deutlich erklären; keine automatische Rechteänderung oder Administratorsuche.
- Weitere UTF-8-Klartextformate berücksichtigen; vorhandene Datei-, Größen-, Zeit- und Linkschutzgrenzen erhalten.
- Anleitung, Hilfe und UX-Suchanforderung an den vom Nutzer präzisierten lokalen Dateisystemscope angepasst.

## Dokumentation: UX-Konzept (24.10.2026; keine Produktänderung)

- Vertiefte Analyse zu Datenumfang, persönlichen Aufgaben, Einstieg, Navigation, Speichern, Suche, Inhaltsbeziehungen, Sprache, Fehlerhilfe und Barrierefreiheit dokumentiert.
- Bestehende Audit-Aufträge verknüpft; zehn ergänzende UX-Aufträge und zwölf geplante Abnahmeszenarien erfasst.
- Konzept im Dokumentationswegweiser verlinkt. Laufende Modulplanung, Laufzeitverhalten, persönliche Daten und Programmversion bleiben unverändert; keine neue GUI- oder Nutzerabnahme behauptet.

## Weitere Modulentwicklung (PR #100–#103, 19.10.2026; kein Release)

- Vorbereitete Update-Slot-Installationen können nach abgeschirmter Prüfung atomar zwischen Programmversionen wechseln und bei Startfehlern zurückfallen. Bestehende Normalinstallationen bleiben unverändert.
- Formularorientierter Modulbaukasten: geprüfte nicht ausführbare Entwürfe, Import/Export und Vorschau.
- Entwicklungspool: lokale Projektordner, Status, Dateiübersicht, unabhängige Kopien und ZIP-Archive.
- Audioplayer mit Playlist, skalierte Bildvorschau und FFmpeg-Slideshow mit Video-Tonspur-Umsetzung, Abbruch und exklusiven Ausgabedateien.
- GitHub-Prüfungen #1039/#1041/#1043/#1046 erfolgreich; die jeweiligen Hauptzweigprüfungen #1040/#1042/#1044 erfolgreich, #1047 nach letzter Integration gestartet.
- Verbleibende Arbeiten: Altinstallations-Migration, echte Drittplugins, Entwicklungs-ZIP-Rückimport, Videoeffekte und ffprobe-Validierung. Kubuntu-Gesamtabnahme weiterhin am Ende.

## Neu in 0.18.5-Entwicklung nach PR #97 und #98 (19.10.2026, kein öffentliches Release)

- PR #97 integriert updateisolierte Laufzeitprobe, versionierte Modulverträge und das lokale Wiki nach gemeinsamer grüner CI #1031; main-CI #1033 ebenfalls erfolgreich.
- PR #98 ergänzt eine rein programmbezogene Checkpoint-Sicherung und eine prüfbar getrennte Rückkehrkopie. Die aktive Installation wird dabei nicht überschrieben; produktive Aktivierung und automatischer Rollback fehlen weiterhin.
- Vier schon vorhandene Zusatzmodule können über „Module verwalten“ tatsächlich ein-/ausgeschaltet werden. Bestehende Arbeitsdaten bleiben erhalten und offene Modulfenster verhindern unbeabsichtigtes Abschalten.
- PR-CI #1035 erfolgreich; Hauptzweig-CI #1036 nach der Integration gestartet. Keine vorgezogene manuelle Kubuntu-Abnahme.

## 0.18.5 – Modulplan und Link-Schnellstarter (Entwicklungskandidat, 19.10.2026)

- Offene PRs bereinigt: #83 als durch #87 überholt geschlossen, #88 und #89 nach automatischer Prüfung integriert.
- Verbindlicher Modulplan umfasst ältere Multimedia-, Verwaltungs- und Entwicklerfunktionen; doppelte/veraltete Todo-Einträge in der aktuellen Übersicht geklärt.
- Link-Schnellstarter: sichere lokale Webadressen, Gruppen, kurzer Symboltext, Import/Export, eigener Editor und platzsparende rechte Leiste.
- Nachpflege: Link-Leiste nach Änderungen aktualisieren, Menülabel kürzen und späte Qt-Theme-Rückrufe nach Fensterende sicher ignorieren.
- Navigation: verzögerte Layout-Nachsynchronisierung darf nach zerstörtem Dashboard nicht mehr auf Qt-Objekte zugreifen (Issue #92).
- Praktische vollständige Kubuntu-Abnahme bleibt ausdrücklich bis zum vollständigen Modulabschluss zurückgestellt; automatisierte Prüfungen laufen fort.


### Text-Strukturhilfen
- Abschaltbare Strukturfarben für Überschriften, Aufgaben und Codeblöcke; begrenzte Gliederung mit Sprungfunktion.
- Darstellung bleibt vom gespeicherten Klartext und seinem Änderungsstatus getrennt.

### Prozessstartmessung
- Echten Programmstart mit synthetischen Daten in neuen Prozessen bis zur ersten Ereignisschleife messen.
- Ersten und wiederholten Start unterscheiden; Betriebssystem-Dateicache bleibt ausdrücklich unkontrolliert.

### Accountmetadaten
- Konten nach Name, E-Mail, Gruppe und Zusatzangaben wiederfinden; validierte Webadressen bewusst öffnen.
- Kein Passwortfeld; sensible Feldnamen/Zugangsdaten-URLs abweisen und unverschlüsselten Metadatenexport bestätigen lassen.

### Ideenarchiv
- Fragmente mit Schlagworten/Herkunft suchen und als Kopien zu neuen Texten zusammenstellen.
- Import/Export, atomare Ablage, Entwurfsschutz und vorhandene Textdatei-Kollisionssicherung wiederverwendet.

## 0.18.4 – Entwicklungskandidat
- Update-Runtime-ZIPs anhand von Paket-/Basis-SHA, Manifest, Version, Dateiliste und Grenzen statisch prüfen.
- Ausschließlich getrenntes Staging; keine Ausführung, Installation oder Aktivierung des Kandidaten.

## 0.18.3 – Ergänzung zentrale Suche
- Gespeicherte Dateinamen und UTF-8-Textinhalte unter daten/ mit Treffern, Zeilennummer und Klartextvorschau suchen.
- Abbruch, feste Suchgrenzen und Schutz vor Linkverfolgung; keine Indexdateien oder automatischen Dateiöffnungen.
- Dateisuche-Kachel, Kopfsuchfeld, bestehende Werkzeugkarten und Strg+Umschalt+F führen zur zentralen Suche.

## 0.18.3 – lokaler Prüfkandidat, noch nicht veröffentlicht
- Persönliche Daten unabhängig sichern und isoliert zurückholen.
- Defekte Startumgebungen und fehlende Pakete trotz Installationsmarker erkennen.
- Schreib-/Ladebenchmarks und Auswertung gespeicherter UI-Kalibrierungsnachweise.
- Versionskennung im Fenstertitel und klare Freigabeunterlagen.

## Entwicklung – UI-Kalibrierung vorbereiten
- Gespeicherte vollständige CI-Evidenz auswerten; Dubletten und ungeklärte Befunde verhindern eine Empfehlung.
- Keine automatische Änderung des Shadow-Modus.

## Entwicklung – Archivlade-Benchmark
- Synthetische Datenklassen und tatsächliche Archivvalidierung in neuen Prozessen; erstes und wiederholtes Lesen getrennt.
- Betriebssystem-Cache und vollständiger Dashboardstart werden nicht als gemessen ausgegeben.

## Entwicklung – robuster Start
- Beschädigte vorhandene Umgebungen bleiben erhalten; klare Wiederanlaufhilfe.
- Paketversion und Qt-Import unabhängig vom Installationsmarker prüfen; begrenzte Installation und Startprüfungen.

## Entwicklung – persönliche Datensicherung
- Eigenständige Sicherung aller regulären Arbeitsdateien, SHA-256 und isolierter Wiederherstellungsvergleich.
- Rückholen ausschließlich in neue Ordner; keine automatische Aktivierung und keine Löschung alter Sicherungen.

## Entwicklung – Diagnose-Benchmark (18.10.2026)
- Isoliertes, begrenztes Entwicklermesswerkzeug für identische Schreibmengen ohne Instrumentierung sowie mit ausgeschalteter/eingeschalteter Diagnose.
- Rohwerte, Flush-Kosten, Quellstand und Systembedingungen; keine neue Laufzeitfunktion oder Abhängigkeit.

## 0.18.2 · 18.10.2026 – Dashboard-Layout aus Issue #86

- Bestehenden Höhen-Grenzwert der kompakten Dashboardansicht auch bei 100 % anwenden.
- Ausgeblendete Planungskarten reservieren keinen Platz mehr; Profil- und Vorgabenfelder überlappen sich nicht.
- Seitenleiste verwendet bei 150 % die kurze Beschriftung „Textbuttons“; zugänglicher Name und Aktion bleiben erhalten.
- Zwei GUI-Rückfalltests; vollständige lokale Release-Matrix: 60 Fälle / 180 Fenster, 0 Fehler / 0 Warnungen.
- Leistungsdiagnose aus PR #85 ist nach ausdrücklicher Freigabe in main enthalten.

## 0.18.1 · 18.10.2026 – lokale Leistungsdiagnose

- Zusätzliche Leistungsmessung ausdrücklich einschaltbar; standardmäßig aus, ohne automatische Übertragung.
- Tagesaggregate für Modul-/Bestandsladezeiten, Dashboardaufbau, zentrale Text-/JSON-Schreibzugriffe und unveränderte gültige Speicherversuche.
- Auswahl, lesbare Übersicht, bereinigte JSON-Vorschau, TXT-/JSON-Export, Aufbewahrung 1–30 Tage und bestätigtes Löschen.
- Rekursionsschutz, gebündelte Speicherung, Größenlimits und fehlertolerante Messung; keine Inhalte oder Dateipfade in den Messdaten.
- Textbuttons und Buchwerkstatt wurden über PR #84 nach ausdrücklicher Freigabe in main übernommen; Hauptzweig-Prüfung erfolgreich.

## 0.18.0 · 18.10.2026 – Textbuttons und Buchwerkstatt

- Informationsdateien, Entwicklungsreview und konkrete Verbesserungsregeln konsolidiert; historische Prüfnachweise klar vom aktuellen PR-Head getrennt.
- Vorhandenen Formularreset wiederverwendet: vier Codezeilen weniger ohne neue Abhängigkeit.

- Textbuttons mit Workflow-Reitern, Kategorien, Suche, Farben, drei Größen, Spalten und Reihenfolge.
- Platzhalter, Unterversionen, Zwischenablage-Einfügen und Monatsstatistik mit TXT-Export.
- Buchwerkstatt mit fünf Vorlagen, bis acht Kapitelebenen, Schreibelementen, Charakterfibel, Status und Notizen.
- Gemeinsame atomare Speicherung, validierte Modularchive, Importvorschau, Entwurfsschutz und optionale lokale Rechtschreibung.
- Bei 175/200 % Zoom verdrängt der zusätzliche GitHub-Projekte-Button keine Profilfelder mehr; Strg+Umschalt+G bleibt als Zugang verfügbar.
- 25 neue Tests; bestehende Nutzerdatenformate unverändert.

## Erweiterungen · 18.10.2026 (Version bleibt vor Praxisabnahme 0.17.4)

- Genrearchiv: Sterne pro Profil/Kategorie, separater Zufall ausschließlich aus Favoriten und fortlaufende Historie mit Kennzeichnung der Favoritenziehungen.
- **Nur Genres:** Stichtagsbezogene Monatsstatistik mit Vorschaufenster, Hilfefenster, manueller TXT-Ausgabe, Profil- und Kategorieauswertung.
- Eigenständige **GitHub-Projektübersicht** für offene und fertige Projekte mit Name, Repository, URL, lokalen Notizen und optionaler Aufgabenliste sowie Kopierfunktion und JSON-Import/-Export.
- Duplikatschutz, Eingabeprüfung, sichere atomare Speicherung und Regressionstests; keine Anmeldung oder externe GitHub-Abfragen.
- Beide sichtbaren Erweiterungen benötigen vor uneingeschränkter Benutzerfreigabe noch die Kubuntu-Praxisabnahme.


## Entwicklungseffizienz – 18.10.2026 (Version weiterhin 0.17.4)

- Letzte manuelle Signalsperre im Kompaktmodus des Songeditors durch zustandserhaltende Qt-Sperre ersetzt.
- GitHub-Messwerkzeug um getrennte Installations- und Prüfzeiten sowie einen ehrlichen Zehn-Läufe-Vergleich erweitert.
- Systempakete-Installation unverändert belassen: Schwankende Dauer ist noch kein ausreichender Grund, notwendige Aktualisierung oder Pakete wegzulassen.
- Rückfalltests ergänzen die Nachweise; keine Änderungen an Benutzeroberfläche, Daten oder Dateiformaten.


## Interne Vereinfachung – 18.10.2026 (weiterhin 0.17.4)

- Doppelte Aktualisierung der Charakterauswahl in Songeditor und allgemeinem Texteditor in eine gemeinsame Hilfsfunktion überführt.
- Bestehende Auswahl, Beschriftung, Fehlerrückfall und Schutz vor Änderungssignalen bleiben erhalten.
- Die Funktion wird durch zusätzliche automatische Tests abgesichert. Keine sichtbare Änderung und kein neues Dateiformat.


## Interne Entwicklungseffizienz – 18.10.2026 (Version weiterhin 0.17.4)

- Doppelungen in Python-Programmdateien können mit einem rein lesenden Analysewerkzeug erkannt werden.
- GitHub-Prüfläufe, ungefähre Dauer, zusätzliche Prüfungen desselben Commits, Zwischenspeicher-Nachweise und Änderungsumfang können mit einem kleinen Werkzeug ausgewertet werden.
- Die bereits vorhandene Fensterverwaltung wurde aus der großen Dashboard-Datei in `app/window_lifecycle.py` verschoben, ohne Funktionen oder Aufrufnamen zu verändern.
- Zwei Rückfalltestdateien sichern die Entwicklungswerkzeuge und die unveränderten Importstellen ab.
- **Keine Änderung** an der Bedienoberfläche, persönlichen Daten oder Speicherformaten.


## Wartung der Entwicklung – 18.10.2026 (Programmversion weiterhin 0.17.4)

- GitHub-Prüfung nur noch bei Pull Requests und neuen `main`-Commits auslösen, statt für denselben PR-Commit zusätzlich einen Zweig-Lauf zu erzeugen.
- Überholte Prüfläufe eines Pull Requests automatisch abbrechen; `main`-Prüfungen niemals dadurch abbrechen.
- Python 3.12 als feste Prüfumgebung und Download-Zwischenspeicher für die festgelegten Python-Pakete verwenden.
- Regressionstests bewachen die unveränderten Sicherheitsprüfungen und den neuen Auslösevertrag.
- Entwicklungsregeln für kleine Patches, gebündelte Commits, gezieltes Lesen und Nachweise zu exakt einem Commit konkretisiert.
- **Keine** Änderung an Programmoberfläche, Nutzerdaten, Dateiformaten oder Sicherheitsschranken.


## Dokumentationspflege und nachträgliche Fehlerkorrekturen – 17.10.2026 (Version weiterhin 0.17.4)

- Gemeinsame Korrekturen gegen Verlust ungespeicherter Texte, versehentliches Überschreiben bei Dateinamen-Kollisionen und Dashboard-Überlappungen über [PR #57](https://github.com/provoware/TOOL_2026_Multi/pull/57) integriert.
- Darstellung der Navigation bei 150–200 % vergrößerter Schrift nachgebessert; Layoutkonflikte anschließend über PR #58–61 behoben.
- Letzter dokumentierter vollständiger Oberflächenlauf: 60 Prüffälle, 180 Fensteransichten, 0 Fehler, 0 Warnungen. [GitHub-Prüflauf](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39065993768).
- README, Einsteigeranleitung, Aufgabenübersicht und Ordnererklärung vereinheitlicht. Historische Iterationsberichte bleiben als Nachweise erhalten.
- Die sichtbare Abnahme an einem echten Kubuntu-26.04-Rechner sowie eine ausdrücklich unabhängige Sicherung persönlicher Daten bleiben offene Aufgaben.
- **Versionshinweis:** Keine neue Produktversion behauptet. Die Versionsnummer bleibt 0.17.4, bis eine eigene Freigabe erfolgt.


## 0.17.4 – Iteration 39: Autonomous UI Quality Gate PRO (Shadow Mode)

- zentrale Qt-unabhängige UI-Verträge für 8-/4-Pixel-Raster, Geometrie, Mindesthöhen und WCAG-Kontrast
- 8-fällige PR-Kernmatrix und vollständige 60-fällige Main-/Release-Matrix
- deterministisches Window-State-Fuzzing für ungültige/offscreen gespeicherte Fensterpositionen
- automatischer PySide6-Shadow-Gate für Dashboard, Songbibliothek und Songeditor
- JSON-Evidenz, Markdown-Zusammenfassung und Raster-Screenshots bei Auffälligkeiten
- Infrastrukturfehler des Prüfsystems werden explizit dokumentiert statt still verschluckt
- GitHub Actions sammelt Shadow-Evidenz getrennt vom unveränderlichen Quell-Manifest; bestehende Hard-Gates bleiben unverändert
- reine Vertrags-/Meta-Tests prüfen das Prüfsystem selbst und erkennen absichtlich fehlerhafte Geometrie, Kontrast und Promotion-Zustände

## 0.17.3 – Iteration 38: Fensterführung, Kompaktmodus und Fokuskontrast

- Songbibliothek wird während einer Editor-Sitzung kontrolliert verborgen und nach dem letzten Editor wiederhergestellt.
- gespeicherte Fensterpositionen werden nur bei aktuell sichtbarer Monitorüberschneidung übernommen; sonst sicher neu zentriert.
- portable Fensterzustände in `daten/ui/fenster.json`, unabhängig von Songdaten.
- Songeditor blendet optionale Metadaten im Kompaktmodus ein/aus; Songbibliothek bündelt Filter/Sortierung/Gruppierung.
- Eingabefelder: neutraler Normalrand, Theme-Akzent bei Fokus, zentrale Rot-/Grün-Zustände sowie kontrastreichere Platzhalter.
- sichtbares `&` in „Hilfe & Fehlerhilfe“ Qt-konform repariert.
- neue GUI-Regressionen für 1366×768, Zoom/Kompaktmodus, Fokusfluss und Fensterzustand.
- erster PR-Gate #795 blockierte korrekt wegen zwei Screenreader-Assertions; die zentrale Accessibility-Normalisierung wurde ursächlich korrigiert.
- technischer Gate #799 vollständig grün: 113 Logik-/Regressionstests, 83 GUI-Tests, 48 Release-Dateien, nativer Qt-Wayland-Start und Restore `OK`.
- Restore-SHA-256: `900e08dbad15d13e005f559715ec2f41c4260f6e53ad1395a3f3c4c243912bd9`; Runtime-Release-SHA-256: `a626f93eade99b5ba4b486b1e9bd60552f17f231ab8c23a4e0adb2b39d39158c`.
- finaler Head-Gate nach Synchronisierung dieser Evidenz bleibt vor dem Merge verpflichtend.


## 0.17.2 – 2026-09-12 – Wartbarkeit, Entwicklungseffizienz und Hilfe

### Neu
- durchsuchbare **Hilfe & Fehlerhilfe** mit F1-Schnellzugriff, acht alltagsnahen Hilfethemen und getrenntem Fehlermeldungs-Reiter,
- `scripts/pruefen.sh --quick` als kurze Entwicklungsprüfung; `--full` bleibt verbindliches Merge-/Release-Gate,
- automatische Entdeckung aller Logik- und GUI-Testdateien anhand des Namensschemas.

### Geändert / bereinigt
- freigegebene Betriebsdateien werden in der Prüfung direkt aus `MANIFEST.json` gelesen statt in einer zweiten langen Shell-Liste gepflegt,
- zentrale UI-unabhängige Hilfetexte in `app/help_content.py`,
- Einmal-Helfer `scripts/_iter33_docs_apply.py` entfernt,
- Repo-Hygiene blockiert künftig bekannte Einmal-Patch-/Finalizer-Präfixe,
- README-Qualitätsabschnitt von veralteten Iterations-Einzelnachweisen auf den aktuellen Referenz-Gate und das zweistufige Prüfverfahren verdichtet.

### Schutz
- keine Nutzerdaten oder Speicherformate geändert,
- keine neue externe Laufzeitabhängigkeit,
- Recovery-Funktionalität bleibt vollständig erhalten, jetzt als zweiter Reiter innerhalb von Hilfe & Fehlerhilfe,
- Version 0.17.1 / Iteration 36 bleibt über Main-Grundprüfung #750 als unveränderte Referenzbasis dokumentiert.

### Technische Abnahme
- erster technischer PR-Gate **#764** blockierte korrekt: das neue Runtime-Modul `app/help_content.py` fehlte noch im Release-Manifest; zusätzlich wurde die noch fehlende Iteration-37-Dokumentation erkannt. Die 77 GUI-Tests waren bereits vollständig grün.
- korrigierter technischer Head `7368488c601160506a7b95a057c3e340bef64e8f` in Grundprüfung **#769** vollständig grün: **113 Logik-/Regressionstests**, **77 PySide6-GUI-Tests**, **47 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich.
- Vollprojekt-Restore `OK`, SHA-256 `000b03420cb2a7cddc4ce80885e27aa9f96bdf62aa43a571116f099c16fbb177`; Runtime-Release-SHA-256 `993786558ce564dfbd5deee90ac9b7f1fe0067a321d5e12a7c0859f97cb6f28a`.
- der vollständig auf **0.17.2 / Iteration 37** synchronisierte Freigabe-Head wird vor dem Merge erneut durch denselben Voll-Gate geprüft.

## 0.17.1 – 2026-09-12 – Charakterzugriff in Schreibmodulen und vollständige CI-ZIPs

### Neu
- zentrale UI-unabhängige Charakterauswahl für Schreibmodule mit stabiler ID, einheitlicher Beschriftung und wiederverwendbarer Referenz,
- direkter Charakterfibel-Zugriff im Songtexteditor; ausgewählte Figuren werden an der aktuellen Schreibposition eingesetzt,
- erfolgreicher CI-Lauf erzeugt nach Grundprüfung, nativem Qt-Wayland-Smoke und Restore zusätzlich ein vollständiges Projekt-ZIP sowie SHA-256 und lädt die geprüften Pakete als Artefakt hoch.

### Fehlerbehebung / Schutz
- der erste Iteration-35-Prüflauf **#716** blockierte korrekt: der zunächst verwendete Marker `[Charakter: …]` kollidierte mit der vorhandenen Songbereichssyntax `[Strophe]`, `[Refrain]` usw.,
- der gemeinsame Marker wurde deshalb auf die klar lesbare und songformat-sichere Form `«Charakter: Name (Rolle)»` geändert,
- Song- und Textdatenformate bleiben unverändert; keine Migration und keine neue Laufzeitabhängigkeit,
- keine bestehenden Nutzerdaten gelöscht, konvertiert oder überschrieben.

### Technische Abnahme
- korrigierter Head `907e65df46ba31d2d5e7df03d137baf1448742b8` in Grundprüfung **#722** vollständig grün,
- **106 Logik-/Regressionstests**, **76 PySide6-GUI-Tests**, **46 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a`,
- CI-Artefakt mit Runtime-Release-ZIP und vollständigem Projekt-ZIP samt Prüfsummen erfolgreich erzeugt.

## 0.17.0 – 2026-09-12 – Charakterfibel, Texteditor und gemeinsame Daten-/UI-Standards

### Neu
- Charakterfibel als eigenständiges Modul mit atomarem Datenbestand, stabilen Charakter-IDs, Suche/Bearbeitung und wiederverwendbaren Charakterreferenzen,
- universeller Texteditor mit sicherem Titel/Dateinamen, Haupttext, Abschlussnotizen, Versionierung, Autosave und Charakterbezug,
- frei benennbare, validierte Songtextbereiche zusätzlich zu den Standardbereichen,
- exakte JSON-Songtext-Importvorlage in der Fehlerhilfe und als `vorlagen/songtext_import_vorlage.json`,
- Startordner-Validierung mit ausdrücklicher Zustimmung vor dem Erstellen und anschließender Schreibbarkeitsprüfung.

### Geändert
- Genres, Stimmungen, Stil, Stimme und Besonderheiten zerlegen Komma-Eingaben in einzelne bereinigte Datenbankwerte und verhindern Dubletten,
- Charakterfibel und Texteditor in Schnellkacheln, Navigation, Fensterregistry, Zoom/Theme und Accessibility integriert,
- Eingabe- und Auswahlfelder erhalten zentral einen kontrastierenden Theme-Hintergrund mit kontrastgeprüfter Schrift,
- Todo-Bestand wird idempotent um neun Projektmodule mit 48 separat abhakbaren Unteraufgaben ergänzt, ohne bestehende oder archivierte Aufgaben zu überschreiben.

### Schutz und technische Abnahme
- keine bestehenden Nutzerdaten gelöscht oder überschrieben,
- neue Charakter-/Textdaten werden atomar gespeichert,
- autonomes Updatemodul bewusst nur als Sicherheits-Backlog aufgenommen; kein blindes Selbstüberschreiben implementiert,
- synchronisierter PR-Head `9d9b608b55a72311d65d627dbe274ab400a2c79d` in Grundprüfung **#696** vollständig grün: **104 Logiktests**, **74 GUI-Tests**, **46 Release-Dateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`,
- PR #45 SHA-geschützt gemergt; Produkt-Main `f3fafe411f48a67e8eff83c07f7caf9e2ea753c7`,
- gemergter Main in Grundprüfung **#697** erneut vollständig grün; Restore-SHA-256 `25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04`,
- Version **0.17.0** technisch freigegeben; reale sichtbare Kubuntu-/Plasma-Wayland-Abnahme bleibt separat.

## 0.16.1 – 2026-09-10 – Codequalitäts-Nachhärtung (Iterationen 30–32)

### Iteration 30 – Log-Wartung
- Zeitermittlung pro Wartungsoperation auf einen UTC-Snapshot vereinheitlicht,
- Rotationsentscheidung als reine Logik getrennt,
- Quarantäne-JSON auf den zentralen atomaren JSON-Schreiber umgestellt,
- Archivsortierung robuster gegen parallel verschwundene Dateien gemacht,
- Grenzwert- und Zeitkonsistenzregressionen ergänzt.

### Iteration 31 – Fenster-Lebenszyklus
- wiederholte Dashboard-Fensterverwaltung in den generischen, typisierten `_open_managed_window()`-Helfer zusammengeführt,
- sichtbare Wiederverwendung, standardmäßige Neuerzeugung und bewusste Kalender-Hidden-Reuse-Semantik explizit erhalten,
- drei deterministische Lebenszyklus-Regressionen ergänzt.

### Iteration 32 – Managed-Window-Registry
- `_managed_window_registry()` als zentrale Quelle der aktuell verwalteten Dashboard-Fenster eingeführt,
- Fenstererkennung für Ctrl+Mausrad, Zoom-Verteilung und selektiven sichtbaren Refresh auf dieselbe Registry vereinheitlicht,
- Recovery, Todo und Kalender bleiben der bewusste automatische Refresh-Scope; Songeditoren behalten ihren speziellen Zoom-Adapter,
- drei GUI-Regressionen für Registry-Vollständigkeit, Zoom-Verteilung und Refresh-Semantik ergänzt.

### Schutz und Abnahme
- keine sichtbaren Texte, Layouts, Themes oder Bedienpfade verändert,
- keine Song-, Profil-, Todo- oder Kalenderdaten oder Speicherformate verändert,
- keine Backup-, Restore- oder Release-Fachlogik verändert und keine neue Abhängigkeit eingeführt,
- Iteration 30: Grundprüfung **#628** vollständig grün – 96 Logiktests, 56 GUI-Tests, 39 Release-Dateien, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `c45fa475055dfb1b5d3e5904321f4d967c96a3ea5d3f82bba46bdb6538ad574c`; PR #40 → Main `20a9106616e4f32677c271906f345f02652b7cdd`,
- Iteration 31: Grundprüfung **#633** vollständig grün – 96 Logiktests, 59 GUI-Tests, 39 Release-Dateien, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `8d6f15df599d92ad60be71fab18c171243cbdfbf5fb55e4d236d23cbec79819a`; PR #41 → Main `c4df362e8518acab07d4aac987ce08b5ff7e60b6`,
- Iteration 32: Grundprüfung **#638** vollständig grün – 96 Logiktests, 62 GUI-Tests, 39 Release-Dateien, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `64c3d081f652abcb29623375336c4d71b5ffd55ebce72e2c33cae64e83cef51b`; PR #42 → Main `a0032bc7977e21d830297828610d9b6d3ac68ea3`.

## 0.16.1 – 2026-09-10 – Präsentationspolicy und Architekturhärtung

### Geändert
- neue Qt-unabhängige `app/presentation_policy.py` als deterministische Klassifikation für Dashboard-Laptopmodus, breite Ansicht und Hochzoom ergänzt,
- Darstellungsgrenzen als benannte Policy-Konstanten zusammengeführt,
- unveränderlichen `PresentationState` für `wide`, `high_zoom`, `laptop_compact` und `restricted_navigation` eingeführt,
- `app/laptop_layout.py` auf die zentrale Policy umgestellt; bisherige private Helfer bleiben nur als Kompatibilitätsadapter,
- `app/navigation_ux.py` von der privaten Laptop-Hilfsfunktion entkoppelt und die bisher doppelte Hochzoom-Entscheidung entfernt,
- in der strengen Nachprüfung auch `app/ui_standards.py` an `WIDE_MIN_WIDTH_PX`, `HIGH_ZOOM_MIN_PERCENT` und die gemeinsame Zoomnormalisierung angebunden; Schwellen und Layoutverhalten bleiben unverändert,
- den eigenständigen Responsive-Breakpoint `compact < 1100 px` bewusst lokal belassen, da er eine andere Layoutklasse beschreibt,
- reine Grenzwerttests ohne QApplication/Eventloop für Referenz-Laptop, Großansicht, Breitengrenze, Hochzoom, Mindestgröße und Nicht-Dashboard-Fenster ergänzt,
- Release-Regression erweitert: jedes produktive `app/*.py`-Modul muss mit `release=true` im Manifest erfasst sein,
- Vollprüfung um Präsentationspolicy, neue Tests und Iteration-29-Dokumentation erweitert.

### Fehlerbehebung / Schutz
- erste Grundprüfung #598 deckte durch den neuen Release-Invariant unmittelbar auf, dass `app/presentation_policy.py` noch nicht im Release-Manifest stand,
- der fehlende Runtime-Eintrag wurde vor Freigabe ergänzt; damit kann derselbe Fehler bei späteren `app/*.py`-Modulen nicht mehr unbemerkt bleiben,
- alle 56 GUI-Tests waren bereits im ersten Lauf grün; der gefundene Fehler betraf ausschließlich Release-Vollständigkeit,
- die akademische Nachprüfung nach PR #37 fand noch rohe Duplikate der gemeinsam verwendeten Grenzen `1450` und `175` in `app/ui_standards.py`; diese wurden isoliert ohne Verhaltensänderung zentralisiert,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Laufzeitabhängigkeit eingeführt,
- sichtbare Nutzerführung und Kubuntu-26.04-/Wayland-Verhalten bleiben funktional unverändert.

### Abnahme
- korrigierter technischer Head `117aa0eee4e3422804506d9bc1c1fc50f75d4591` in Grundprüfung **#600** vollständig erfolgreich; Restore-SHA-256 `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`,
- vollständig synchronisierter 0.16.1-Head `306eb551234882401d98114182b51c2ecdbdfdcb` in Grundprüfung **#612** erneut vollständig erfolgreich: **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `78813816a492133dab8687112f80479bd7eff7309577ab2853833b9baf5b479f`,
- PR #37 anschließend ausschließlich für den geprüften Head per SHA-geschütztem Squash-Merge übernommen; resultierender Produkt-Main-Commit `608f7236f68161436b5d77e6e4c907ff6c1aa1a0`,
- isolierter Single-Source-of-Truth-Konsistenzhead `5d0eb33165bfe721a380912cd528981c51a88042` in Grundprüfung **#616** vollständig erfolgreich: erneut **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`; Restore-SHA-256 `f745cfd8ae287ecfe7b34340f695959317f7a19901dae3cee9131133d5f90c82`,
- PR #38 anschließend mit exaktem Head-SHA-Schutz per Squash-Merge übernommen; resultierender Main-Commit `e74d0ddc45258dc51926c94662ab23303f80e5f2`,
- Iteration 29 ist damit unter der strengeren Architekturdefinition technisch abgeschlossen; die reale sichtbare Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme bleibt ein separates Projektgate.

## 0.16.0 – 2026-09-10 – Kubuntu 26.04 / native Wayland-Unterstützung

### Geändert
- Kubuntu 26.04 LTS mit KDE Plasma Wayland als offizielles Linux-Zielsystem für die reale Endabnahme festgelegt,
- bisherige X11-only-Prüfung auf Wayland-Sitzung, `WAYLAND_DISPLAY`, KDE/Plasma und Ubuntu/Kubuntu-Basis 26.04 umgestellt,
- tatsächlichen Qt-Plattformnamen über `QApplication.platformName()` in die Abnahme aufgenommen; `xcb`/XWayland gilt nicht als nativer Wayland-Pass,
- `kubuntu_abnahme.sh` weist ausdrücklich erzwungenes `QT_QPA_PLATFORM=xcb`, `offscreen` und `minimal` für die reale Abnahme ab,
- neuen `scripts/wayland_smoke.py` für einen echten nativen Qt-Wayland-Fensterstart ergänzt,
- GitHub-Grundprüfung um einen isolierten headless Weston-Compositor und echten Qt-Wayland-Smoke erweitert,
- bisherige Offscreen-GUI-Regressionen parallel beibehalten,
- Wayland-/26.04-Regressionen für gültige und blockierte Sitzungen, erzwungenes X11, alten Distributionsstand und Reportstatus ergänzt,
- reale Sichtabnahme um Wayland-spezifisches Fenster-, Menü- und Eingabefokus-Verhalten erweitert.

### Bewusst unverändert / Schutz
- `schnellstart.sh` bleibt backend-neutral und erzwingt weder Wayland noch X11,
- X11 wird nicht künstlich aus der allgemeinen Laufzeit entfernt; es ist lediglich kein gültiger Pass für die offizielle Kubuntu-26.04-Wayland-Endabnahme,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- Weston ist ausschließlich CI-Testinfrastruktur und keine neue Nutzer-Laufzeitabhängigkeit.

### Abnahme
- technischer Head `a7f2c168ecc3f0a2310fbff874cea33d30793d25` in GitHub-Grundprüfung **#567** vollständig erfolgreich,
- finaler 0.16.0-Head `2536bd3183e39ad1566496a067b817dd3ad30b07` in Grundprüfung **#579** erneut vollständig erfolgreich,
- **86 Logik-/Regressionstests** und **56 PySide6-GUI-Tests** erfolgreich,
- nativer Qt-Wayland-Smoke unter isoliertem Weston in beiden vollständigen Abnahmen erfolgreich; Qt meldet Plattform `wayland`,
- Release-Manifest mit **38 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale Feature-SHA-256 `23792d1c96db0b0fd61eaf74630593fbbf37578b64c4f82fd1f6644d2efa103e`,
- GitHub-CI lief auf Ubuntu 24.04.4; die reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt deshalb zusätzlich erforderlich,
- PR #35 anschließend ausschließlich für den geprüften Head per SHA-geschütztem Squash-Merge übernommen; resultierender Produkt-Main-Commit `3b829e799536cc1464e760f77ac7c28295c6ea70`.

## 0.15.3 – 2026-09-10 – Menü-Übersicht und Laiennavigation

### Geändert
- linke Dashboard-Navigation auf eine klare Nutzerhierarchie umgestellt: fertige Wege zuerst unter `Direkt nutzbar`, geplante Wege getrennt unter `Noch nicht fertig`,
- `Songtexte`, `Genres & Vorgaben`, `Todo-Liste`, `Kalender` und `Fehlerhilfe (Recovery)` als direkte fertige Hauptwege priorisiert,
- redundanten sichtbaren Menüpunkt `Alle Bereiche · geplant` entfernt,
- zehn geplante Bereiche standardmäßig eingeklappt und über einen einzigen Schalter ein-/ausblendbar gemacht,
- geplante Bereiche bei Bedarf in `Kreativ & Inhalte`, `Dateien & Werkzeuge` und `Projekte` gruppiert,
- wiederholte `· geplant`-Zusätze aus den einzelnen Planungszeilen entfernt,
- Menütexte in `texte/registry.json` zentralisiert,
- `app/navigation_ux.py` als eigene wiederverwendbare Menüschicht ergänzt und in Start-, Runtime- und Release-Pfad eingebunden,
- gezielte GUI-Regressionen für Standardmenü, Auf-/Zuklappen, Laptopmodus, 175/200-%-Hochzoom, Rückkehr zur großen Ansicht und Accessibility ergänzt.

### Fehlerbehebung / Schutz
- erste CI-Läufe deckten zwei Qt-Synchronisationsrückfälle zwischen Planungsmenü und bestehendem Laptop-/Hochzoom-Layout auf,
- die finale Lösung leitet Einschränkungen direkt aus der aktuellen Geometrieprüfung des Laptopmodus ab und ist damit unabhängig von der Reihenfolge einzelner Qt-Ereignisse,
- keine Song-, Profil-, Todo- oder Kalenderdaten verändert,
- keine Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Abhängigkeit eingeführt,
- große Dashboard-Ansicht außerhalb der Menüstruktur bewusst nicht umgebaut.

### Abnahme
- korrigierter technischer Head `b129b47bb8123fc7ea49680f2fa921f457164c56` in GitHub-Grundprüfung **#540** vollständig erfolgreich,
- finaler 0.15.3-Head `9cd8101ba19c5e28b41fa7793d35860462d38864` in Grundprüfung **#554** erneut vollständig erfolgreich,
- **81 Logik-/Regressionstests**, **56 PySide6-GUI-Tests** und **38 Release-Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale SHA-256 `add4af04204e694427aa2332edea4136c2816e0c196676391a5763e044be3718`,
- PR #34 anschließend per SHA-geschütztem Squash-Merge übernommen; resultierender Main-Commit `e7027e57c3c8709263b73543fd2b01be84e6639d`.

## 0.15.2 – 2026-09-10 – Release- und Bericht-I/O-Härtung

### Geändert
- zentralen `app.atomic_io.atomic_publish_file()`-Schritt für bereits fertig erzeugte Dateien ergänzt: Datei-`fsync`, atomarer Replace, bestmöglicher Verzeichnis-`fsync` und Temp-Cleanup,
- Log-Quarantäne und bereinigte JSONL-Neuschreibung, Rückfall-Lernstatus sowie menschenlesbare Ereignis-/Wächterberichte auf den zentralen atomaren Textschreiber umgestellt,
- Startstatus und Kubuntu-Abnahmeberichte auf denselben zentralen Schreibvertrag umgestellt,
- Release-ZIP von festem `.zip.tmp` auf eindeutige Tempdateien sowie zentralen Prepared-File-Publish umgestellt,
- Release-SHA-256-Begleitdatei atomar geschrieben,
- Diagnose-ZIP auf denselben zentralen Publish-Schritt vereinheitlicht,
- direkt startbare Diagnose-, Startstatus-, Prozesswächter-, Kubuntu-Abnahme- und Release-Skripte gegen fehlenden Projektimport abgesichert,
- Vollständigkeitsprüfung um `app/laptop_layout.py` und Iterationsdokumente 22–26 ergänzt,
- gezielte Regressionen für Replace-Fehler, Altbestandsschutz, Temp-Cleanup und direkte Skriptstarts ergänzt.

### Bewusst unverändert
- Append-only Ereignislog und Projekt-Notiz bleiben Append-only,
- Song-, Profil-, Todo- und Kalenderdatenformate bleiben unverändert,
- vorhandene Backup-/Restore-Fachlogik bleibt unverändert; der bereits gehärtete Restore-ZIP-Pfad wird nicht unnötig refaktoriert,
- keine neue Produktfunktion und keine neue externe Abhängigkeit.

### Abnahme
- technische Grundprüfung **#503** vollständig erfolgreich; Restore-SHA-256 `c7ff7f7e107d815918e9d52a84302bd245baa19f301cb3d4730ee5acff4b0806`,
- finaler Version-/Evidence-Head `d386f9e848237ff400fc60c518f73645b6516cee` in Grundprüfung **#513** erneut vollständig erfolgreich,
- **81 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich,
- Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, finale SHA-256 `560b9d9ca46ec3e0964f03b385941782e18e892d734c1b5e208dd69c6d4b5bf3`,
- PR #31 anschließend per SHA-geschütztem Squash-Merge in `main` übernommen; resultierender Main-Commit `00513bbaaee124da1e04a963aa70ce9e4757108e`.

## 0.15.1 – 2026-09-09 – Laptop-Kompaktlayout

### Geändert
- reversiblen Laptop-Kompaktmodus ausschließlich für das Dashboard ergänzt,
- Aktivierung auf knappe Laptopfläche bei Fensterbreite unter 1450 px und 125/150 % Zoom begrenzt,
- redundante geplante Navigation und die beiden reinen Planungskarten in diesem Modus ausgeblendet,
- produktive Navigation, alle sieben oberen Modulkacheln, Zoom und Farbtheme bleiben erreichbar,
- Profilkopf und entbehrliche Hilfstexte werden platzsparend verkürzt,
- Rückkehr auf große Fenster stellt die vollständige Darstellung automatisch wieder her,
- bestehende zentrale Responsive-/Theme-/Hochzoom-Engine bewusst nicht umgebaut,
- Regression für 1366×768 bei 125 %, Navigationszustand, produktive Erreichbarkeit, 1594×926-Rückkehr und unveränderten 175/200-%-Hochzoom ergänzt.

### Fehlerbehebung / Schutz
- erste Grundprüfung #464 fand ein fehlendes Testdouble für den neuen Startimport und eine ungewollte Wiederherstellung der Planungskarten beim Übergang in den bestehenden Hochzoom,
- beide Ursachen minimal korrigiert, ohne den Funktionsumfang zu erweitern,
- keine Nutzerdaten, Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine neue externe Abhängigkeit eingeführt.

### Abnahme
- korrigierter Produktions-/Test-Head `d21799baa13562496b5e0821a17b1fb2c6cd89fe` in GitHub-Grundprüfung **#468** vollständig erfolgreich,
- **75 Logik-/Regressionstests** und **52 PySide6-GUI-Tests** erfolgreich,
- Release-Manifest mit **37 freigegebenen Betriebsdateien** erfolgreich,
- Headless-Start erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `9ace0f9d3311dbe98fa4875b9c1ed86ed51ef1d48ad50a41b6527be09c160b01`,
- der nachgezogene Evidence-Sync wird vor Merge nochmals als finaler PR-Head vollständig geprüft.

## 0.15.0 – 2026-09-09 – Barrierefreiheit und Farbthemes

### Hinzugefügt / verbessert
- vier zentrale, sitzungsweite Farbthemes `Amber`, `Türkis`, `Lila` und `Kontrast`,
- kompakter Theme-Schalter im Dashboard-Statusbereich; geöffnete Fenster wechseln gemeinsam und neu geöffnete Fenster übernehmen das aktive Theme,
- Hochkontrast-Theme mit schwarzem Hintergrund, weißem Text, gelbem Akzent und 3-px-Fokusrahmen,
- zentrale `Qt.StrongFocus`-Grundregel für interaktive Buttons, Eingaben, Auswahlfelder, Listen und Tabellen,
- automatische Accessible Names aus sichtbaren Beschriftungen/Platzhaltern und Accessible Descriptions aus Tooltips,
- Screenreader-Bezeichnung `Farbtheme auswählen` für den Theme-Schalter,
- automatische WCAG-Kontrastregression der Kernfarben aller vier Themes mit mindestens 4,5:1,
- Hochzoom-Statusbereich so angepasst, dass bei 175/200 % die entbehrliche Legende ausgeblendet werden kann, der Theme-Schalter aber erreichbar bleibt.

### Schutz / Abnahme
- Theme-Auswahl gilt bewusst nur für die laufende Sitzung und erzeugt keinen neuen Schreibpfad,
- keine Nutzerdaten, Speicherformate, atomaren Schreiber, Backup- oder Restore-Fachlogik verändert,
- keine externe Font- oder Theme-Abhängigkeit ergänzt,
- Grundprüfung #428 für den Produktions-/Test-Head `cf2d694564909de72dfc65891af23fc525e87cc9` vollständig erfolgreich,
- 75 Logik-/Regressionstests und 50 PySide6-GUI-Tests erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `76a861f4e2e2466906f0eee50f1d19339aa2ea5709c0a540cf0bb51b15a49d20`,
- nach Synchronisierung von Doku/MANIFEST/TODO/CHANGELOG bleibt die Safe-Merge-Regel bestehen: der finale PR-Head wird nochmals vollständig geprüft.

## 0.14.2 – 2026-09-09 – Zoom-Härtung 150–200 %

### Geändert
- Schriftzoom und Geometriezoom getrennt, damit 200 % Schrift nicht gleichzeitig Abstände, Radien und Mindesthöhen verdoppelt,
- Geometriewachstum selbst bei 200 % auf maximal 25 % begrenzt und zusätzliche Breitenreserve auf maximal 10 % reduziert,
- ab 175 % reversiblen Hochzoom-Modus eingeführt,
- redundante geplante Navigationseinträge und reine Planungskarten bei 175/200 % platzsparend ausgeblendet, während obere Modulkacheln und produktive Bereiche erreichbar bleiben,
- Profilsteuerung, Songbereichsliste und Songeditor-Splitter für Hochzoom kompakter verteilt,
- Rückkehr auf 100/125/150 % stellt den vollständigen Normalmodus automatisch wieder her,
- gezielte GUI-Regression für Schriftwachstum, Geometriegrenze, Hochzoom-Sichtbarkeit und Rückkehr in den Normalmodus ergänzt.

### Schutz / Abnahme
- keine Daten- oder Fachlogik verändert,
- Grundprüfung #419 einschließlich Vollprüfung und Restore-Gate erfolgreich,
- PR #26 sicher in `main` übernommen; resultierender Main-Commit `80544ad8cfd13452f35f9218247570f65beb8b05`.

## 0.14.1 – 2026-09-09 – Responsive Design und visuelle Härtung

### Geändert
- reales Dashboard, Songbibliothek und Songeditor anhand der Kubuntu-Screenshots auf Schriftwirkung, Breiten, Abstände, Kontraste und Platznutzung geprüft,
- zentrale Dark-Palette ruhiger aufgebaut und Amber von flächendeckenden Rahmen auf gezielte Akzente, Primäraktionen und Status reduziert,
- systemweite Sans-Serif-Schrift ohne zusätzliche Font-Abhängigkeit festgelegt,
- Schrift-Hierarchie, Innenabstände, Rundungen, Eingabehöhen, Fokusrahmen, Tabs, Scrollleisten und Splitter vereinheitlicht,
- aktive Navigation auf dunkle Auswahlfläche mit linker Akzentlinie umgestellt,
- responsive Breitenstufen für kompakte, normale und breite Fenster eingeführt,
- Sidebar, Dashboard-Suche, Profilfelder und Songbereichsliste passen sich abhängig von Fensterbreite und Zoom an,
- Songeditor-Splitter verteilt Arbeitsbereich und Gesamtvorschau dynamisch,
- Songbibliothek verteilt Tabellenbreite gezielt auf Titel und Tags und hält kurze Spalten inhaltsbezogen,
- drei GUI-Rückfälle aus Grundprüfung #368 korrigiert: Suchplatzhalter-Erwartung, alte Recovery-Beschriftung und zu starre Kartenbreitenannahme,
- Responsive-Regressionen für Dashboardbreiten, Zoom-Breitenreserve und Tabellen-Spaltenmodi ergänzt.

### Schutz / Abnahme
- keine Datenmigration und keine Änderung an Song-, Todo-, Kalender- oder Profildaten,
- atomarer Schreibweg, Backup- und Restore-Fachlogik bleiben unverändert,
- keine externe Schriftart und keine neue Abhängigkeit eingeführt,
- Grundprüfung #368 hatte bereits 75 Logiktests erfolgreich abgeschlossen; das Restore-Gate wurde nur wegen der drei GUI-Rückfälle übersprungen,
- GitHub-Grundprüfung **#385** vollständig erfolgreich: 75 Logik-/Regressionstests und 46 PySide6-GUI-Tests grün,
- Schreibfehler-Simulation, Headless-Start und Release-Manifest mit 36 Betriebsdateien erfolgreich,
- Vollprojekt-Restore erfolgreich mit Status `OK` und SHA-256 `c18e1ac25b8b2b43cf7c93d2c9dc8edf8b22dc9a521f3956c1d13d6cfae1d5de`,
- PR #24 wurde anschließend in `main` übernommen (`1f12951156a7ca86e5533f05a17ade4802c79543`).

## 0.14.0 – 2026-09-09 – Laien-UX-Konsistenz

### Geändert
- gesamtes produktives Projekt aus Sicht eines Nutzers ohne technisches Vorwissen auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft,
- Dashboard-Suche wahrheitsgemäß als Song-Suche bezeichnet und `Logout` durch `Programm beenden` ersetzt,
- technische Oberflächenbezeichnung `Entwicklerinfo` zu `Projekt-Notiz` vereinfacht, ohne das bestehende Speicherformat zu ändern,
- geplante Bereiche sichtbar mit `In Planung` und gestricheltem Zustand von fertigen Bereichen getrennt,
- echte Startwege zu Songtexte, Todo-Liste und Kalender in der Dashboard-Startkarte ergänzt,
- Erstnutzer-Sackgasse in der leeren Songbibliothek durch `＋ Neuen Song schreiben` geschlossen,
- Songbibliothek gegen stille Nicht-Reaktionen bei fehlender Auswahl gehärtet und Datumsanzeige auf deutsches Format umgestellt,
- Songeditor mit Drei-Schritt-Führung, verständlicher Speicheranzeige und Sicherheitsfrage vor dem Entfernen eines Songbereichs ergänzt,
- Wiederherstellung älterer Songversionen zusätzlich nach Vorschau bestätigungspflichtig gemacht; automatische Sicherung des aktuellen Stands bleibt bestehen,
- Todo, Kalender und Profilverwaltung mit eindeutiger Schrittfolge und nächstem sinnvollen Schritt vereinheitlicht,
- Recovery als `Fehlerhilfe (Recovery)` auf einfache Nutzerfragen ausgerichtet; technische Details bleiben standardmäßig verborgen,
- Schnellstart und grafische Startanzeige auf sechs verständliche Prüfschritte umgestellt,
- `ANLEITUNG_LAIEN.md` auf schnellen Einstieg und konkrete Arbeitsabläufe neu strukturiert,
- README auf den aktuellen Stand 0.14.0 synchronisiert und von doppelter Versionshistorie befreit.

### Prüfung / Schutz
- neuer Regressionstest `tests/test_layman_ux_gui.py` prüft wahrheitsgemäße Beschriftungen, sichtbare Planungszustände, Erstnutzer-Songstart, Nicht-Silent-Fail-Verhalten und Sicherheitsbestätigungen,
- Kernkontraste für normalen Text, Hinweistext und Akzent gegen den Hintergrund werden automatisiert auf mindestens 4,5:1 geprüft,
- Laien-UX-Test ist in `bash scripts/pruefen.sh --full` integriert,
- keine Datenmigration, keine Änderung der Song-/Todo-/Kalender-/Profilformate und keine Änderung der atomaren Speicher- oder Restore-Fachlogik,
- PR #23 wurde als Merge-Commit `47a6124061268843d05d98ddadcb90066cc0d851` in `main` übernommen; die anschließend ausgewertete Grundprüfung #368 zeigte drei GUI-Test-Rückfälle, die in 0.14.1 korrigiert wurden.

## 0.13.4 – 2026-09-09 – Repository-Hygiene

### Geändert
- unreferenziertes Root-Artefakt `ChatGPT Image 8. Sept. 2026, 02_16_14.png` mit 2.056.107 Bytes aus dem Repository entfernt,
- `.gitignore` um typische unsortierte ChatGPT-/Screenshot-Bildexporte ausschließlich im Repository-Root ergänzt,
- neuen Regressionstest `tests/test_repo_hygiene.py` ergänzt,
- Vollprüfung um automatische Kontrolle auf versionierte Laufzeit-/Temp-Artefakte, lokale Root-Screenshots und übergroße Root-Dateien erweitert,
- veralteten, nicht mergebaren PR #2 als überholt geschlossen.

### Schutz / Abnahme
- keine Anwendungs-, Speicher-, Backup-, Restore- oder UI-Fachlogik verändert,
- keine Nutzerdaten verändert oder gelöscht,
- reguläre Projektbilder in passenden Unterordnern bleiben weiterhin versionierbar,
- Grundprüfung #335 zeigte einen Restore-spezifischen Rückfall: der Git-Hygienetest erwartete im entpackten Restore irrtümlich `.git`,
- der Test wurde auf seinen tatsächlichen Geltungsbereich begrenzt; das Restore-Gate selbst blieb unverändert aktiv,
- Grundprüfung #337 war anschließend vollständig erfolgreich, einschließlich Vollprüfung und Restore-Gate,
- geprüfter Head `caefca0d51b158ac9a3c8cfedc6fb18e0899a580` wurde als PR #21 per Squash-Merge übernommen; resultierender Main-Commit `aa66dc5ed106e470a533c4dd9f65cf80b726b05c`.

## 0.13.3 – 2026-09-09 – Backup-/Restore-I/O-Konsistenz

### Geändert
- Backup-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- validiertes ZIP wird vor Veröffentlichung per Datei-`fsync` synchronisiert, atomar ersetzt und der Verzeichniseintrag bestmöglich synchronisiert,
- Tempdateien werden auch bei Fehlern bereinigt,
- SHA-256-Begleitdatei und RESTORE-JSON-Bericht verwenden `app.atomic_io.atomic_write_text`,
- Backup-Dateinamen enthalten Mikrosekunden gegen schnelle Mehrfachlauf-Kollisionen,
- `ZipFile.testzip()` wird explizit ausgewertet und meldet beschädigte Einträge,
- Restore-Regressionen für Altbestandsschutz bei Replace-Fehler und Temp-Cleanup ergänzt.

### Schutz / Abnahme
- Restore-Pfadprüfung, Manifestvergleich, Vollprüfung und Headless-Start bleiben unverändert,
- Append-only Ereignislogs und Nutzerdaten wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #315 war erfolgreich; Vollprüfung und Restore-Gate sind grün bestätigt,
- geprüfter PR-Head `ca6ff3a7eb29a6bbf237a81199a8a8764280784a` wurde als PR #19 per Squash-Merge in `main` übernommen; resultierender Main-Commit `72719acbef5be379c1340b5771962a81fb40fc85`.

## 0.13.2 – 2026-09-09 – Diagnose-I/O-Konsistenz

### Geändert
- Diagnose-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- ZIP-Datei wird vor Veröffentlichung per `fsync` synchronisiert und anschließend atomar ersetzt,
- bestmöglicher Verzeichnis-`fsync` und Temp-Cleanup bei Fehlern ergänzt,
- SHA-256-Begleitdatei auf `app.atomic_io.atomic_write_text` umgestellt,
- Diagnose-Dateinamen um Mikrosekunden ergänzt, damit schnelle Mehrfachexporte nicht kollidieren,
- gezielte Regression für eindeutige Exportnamen und Replace-Fehler ergänzt.

### Schutz / Abnahme
- bestehende Datenschutz- und ZIP-Inhaltsprüfungen bleiben unverändert aktiv,
- Append-only Ereignislogs, Nutzerdaten, Restore-Logik, Backup-Skript und sonstige Berichtsschreiber wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #294 war erfolgreich und führte sowohl `bash scripts/pruefen.sh --full` als auch `python3 scripts/iteration_restore.py` aus,
- damit sind Vollprüfung und Restore-Gate für den geprüften Produktionspatch grün nachgewiesen.

## 0.13.1 – 2026-09-08 – Prozess- und Schreibkonsistenz

### Geändert
- zentralen Produktions-Schreibweg `app/atomic_io.py` für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien eingeführt,
- feste `.tmp`-Dateinamen durch eindeutige Tempdateien im jeweiligen Zielordner ersetzt,
- Datei-`fsync`, atomaren `os.replace` und bestmöglichen Verzeichnis-`fsync` vereinheitlicht,
- pro Projektordner einen `QLockFile`-basierten Einzelinstanz-Schutz eingeführt,
- Todo-Termine auf dieselbe lokale, zeitzonenlose ISO-8601-Semantik wie Kalendertermine vereinheitlicht,
- ENOSPC-/EROFS-Simulation auf den echten Produktionsschreiber umgestellt,
- gezielte Prozesskonsistenz-Regressionstests ergänzt.

### Schutz / Fehlerbehebung
- ein zweiter schreibender Dashboard-Prozess wird kontrolliert beendet, bevor er Nutzerdaten oder Laufzeitlogs öffnet,
- der Prozesswächter behandelt den kontrollierten Mehrfachstart-Code 10 nicht als Absturz,
- ein Replace-Fehler erhält den vorherigen Datenbestand und hinterlässt keine Tempdatei,
- unterschiedliche Schreibversuche kollidieren nicht mehr über denselben Tempnamen,
- nicht unterstützter Verzeichnis-`fsync` erzeugt nach bereits erfolgreichem Dateiersatz keinen falschen Speicherfehler,
- beschädigte Profilbestände mit doppelten Werten werden nicht mehr still bereinigt, sondern klar abgewiesen,
- die erste CI-Prüfung deckte drei Rückfälle in Testimport, Qt-Testdouble und direktem Simulationsstart auf; alle wurden ursächlich behoben und in der folgenden Vollprüfung verifiziert.

## 0.13.0 – 2026-09-08 – Kalender und Erinnerungen

### Hinzugefügt
- eigenes PySide6-Kalendermodul unter `Planung → Kalender`,
- echte Tages-, Wochen-, Monats- und Jahresbereiche für den gewählten Kalendertag,
- Termine mit Titel, optionaler Notiz, Beginn und Ende,
- Erinnerungen zum Terminbeginn sowie 5/15/30/60 Minuten oder 1 Tag vorher,
- 30-Sekunden-Erinnerungsprüfung als Kind des laufenden Dashboards, auch bei geschlossenem Kalenderfenster,
- gezielte Logik- und GUI-Rückfalltests für Bereichsgrenzen, Mehrtagestermine, Termineingabe, Einmal-Erinnerung, Dashboardbetrieb und Zoom.

### Schutz
- Beginn und Ende verwenden lokale Rechnerzeit ohne erfundene Zeitzonenumrechnung,
- Ende muss nach Beginn liegen; ungültige Termine werden vor dem Schreiben abgewiesen,
- Kalenderdaten werden atomar unter `daten/kalender/termine.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- eine Erinnerung wird erst nach erfolgreicher Anzeige atomar als erinnert markiert,
- Wiedereintritt während einer geöffneten Erinnerung wird blockiert,
- bei vollständig beendetem Dashboard wird bewusst kein separater Hintergrunddienst gestartet,
- keine destruktive Terminlöschung in dieser Iteration,
- bestehende Todo-, Profil-, Song-, Recovery-, Referenz-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.12.0 – 2026-09-08 – Todo-Liste mit Termin und Archiv

### Hinzugefügt
- eigenes PySide6-Todo-Modul unter `Planung → Todo-Liste`,
- Aufgaben mit Pflicht-Titel, optionaler Notiz und optionalem Datum/Uhrzeit-Termin,
- getrennte Ansichten für aktive Aufgaben und Archiv,
- Abhaken verschiebt die vollständige Aufgabe ins Archiv und setzt einen Abschlusszeitpunkt,
- zentrale Zoom-/Schriftsteuerung gilt auch im Todo-Fenster,
- gezielte Logik- und GUI-Rückfalltests für Terminierung, Abhaken, Archiv und Zoom.

### Schutz
- aktive Aufgaben und Archiv liegen zusammen in `daten/todo/todo.json`, damit beim Abhaken kein Zwischenzustand zwischen zwei Dateien entstehen kann,
- Speicherung erfolgt atomar über Tempdatei, `fsync` und `os.replace`,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- Abhaken löscht keine Aufgabe; der Eintrag wird vollständig ins Archiv verschoben,
- ungültige Termine und leere Titel werden vor dem Schreiben abgewiesen,
- bestehende Song-, Profil-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.11.0 – 2026-09-08 – profilbasierte DB-Eingaben

### Hinzugefügt
- Profile `HardTechno`, `HipHop/Rap` und `Hörspiele` mit Startwerten,
- getrennte Kategorien Genres, Stimmungen, Stil, Stimme und Besonderheiten,
- PySide6-Profilverwaltung zum Anlegen von Profilen und Werten,
- Profilauswahl direkt in der Dashboard-Karte `DB-Eingaben`,
- sofortige Aktualisierung der Dashboard-Auswahlfelder nach Profiländerungen,
- gezielte Logik- und GUI-Rückfalltests für Profilisolation, Duplikate und Dashboardbefüllung.

### Schutz
- Startprofile liegen bis zur ersten eigenen Änderung nur im Programmbestand und schreiben nicht beim Start,
- eigene Profildaten werden atomar unter `daten/profile/db_profile.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen lässt die vorherige Datei unverändert,
- doppelte Werte werden ohne Beachtung der Groß-/Kleinschreibung abgewiesen,
- Entfernen eines Werts verlangt eine ausdrückliche Bestätigung,
- bestehende Song-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.10.2 – 2026-09-08 – Zoom und Schriftgrößensteuerung

### Hinzugefügt
- `Strg + Mausrad` für zentrale Zoom-/Schriftgrößenänderung,
- sichtbare `A−`-/`A+`-Schaltflächen mit Prozentanzeige in der Statusleiste,
- Weitergabe der Zoomstufe an Dashboard, offene Songeditoren, Songbibliothek und Recovery,
- gezielter PySide6-GUI-Rückfalltest für Mausrad, Zoomgrenzen und sichtbare Bedienung.

### Schutz
- bestehende Zoomstufen 100/125/150/175/200 % bleiben unverändert,
- kein zweites Schriftgrößensystem eingeführt,
- keine Nutzerdaten verändert,
- globaler Ereignisfilter wird beim Schließen des Dashboards wieder entfernt.

## 0.10.1 – 2026-09-08 – Kubuntu/X11-Endabnahme vorbereitet

### Hinzugefügt
- neuer Klickstart `kubuntu_abnahme.sh`,
- neuer PySide6-Abnahmeassistent `scripts/kubuntu_abnahme.py`,
- Vorprüfung auf Linux, echte X11-Sitzung und KDE/Plasma,
- echter SIGTERM-/Prozesswächtertest ausschließlich in Tempdaten,
- sichtbare Bestätigung für Referenzlayout, Tastaturfokus und Zoomstufen 100/125/150/175/200 %,
- TXT- und JSON-Abnahmeberichte unter `berichte/`,
- gezielte Tests für X11/KDE-Erkennung, Signalprobe und Berichtsstatus.

### Schutz
- Wayland oder fehlendes `DISPLAY` werden nicht still als X11 akzeptiert,
- der Signaltest verändert keine Song-, Versions- oder sonstigen Nutzerdaten,
- `OK` wird nur vergeben, wenn automatische Prüfungen und alle sichtbaren Bestätigungen erfolgreich sind,
- Offscreen-CI wird ausdrücklich nicht als reale Kubuntu/KDE-X11-Sichtabnahme gewertet.

## 0.10.0 – 2026-09-08 – PySide6-Referenzdashboard

### Geändert
- gesamte produktive Oberfläche einheitlich auf **PySide6 6.11.2** migriert,
- Dashboardtitel auf `Provoware-Datenbank-Dashboard 2026` gesetzt,
- Dashboard nach dem bereitgestellten Dark-Orange-Referenzentwurf neu strukturiert: kompakter Header, Schnellkachelleiste, einklappbare linke Navigation, schmale „Zuletzt bearbeitet“-Zeile, 2×2-Hauptkarten und Statusleiste,
- zentrale Qt/QSS-Standards für Farben, Abstände, Schriftgrößen, Fokus und Zoom eingeführt,
- Songeditor, Songbibliothek, Recovery-Zentrale und Startanzeige ebenfalls auf PySide6 migriert,
- Recovery aus der Startfläche entfernt und **genau einmal** als linker Navigationspunkt geführt.

### Schutz
- bestehendes Song-Textformat und alle Nutzerdatenpfade bleiben unverändert,
- Autosave, Fokusverlust-Speicherung, Versionierung, Restore-Sicherung, Favoriten/Status, Metadaten und Exporte bleiben erhalten,
- geplante noch nicht freigegebenen Dashboardbereiche verändern keine Daten,
- zusätzlicher Referenzlayout-Test prüft Kartenstruktur/-proportionen, Sidebarbreiten, Schnellkacheln, Dark-Orange-Akzent und exakt einen Recovery-Eintrag,
- produktive GUI-Dateien werden auf unerlaubte Tkinter-Reste geprüft,
- bestehende Logik-, Sicherheits-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Gates bleiben verbindlich.

## 0.9.1 – 2026-09-08 – CI-Wartung

### Geändert
- GitHub Actions Checkout von `actions/checkout@v4` auf **`v7.0.1`** aktualisiert.

### Schutz
- keine fachliche Funktion, Songdatei oder Laufzeitlogik verändert,
- vollständige bestehende Logik-, Tk-GUI-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Prüfung bleibt unverändert verbindlich.

## 0.9.0 – 2026-09-08 – Songbibliothek vervollständigt

### Hinzugefügt
- freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags,
- kombinierbare Filter nach Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten,
- Favoritenkennzeichnung im Editor und Favoritenfilter in der Bibliothek,
- Bearbeitungsstatus `Idee`, `Entwurf`, `Überarbeitung`, `Fertig`,
- Sortierung nach letzter Bearbeitung, Titel, Genre, Tags und Status,
- Gruppierung nach Genre, Tags und Status,
- Versionswiederherstellung aus der schreibgeschützten Vorschau heraus,
- gezielte Logik- und Tk-GUI-Tests für Suche, Filter, Gruppierung, Status/Favorit und Restore.

### Schutz
- ältere Songdateien ohne Status/Favorit bleiben lesbar und erhalten nur sichere Standardwerte,
- Filtern, Sortieren und Gruppieren sind reine Ansichtsoperationen,
- vor jeder tatsächlichen Versionswiederherstellung wird der aktuelle Song erneut als Versionsstand gesichert,
- die Restore-Funktion akzeptiert nur die direkte Arbeitsdatei und den zugehörigen `.versionen/<Titel>/`-Pfad,
- fremde Versionspfade werden vor Schreibzugriff abgewiesen,
- Arbeitsdatei und Sicherungsstand werden atomar geschrieben,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.8.0 – 2026-09-08 – Songbibliothek und Versionsverwaltung

### Hinzugefügt
- Songbibliothek mit Titel, Genre, letzter Bearbeitung und Versionsanzahl,
- direktes Öffnen vorhandener Songs per Doppelklick, Enter oder Schaltfläche,
- bis zu fünf zuletzt bearbeitete Songs als Schnellkacheln im Dashboard,
- Song-Metadaten Stimmung, Stil, Stimme, Besonderheiten und Tags,
- automatische Versionsschnappschüsse vor geänderten Überschreibungen,
- schreibgeschützte Vorschau älterer Versionsstände,
- Exporte als TXT, Markdown, JSON und Nur-Songtext-TXT,
- Rückwärtslesen der bisherigen 0.7.0-Textdateien,
- gezielte Logik- und Tk-GUI-Tests für Bibliothek, Metadaten, Versionen, Kacheln und Exporte.

### Schutz
- das bestehende `.txt`-Arbeitsformat bleibt kanonisch; kein paralleles internes Songformat,
- identische Speicherungen erzeugen keinen Versionsmüll,
- Versionsstände werden getrennt unter `.versionen/` gesichert und nicht still überschrieben,
- Versionsansicht ist zunächst schreibgeschützt,
- Exporte verändern weder Arbeitsdatei noch Versionshistorie,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.7.0 – 2026-09-08 – Dashboard-Schnellspeicher und Songtexteditor

### Hinzugefügt
- einzeilige Entwickler-Schnelleingabe im Dashboardheader mit Enter- und Schaltflächenbestätigung,
- append-only Speicherung mit Zeitstempel in `Entwicklerinformation.txt`,
- Songtexteditor mit Titel, optionalem Genre, optionalem Sonstiges und Live-Vorschau,
- auswählbare Bereiche Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken und Instrumental,
- atomare Speicherung unter `daten/songtexte/<Titel>.txt`,
- Autosave alle fünf Minuten sowie bei Fokusverlust und beim Schließen,
- Logout-Schaltfläche mit Speichern aller offenen Songeditoren vor Sitzungsende,
- gezielte Logik- und Tk-GUI-Tests für Schnelleingabe, Speicherpfad, Bereichswechsel, Autosave und Logout.

### Schutz
- Schnellinfos überschreiben vorhandene Informationen nicht,
- Songdateien werden über eine temporäre Datei atomar ersetzt,
- ein Titelwechsel löscht keinen vorherigen Songstand,
- Logout wird gestoppt, wenn ein offener Songtext nicht gespeichert werden kann,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.6.0 – 2026-09-08 – Debug- und Recovery-Zentrale

### Hinzugefügt
- kombinierbare Filter nach Schweregrad und Bereich,
- Ereignisdetails per Doppelklick, Enter oder Schaltfläche,
- Wiederholungszähler und dauerhaft gespeichertes erstes Auftreten,
- zentrale Zoomstufen 100/125/150/175/200 Prozent,
- standardmäßig eingeklappte technische Details,
- gefahrlose `ENOSPC`-/`EROFS`-Simulation ohne echten Datenträgerverbrauch,
- automatisierte Tk-GUI-Prüfung für Tastatur, Fokus, Detailansicht und Zoom.

### Bedienung
- `F5` aktualisiert,
- `Ctrl++` und `Ctrl+-` ändern die Anzeigegröße,
- `Ctrl+0` setzt auf 100 Prozent,
- `Escape` schließt Detailfenster,
- interaktive Filter, Tabelle und Schaltflächen sind in der Fokusreihenfolge.

### Schutz
- Schreibfehlersimulation arbeitet ausschließlich in temporären Testpfaden,
- vorhandener Bestand muss bei simuliertem Fehler unverändert bleiben,
- ohne echte Tk-Sitzung wird die GUI-Prüfung nicht als bestanden gewertet,
- vorhandene Restore-, Diagnose-, Redaktions- und Wächter-Gates bleiben aktiv.

## 0.5.0 – 2026-09-08 – Diagnose- und Logging-Härtung

### Hinzugefügt
- Größen-/Altersrotation für das Ereignislog mit maximal fünf Archiven,
- Quarantäne beschädigter JSONL-Zeilen mit bereinigter Beweiskopie,
- datenschutzgeprüftes Diagnosepaket mit SHA-256,
- eigenes `ENDE`-Ereignis bei kontrolliertem Programmabschluss,
- gezielte Tests für Rotation, Quarantäne, Diagnoseexport und normales Programmende.

### Schutz
- beschädigte Logzeilen werden nicht mehr still verworfen,
- gültige Logzeilen bleiben beim Bereinigen atomar erhalten,
- Diagnosepakete enthalten nur bereinigte Textkopien und keine unveränderten Rohprotokolle,
- Datenschutzprüfung läuft unmittelbar vor ZIP-Übernahme erneut,
- vorhandene Restore-, Headless- und Wächter-Gates bleiben aktiv.

## 0.4.0 – 2026-09-08 – Recovery-Härtung

### Hinzugefügt
- vollständige Iterations-ZIP-/Restore-Kette mit SHA-256, sicherem Entpacken, Manifestvergleich, Vollprüfung und Headless-Start,
- fensterlose Startabnahme über `python3 -m app.main --headless-check`,
- separate Prozesswache `scripts/process_watch.py`,
- zentrale Log-Bereinigung `app/redaction.py`,
- gezielte Sicherheits-, Wächter- und Restore-Tests,
- sechsten Start-Checkpoint für Prozesswache/Headless-Gate,
- CI-Restore-Gate auf jedem Push und Pull Request.

## 0.3.0 – 2026-09-08 – Regression, Start, Standards und Release
- `REG-LOG-001` behebt `recent(0)`.
- globale UI-Standards, Start-Checkpoints und manifestgesteuerter Releasefilter ergänzt.
