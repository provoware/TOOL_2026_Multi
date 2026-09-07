# AGENTS.md – verbindliche Entwicklungsregeln

Version: 1.0 · Gültig ab: 2026-09-08

## 1. Hauptziel

TOOL_2026_Multi wird möglichst autonom, sicher, wartbar und für absolute Laien verständlich entwickelt. Der Nutzer wird nur einbezogen, wenn eine Entscheidung ohne ihn sachlich nicht sicher getroffen werden kann.

## 2. Entscheidungsregel: autonom vor Rückfrage

Ohne Rückfrage zulässig sind:
- klar abgegrenzte Fehlerbehebungen mit Prüfung,
- wartbarkeitssteigernde interne Umstrukturierungen ohne Funktionsänderung,
- Dokumentationspflege,
- Ergänzung fehlender Tests zu geändertem Verhalten,
- sichere, rücknehmbare Konfigurationsverbesserungen,
- Sicherungen, Prüfsummen, Protokollierung und Wiederherstellungsverbesserungen,
- kleine Oberflächenverbesserungen, wenn Bedeutung und Ablauf unverändert bleiben.

Eine Rückfrage ist nur nötig bei:
- möglichem Verlust oder Überschreiben von Nutzerdaten,
- nicht rücknehmbaren Datenumwandlungen,
- Zugangsdaten, bezahlten Diensten oder externen Konten,
- widersprüchlichen Produktzielen,
- neuen Hauptfunktionen außerhalb des vereinbarten Umfangs,
- rechtlich oder organisatorisch zwingenden Nutzerentscheidungen.

Bei Unsicherheit über eine zerstörerische Aktion gilt: **nicht ausführen, sicher abbrechen, Grund und nächsten sicheren Schritt dokumentieren.**

## 3. Iterationsdisziplin

Jede Iteration hat genau ein Hauptziel und eine nummerierte Kurzplanung. Vor Änderungen werden betroffene Dateien, Stellen, Risiken und vorhandene Prüfungen bestimmt. Danach werden nur die kleinsten nötigen Änderungen ausgeführt.

Ablauf:
1. Ist-Stand bestimmen.
2. Ziel und Abnahmekriterien festlegen.
3. Sicherungspunkt vor Änderung erzeugen, wenn bereits ausführbarer Bestand betroffen ist.
4. genaue Änderungsstellen bestimmen.
5. kleinen Patch ausführen.
6. unmittelbar passende Prüfungen ausführen.
7. Fehler ursachengerecht beheben, nicht Symptome verdecken.
8. Rückfallprüfung ausführen.
9. Dokumentation, Aufgabenliste, Änderungsverlauf und Manifest aktualisieren.
10. vollständigen Stand sichern und Iterationsbericht ausgeben.

Offene Punkte aus einer Iteration werden mit Ursache, Priorität und Abhängigkeit in die nächste Iterationsplanung übernommen. Nichts wird stillschweigend vergessen.

## 4. Änderungsgrenzen

- Keine kosmetischen Nebenarbeiten außerhalb des Iterationsziels.
- Keine großen Ersetzungen, wenn ein kleiner Patch genügt.
- Keine Prüfungen ohne klare Fehlerhypothese, Abnahmekriterium oder Schutzfunktion.
- Keine wiederholten Prüfungen ohne neue Codeänderung oder neue Evidenz.
- Schleifen, Wiederholungen und Wartevorgänge müssen eine feste Obergrenze oder einen Zeitabbruch besitzen.
- Jede externe Operation erhält einen sinnvollen Zeitabbruch, soweit technisch möglich.

## 5. Wartbarkeit

- Wiederverwendbare Logik wird zentral gekapselt.
- Oberflächentexte werden nicht mehrfach im Quellcode verteilt, sondern über eine versionierte Textregistrierung bezogen.
- Einstellungen, Texte, Zustände und Programmlogik werden getrennt gehalten.
- Funktionen sollen eine Aufgabe besitzen; als Richtwert höchstens 60 Zeilen.
- Quellcodedateien sollen als Richtwert höchstens 500 Zeilen enthalten. Überschreitungen brauchen einen dokumentierten Grund oder eine Aufteilung.
- Doppelte Logik wird vermieden.
- Kommentare erklären **warum**, Randfälle und Schutzmechanismen; offensichtlichen Code beschreiben sie nicht erneut.

## 6. Sprache für Nutzer

- Oberfläche und Hilfen: einfache deutsche Sprache.
- Unvermeidbare Fachbegriffe werden beim ersten Auftreten kurz erklärt.
- Keine unnötigen Abkürzungen oder englischen Bedienbegriffe.
- Fehlermeldungen müssen sagen: **Was ist passiert? Wo? Warum vermutlich? Was wurde geschützt? Was kann als Nächstes getan werden?**
- Technische Details dürfen zusätzlich vorhanden sein, stehen aber hinter der menschlichen Erklärung.

## 7. Fehler- und Rückfallmanagement

Jeder relevante Fehler erhält eine eindeutige Ereigniskennung. Ein Ereignis enthält mindestens:
- Zeit,
- Ereigniskennung,
- Schweregrad,
- betroffenen Bereich,
- menschliche Kurzbeschreibung,
- technische Ursache, soweit bekannt,
- sichere Sofortmaßnahme,
- Lösung oder nächster Prüfschritt,
- zugehörige Programmversion,
- optional Ausnahmeart und technische Spur.

Maschinenlesbare Protokolle werden als JSON-Zeilen geführt; zusätzlich wird ein menschlich lesbarer TXT-Bericht erzeugt. Protokolle liegen niemals zwischen Basisdaten.

Ein behobener Fehler wird, wenn sinnvoll reproduzierbar, durch einen Rückfalltest abgesichert. Fehlerbehebung gilt erst als abgeschlossen, wenn der ursprüngliche Fehlerweg und die unmittelbar betroffenen Nachbarwege geprüft wurden.

## 8. Sicherung

Drei Ebenen sind zu unterscheiden:
1. Git-Verlauf für Quellcode und Dokumentation.
2. lokaler Sicherungspunkt vor riskanten Änderungen.
3. vollständiges Versions-ZIP nach einer abgeschlossenen Iteration.

Sicherungen enthalten keine virtuellen Umgebungen, temporären Dateien, Protokolle oder verschachtelten Sicherungen. Jede Sicherung erhält eine SHA-256-Prüfsumme. Wiederherstellung wird vor produktiver Nutzung des Sicherungssystems mindestens einmal getestet.

## 9. Versionierung

Quell- und Dokumentdateien behalten stabile Dateinamen. Ihre Version oder ihr Stand steht im Inhalt bzw. Manifest. Das verhindert kaputte Verweise und unnötige Dateiumbenennungen.

Version und Status gehören in Dateinamen bei:
- Veröffentlichungs-ZIPs,
- Sicherungen,
- exportierten Berichten,
- bewusst unveränderlichen Beweisdateien.

Toolversion folgt `Haupt.Neben.Korrektur`, zum Beispiel `0.1.0`.

## 10. Prüfung

Prüfungen sind risikobasiert und endlich:
- Syntax nur für geänderte ausführbare Dateien,
- gezielte Funktionstests für geändertes Verhalten,
- Rückfalltests für bekannte Fehler,
- Manifest-/JSON-Prüfung für strukturierte Dateien,
- Startprüfung bei Änderungen am Startablauf,
- vollständigerer Prüfblock nur vor Veröffentlichung oder bei Querschnittsänderungen.

Kein „grün rechnen“: Nicht ausführbare Prüfungen werden als **nicht geprüft** dokumentiert.

## 11. Protokolle und Berichte

Laufzeitprotokolle: `logs/` und nicht im Git-Verlauf.
Fehlerberichte: `berichte/` und standardmäßig nicht im Git-Verlauf.
Entwicklerdokumentation: `docs/`.
Basisdaten: `daten/`.
Anwendungsquellcode: `app/`.
Tests: `tests/`.
Werkzeugscripte: `scripts/`.
Nutzertexte: `texte/`.

Nur für den Betrieb nötige Dateien werden in ein Veröffentlichungs-ZIP übernommen. Entwicklerberichte, Testdaten und lokale Protokolle bleiben draußen, außer sie werden ausdrücklich als Diagnosepaket angefordert.

## 12. Start und Abhängigkeiten

`schnellstart.sh` ist der Standardstart. Es soll:
- Projektpfad robust bestimmen,
- `.venv` anlegen oder wiederverwenden,
- `pip` in der virtuellen Umgebung verwenden,
- `requirements.txt` installieren,
- einen begrenzten Vorabtest ausführen,
- bei Erfolg das Tool starten,
- bei Fehlern klar und laienverständlich abbrechen.

Abhängigkeiten werden in `requirements.txt` mit Version festgelegt, sobald sie tatsächlich benötigt werden. Unbenötigte Pakete werden nicht vorsorglich installiert.

## 13. Oberflächenstandard

- nächster sinnvoller Schritt sichtbar,
- Fortschritt bei längeren Vorgängen sichtbar und bewegt,
- keine überladene Oberfläche,
- zentrale Größen, Abstände und wiederkehrende Elemente aus gemeinsamen Definitionen,
- Hilfen und Tooltips direkt am relevanten Element,
- gefährliche Aktionen deutlich von sicheren Aktionen unterscheiden,
- Standardweg in 1–2 Schritten erreichbar, soweit funktional sinnvoll.

## 14. Abschluss jeder Iteration

Auszugeben sind:
1. Toolname und Repositoryname.
2. erledigte und offene Punkte, jeweils mit echter Anzahl.
3. grafische Fortschrittsanzeige.
4. fünf weiterführende Vorschläge plus genau eine priorisierte Empfehlung.
5. nächster logischer Schritt.
6. Kurzdetails und Änderungsvolumen der abgeschlossenen Iteration.
7. Kurzdetails und erwartetes Volumen der nächsten Iteration.
8. vollständiges ZIP und Repository-Stand.

Nur tatsächlich ausgeführte und nachgewiesene Punkte werden als erledigt gezählt.
