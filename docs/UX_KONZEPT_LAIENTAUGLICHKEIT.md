# UX-Analyse und Verbesserungskonzept für Provoware

**Stand:** 24. Oktober 2026 · **Dokumentversion:** 1.0  
**Repository:** `provoware/TOOL_2026_Multi`  
**Analysierter Ausgangsstand:** `5c143fe87a1890017829580987b3c1776f184c40`  
**Status:** Analyse und Planung; vorgeschlagene Produktänderungen sind nicht umgesetzt.

## 1. Auftrag und Geltungsbereich

Ziel ist eine verständliche, verlässliche Bedienung ohne technisches Vorwissen. Nutzer sollen persönliche Inhalte erstellen, speichern, wiederfinden, weiterbearbeiten und sichern können, ohne interne Datenformate, Ordnerstrukturen oder Modulgrenzen verstehen zu müssen.

Grundlagen sind Quellcode, Nutzertexte, Anleitungen und der [Interoperabilitätsaudit vom 22.10.2026](../TODO.md#neuer-prüf--und-entwicklungsbedarf--nutzerinteroperabilität-audit-vom-22102026). Die Untersuchung ist eine qualitative Code- und Dokumentationsanalyse. Es wurden keine neue interaktive GUI-Prüfung, Screenreader-Prüfung, Erstnutzerstudie oder reale Kubuntu-Abnahme durchgeführt. Historische Prüfberichte belegen ausschließlich ihren jeweiligen Stand.

Der [Modulplan](MODULPLAN_2026.md) und laufende freigegebene Arbeiten bleiben maßgeblich. Dieses Konzept ergänzt die nächste Aufgabenplanung; es ersetzt keinen bestehenden Auftrag und bestätigt keine Umsetzung. Überlappende Anforderungen bleiben unter ihrer bestehenden `PV-AUD`-Kennung führend. Die [TODO-Ergänzung](../TODO.md#ux-folgeplanung--nutzerfreundlichkeit-und-laientauglichkeit-24102026) erfasst ausschließlich ergänzende UX-Aufträge.

## 2. Gesamtbewertung und Leitprinzipien

Provoware besitzt einen breiten Funktionsbestand und wichtige Schutzmechanismen: Einstiegshilfen, Zoom, Kontrastdarstellung, Tastaturwege, Schutz vor unbeabsichtigtem Überschreiben, Versionsverwaltung und isolierte Wiederherstellung. Diese Grundlagen sollen erhalten bleiben.

Der größte Verbesserungsbedarf liegt in durchgängigen Arbeitsabläufen. Nutzer müssen noch zu häufig selbst erschließen, welches Werkzeug zuständig ist, welche Angaben zusammengehören, ob Änderungen gespeichert wurden und was eine Sicherung enthält. Eine geringe Klickzahl allein belegt keine einfache Bedienung.

Drei Qualitätsziele bestimmen die Weiterentwicklung:

1. **Orientierung:** Aufgabe, aktueller Bereich und nächster sinnvoller Schritt sind erkennbar.
2. **Verlässlichkeit:** Beschriftung und tatsächliche Wirkung stimmen überein.
3. **Handlungssicherheit:** Zustand der Arbeit und Folgen einer Entscheidung sind verständlich.

Gestaltungsmaßstab: **Vor einer Aktion ist ihre Wirkung verständlich; danach sind Ergebnis, Speicherzustand und nächster Schritt erkennbar.**

## 3. Nachweisstatus und Priorisierung

- **OBSERVED:** Verhalten oder Text im analysierten Quellcode bzw. Dokument vorhanden. Dies belegt keine beobachtete Nutzerreaktion.
- **SUSPECTED:** begründete Vermutung über eine Bedienhürde; durch Aufgabenversuch zu überprüfen.
- **RECOMMENDATION:** vorgeschlagener Sollzustand; noch keine vorhandene Funktion.
- **NOT TESTED:** praktischer Nachweis in dieser Untersuchung nicht durchgeführt.

Priorisierung: zuerst Datenbewahrung und unerwartete Änderungen, danach Orientierung, Speicherverständnis und vollständige Arbeitsabläufe, anschließend Personalisierung. Bestehende Audit-Prioritäten bleiben erhalten; die Reihenfolge hier ist eine Empfehlung für Folgearbeit und kein Ersatz des eingefrorenen Plans.

## 4. Befunde und Maßnahmen

### 4.1 Persönliche Inhalte und Sicherungsumfang

**OBSERVED:** `append_developer_info()` in [quick_note.py](../app/quick_note.py) schreibt die als „Projekt-Notiz“ angebotene Eingabe nach `Entwicklerinformation.txt` im übergebenen Projektstamm. Die [dokumentierte persönliche Sicherung](DATENSICHERUNG.md) umfasst `daten/`. Diese Notiz ist daher nicht Teil dieses beschriebenen Daten-ZIPs. Vor einer Umsetzung sind zusätzlich aktuelle Laufzeitwurzel und abweichende Datenpfadkonfigurationen zu prüfen.

**Risiko:** Nutzer dürfen eine prominent angebotene persönliche Notiz als Bestandteil ihrer gesicherten Arbeit verstehen. Eine technisch vorhandene Sicherung kann deshalb eine unvollständige Erwartung erzeugen.

**RECOMMENDATION:** Notizen künftig datenseitig ablegen; bestehende Notizen nur gesichert und nachvollziehbar übernehmen. Keine stille Löschung, Überschreibung oder automatische Zusammenführung historischer Inhalte. Führender Auftrag: `PV-AUD-01`.

Extern referenzierte Audio-, Bild- und Videodateien sind ebenfalls nicht automatisch Bestandteil der persönlichen Datensicherung (`PV-AUD-14/15/29`). Drei Angebote müssen klar getrennt werden:

| Angebot | Zweck | Erforderliche Rückmeldung |
|---|---|---|
| Persönliche Daten sichern | Gespeicherte eigene Inhalte schützen | Enthaltene Inhalte und bekannte Ausschlüsse nennen |
| Vollständiges Projektpaket erstellen | Zusammengehörige Arbeit übertragen | Eingebettete und nur referenzierte Medien unterscheiden |
| Programm für ein Update sichern | Rückkehr zu einem Programmstand ermöglichen | Abgrenzung zu persönlichen Daten erläutern |

Eine grafische Sicherung soll Zielauswahl, Umfang, laufenden Vorgang und überprüftes Ergebnis verständlich zeigen. Wiederherstellung zunächst ausschließlich in einen neuen isolierten Ordner; Aktivierung zurückgeholter Daten bleibt ein gesonderter kontrollierter Schritt. Niemals pauschal „Alles gesichert“ melden, wenn Quellen fehlen. Bestehende Größen-, Pfad- und Integritätsgrenzen erhalten.

**Abnahme:** Notizen und reguläre Inhalte sind nach einem isolierten Sicherungs-Roundtrip vollständig vorhanden; externe Medien sind enthalten oder ausdrücklich ausgeschlossen. Abbruch, fehlender Speicherplatz, beschädigtes Archiv und vorhandener Zielordner führen zu verständlichen Ergebnissen ohne Überschreibung. Neue UX-Ergänzung: `PV-UX-06`.

### 4.2 Persönliche Aufgaben und Entwicklungsplanung

**OBSERVED:** [TodoWindow](../app/todo_window.py) ruft beim Öffnen `ensure_project_module_backlog()` aus [todo_store.py](../app/todo_store.py) auf. Dadurch können Entwicklungsaufgaben im persönlichen Bestand entstehen.

**Risiko:** Das Öffnen eines Werkzeugs wird als lesender Einstieg erwartet. Unerwartete Aufgaben erschweren Orientierung und Vertrauen.

**RECOMMENDATION:** Entwicklung und persönliche Aufgaben trennen. Beispiele nur ausdrücklich übernehmen lassen. Historische Einträge erhalten und vor einer Zuordnung auf Herkunft und Konflikte prüfen. Führender Auftrag: `PV-AUD-05`; kein zusätzlicher Doppelauftrag.

**Abnahme:** Eine neue persönliche Aufgabenliste bleibt beim ersten Öffnen leer. Vorhandene eigene Aufgaben bleiben vollständig erhalten; wiederholtes Öffnen erzeugt keine Fremdeinträge.

### 4.3 Tätigkeitsorientierter Einstieg

**OBSERVED:** Die Karte „So startest du“ in [ui.py](../app/ui.py) nummeriert die unabhängigen Zugänge zu Songtexten, Aufgaben und Kalender mit ①–③.

**SUSPECTED:** Erstnutzer könnten darin eine verpflichtende Reihenfolge sehen. Diese Interpretation wurde nicht praktisch geprüft.

**RECOMMENDATION:** „Was möchtest du tun?“ mit klaren Aktionen anbieten: „Song schreiben“, „Text schreiben“, „Buch beginnen“, „Aufgabe notieren“, „Termin eintragen“. Erstellen und vorhandene Inhalte ansehen unterscheiden. Kein verpflichtender langer Einrichtungsassistent; Darstellung bei Bedarf einstellen lassen.

Leere Bereiche erklären kurz ihren Zweck, bieten genau eine hervorgehobene Hauptaktion und höchstens eine passende Nebenaktion wie Importieren. Beispiel: „Du hast noch keine Texte gespeichert. Beginne mit deinem ersten Text.“

**Abnahme:** Ein Erstnutzer kann ohne mündliche Anleitung ein Dokument erstellen, speichern und erneut öffnen. Auftrag: `PV-UX-01`.

### 4.4 Verlässliche Werkzeugnavigation

**OBSERVED:** Navigation, Kacheln, Karten und ein Symbolmenü hinter `▦` verteilen die Zugänge. Das Menü hat Tooltip und barrierefreien Namen, jedoch keine dauerhaft sichtbare Wortbeschriftung. Quellen: [ui.py](../app/ui.py), [navigation_ux.py](../app/navigation_ux.py).

**SUSPECTED:** Zusätzliche Werkzeuge sind für neue Nutzer schwerer auffindbar. Mehrere Zugänge sind nicht grundsätzlich problematisch; ihre tatsächliche Wirkung bleibt zu prüfen.

**RECOMMENDATION:** Sichtbaren Zugang „Alle Werkzeuge“ ergänzen; häufige Funktionen direkt erreichbar halten. Gruppierung als Entwurf:

| Gruppe | Beispiele |
|---|---|
| Schreiben | Songs, Texte, Bücher |
| Ideen & Vorlagen | Ideenarchiv, Textbausteine, Figuren, Vorgaben |
| Organisieren | Aufgaben, Kalender, Wissen, Links |
| Medien | Audio, Bilder, Video |
| Einstellungen & Hilfe | Anzeige, Werkzeugverwaltung, Sicherung, Fehlerhilfe |

Deaktivierte, geplante und nutzbare Funktionen unterscheiden. Bei ausgeschalteten Werkzeugen den Erhalt vorhandener Inhalte erklären; Aktivierung nur nach den bestehenden Regeln. Planung optional halten. Layoutänderung bei Zoom darf den einzigen Zugang zu einer fertigen Funktion nicht entfernen.

**Abnahme:** Alle nutzbaren Werkzeuge sind über einen beschrifteten Weg erreichbar; Tastatur, Zoom und Aktivierungsstatus stimmen überein. Auftrag: `PV-UX-02`, mit `PV-AUD-16/18` abgleichen.

### 4.5 Speicherzustände und unbetitelte Entwürfe

**OBSERVED:** [Songeditor](../app/song_editor.py), [Texteditor](../app/text_editor_window.py) und [Buchwerkstatt](../app/book_window.py) haben unterschiedliche Speicherabläufe. Der Texteditor verwendet einen Fünfminutentimer und speichert automatisch nur mit vorhandenem Titel; die Buchwerkstatt prüft betitelte geänderte Entwürfe jede Minute. Rückmeldungen sind nicht einheitlich.

**RECOMMENDATION:** Gemeinsame Zustände und Begriffe festlegen, ohne technisch notwendige Fachunterschiede zu verdecken:

| Zustand | Darstellung |
|---|---|
| Neuer Entwurf | Noch nicht gespeichert |
| Änderungen vorhanden | Ungespeicherte Änderungen |
| Speicherung läuft | Wird gespeichert … |
| Speicherung erfolgreich | Gespeichert um 14:32 |
| Speicherung fehlgeschlagen | Nicht gespeichert; zutreffend erklären, was erhalten ist und was jetzt getan werden kann |

Unbetitelte Entwürfe müssen ihren Zustand deutlich anzeigen. Eine spätere automatische Entwurfssicherung benötigt ein eigenes Konzept für Identität, Wiederherstellung und Mehrfachstarts; keine ungesicherte Zusage einführen. Speicherstatus nur nach tatsächlichem Schreibabschluss aktualisieren und bei neuer Änderung wieder korrigieren.

**Abnahme:** Nutzer erkennen den wirklichen Zustand bei Bearbeitung, automatischem Speichern, Fehler, Titeländerung und Schließen. Auftrag: `PV-UX-03`.

### 4.6 Eindeutige Entscheidungen beim Verlassen

**OBSERVED:** [Texteditor](../app/text_editor_window.py), [gemeinsame Moduloberfläche](../app/module_widgets.py) und [Modulsteuerung](../app/module_controls_window.py) verwenden „Ja / Nein / Abbrechen“ mit erklärendem Meldungstext.

**RECOMMENDATION:** Aktionsbezogene Beschriftungen einsetzen: beim Schließen „Speichern und schließen“, „Änderungen verwerfen“, „Weiter bearbeiten“; beim Datensatzwechsel entsprechend „Speichern und wechseln“. Die sichere Standardentscheidung erhält die geöffnete Arbeit. Ein fehlgeschlagener Speicherversuch darf den Wechsel nicht als erfolgreich abschließen.

**Abnahme:** Jede Auswahl hat die angekündigte Wirkung, einschließlich fehlgeschlagener Speicherung, Dialogabbruch und Beenden mehrerer geänderter Fenster. Auftrag: `PV-UX-04`.

### 4.7 Suche bis zur Weiterbearbeitung

**OBSERVED:** [SearchWindow](../app/search_window.py) zeigt Datei, Zeile und Textausschnitt sowie eine lesende Vorschau. Ein direkter Facheditor-Aufruf fehlt dort. Das Kopfsuchfeld in [ui.py](../app/ui.py) führt bereits zur zentralen Suche; die ältere reine Song-Suchbeschreibung in der Laienanleitung ist insoweit überholt.

**RECOMMENDATION:** Treffer als fachliche Inhalte mit Titel, Typ, Vorschau und eindeutiger Öffnen-Aktion darstellen. Pfade unter Details behalten. Nur geprüft aufgelöste Datensätze öffnen; kein blindes Ausführen gefundener Dateien. Führend: `PV-AUD-10/18`.

Suchumfang sichtbar benennen: aktuelle gespeicherte erlaubte Inhalte; unter anderem keine ungespeicherten Entwürfe oder älteren Versionen. Null Treffer nicht mit Datenverlust gleichsetzen. Beispiel: „Keine Treffer in den gespeicherten aktuellen Inhalten.“ Führend: `PV-AUD-11`.

**Abnahme:** Unterstützter Treffer öffnet genau den gesuchten Datensatz. Nicht unterstützte oder fehlende Ziele liefern verständliche Hinweise; bestehende Suchgrenzen und Abbruch bleiben erhalten.

### 4.8 Zusammengehörige Inhalte und letzte Arbeiten

**OBSERVED:** Das Dashboard zeigt zuletzt bearbeitete Songs; andere Inhaltstypen sind darin nicht gleichwertig vertreten. Quelle: [ui.py](../app/ui.py). Der bestehende Audit beschreibt außerdem fehlende durchgängige Projekt- und Medienbeziehungen.

**RECOMMENDATION:** „Zuletzt bearbeitet“ für unterstützte Inhaltstypen mit Typ und sicherer Öffnen-Aktion ergänzen (`PV-UX-05`). Ein optionaler Projektkontext verbindet später Songs, Bücher, Figuren, Medien, Aufgaben und Termine; einzelne Texte bleiben ohne Projektanlage möglich.

| Aktion | Verbindliche Bedeutung im Entwurf |
|---|---|
| Kopie einfügen | Inhalt anschließend unabhängig |
| Verknüpfen | Beziehung zum ursprünglichen Eintrag bleibt erhalten |
| Neue Fassung erstellen | Eigenständiger weiterer Bearbeitungsstand |

Beständige Kennungen und geprüfte Beziehungen sind Voraussetzung. Historische künstlerische Texte nicht automatisch an neue Figurennamen anpassen. Fachmodule erhalten; keine überladene gemeinsame Bearbeitungsfläche schaffen. Führend: `PV-AUD-03/07/08/09/12/14/22/28/29`.

**Abnahme:** Titelwechsel, fehlende Dateien, Umzug, Import und Versionswechsel werden kontrolliert behandelt; eine Liste letzter Arbeiten führt nicht zu veralteten oder falschen Objekten.

### 4.9 Verständliche Sprache und aktuelle Hilfe

**OBSERVED:** Technische Begriffe wie „Datenbank-Dashboard“ und „atomar“ sowie mehrdeutige Profilbezeichnungen stehen in sichtbaren Texten. Die Laienanleitung enthält auch Entwicklerprüfungen und Zielsystemabnahme. Quellen: [ui.py](../app/ui.py), [Texteditor](../app/text_editor_window.py), [Textregistrierung](../texte/registry.json), [Anleitung](../ANLEITUNG_LAIEN.md), [Hilfethemen](../app/help_content.py).

**RECOMMENDATION:** Folgende Bezeichnungen als redaktionellen Entwurf prüfen; sichtbare Namen, Hilfen, Suche und barrierefreie Namen gemeinsam aktualisieren:

| Bisher | Vorschlag |
|---|---|
| Provoware-Datenbank-Dashboard 2026 | Provoware – Übersicht |
| Todo-Liste | Aufgaben |
| Textbaustein-Buttons | Textbausteine |
| Profil- & Accountmanager | Kontenübersicht |
| atomar gespeichert | sicher gespeichert |
| JSON-Importvorlage | Vorlage für den Import; Dateiformat unter Details |

„Charakterfibel“ kann mit „Figuren verwalten“ erläutert werden. Kreative Vorgaben und Kontoprofile sprachlich unterscheiden. Die Kontenübersicht bleibt ausdrücklich kein Passworttresor; vorhandene Warnungen und Schutzprüfungen erhalten.

Kurzen Alltagseinstieg von Entwicklerprüfung und Systemabnahme trennen. Aktuelle Funktionsaussagen aus Code und Nachweisen ableiten; Historie erkennbar belassen. Zentrale Textregistrierung verwenden und verstreute Direkttexte gezielt erfassen. Aufträge: `PV-UX-07/08`; Dokumentationsstatus mit `PV-AUD-19` abgleichen.

### 4.10 Handlungsfähige Fehlerbehandlung

**OBSERVED:** Hilfe und gemeinsame Moduloberflächen bieten menschliche Erklärungen und optionale Details. Einige Meldungen geben allgemeine Hinweise wie die Prüfung von Eingaben und Dateirechten. Quellen: [module_widgets.py](../app/module_widgets.py), [help_content.py](../app/help_content.py), [text_editor_window.py](../app/text_editor_window.py).

**RECOMMENDATION:** Meldungen beantworten: Was scheiterte? Wo? Welche Ursache ist bekannt oder nur vermutet? Was ist erhalten? Was gilt für aktuelle Änderungen? Was kann der Nutzer konkret tun? Ursache und Schutzwirkung nicht pauschal zusichern.

Passende Aktionen wie „Anderen Speicherort wählen“, „Erneut versuchen“ oder „Details anzeigen“ nur anbieten, wenn der jeweilige Ablauf sie unterstützt. Wiederkehrende automatische Fehler bündeln, ohne den ungespeicherten Zustand zu verbergen. Auftrag: `PV-UX-09`.

**Abnahme:** Schreibschutz, volle Datenträger, wiederholter Autosave-Fehler und anschließende erfolgreiche Speicherung führen weder zu irrtümlichem Erfolgsstatus noch zu einer unkontrollierten Folge blockierender Dialoge.

### 4.11 Barrierefreiheit und Personalisierung

Vorhandene Zoom-, Kontrast-, Fokus- und Namensgrundlagen bleiben erhalten. **NOT TESTED:** Vollständige Zugänglichkeit mit Screenreader und ausschließlich per Tastatur ist durch diese Analyse nicht nachgewiesen.

**RECOMMENDATION:** Ganze Aufgaben prüfen: Dokument erstellen, speichern, Fehler verstehen, Treffer öffnen und sicher verlassen. Statusänderungen müssen wahrnehmbar sein; Fokus nach Dialogen und Listenupdates muss sinnvoll bleiben. Für Ziehen mit der Maus eine Tastaturalternative vorsehen, vollständige Namen trotz Kürzung zugänglich halten. Auftrag: `PV-UX-10`, ergänzt `PV-AUD-20/25`.

Personalisierung folgt einer guten Standardansicht: wenige verständliche Optionen, dauerhafte Einstellungen mit klarem Geltungsbereich, sichtbares Zurücksetzen. Freie Rasterbelegung löst keine Probleme mit Sicherungsumfang oder Speicherverständnis. Kein zusätzlicher Anfängermodus nötig, solange bedarfsgerecht eingeklappte Zusatzoptionen genügen. Führend: `PV-AUD-23/24/26`.

## 5. Empfohlene Folgeplanung und Abhängigkeiten

| Reihenfolge | Ziel | Führende Anforderungen |
|---|---|---|
| 1 | Persönliche Arbeit zuverlässig erfassen und schützen | PV-AUD-01/05/15; Umfang und Altbestand klären |
| 2 | Einstieg und Werkzeugzugang vereinfachen | PV-UX-01/02/07/08; PV-AUD-16/19 |
| 3 | Speicherzustände und Verlassen vereinheitlichen | PV-UX-03/04/09 |
| 4 | Wiederfinden und Weiterbearbeiten verbinden | PV-AUD-10/11/18; PV-UX-05 |
| 5 | Persönliche Sicherung grafisch zugänglich machen | PV-UX-06 REQUIRES überprüften Sicherungsvertrag; vollständige Medienpakete bleiben getrennt |
| 6 | Modulübergreifende Projekte verbinden | PV-AUD-03/07/08/09/14/22/29; IDs vor Beziehungen und Projekttransport |
| 7 | Personalisierung ausbauen | PV-AUD-23/24/26; Zugänglichkeit PV-UX-10 durchgehend mitführen |

Diese Reihenfolge bewertet UX-Wirkung. Sicherheitsblocker des vorhandenen Audits bleiben vorrangig. Reine Wort- und Einstiegskorrekturen können unabhängig erfolgen, sofern sie keine gesperrten Datenänderungen benötigen. Suchöffnung und letzte Arbeiten benötigen eine sichere Datensatzauflösung; das erfordert keine pauschale Neuentwicklung aller Module.

**Eine priorisierte Empfehlung:** Zunächst `PV-AUD-01` am aktuellen HEAD untersuchen und in einer begrenzten Folgeiteration beheben. Aufgabenabgrenzung und Sicherungsumfang als zusammenhängende Qualitätsziele verfolgen, aber getrennte riskante Änderungen nicht in einen unübersichtlichen Patch bündeln.

## 6. Aufgabenbezogene Abnahme

Die folgenden Szenarien sind **geplant, nicht ausgeführt**. Sie ergänzen bestehende UATs und ersetzen keine automatisierten Schutzprüfungen.

| ID | Aufgabe | Erwartetes Ergebnis |
|---|---|---|
| UX-UAT-01 | Ersten Text ohne Erklärung erstellen | Erstellen, Speichern und Wiederöffnen gelingen; Hilfebedarf dokumentiert |
| UX-UAT-02 | Speicherzustand beurteilen | Nutzer erkennt neuen Entwurf, Änderung, Erfolg und Fehler korrekt |
| UX-UAT-03 | Werkzeug erstmals finden | Beschrifteter Zugang ohne Hinweis auf verstecktes Symbol auffindbar |
| UX-UAT-04 | Persönliche Aufgaben erstmals öffnen | Keine ungefragt erzeugten Entwicklungsaufgaben |
| UX-UAT-05 | Suchtreffer weiterbearbeiten | Richtiger Originaldatensatz öffnet; ungültiges Ziel wird erklärt |
| UX-UAT-06 | Daten sichern und isoliert zurückholen | Umfang korrekt verstanden; Projekt-Notiz vorhanden; Ausschlüsse sichtbar |
| UX-UAT-07 | Verändertes Dokument verlassen | Jede Schaltfläche hat die angekündigte Wirkung; Speicherfehler hält Arbeit offen |
| UX-UAT-08 | Bei Speicherfehler weiterarbeiten | Kein falscher Erfolgsstatus; sichere nächste Handlung verständlich |
| UX-UAT-09 | Kernablauf nur mit Tastatur und bei 200 % Zoom | Relevante Inhalte und Aktionen erreichbar; Fokus nachvollziehbar |
| UX-UAT-10 | Kernablauf mit Screenreader | Namen, Zustände und Dialoge verständlich; reale Prüfung dokumentiert |
| UX-UAT-11 | Verknüpften Inhalt umbenennen oder verschieben | Beziehung bleibt gültig oder fehlende Quelle wird kontrolliert behandelt |
| UX-UAT-12 | Ansicht anpassen und zurücksetzen | Verständliche Voreinstellung wiederherstellbar; persönliche Inhalte unverändert |

Für eine spätere qualitative Erstnutzerprüfung eignen sich zunächst fünf bis sechs Personen ohne Projektkenntnis. Das ist eine Empfehlung für die abschließende Untersuchung, keine statistisch repräsentative Wirksamkeitsmessung und kein neues Zwischenabnahme-Gate. Aufgaben neutral formulieren, vor Hilfe zunächst selbstständigen Versuch zulassen und Beobachtung von Interpretation trennen.

Erfassen: erfolgreicher Abschluss, Hilfebedarf, Fehlwege, Abbruch, falsche Annahmen zu Speicherung/Sicherung und ergänzend Bearbeitungszeit. Keine erfundenen Erfolgsquoten oder pauschalen UX-Punktwerte. Schwerwiegende falsche Sicherheitsannahmen müssen vor breiter Veröffentlichung geklärt sein. Die praktische vollständige Kubuntu-/Plasma-Gesamtabnahme bleibt einmalig am Projektende.

## 7. Umsetzungskontrolle und Übergabe

1. Vor Produktänderungen HEAD, Modulplan, offene PRs, Datenpfade und passende Tests erneut prüfen.
2. Bestehende PV-AUD-Aufträge nicht erneut implementieren oder als zusätzliche erledigte Punkte zählen.
3. Jede Änderung verbindet Anforderung → Code/Text → positive und negative Prüfung → passende CI-Evidenz.
4. Nachweise für Datenverlustschutz, Wiederherstellung und Barrierefreiheit ausschließlich nach tatsächlicher Prüfung ausweisen.
5. Produktivdaten nicht für Migrationsexperimente oder Fehler-Injektionen verwenden.
6. Kein Versionssprung und keine Release-Freigabe allein aufgrund dieses Konzepts.

**Recovery Key:** Dokumentationsauftrag vom 24.10.2026; Ausgangs-SHA oben; erlaubter Scope `docs/UX_KONZEPT_LAIENTAUGLICHKEIT.md`, `docs/README.md`, `TODO.md`, `CHANGELOG.md`, `MANIFEST.json`. Ziel ist ausschließlich Übertragung und Verknüpfung der Analyse. Keine Laufzeit-, Nutzer- oder Testdateien ändern. Nächster Produktschritt ist ein eigener abgegrenzter Auftrag zu `PV-AUD-01`, kein automatischer Beginn einer Migration. Neue UX-Aufträge bleiben offen.

## 8. Prüfung dieser Dokumentationsänderung

Am 24.10.2026 lokal ausgeführt:

- `python3 -m unittest discover -s tests -p test_documentation_consistency.py`: neun bestehende Prüfungen erfolgreich.
- Relative Dateiverweise in den betroffenen Markdown-Dateien auf vorhandene Ziele geprüft.
- Bestehenden TODO-Inhalt als unveränderten Präfix geprüft; zehn neue UX-Aufträge sind offen.
- Zwölf geplante UX-Abnahmeszenarien gezählt; kein Szenario als ausgeführt markiert.
- Manifest gegen Ausgangsstand verglichen: ausschließlich zusätzliche Dokumentationsmetadaten, keine Änderung der bisherigen Laufzeitangaben.
- `git diff --check`: ohne Befund nach Entfernung einer überzähligen Leerzeile.

Dies sind Dokumentationsprüfungen. Vollständige Logik-/GUI-, Wayland-, Restore- und Releaseprüfungen wurden in diesem Dokumentationsschritt nicht lokal ausgeführt. Vor einem Merge bleibt die nach Repositoryregeln erforderliche vollständige GitHub-Prüfung maßgeblich. Ein PR allein bedeutet keine bestandene CI und kein Release.


## 9. Anforderungskorrektur: lokales Dateisystem (24.10.2026)

Der Nutzer präzisiert den Suchauftrag: Dateinamen- und Textinhaltssuche beziehen sich auf das lokale Dateisystem. Ein frei wählbarer Pfad und eine ausdrückliche Bestätigung zusätzlicher Zugriffe sind erforderlich. Die frühere Beschränkung auf `daten/` war eine Implementierungsgrenze und kein gewünschtes Produktziel. Die Bestandsbeobachtungen in Abschnitt 4.7 beziehen sich weiterhin auf den dort angegebenen ursprünglichen SHA; die Sollreichweite wird durch diese Präzisierung ersetzt (**SUPERSEDES** nur die bisherige Annahme eines ausschließlichen Datenordnerscopes).

Der neue Implementierungskandidat ergänzt einen sichtbaren Suchordner, native Ordnerauswahl, Bestätigung vor Suche außerhalb des Standardbereichs und ausdrückliche Kennzeichnung fehlender Leserechte. Er verändert keine Linux-Dateirechte. Systemseitige Ordnerfreigaben bleiben von Provowares Umfangsbestätigung getrennt. Grenzfälle und Bedienung: [Dateisuche](DATEISUCHE.md). Führender Zusatzauftrag `PV-SEARCH-01` in TODO; bestehende `PV-AUD-10/11/18` bleiben für fachliche Treffer und Öffnen zuständig. Externe Treffer sind Dateien; sie müssen nicht zu einem Provoware-Facheditor gehören.
