# Erweiterung 40: Textbuttons und Buchwerkstatt

Stand: 18.10.2026 · Version 0.18.0 · TOOL_2026_Multi · provoware/TOOL_2026_Multi

## Ziel und Sicherungspunkt

Ein Hauptziel: zwei einfach bedienbare Kreativmodule auf einer gemeinsamen, wiederverwendbaren Modulbasis ergänzen. Der GitHub-Änderungsantrag basiert isoliert auf `f9f59fbaca5a36d8b15e0c9a3d5e9878fa827243`. Die zuvor vorgefundenen lokalen Hilfe-/Theme-Änderungen sind im ursprünglichen Arbeitsordner erhalten und nicht in diesen Änderungsantrag aufgenommen. Die neuen Module wurden gezielt auf die vorhandene Dashboard-Struktur portiert. Zugriff über obere Kacheln, Navigation oder Strg+Alt+T / Strg+Alt+B.

Nummerierte Planung: 1. Bestand und Regeln prüfen. 2. Archiv-/Bedienbasis und Textbuttons ergänzen. 3. Buchwerkstatt ergänzen. 4. Gezielt und vollständig prüfen, dokumentieren und paketieren. Verbotener Scope: Änderungen bestehender Nutzerdaten, neue Netzwerkdienste, Überschreiben vorgefundener Arbeit und ungeprüfte Veröffentlichung auf main.

## Umsetzung und Abnahmeziele

1. Textbuttons: Workflow-Reiter Coding, Schreiben, Prompting, Linux und eigene Bereiche; Kategorien, Titelsuche und Inhaltssuche.
2. Zwischenablage: unverändert gespeicherte Fragmente, Einfügen unter den drei Textfeldern, Platzhalterabfrage mit Abbruchschutz und eigener erfolgreicher Kopierrückmeldung.
3. Darstellung: sechs benannte Farboptionen einschließlich Standard, drei Größen, ein bis drei Spalten abhängig vom Platz und gespeicherte Reihenfolge pro Kategorie.
4. Unterversionen: Variantenfamilie mit stabiler Kennung und fortlaufender Versionsnummer; Original bleibt erhalten. Gleicher Text führt zu einem ausdrücklichen Variantenangebot.
5. Monatsstatistik: lokale Monatszähler je Button, TXT-Bericht, getrennte Monate; importierte Kopien zählen ab null. Keine Beobachtung anderer Programme.
6. Buchwerkstatt: fünf Vorlagen einschließlich leerer Vorlage, Kapitel und Unterkapitel (bis acht Ebenen), Reihenfolge, Entfernen mit Bestätigung, Kapitelstatus, Zielgruppe und getrennte Notizen.
7. Schreibwerkzeuge: passende Textbausteine für Hörspiel, Satire, Sachtext, Tutorial; zentrale Charakterfibel; Wortzahl / grobe Sprechzeit; neue Fassungen; Markdown-/TXT-Manuskript ohne private Notizen; Speichern per Strg+S und jede Minute bei betitelten Änderungen.
8. Gemeinsame Standards: zwei eigene Fenster, zentrale Themes und Zoom, zugängliche Eingaben, F1-Kontexthilfe, scrollbare Bereiche, responsive Kopfzeile, atomare Speicherung, geprüfter Modulimport mit Vorschau und Ergänzung als Kopien, ungespeicherte Änderungen auch beim Dashboard-Beenden geschützt; optionale lokale Rechtschreibprüfung.

Die vorhandenen Module und deren Dateiformate werden weiterverwendet. Die neue gemeinsame Archivbasis wird von den beiden neuen Modulen genutzt; ein pauschaler Umbau aller älteren Modularchive ist nicht Bestandteil dieser Änderung.

## Daten- und Fehlergrenzen

`app/module_archive.py` verwendet die bestehende zentrale atomare Speicherung. Ein Archiv ist eindeutig als `provoware.module`, Modul und Schema 1 gekennzeichnet. Laden, Import und Speicherung validieren den vollständigen Kandidaten, bevor Nutzerdaten ersetzt werden. Maximal 10 MB je Bestand / Eingabe; bis 5000 Buttons, 100 Workflows, 500 Bücher und 2000 Kapitel je Buch. Ungültige Kennungen, doppelte IDs, unbekannte Optionen, negative Zähler, fehlende Eltern und Hierarchiekreise werden abgewiesen. Exportziele dürfen weder interne Projektdateien noch Arbeitsdaten ersetzen; auch aufgelöste symbolische Links werden geprüft. Importiert wird erst nach Dateiauswahl, vollständiger Prüfung und Vorschau; bestehende Einträge werden nicht überschrieben. Wiederholter Import legt zusätzliche Kopien an.

Zwischenablage und Dateispeicherung sind zwei getrennte Betriebssystemaktionen. Scheitert allein die Statistik nach erfolgreichem Kopieren, wird dies ausdrücklich gemeldet. Gezählt wird eine Übernahme in die Qt-Zwischenablage; eine spätere Einfügung in andere Programme ist nicht messbar. Ein Absturz zwischen Kopieren und Zählerspeicherung kann daher einen Kopiervorgang ungezählt lassen.

Die Rechtschreibprüfung verwendet optional `aspell` mit `aspell-de`, ohne Shell oder Netzübertragung und mit fünf Sekunden Zeitlimit. Sie zeigt unbekannte Wörter zur manuellen Korrektur. Namen / Fachbegriffe können korrekt sein. Fehlende Wörterbücher werden erklärt; sie blockieren weder Schreiben noch Kopieren.

## Prüfnachweise

Die erste lokale Prüfung des ursprünglichen erweiterten Arbeitsordners umfasste 196 Logik- und 151 GUI-Tests. Diese Zahlen gehören zum damaligen lokalen Gesamtstand, nicht zum isolierten PR. Nach der Portierung wird der isolierte Stand separat vollständig geprüft. Der GitHub-Arbeitsablauf prüft denselben Commit einschließlich nativem Wayland-Start, UI-Shadow-Evidenz, Restore und ZIP-Erzeugung. Ein echter Plasma-Bildschirm bleibt eine getrennte Prüfung. Es wird kein Erfolg ohne passenden Prüfnachweis behauptet.

## Offene Abnahme und nächste Warteschlange

Zwei Freigabepunkte sind getrennt von der Implementierung offen:

1. Sichtbare Prüfung auf echtem Kubuntu / KDE Plasma-Wayland, einschließlich Systemzwischenablage und installiertem deutschen Wörterbuch. REQUIRES: Zielrechner. Priorität: hoch.
2. GitHub-Prüfung und Freigabe des isolierten Änderungsantrags. REQUIRES: erfolgreiche Commit-bezogene CI einschließlich Wayland, Restore und ZIP. Die vorgefundenen lokalen Änderungen bleiben getrennt erhalten. Priorität: hoch.

Fünf weiterführende Vorschläge: sichtbare Kubuntu-Abnahme, optionale Buchsatz-/PDF-Ausgabe, eigene speicherbare Buchvorlagen, Filter über Kapitelstatus, spätere Übernahme der gemeinsamen Archivbasis durch ältere Module. Priorisierte Empfehlung: **sichtbare Kubuntu-Abnahme**.

Nächster logischer Schritt: reale Bildschirm- und Zwischenablageprüfung nach den erfolgreichen lokalen Gates. Erwartetes Volumen: eine Abnahmerunde, ein Ergebnisprotokoll; Codeumfang erst bei tatsächlich gefundenen Fehlern bestimmen. Kein vorsorglicher Zusatzumbau.


## Folgeplanung: datensparsame Leistungsmessung

Der konkrete Vorschlag für Ladezeiten, Schreibzugriffe, Cachegrößen, Ressourcen und sichere Weitergabe steht in [DIAGNOSE_MESSPLAN.md](DIAGNOSE_MESSPLAN.md). Er ist ein Konzept für die nächste Iteration; zusätzliche Erhebung und automatische Übertragung werden hier nicht implementiert.
