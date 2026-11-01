# Bestandsabgleich Profile und Datenbank · 01.11.2026

## Ziel, Stand und Grenze

Paket A aus [UI-/Profilplanung](UI_PROFIL_UNTERAUFGABEN_2026.md): Bestandsabgleich der 16 UI-05- und 11 UI-13-Unteraufgaben. Geprüfter Produktcode: main `fb45df8a37cf759592a957c5c3a3b759fa64b457`, nach Integration von PR #164. Nur Dokumentation geändert; kein zweiter Store, keine Migration, keine persönlichen Daten gelesen oder geschrieben. Test- und Fehlerproben liefen ausschließlich in temporären Verzeichnissen.

Nummerierte Kurzplanung: 1. Source und bestehende Tests abgleichen. 2. Lücken isoliert reproduzieren und Startbestand zählen. 3. README, Aufgaben, Manifest und Folgequeue gemeinsam pflegen. Risiken: unbelegte Fertigmeldung und doppelte Aufgabenregister; diese Tabelle ist der Nachweis zu den bestehenden IDs, kein neuer Auftrag.

## Nachweise

51 bestehende Prüfungen erfolgreich: `test_profile_store.py` (8), `test_profile_store_invalid_types.py` (4), `test_iteration34_core.py` (8), `test_genre_random.py` (11), `test_profile_gui.py` (4), `test_iteration34_gui.py` (5), `test_genre_random_gui.py` (2), `test_documentation_consistency.py` (9). Qt-Offscreen; keine neue reale Bildschirmabnahme.

Ergänzende echte Proben: [maschinenlesbarer Befund](PROFIL_BESTAND_2026_11_01.json). Ein erneut importierter Export meldet 0 neue Profile/0 Werte und lässt die Bestandsbytes unverändert. Derselbe Begriff in zwei verschiedenen Profilen bleibt erlaubt. Casefold-Dubletten und leere Teilwerte werden bereits übersprungen. Zitierte Kommas werden jedoch fälschlich geteilt; NFC und NFD desselben Umlautworts werden als zwei Werte angenommen. Diese beiden Befunde sind **reproduziert, nicht behoben**.

## UI-05: Zuordnung zu Source, Tests und Restumfang

„Belegt“ meint den beschriebenen vorhandenen Teilumfang. Kein Eintrag hebt Abhängigkeiten, die Gesamt-Funktionsabnahme oder CI-Gates auf. „Teilweise“ und „fehlt“ bleiben offen.

| ID | Befund | Source / Nachweis und nächste Handlung |
|---|---|---|
| UI-05.01 | Belegt im bestehenden Modell | `app/profile_store.py`: Profil → fünf feste Kategorien → Textlisten; `test_profile_store.py`. Für erweiterte Taxonomie zuerst Paket B entscheiden. |
| UI-05.02 | Belegt | `save_profiles`, `app/atomic_io.py`; Speichern/Laden und simuliertes Replace-Versagen bewahren Altbytes (`test_profile_store.py`). |
| UI-05.03 | Teilweise | `add_profile`, `app/profile_editor.py`: Anlegen/Auswählen vorhanden; Profil-Umbenennen und geschütztes Löschen fehlen. |
| UI-05.04 | Teilweise | Fünf feste `CATEGORIES` werden gespeichert/geladen; freie Kategorieverwaltung fehlt. |
| UI-05.05 | Belegt | `app/ui.py`: `db_profile_combo`; `test_profile_gui.py`: Dashboard-Profilwahl. |
| UI-05.06 | Teilweise | `ProfileEditor.create_value` speichert in gewähltes Profil/Kategorie; direkte Dashboard-Schnelleingabe mit Vorschau fehlt. |
| UI-05.07 | Belegt | `split_input_values`, `add_values`; Kommaliste/Leerwerte/Dubletten (`test_iteration34_core.py`, `test_iteration34_gui.py`). |
| UI-05.08 | Fehlt, reproduziert | `"warm, dunkel", ruhig` liefert drei statt zwei Werte. Parser-/Quotierungsvertrag vor Änderung festlegen. |
| UI-05.09 | Teilweise | JSON UTF-8, LF-Abschluss, Whitespace-Bereinigung; keine Shell-Ausführung. Unicode-Normalisierung fehlt, NFC/NFD-Probe liefert zwei Werte. |
| UI-05.10 | Teilweise | Eingabeintern `casefold`/Whitespace geprüft; kanonisch gleiche Unicode-Werte bleiben doppelt. |
| UI-05.11 | Teilweise | Bestandssuche pro Profil/Kategorie vorhanden; Unicode-Grenze wie UI-05.09. Gleiche Werte in unterschiedlichen Profilen erlaubt (Probe). |
| UI-05.12 | Teilweise | Editor meldet Zahl neuer Werte oder „alles vorhanden“; getrennte Vorschau und Anzahl übersprungener/fehlerhafter Werte fehlen. |
| UI-05.13 | Teilweise | Profil-/Kategoriefilter im Editor, Bearbeiten über `genre_random.rename_value`; keine vollständige gemeinsame Datenbank-Suchansicht. |
| UI-05.14 | Teilweise | GUI-unabhängiges `load_profiles` wird bereits geteilt; keine separate gefilterte Repository-API mit festem Vertrag. |
| UI-05.15 | Belegt im bestehenden Umfang | `genre_random.generate` nutzt ausschließlich gewähltes Profil, prüft Mengen und fehlende Werte vor Protokollierung (`test_genre_random.py`). Neue Taxonomie braucht eigenen Nachweis. |
| UI-05.16 | Teilweise | `archive_export`/`archive_import`: Merge, Fehlererhaltung und Wiederholungsimport belegt; Unicode-/Quotierungsvertrag und erweiterte Importanforderungen noch offen. |

## UI-13: Fachstruktur und Startinhalte

| ID | Befund | Source / Nachweis und nächste Handlung |
|---|---|---|
| UI-13.01 | Fehlt | Keine fachlich geprüfte Herkunfts-/Rechtedokumentation für den erweiterten Katalog nachgewiesen; verlinkte Quellen sind noch keine gelesene Recherche. |
| UI-13.02 | Teilweise | Vier Profile und fünf Kategorien benannt; gewünschte breite Taxonomie/Abgrenzung fachlich definieren. |
| UI-13.03 | Teilweise | `DEFAULT_PROFILES` ist Wiederverwendungsbasis; breite geprüfte Zielstruktur fehlt. |
| UI-13.04 | Belegt für aktuellen Startbestand | 4 × 5 = 20 Kombinationen vollständig im JSON-Befund; Zielmatrix nach Paket B erneut festlegen. |
| UI-13.05 | Teilweise | Technische Eindeutigkeit pro Profil/Kategorie über Casefold, aber kein fachlicher Synonym-/Detailtiefenvertrag. |
| UI-13.06 | Fehlt | 78 Werte insgesamt, 3–6 je Kombination; 1.922 fehlen zu 2.000 für die aktuelle Matrix. Keine Füllwerte erzeugt. |
| UI-13.07 | Teilweise | `_validate` weist Casefold-Dubletten zurück; keine NFC-/Synonymprüfung und kein vollständiger Zielkatalog. |
| UI-13.08 | Fehlt | Kein redaktioneller Nachweis je Kombination; Automatik kann fachliche Gleichheit nicht bestätigen. |
| UI-13.09 | Teilweise | Startdaten im versionierten Source, Export-Schema 1; Herkunft und eigenständige Inhaltsversion fehlen. |
| UI-13.10 | Teilweise | Wiederholungsimport des aktuellen Bestands belegt (0/0 und bytegleich); erweiterter Katalog fehlt, daher keine Gesamt-Abnahme. |
| UI-13.11 | Teilweise | Generator auf vorhandenem Profilbestand getestet; passende Ergebnisse für die zukünftige fachliche Zielmatrix noch nicht nachgewiesen. |

## Mengen des unveränderten Startbestands

| Profil | Genres | Stimmungen | Stil | Stimme | Besonderheiten | Summe |
|---|---:|---:|---:|---:|---:|---:|
| HardTechno | 4 | 4 | 4 | 3 | 3 | 18 |
| Chill | 4 | 4 | 4 | 3 | 3 | 18 |
| HipHop/Rap | 4 | 4 | 4 | 4 | 3 | 19 |
| Hörspiele | 6 | 5 | 4 | 4 | 4 | 23 |

Zählung betrifft eingebettete Standardwerte, nicht persönliche Bestände. Profilübergreifend oder zwischen Kategorien wiederverwendete Begriffe sind nicht automatisch unzulässige Dubletten. 78 ist die Zahl der Kategorieeinträge, keine Behauptung 78 global unterschiedlicher Begriffe.

## Folgequeue und Integration

Paket A für UI-05/UI-13 abgeschlossen: **27/27 IDs untersucht**, Gesamt-Paket A für weitere UI-Bereiche bleibt offen. Keine der 27 Funktionen wird allein aufgrund dieses Berichts vollständig abgehakt. Priorisierte Empfehlung: Paket B, fachliche Zielstruktur und Eindeutigkeitsregeln festlegen; danach Parser/Dubletten ergänzen, ohne Altbestände automatisch umzuschreiben. Weitere Kandidaten: Vorschau/Speicherzahlen, gemeinsame gefilterte API, Dashboard-Schnelleingabe, optionaler belegter Katalogimport. REQUIRES: Fachvertrag vor Katalogerstellung; UI-05.09 BLOCKS vollständige Unicode-Dublettenabnahme; vorhandene Stores/Generatoren wiederverwenden.

PR-Bestand: vor Integration 1 offener PR / 0 Drafts, nach geprüfter Übernahme #164 0 / 0. PR-CI [41308733154](https://github.com/provoware/TOOL_2026_Multi/actions/runs/41308733154) vollständig erfolgreich einschließlich GUI, Wayland, Restore und ZIP. Separate main-Prüfung [41310384010](https://github.com/provoware/TOOL_2026_Multi/actions/runs/41310384010) zum Integrationsstand ebenfalls vollständig erfolgreich. Für diese gemeinsame Dokumentationsnachpflege genau ein Commit ohne neuen PR vorgesehen; GitHub-main-Prüfung danach separat verfolgen. Keine öffentliche Veröffentlichung und keine vorgezogene Kubuntu-Endabnahme.


## Folgekorrektur: technischer Eingabevertrag

Die obige Tabelle und JSON-Probe bleiben historische Befunde am angegebenen Ausgangs-SHA. Die spätere [Parser-/Unicode-Korrektur](PROFIL_EINGABEREGELN.md) ergänzt UI-05.08–05.11 sowie Unicode-Vergleiche bei Import/Umbenennung. Neue Regressionstests: `tests/test_profile_input_rules.py` und `tests/test_profile_input_rules_gui.py`. Der erweiterte Fachkatalog und Paket B als Ganzes bleiben offen; endgültige CI und Integration am Kandidaten verfolgen.
