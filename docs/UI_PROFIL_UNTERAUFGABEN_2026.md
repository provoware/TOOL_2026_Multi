# UI- und Profildatenplanung: 13 Hauptaufgaben

Stand: 01.11.2026 · Quelle: Nutzeranforderungen vom 01.11.2026, 12:05–12:50 Uhr (Europe/Berlin).

## Auftrag und Status

Diese Zerlegung ergänzt den [verbindlichen Modulplan](MODULPLAN_2026.md) als Next Queue. Sie ersetzt weder den eingefrorenen laufenden Plan noch dessen Integrations- und Release-Gates. Keine Funktionsumsetzung wird durch dieses Dokument als erledigt erklärt. Bereits vorhandene Funktionen werden zuerst gegen Source und passende Tests abgeglichen, anschließend wiederverwendet.

Jede ID ist unabhängig abnehmbar. Status aller Arbeitspakete: **OFFEN – Bestandsabgleich erforderlich**. Aufwand und betroffene Dateien werden nach dem Bestandsabgleich je Paket geschätzt; Zahlen ohne Untersuchung wären unbelegt. Prüfreferenzen für Web-Barrierefreiheit sind für die Qt-Desktopanwendung fachlich anzupassen und begründen keine pauschale WCAG-Konformitätsbehauptung.

## Nummerierte Kurzplanung und Scope

1. Alle 13 Anforderungen mit stabilen Unteraufgaben und Abnahmekriterien sichern.
2. Abhängigkeiten und getrennte Lieferpakete festhalten.
3. Dokumentlinks, eindeutige IDs, Vollständigkeit und Manifest prüfen; gemeinsam ins Repository übertragen.

Ausgangs-SHA: `4f188bb77d3e2aa803987dda39563efc4a266589`; Ausgangsbaum sauber. Autorisierter Scope: dieses Planungsdokument, Wegweiser, append-only Modulplan-Verweis, Änderungsverlauf und Manifest. Ausgeschlossen: Anwendungscode, Nutzerdaten und Migrationen. Lieferweg: isolierter Worktree und eigener Repository-Zweig; keine automatische Veröffentlichung oder Zusammenführung.

## 1. Kacheln kompakter gestalten

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-01.01 | Abstände vereinheitlichen | Einheitliches Raster; geringerer Platzbedarf bei gleicher Fenstergröße. |
| UI-01.02 | Kachelhöhen optimieren | Alle bisherigen Inhalte und Aktionen bleiben erreichbar. |
| UI-01.03 | Kleine Ansichten prüfen | 800×600 und 200 % Schrift: keine Überlagerung oder unerreichbare Aktion. |

## 2. Notizen in den Header verschieben

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-02.01 | Header in Spalten aufteilen | Hauptfunktionen, Notizen und Status sind klar getrennt. |
| UI-02.02 | Notizeingabe verschieben | Bestehende Notizen bleiben erhalten; Bearbeitung und erneutes Laden funktionieren. |
| UI-02.03 | Responsiven Umbruch ergänzen | Bei geringer Breite ordnen sich Bereiche ohne Überlagerung neu an. |
| UI-02.04 | Tastaturzugang ergänzen | Notizfeld mit Beschriftung ist per Tab erreichbar. |

## 3. Themes und Flächenkontraste

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-03.01 | Farbrollen definieren | Hintergrund, Kacheln, Bereiche und Eingaben verwenden unterscheidbare Farbtöne. |
| UI-03.02 | Textkontraste messen | Normaler Text mindestens 4,5:1; großer Text mindestens 3:1 nach WCAG 2.2 AA als Prüfreferenz. |
| UI-03.03 | Elementkontraste messen | Erforderliche visuelle Kennzeichnungen mindestens 3:1 zu angrenzenden Farben. |
| UI-03.04 | Zustände kennzeichnen | Fehler, Erfolg und Auswahl zusätzlich durch Text, Symbol oder Form erkennbar. |
| UI-03.05 | Alle Themes prüfen | Messbericht je Theme und Zustand vorhanden. |

## 4. Bereiche flexibel verstellen

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-04.01 | Verstellbare Bereiche festlegen | Für jeden Bereich sind Richtung, Mindestgröße und Überlauf dokumentiert. |
| UI-04.02 | Horizontale Verstellung | Trennlinien verändern Breiten ohne Inhaltsverlust. |
| UI-04.03 | Vertikale Verstellung | Trennlinien verändern Höhen ohne Inhaltsverlust. |
| UI-04.04 | Dynamische Anpassung | Inhalte umbrechen; Mindestgrößen verhindern unbedienbare Bereiche. |
| UI-04.05 | Tastatursteuerung | Trennlinien sind fokussierbar und per Pfeiltasten bedienbar. |
| UI-04.06 | Layout speichern und zurücksetzen | Neustart stellt Aufteilung wieder her; Standard ist wiederherstellbar. |

## 5. Profildatenbank und Schnelleingabe

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-05.01 | Datenmodell definieren | Profil, Kategorie und Eintrag sind eindeutig verknüpft; bestehendes Speicherformat auf Wiederverwendung geprüft. |
| UI-05.02 | Persistente Speicherung | Einträge überstehen Neustart und fehlgeschlagene Schreibversuche ohne Verlust bestehender Daten. |
| UI-05.03 | Profilverwaltung | Anlegen, Umbenennen und Auswählen funktionieren; Löschen schützt abhängige Inhalte. |
| UI-05.04 | Kategorieverwaltung | Kategorien werden eindeutig zugeordnet und wieder geladen. |
| UI-05.05 | Profilwahl im Hauptbereich | Zielprofil ist vor Eingabe sichtbar. |
| UI-05.06 | Kategorie-Schnelleingabe | Eingabe landet ausschließlich in der ausgewählten Profil-Kategorie-Kombination. |
| UI-05.07 | Kommagetrennte Werte zerlegen | warm, dunkel, ruhig ergibt drei Einträge; Leerwerte werden verworfen. |
| UI-05.08 | Enthaltene Kommas behandeln | Dokumentierte Quotierung erlaubt einen einzelnen Eintrag mit Komma. |
| UI-05.09 | Linux-Textregeln konkretisieren | UTF-8, LF, Unicode-Normalisierung und äußere Leerzeichen dokumentiert; Umlaute bleiben erhalten; keine Shell-Ausführung. |
| UI-05.10 | Eingabeinterne Dublettenprüfung | Wiederholte Werte werden nach dokumentierter Normalisierung erkannt. |
| UI-05.11 | Dublettenprüfung gegen Bestand | Vorhandene Werte werden innerhalb des definierten Geltungsbereichs erkannt; andere Profile bleiben getrennt. |
| UI-05.12 | Speicherrückmeldung | Gespeicherte, übersprungene und fehlerhafte Werte werden mit Anzahl gemeldet. |
| UI-05.13 | Datenbankansicht | Suche, Profil-/Kategoriefilter und Bearbeitung liefern reproduzierbare Ergebnisse. |
| UI-05.14 | Modulzugriff kapseln | Gemeinsame Schnittstelle liefert gefilterte Werte ohne GUI-Abhängigkeit. |
| UI-05.15 | Zufallsgenerator anbinden | Ausgabe verwendet ausschließlich die ausgewählte Datenmenge; leere Auswahl wird erklärt. |
| UI-05.16 | Import und Export | Roundtrip ohne Inhaltsverlust; erneuter Import erzeugt keine Dubletten. |

## 6. Menü und Einstellungen

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-06.01 | Menüstruktur festlegen | Häufige Funktionen sind verständlich benannt und gruppiert. |
| UI-06.02 | Oberflächeneinstellungen bündeln | Theme, Schriftgröße und Abstände zentral erreichbar. |
| UI-06.03 | Optionen erklären | Erklärungsbedürftige Optionen haben kurze deutsche Hilfen. |
| UI-06.04 | Vorschau anwenden | Darstellungsänderungen werden unmittelbar sichtbar. |
| UI-06.05 | Speichern und Zurücksetzen | Werte bleiben erhalten; Standardwerte sind wiederherstellbar. |
| UI-06.06 | Laienbedienung prüfen | Themewechsel und Schriftvergrößerung gelingen anhand definierter Aufgaben; echter Bediennachweis bleibt separat. |

## 7. Linke Navigation reparieren

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-07.01 | Abschneidefehler reproduzieren | Betroffene Größen, Schriftstufen und Layoutursache dokumentiert. |
| UI-07.02 | Navigationsmuster recherchieren | Professionelle Quellen und begründete Musterauswahl dokumentiert. |
| UI-07.03 | Scrollverhalten korrigieren | Letzter Menüpunkt bleibt auch bei geringer Höhe erreichbar. |
| UI-07.04 | Kompakte Navigation ergänzen | Eingeklappte Darstellung bietet zugängliche vollständige Namen. |
| UI-07.05 | Regression prüfen | Lange Texte, 800×600 und 200 %: kein dauerhaft verdeckter Menüpunkt. |

## 8. Textbuttons und Favoriten

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-08.01 | Buttons kompakter gestalten | Einheitliche Abstände; Text bleibt lesbar und Bedienfläche ausreichend. |
| UI-08.02 | Fachlich gruppieren | Gruppen haben Namen und unterstützende Farben. |
| UI-08.03 | Sternmarkierung | Favorit hinzufügen und entfernen funktioniert per Maus und Tastatur. |
| UI-08.04 | Favoriten speichern | Markierungen bleiben nach Neustart erhalten. |
| UI-08.05 | Rechte Seitenleiste schalten | Beschrifteter Button öffnet und schließt die Leiste. |
| UI-08.06 | Favoriten anzeigen | Markierungsänderungen aktualisieren die Liste unmittelbar. |
| UI-08.07 | Größenautomatik | Buttons passen sich der verfügbaren Breite ohne abgeschnittene Aktionen an. |
| UI-08.08 | Automatik abschalten | Persistente Option wechselt zwischen automatischer und fester Darstellung. |

## 9. Was möchtest du tun? verschieben

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-09.01 | Oben in rechte Leiste integrieren | Bereich erscheint vor den Favoriten. |
| UI-09.02 | Aktionen übernehmen | Alle bisherigen Aktionen funktionieren unverändert. |
| UI-09.03 | Schmale Darstellung | Beschriftungen und Aktionen bleiben zugänglich. |
| UI-09.04 | Geschlossene Leiste berücksichtigen | Klarer Zugang zu den Aktionen bleibt sichtbar. |

## 10. Buttons und Aktionskontraste

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-10.01 | Standards recherchieren | Quellen zu WCAG 2.2, Fokus, Zielgrößen und Typografie mit Abrufdatum dokumentiert. |
| UI-10.02 | Buttons von Flächen absetzen | Normale Buttons sind eindeutig als bedienbar erkennbar. |
| UI-10.03 | Aktionshierarchie | Primäre, sekundäre und destruktive Aktionen zusätzlich zur Farbe unterscheidbar. |
| UI-10.04 | Neonrand gestalten | Rand verbessert Erkennbarkeit und verschlechtert Textkontrast nicht. |
| UI-10.05 | Interaktionszustände | Hover, Fokus, Aktiv und deaktiviert sind unterscheidbar; Fokus bleibt sichtbar. |
| UI-10.06 | Bedienflächen prüfen | Für Qt logische Pixel dokumentieren; WCAG-Zielgröße 24×24 CSS-Pixel als Referenz mit dokumentierten Ausnahmen; Touchziel möglichst 44×44. |

## 11. Tastatur und Eingabefelder

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-11.01 | Tastaturinventar prüfen | Wesentliche Funktionen ohne Maus erreichbar; keine Tastaturfalle. |
| UI-11.02 | Fokusreihenfolge | Tab und Umschalt+Tab folgen der sichtbaren Struktur. |
| UI-11.03 | Enter und Escape | Speichern, Abbrechen und Mehrzeileneingabe sind konsistent dokumentiert. |
| UI-11.04 | Platzhalter unterscheiden | Platzhalter und Nutzereingabe sind unterscheidbar und kontrastreich. |
| UI-11.05 | Vorbelegte Werte kennzeichnen | Echte Vorgaben sind zusätzlich zur Farbe erkennbar. |
| UI-11.06 | Beschriftung und Fehlerhilfe | Feldzweck bleibt nach Eingabe sichtbar; Fehlermeldung erklärt die Korrektur am Feld. |

## 12. Ereignisanzeige erweitern

Priorität: P2. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-12.01 | Fünf Einträge einblenden | Standardansicht zeigt mindestens fünf letzte Ereignisse gleichzeitig. |
| UI-12.02 | Ereignisformat | Jeder Eintrag enthält Zeit, Typ und verständliche Meldung. |
| UI-12.03 | Verlauf und Reihenfolge | Neue Ereignisse konsistent einsortiert; ältere per Scrollen erreichbar. |
| UI-12.04 | Lange Meldungen | Volltext zugänglich ohne Überlagerung benachbarter Einträge. |
| UI-12.05 | Barrierearme Aktualisierung | Kein Fokusdiebstahl; relevante Meldungen über Qt-Zugänglichkeit verfügbar. |

## 13. Profilstruktur und Standardinhalte

Priorität: P1. Status je Zeile: OFFEN.

| ID | Einzeln prüfbare Unteraufgabe | Abnahmekriterium |
|---|---|---|
| UI-13.01 | Fachrecherche | Professionelle Genre-/Stimmungsquellen mit Abrufdatum, Ableitung und Nutzungsrechten dokumentiert. |
| UI-13.02 | Begriffe definieren | Profil, Kategorie und Detailinhalt mit Beispielen eindeutig beschrieben. |
| UI-13.03 | Profilstruktur entwerfen | Breite, erweiterbare Taxonomie mit klaren Abgrenzungen. |
| UI-13.04 | Kombinationsmatrix | Alle gültigen Profil-Kategorie-Kombinationen vollständig aufgelistet. |
| UI-13.05 | Qualitätsregeln | Sprache, Detailtiefe, Synonyme und Geltungsbereich der Eindeutigkeit dokumentiert. |
| UI-13.06 | Standardinhalte erstellen | Mindestens 100 fachlich unterschiedliche Inhalte je gültiger Kombination; keine bloß kombinatorischen Füllwerte. |
| UI-13.07 | Exakte Dubletten prüfen | Automatischer Bericht: keine unzulässigen exakten oder normalisierten Wiederholungen. |
| UI-13.08 | Semantische Wiederholungen prüfen | Redaktioneller Nachweis für jede Kombination; bloße Umformulierungen ersetzt. |
| UI-13.09 | Versionierte Daten bereitstellen | Version, Herkunft und Importformat vorhanden. |
| UI-13.10 | Wiederholten Import prüfen | Erstimport vollständig; erneuter Import erzeugt keine Dubletten. |
| UI-13.11 | Generatorfähigkeit prüfen | Jede gültige Kombination liefert passende Ergebnisse; leere Daten werden behandelt. |

## Abhängigkeiten und getrennte Lieferpakete

| Paket | Umfang | REQUIRES |
|---|---|---|
| A: Bestandsabgleich | Source, Tests, offene PRs den IDs zuordnen | vor Implementierung aller Pakete |
| B: Profilstruktur | UI-13.01–13.05 | A |
| C: Datenbankkern | UI-05.01–05.04 | A, B |
| D: Parser und Dubletten | UI-05.07–05.11 | C; eigene Logiktests ohne Schnelleingabe-GUI |
| E: Schnelleingabe | UI-05.05–05.06, 05.12 | C, D |
| F: Modulverknüpfung | UI-05.14–05.15 | C; unabhängig von E abnehmbar |
| G: Datenpflege und Transfer | UI-05.13, 05.16 | C, D |
| H: Standardbestand | UI-13.06–13.11 | B, C, D, G; Generatorprüfung zusätzlich F |
| I: Navigation und flexible Bereiche | UI-04, UI-07, UI-11 | A; Prüfung bestehender Layoutkandidaten vor Neuerstellung |
| J: Farb- und Buttonsystem | UI-03, UI-10 | A; recherchierte Referenzen |
| K: Kompaktheit, Header und Einstellungen | UI-01, UI-02, UI-06 | I, J |
| L: Rechte Leiste | UI-08, UI-09 | I, J |
| M: Ereignisse | UI-12 | A; Mindestanzeige bei Layoutprüfung berücksichtigen |

B BLOCKS H. C BLOCKS D/E/F/G. UI-09 REQUIRES UI-08.05. Farbarbeiten in UI-03 und UI-10 teilen dieselben Tokens und Messungen; keine doppelte Implementierung. Bestehende Profile, Zufallsgenerator, Textbuttons und Layoutregler sind Wiederverwendungskandidaten, kein ungeprüftes PASS. Import/Export und zusätzliche Verwaltung aus der Chat-Zerlegung werden vor Umsetzung auf Abdeckung durch den bestehenden Modulplan geprüft; Zusatzumfang bleibt Next Queue.

## Messbare Abnahme und Fortschritt

- Jede ID erhält bei Bearbeitung: Source-Pfade, Testfälle, geprüften Commit, Ergebnis, Evidenzpfad und Restblocker. Statusfolge: OFFEN → IN ARBEIT → IMPLEMENTIERT/UNGEPRÜFT → GEPRÜFT. BLOCKIERT enthält Grund und nächsten Schritt.
- Fehlerhypothesen für Datenpfad: leere Eingabe, nur Trennzeichen, zitierte Kommas, Unicode, Groß-/Kleinschreibung, erneuter Import, falsches Profil, Schreibfehler und leere Generatorauswahl. Bestehende Nutzerdaten bleiben geschützt.
- Layoutmatrix mindestens 800×600, 1280×720 und 1920×1080 mit 100/150/200 % sowie allen angebotenen Themes. Für physisch unmögliche Mindestansichten muss ein zugänglicher Scroll-/Einklappweg dokumentiert werden.
- Recherche gilt erst mit tatsächlich gelesenen Quellen und Ableitung als erledigt. In dieser Planungsiteration wurde keine Internet-Fachrecherche durchgeführt.
- Standardbestand: 100 × Anzahl gültiger Profil-Kategorie-Kombinationen. Beispiel 12 × 8 × 100 = 9.600 Inhalte; Struktur vor Inhaltserstellung einfrieren.
- Nächste priorisierte Empfehlung: Paket A mit Fokus auf UI-05 und UI-13; danach Datenbankkern getrennt von Schnelleingabe und Generator abnehmen.
- Weitere nächste Kandidaten: Navigationsfehler reproduzieren; Farbkontraste inventarisieren; bestehende Layoutregler prüfen; Standardinhalte auf Dubletten untersuchen. Keine zusätzlichen Features eröffnen.

## Recovery und Prüfung dieser Planungsiteration

Frozen Plan: ausschließlich Zerlegung und Repository-Dokumentation. Risiken: doppelte Aufgabenregister, unbelegte Fertigmeldungen und Überschreiben bestehender Planung; Gegenmaßnahmen: stabiler Verweis im Modulplan, explizit offene Status, append-only Ergänzung. Keine ausführbaren Änderungen, daher keine GUI-/Wayland-/Restore-Abnahme für diese Dokumentation behauptet. Manifest/JSON, IDs, Kapitelzahl, Verweise und `git diff --check` sind vor Commit zu prüfen. Remote-Übertragung und CI separat anhand des tatsächlichen Repository-Stands berichten.


## Nachweis Paket A · 01.11.2026

[Bestandsabgleich UI-05 und UI-13](PROFIL_BESTANDSABGLEICH_2026_11_01.md): alle 27 zugehörigen IDs gegen Source, 51 bestehende Prüfungen und isolierte Fehlerproben untersucht. Die Zeilen mit OFFEN oben beschreiben den ursprünglichen Planungsstand; maßgeblich für den untersuchten Teilumfang ist die verlinkte Befundmatrix. Funktionen bleiben bis zur jeweiligen vollständigen Abnahme offen. Übrige Bereiche von Paket A noch nicht abgeschlossen.

## Folgeplanung Paket B · 01.11.2026

[Fachstruktur, gelesene Quellen und Qualitätsregeln](PROFIL_FACHSTRUKTUR_2026.md) konkretisieren UI-13.01–13.05. Die [vollständige Zielmatrix](PROFIL_ZIELMATRIX_2026.json) enthält zwölf Profile × fünf unveränderte Kategorien = 60 Kombinationen. Diese Struktur ersetzt das frühere reine Rechenbeispiel 12 × 8; das 100er-Ziel je gültiger Kombination bleibt bestehen. 6.000 Zielplätze, 78 beobachtete Altwerte, noch keine einzeln freigegebenen erweiterten Katalogeinträge. Keine produktiven Daten verändert oder neue Profile aktiviert. UI-13.06–13.11 bleiben offen; aktuelle PR-/main-Nachweise vor Gesamtabschluss prüfen.

UI-05.08–05.11 im technischen Eingabeumfang sind seit PR #165 integriert (main-CI #41313008102). UI-05.12 ist seit PR #166 auf main `c0b982772a51d660f4dd7ba51a5bb47ad57f9e12` mit eigener erfolgreicher CI #41317682933 umgesetzt; Vorschau und Speicherzahlen im bestehenden Editor. Das schließt die direkte Dashboard-Schnelleingabe nicht ein. Frühere OFFEN-/Teilweise-Zeilen beschreiben den damaligen Stand und werden nicht als neue Implementierungsaufträge dupliziert.
