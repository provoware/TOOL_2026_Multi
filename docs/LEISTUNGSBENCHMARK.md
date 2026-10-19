# Iteration 43 – Diagnose-Zusatzaufwand reproduzieren

Basis: d1ee488, Version 0.18.2. Lieferung lokal im isolierten Branch `performance-benchmark`; keine automatische Veröffentlichung. Sicherungspunkt ist der unveränderte Ausgangscommit. Scope: Entwicklerscript, Schutztests, Manifest und Informationsdateien. Produktcode, persönliche Daten und Prüfgrenzen bleiben unverändert.

1. Identische Schreibarbeit in drei Varianten mit wechselnder Reihenfolge messen.
2. Inhalte, Zähler, Isolation und Wiederherstellung des aktiven Trackers prüfen.
3. Ergebnisse und Grenzen dokumentieren, Grundprüfung und vollständige Sicherung erstellen.

Auf dem gewünschten Datenträger ausführen:

```bash
python3 scripts/leistungsbenchmark.py --rounds 9 --writes 100 --bytes 4096 --temp-parent /pfad/zum/testordner > benchmark.json
```

Der Testordner muss existieren. Das Script erzeugt darin einen eigenen temporären Unterordner und entfernt nur diesen. JSON wird auf Standardausgabe ausgegeben. Bei der Umleitung einen neuen Dateinamen wählen. Kein Test greift auf den persönlichen Datenbestand zu. Maximal 60 Runden, 10000 Schreibvorgänge und 1 MiB je Schreibvorgang. Jeder Fehler bricht ab; es gibt keine Reparaturschleife.

Verglichen werden der bestehende interne atomare Writer ohne Messwrapper (`baseline`), der öffentliche Writer mit ausgeschalteter Diagnose und derselbe mit eingeschalteter Diagnose. Jede Variante erhält dieselbe UTF-8-Bytezahl und einen ungemessenen Warm-up. Nach jeder Serie wird genau einmal die Statistik gesichert; diese Flush-Zeit wird separat und zusätzlich im Gesamtwert ausgewiesen. Der echte Timer läuft hier nicht. Rohwerte bleiben erhalten. Der Median der Gesamtzeiten bildet die Grundlage der relativen Mehrkosten gegenüber baseline.

Lokaler Entwicklungsversuch: 9 Runden, jeweils 100 Schreibvorgänge mit 4096 Bytes. Median einschließlich Flush: baseline 9,941 ms, ausgeschaltet 10,578 ms, eingeschaltet 21,620 ms. Relative Mehrkosten: 6,41 % und 117,48 %. Das sind synthetische Warm-Schreibvorgänge in der Cloud; keine Anwendungs-, Kaltstart-, GUI-, SSD- oder Kubuntu-Abnahme. Das 1%-Ziel ist nicht belegt. Keine Optimierung wird allein aus diesem Versuch behauptet.

Die JSON-Ausgabe enthält Python-/Systemversion, Zeit, Ausgangs-HEAD und Dirty-Status. Für belastbare Vergleiche denselben geprüften Quellstand, Datenträger, Energiezustand und dieselbe Arbeitsmenge verwenden; Hintergrundlast dokumentieren. Wiederholungen nur mit konkretem Vergleichszweck. Einzelne kleine Prozentunterschiede nicht ohne Streuungsbewertung interpretieren.

Abnahmekriterien: drei Varianten vollständig, identische Inhalte, exakt erwartete Messzähler, keine verbleibenden Testdateien, vorheriger Tracker wiederhergestellt, Arbeitsgrenzen vor dem ersten Schreibzugriff geprüft. Zwei neue Schutztests und zwölf vorhandene Diagnosetests bestanden.

Fortschritt: 3 erledigte Entwicklungspunkte, 1 offene Zielrechnermessung: `███████░░░`.

Fünf Folgevorhaben: (1) priorisiert: denselben Benchmark auf dem Zielrechner ausführen; (2) erst anhand dieser Werte den bestätigten Engpass optimieren; (3) Kalt-/Warmstart gesondert planen; (4) reale Kubuntu-Sichtabnahme abschließen; (5) vergleichbare Entwicklungsiterationen auswerten. Nächste Iteration: Zielrechner-Ergebnis bewerten, voraussichtlich ein Messbericht; Codeänderungen erst nach bestätigtem Befund.

## Ergänzung: Datenmengengruppen und neue Prozesse

`python3 scripts/ladebenchmark.py --rounds 3 --repeats 10` erzeugt ausschließlich synthetische Buchbestände mit 1, 25 und 100 Büchern à 4096 Zeichen Kapitelinhalt. Für jede Gruppe startet es neue Python-Prozesse und unterscheidet erstes Lesen und wiederholtes Lesen im selben Prozess. Prozess-Gesamtzeit (einschließlich Imports und aller Lesevorgänge) steht getrennt von den einzelnen Archivladezeiten. Jeder Prozess hat 30 Sekunden Zeitgrenze, insgesamt maximal 20 Prozesse je Gruppe und 100 Wiederholungen. Temporäre Bestände werden entfernt.

Diese Messung nutzt den echten Bucharchiv-Lader einschließlich Validierung. Der Betriebssystem-Dateicache wird nicht geleert; gerade erzeugte Daten können bereits darin liegen. Deshalb heißen die Zustände `first_read` und `repeated_read`, nicht Betriebssystem-Kaltstart. Dashboardaufbau und Erstinstallation sind nicht enthalten. Der vollständige echte Kalt-/Warmstart bleibt separat offen.

Im Buch-/Archivlader gibt es keinen app-eigenen Cache. Trefferrate und Cachegröße sind dort nicht anwendbar und werden nicht als null gemeldet. Es wurde kein Cache allein zum Erzeugen einer Kennzahl hinzugefügt. Künftige reale Caches benötigen eigene messbare Verträge.

Lokaler Nachweis: drei Durchgänge je Größenklasse und zehn Wiederholungen je Prozess vollständig ausgeführt. Zwei Schutztests prüfen reale Unterprozesse, Datenklassen, Isolation und feste Arbeitsgrenzen. Keine Aussage über Zielrechnerleistung oder eine Effizienzverbesserung.
