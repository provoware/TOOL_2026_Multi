# Iteration 41: lokale Leistungsdiagnose

Stand: 18.10.2026 · Version 0.18.1

## Ziel und Scope

Den nächsten ausführbaren Punkt der Todo-Liste umsetzen: lokale Start-/Modulladezeiten, zentrale Text-/JSON-Schreibzugriffe und unveränderte gültige Speicherversuche messen; Vorschau und Export in der bestehenden Hilfe. Keine automatische Datenübertragung, keine Nutzinhalte und kein zweiter Fehlerlogger. Basis ist der vollständig geprüfte Quellbaum von PR #84, nach dessen genehmigtem Merge main `45c24966178dcc31266f6cdb71dbd7bd983b9a41`.

Plan: 1. Opt-in und begrenzte Aggregate. 2. Vorhandene zentrale Wege instrumentieren. 3. Bestehende Hilfe um Übersicht und Exportvorschau ergänzen. 4. Negativtests, Nachbarprüfungen, Informationsdateien und GitHub-Prüfung.

## Bedienung

**Hilfe & Fehlerhilfe → Leistung & Verbesserung** öffnen. „Lokale Leistungsmessung einschalten“ ist zunächst nicht ausgewählt. Die Wahl wird lokal gespeichert. Bei aktivierter Messung ab nächstem Start wird der Aufbau des Dashboards bis zur ersten Ereignisschleife erfasst; ein bereits vergangener Start wird nicht nachträglich geschätzt.

Aufbewahrung: 1–30 Tage, Vorgabe 30. Berichtszeitraum: letzte 1–30 Tage. Die Gruppen Ladezeiten, Dateischreibzugriffe und Speicherversuche lassen sich einzeln abwählen. Übersicht und JSON-Vorschau enthalten dieselbe Auswahl. Export erfolgt ausschließlich nach Dateiauswahl als TXT oder JSON; nichts wird hochgeladen.

Ausschalten beendet neue Messungen sofort, behält aber vorhandene Tagesaggregate. „Alle Leistungsdaten löschen und Messung ausschalten“ fragt nach Bestätigung und entfernt nur den zusätzlichen Leistungsbestand; Arbeitsdaten und vorhandene Fehlerprotokolle bleiben erhalten. Die Einstellungsdatei hält danach ausdrücklich „aus“ fest.

## Datenmodell und Messgrenzen

Erlaubt sind ausschließlich feste Operations-/Bereichskennungen, numerische Programmversion, lokales Tagesdatum und numerische Zähler. Pro Gruppe werden Anzahl, Fehler, unveränderte Versuche, logische Bytes, Gesamtdauer, Maximum und begrenzte Laufzeitklassen gehalten. Keine Rohereignisse, Titel, Texte, Suchbegriffe, Zwischenablageinhalte, Dateipfade, Nutzernamen oder Exceptionmeldungen werden gespeichert. Es gibt keine eindeutige Installationskennung.

Messwerte bleiben zunächst im Speicher. Der Programmstart bindet einen 60-Sekunden-Timer und einen abschließenden Flush beim normalen Beenden ein. Die Statistikdatei ist auf 2 MiB, die Aufbewahrung auf 30 Tage und Tagesgruppen auf 128 begrenzt. Statistik- und Konfigurationsschreiben sind von ihrer eigenen Messung ausgeschlossen. Exportierte Leistungsberichte werden ebenfalls nicht als neue Arbeitszugriffe gezählt.

Die Datei `logs/leistung/statistik.json` wird über den vorhandenen atomaren Writer geschrieben. `daten/ui/leistung.json` hält nur Ein-/Ausschalten und Aufbewahrung fest. Fehler beim Speichern von Messwerten blockieren keine Arbeitsdateien; ausstehende Messwerte bleiben bis zu einem späteren Versuch im Speicher. Bei einem Absturz können bis zu 60 Sekunden ungesicherte Statistik fehlen. Beschädigte Bestände werden nicht still ersetzt; zunächst bleibt die Erhebung aus und die Oberfläche erklärt die ausdrückliche Löschmöglichkeit.

`file.write` zählt jeweils einen Versuch des zentralen Text-/JSON-Writers einschließlich vorheriger Vorbereitung und atomarem Publish. Unterliegende fsync-/Replace-Schritte und Bytes auf einer SSD werden nicht als zusätzliche Arbeitsspeicherungen ausgegeben. Binäre Release-Publish-Vorgänge außerhalb dieses Writers gehören nicht zu dieser Zählung.

`save.attempt` zählt nach erfolgreicher fachlicher Validierung gültige Speicherversuche in Buchwerkstatt, Textbuttons und allgemeinem Texteditor. „Unverändert“ stammt aus dem bereits vorhandenen Vergleich im Speicher; dafür wird keine zusätzliche Datei gelesen. Die Speicherung wird durch diese Messung nicht übersprungen. Fehler der tatsächlichen Dateioperation erscheinen getrennt unter `file.write`.

`module.open` misst den bestehenden gemeinsamen Fenster-Öffnungsaufruf, einschließlich Wiederanzeigen. Die feste Bereichszuordnung erfolgt anhand bekannter Fensterklassen; unbekannte Klassen werden als „Sonstiges“ zusammengefasst. Das Ende des Aufrufs beweist keinen vollständig dargestellten Bildschirm. `archive.load` misst Lesen und Prüfung der beiden neuen Modulbestände.

Ab 20 Beobachtungen zeigt die Auswertung grobe Median-/95%-Grenzen aus festen Laufzeitklassen; unterhalb davon ausdrücklich keine belastbare Verteilungsbewertung. Es handelt sich um Klassengrenzen, nicht um erfundene exakte Perzentile.

## Bewusst noch offen

Automatische Unterscheidung von Kalt-/Warmstart, getrennte Datenmengengruppen, CPU/RAM, Cachegrößen und Cachetreffer, physische Datenträgerzugriffe sowie Nutzung anderer Anwendungen werden nicht ermittelt. Vergleichbare Zielrechner-Benchmarks müssen den Zusatzaufwand und die geplante 1%-Zielgröße erst belegen; diese Iteration behauptet keine entsprechende Leistungsgarantie.

Die realen Kubuntu-/Plasma-Prüfungen und eine Wirksamkeitsbewertung nach mehreren vergleichbaren Entwicklungsiterationen bleiben offen. Diese Punkte sind durch eine einzelne Headless-Entwicklungsumgebung nicht ersetzbar.

## Lokaler Prüfnachweis

Vollprüfung nach Korrektur: **200 Logiktests, 148 GUI-Tests, 67 freigegebene Betriebsdateien, Headless-Start erfolgreich**. UI-Shadow-Profil `pr`: **8 Matrixfälle, 24 Fenster, 0 Fehler, 0 Warnungen**. Das Shadow-Gate umfasst die bestehenden Dashboard-/Songfenster; den neuen Hilfe-Reiter prüfen zusätzlich die gezielten GUI-Tests bei 100/150/200 %. Nativer Wayland-Start, Restore und ZIP-Erzeugung werden zusätzlich im GitHub-Lauf geprüft; dessen Ergebnis wird am PR dokumentiert.

## Entwicklungsreview und nächster Schritt

Die neue Ausbaustufe verwendet den vorhandenen atomaren Writer, Modul-Exportschutz, Fenster-Lebenszyklus, Textregistrierung und Hilfebereich. Drei kleine Laufzeitmodule ohne zusätzliche Abhängigkeiten halten Erfassung, Auswertung und Oberfläche getrennt. 16 neue Tests prüfen Verhalten und Schutzgrenzen; 39 gezielte neue und benachbarte Tests bestanden lokal. Der erste vollständige Lauf fand einen veralteten Start-Testdouble: Der neu benötigte Qt-Timer war nicht nachgebildet. Der Testdouble wurde ergänzt; die Produktlogik wurde dafür nicht abgeschwächt. Das ist ein echter zusätzlicher Prüflauf, dessen Ursache festgehalten bleibt.

Ein begrenzter lokaler Mikrobenchmark (drei rotierte Durchgänge mit jeweils 100 atomaren Schreibvorgängen à 4096 UTF-8-Bytes) ergab Medianwerte von rund 0,149 ms ohne Instrumentierung, 0,149 ms ausgeschaltet und 0,524 ms eingeschaltet. Die eingeschaltete Messung kostete in diesem Versuch zusätzlich etwa 0,375 ms je Schreibvorgang, relativ rund 251 %. Die wenigen Durchgänge schwankten stark; dies ist weder ein belastbarer Anwendungsbenchmark noch ein Kubuntu-/SSD-Nachweis. Das 1%-Ziel ist damit ausdrücklich **nicht nachgewiesen**. Eine zwischenzeitliche Vereinfachung der logischen Pfadzuordnung liefert aus diesen Messungen keinen belegten Geschwindigkeitsgewinn.

Qualitätsbewertung: Schutz- und Fehlerwege sind konkret geprüft, Produktivdaten bleiben getrennt, keine neue Bibliothek und keine automatische Übertragung. Effizienzbewertung: vorhandene Infrastruktur wird wiederverwendet; die eingeschaltete Erfassung braucht vor breiter Aktivierung bessere Messungen. Keine pauschalen Qualitätsnoten oder Verbesserungsprozente ohne Vergleichsbasis. Keine vorsorglichen Caches, zusätzlichen Frameworks oder Wiederholungsprüfungen ohne neue Ursache.

Fünf Folgevorhaben:
1. **Priorisierte Empfehlung:** reproduzierbare Zielrechner-Messung mit ausgeschalteter/eingeschalteter Erfassung und identischer Arbeitsmenge; erst danach gezielt optimieren.
2. Kalt-/Warmstarts und feste Datenmengengruppen getrennt bewerten.
3. Nur tatsächlich vorhandene app-eigene Caches mit Größe, Treffern und Begrenzung erfassen.
4. Reale Kubuntu-/Plasma-Bedienung samt Zwischenablage und Wörterbuch abnehmen.
5. Über mehrere vergleichbare Iterationen Fehlerwiederholungen, Prüfläufe je abgenommenem Paket und nachgewiesene Wirksamkeit einer Regeländerung auswerten.

Der nächste abgegrenzte Entwicklungsauftrag sollte ausschließlich den Benchmarkaufbau betreffen: ein kleines Entwicklerscript und dokumentierte Messbedingungen, keine neue Nutzerfunktion. Erwartetes Volumen: wenige Dateien, keine Abhängigkeiten; genaue Änderungen erst nach Bestandsprüfung. Der Lernkreislauf bleibt: Befund → reproduzierbare Ursache → kleinste Korrektur → passende Prüfung → dokumentierte Wirkung. Neue Ideen bleiben in der Warteschlange.

GitHub-Prüfung, geprüfter Head, Änderungsvolumen und ZIP-Artefakte werden am zugehörigen Pull Request dokumentiert. Eine reale Sichtabnahme und längerfristige Wirksamkeitsmessung bleiben gesondert offen.
