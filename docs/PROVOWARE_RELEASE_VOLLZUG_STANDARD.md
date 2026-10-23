# PROVOWARE – sparsamer Release-Vollzug (Pilotstandard 1.0)

Status: Pilot auf Entwicklungszweig. Bestehende AGENTS.md, Schutzregeln, Pflichtprüfungen und Produktanforderungen haben Vorrang. Diese Regeln ergänzen sie, ersetzen sie nicht.

## Ziel
Jede Entwicklungsiteration muss eine überprüfbare Release-Anforderung erfüllen, einen nachgewiesenen Blocker abbauen oder eine konkrete notwendige Voraussetzung schaffen. Ressourcenverbrauch ist nachrangig gegenüber Datenintegrität, Sicherheit, korrekter Funktion und Release-Fortschritt.

## Vor jedem Prozess – kleinste notwendige Prüfung
1. Release-Anforderung und messbares Abschlusskriterium nennen; falls bereits erfüllt, nicht erneut arbeiten.
2. Erwarteten Nutzen und Risiko des Nichtstuns anhand vorhandener Belege bestimmen.
3. Risiken der Änderung und mögliche irreversible Folgen prüfen; bei fehlenden Belegen Unsicherheit markieren.
4. Bekannte verwandte Aufgaben auf gemeinsame Dateien, Funktionen und Prüfungen abgleichen. Gemeinsame Analyse bevorzugen; Änderungen nur bei geringerem Gesamtrisiko bündeln. Kritische oder blockierende Aufgaben nicht auf Bündelung warten lassen.
5. Bereits gültige Ergebnisse wiederverwenden, sofern Code, Konfiguration, Abhängigkeiten und Prüfbedingungen unverändert und Nachweise nicht veraltet sind.
6. Kleinstes angemessenes Untersuchungs- und Änderungsbudget wählen. Bei neu entdeckten Abhängigkeiten begründet erweitern; Pflichtprüfungen nie wegen Budgetgrenzen überspringen.

## Ausführung
- Einen abgegrenzten Schritt umsetzen; unnötige Änderungen vermeiden. Arbeitsstand und Nachweise sichern.
- Betroffene Tests früh ausführen; vor Integration sämtliche laut bestehender Projektregel erforderlichen Prüfungen durchführen.
- Nach jeder Änderung muss der geschützte Hauptstand startbar bleiben; unfertige Arbeit bleibt isoliert.
- Nicht dieselbe erfolglose Analyse ohne neue Hypothese wiederholen. Stattdessen Ursache, fehlenden Beleg oder alternative Lösung konkretisieren.

## Abschlussnachweis
Für jeden Schritt knapp festhalten: Release-Anforderung, Ausgangszustand, erwartete Wirkung, Risiko, betroffene Bereiche, verwendete bzw. wiederverwendete Prüfungen, Ergebnis, verbleibende Blocker und nächster konstruktiver Schritt. Nur nachgewiesene Verbesserungen als abgeschlossen markieren. Prognosen nicht als Tatsachen ausgeben.

## Nutzerentscheidung bei Konflikten
Bei widersprüchlichen Anforderungen, unklaren Produktzielen, Datenverlustgefahr, irreversiblen Migrationen, kostenpflichtigen Aktionen oder unvorhersehbaren Konflikten mit erheblicher Auswirkung: nur die betroffene Änderung sicher anhalten, Befund und Optionen verständlich melden und eine gezielte Nutzerfrage stellen. Unabhängige sichere Arbeiten dürfen fortgesetzt werden. Keine Schutzregel umgehen; keine Nutzerabnahme vor dem vereinbarten abschließenden Release-Schritt fingieren.

## Fortschrittskontrolle
Jede Iteration dokumentiert mindestens eine erfüllte Abschlussbedingung, einen konkret beseitigten Blocker oder eine nachweislich entscheidungsrelevante neue Erkenntnis. Andernfalls den Leerlauf kennzeichnen und den nächsten Ansatz ändern. Bündelung, Token- und Zeitersparnis gelten allein nicht als Release-Fortschritt.

## Einführung
Zunächst beobachtend mit echten Aufgaben und vorhandenen Prüfungen testen. Erst nach nachgewiesener Eignung als verpflichtende automatische Prüfung aktivieren; bestehende laufende Entwicklungszweige und Pull Requests nicht pauschal blockieren.
