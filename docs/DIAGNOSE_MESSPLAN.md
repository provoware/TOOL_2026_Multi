# Messplan: Diagnose und Verbesserung

Stand: 18.10.2026 · Vorschlag für die nächste Iteration, noch keine zusätzliche Datenerhebung implementiert.

## Ziel und Einbindung

Messwerte sollen konkrete Fragen beantworten: Was lädt langsam? Wo wird unnötig geschrieben? Bringt ein Cache einen belegbaren Vorteil? Welche Fehler betreffen wie viele Vorgänge? Die vorhandene Hilfe und Diagnose wird dafür um einen Bereich „Leistung & Verbesserung“ ergänzt. Ein eigenständiges Modul mit zweiter Ereignisdatei würde dieselbe Logik doppeln.

Der folgende Plan verwendet ausschließlich technische Messwerte mit erlaubten Feldern. Eigene Texte, Titel, Suchbegriffe, Zwischenablageinhalte, Tastatureingaben, vollständige Pfade, Benutzernamen und Zugangsdaten gehören nicht hinein. Ausführliche technische Spuren dürfen nur nach Bereinigung separat in eine ausdrücklich gewählte Diagnose aufgenommen werden.

## Welche Messwerte helfen?

| Bereich | Messwerte | Konkreter Nutzen |
|---|---|---|
| Start und Laden | Prozessstart → bedienbares Dashboard; Modul öffnen → bedienbar; Lesen, JSON-Prüfung, Sortieren, Listen-/Kapitelaufbau getrennt; Anzahl Einträge und Größenklasse | Langsamen Teil statt nur Gesamtdauer finden |
| Reaktionsfähigkeit | Verzögerung einer regelmäßigen Qt-Zeitgeberprüfung; Anzahl/Höchstdauer von Blockaden über einem festgelegten Schwellwert | Hängende Oberfläche von langsamer Datei unterscheiden |
| Speichern | Versuche, Erfolge, Fehler, Dauer, Nutzdatenbytes; vorher/nachher unverändert; manuell oder automatisch; Versionserzeugung; Replace und fsync getrennt | Überflüssige Autosaves, Vollbestands-Schreiben und teure Sicherungen erkennen |
| Lese-/Schreibzugriffe | Logische App-Vorgänge und Bytes; optional Linux-Prozesszähler als getrennte Messquelle | Schreibverstärkung und I/O-Spitzen nachvollziehen |
| Cache | Nur tatsächlich implementierte app-eigene Caches: Bytes, Einträge, Treffer, Fehlschläge, Verdrängungen, Alter, Invalidierungen, Aufbauzeit | Nutzen, Speicherverbrauch und veraltete Ergebnisse beurteilen |
| Speicher/CPU | Prozess-RSS periodisch, Spitzenwert, CPU-Zeit für einzelne Arbeitsschritte, offene eigene Fenster | Wachstum über Sitzungen und teure UI-Neuaufbauten finden |
| Datenumfang | Klassen für Bücher/Kapitel/Buttons und Bestandsbytes; Versions-/Export-/Logumfang getrennt; freier Platz im Arbeitslaufwerk | Laufzeiten mit vergleichbarer Arbeitsmenge vergleichen |
| Qualität | Fehlercode, Modul, Operation, Schwere, Programmversion, Anzahl betroffener Versuche/Sitzungen, Wiederholungen und Recovery-Ergebnis | Häufige und schwere Fehler richtig priorisieren |
| Bedienung | Optional aggregierte Nutzungszahlen für definierte Aktionen; freiwillige Bewertung „einfach / schwierig“; Abbrüche getrennt von Fehlern | Reibung erkennen, ohne Abbruchgründe zu erfinden |
| Automatische Prüfung | Commit-SHA, Testzahl, Laufzeiten, UI-Befunde, Restore-Ergebnis und Paket-Prüfsumme | Verbesserungen genau einer geprüften Revision zuordnen |

Ein Betriebssystem hat viele Caches. Deren Gesamtgröße oder die physisch auf eine SSD geschriebenen Bytes dürfen nicht aus logischen App-Zählern abgeleitet werden. Linux `/proc/self/io` enthält Prozesszähler mit Cache-/Writeback-Effekten, keine vollständige Lebensdauerstatistik des Datenträgers. Diese Werte bekommen eine eigene Quellenbezeichnung. Nicht messbare Felder erscheinen als „nicht ermittelt“, nicht als null.

## Wie erheben?

1. Gemeinsame, kleine Messschnittstelle für feste Operationsnamen vorsehen, beispielsweise `books.open`, `snippets.render`, `store.atomic_write`. Messung mit monotoner Uhr (`perf_counter_ns`); CPU-Zeit separat. Keine freien Nutzereingaben als Messnamen verwenden.
2. Fachliche Aktion und technische Teiloperation unterscheiden. Ein Speichervorgang kann Nutzdatei, Version, fsync und atomaren Replace auslösen. Eltern-/Kindbeziehung verhindert Doppelzählung als mehrere Nutzerspeicherungen.
3. Bestehende zentrale atomare Dateifunktionen instrumentieren und einen Rekursionsschutz setzen: das Schreiben von Messdaten erzeugt nicht wieder neue Messdaten. Temporäre Datei und endgültiger Replace sind keine zwei gespeicherten Dokumente.
4. Zähler und begrenzte Laufzeithistogramme im Speicher sammeln. Geplante Vorgabe: höchstens alle 60 Sekunden gesammelt lokal schreiben, zusätzlich beim regulären Ende; keine Datei je Klick oder Tastendruck. Ein Absturz darf eine Minute Leistungsstatistik verlieren, aber nie deshalb Arbeitsdaten gefährden.
5. Ressourcen beispielsweise alle 60 Sekunden messen; eigenen Cache-/Versionsumfang höchstens beim Öffnen der Diagnose beziehungsweise begrenzt in größeren Abständen. Kein rekursives Durchsuchen des persönlichen Ordners. Große Bestände im Hintergrund und mit Abbruchmöglichkeit prüfen.
6. Technische Fehler weiter über den bestehenden Ereignislogger führen. Leistungsdaten getrennt von Arbeitsdaten ablegen, mit festem Speicherlimit, Rotation und Löschfunktion. Vorgeschlagene Aufbewahrung: Rohdiagnose höchstens 7 Tage, Tagesaggregate 30 Tage; beide konfigurierbar und vollständig löschbar.
7. Zusätzliche Leistungsmessung und Bedienungsstatistik ausdrücklich einschaltbar machen. Sichtbar anzeigen, was erfasst wird. Ausschalten beendet diese Erhebung sofort. Bestehende notwendige lokale Fehlerprotokollierung getrennt erklären.
8. Aufwand der Messung selbst mit Vorher-/Nachher-Benchmarks prüfen. Zielwert: unter 1 % Zusatzlaufzeit bei definierten Szenarien; kein behaupteter Grenzwert ohne Messung. Belastungsproben mit großen Beständen, vollem Datenträger und ausgeschalteter Erhebung ergänzen.

## Wie auswerten?

- Je Programmversion, Modul, Operation, Datenklasse und Kalt-/Warmstart trennen. Ein Erststart nach Installation gehört nicht in dieselbe Gruppe wie ein erneutes Öffnen.
- Anzahl der Beobachtungen, Median, p95, Maximum und Fehlerrate anzeigen. p95 bedeutet: 95 % der gemessenen Vorgänge waren höchstens so langsam. Bei kleinen Stichproben die Beobachtungen direkt zeigen und keine belastbare Verbesserung behaupten.
- Sinnvolle Kennzahlen: Speicherungen pro Änderungssitzung, unveränderte Speicherungen / Speicherversuche, geschriebene Bytes / geänderte Nutzdatenbytes, Cache-Treffer / (Treffer + Fehlschläge), fehlgeschlagene Vorgänge / Versuche. Nenner immer mit anzeigen.
- Vorher-/Nachher-Vergleich nur bei ähnlicher Datenmenge, Hardwareklasse und Kalt-/Warmzustand. Eine größere Bibliothek kann trotz optimierter Software länger laden.
- Schwellen zuerst aus einer Ausgangsmessung und Nutzerziel ableiten. Beispielhafte Warnschwellen sind Hypothesen, keine universellen Defektgrenzen. Cachewachstum ohne höhere Trefferquote oder viele unveränderte Autosaves sind konkrete Optimierungskandidaten.
- Zunächst Ladezeit und Schreibverstärkung priorisieren. Cache erst hinzufügen oder vergrößern, wenn ein wiederholbarer Engpass und eine korrekte Invalidierung nachgewiesen sind.

## Wie weitergeben?

Laienfreundlicher Ablauf: **Zeitraum wählen → Bericht ansehen → Felder abwählen → bereinigtes Paket exportieren → selbst weitergeben**. Ein verständlicher TXT-Bericht und ein versioniertes JSON mit Einheiten, Stichprobenzahl, Quelle und Programmversion reichen meist. Screenshots und Rohprotokolle sind gesonderte, ausgeschaltete Optionen, weil sie Inhalte enthalten können.

Die Exportfunktion verwendet eine Feld-Erlaubnisliste statt einer bloßen Suche nach Geheimnissen. Beispielhafte Inhalte sind ausschließlich Modulname, feste Aktion, Ergebniscode, aggregierte Millisekunden, Größenklasse und Zähler. Keine unveränderte Übernahme beliebiger Exceptions oder Metadaten.

Standard: lokale Speicherung, **keine automatische Übertragung**. Für GitHub wird nach der Vorschau eine bereinigte Problemvorlage vorbereitet. Das Repository ist öffentlich: Der Nutzer muss die Veröffentlichung ausdrücklich auslösen und vorher genau sehen, was veröffentlicht wird. Private Arbeitsdateien, Rohlogs oder Diagnosepakete gehören nicht automatisch in Git-Commits. GitHub-Token werden nicht in Programmcode, Berichte oder Archive geschrieben.

## Erste geplante Umsetzung

Priorisierte kleine Iteration: Start-/Modulladezeiten, zentrale Schreibzugriffe und unveränderte Autosaves messen; Tagesübersicht und bereinigter TXT-/JSON-Export in der vorhandenen Diagnose. Cachekennzahlen erst für reale Caches hinzufügen. Vor Umsetzung Datenmodell, Ein-/Ausschalten, Löschung, Aufbewahrung, Messaufwand und öffentliche Exportvorschau gemeinsam als Abnahmekriterien festschreiben.
