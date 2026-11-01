# Fachstruktur für Profile und Kataloge

Stand: 01.11.2026 · Strukturversion: 1 · Ausgangs-main: `c0b982772a51d660f4dd7ba51a5bb47ad57f9e12`.

## Auftrag und Abnahmegrenze

Paket B, UI-13.01–13.05 aus der [bestehenden Planung](UI_PROFIL_UNTERAUFGABEN_2026.md). Nummerierte Kurzplanung: 1. Quellen und Nutzungsbedingungen lesen. 2. Begriffe, Profilgrenzen, vollständige Zielmatrix und Qualitätsregeln festlegen. 3. Mengen, Verweise, Manifest und Repository-Gates prüfen. Die [maschinenlesbare Zielmatrix](PROFIL_ZIELMATRIX_2026.json) dokumentiert denselben Plan.

Diese Iteration entscheidet die fachliche Struktur für die nachfolgenden Pakete. Sie aktiviert keine neuen Profile oder Kategorien, importiert keine Inhalte und verändert weder Nutzerdaten noch Anwendungscode. Die Laufzeit behält vier Startprofile und die fünf festen Kategorien. Die zwölf Zielprofile sind Arbeitsvorgaben für einen später bewusst auswählbaren Katalog, keine zwölf bereits vorhandenen Module. Ein neuer Gegenstand außerhalb dieser Struktur erhält eine neue Strukturversion vor seiner Katalogerstellung.

## Gelesene Quellen und Ableitung

Alle folgenden Quellen am 01.11.2026 tatsächlich über den Webzugang gelesen; kurze eigene Zusammenfassungen, keine kopierten Listen oder Beschreibungstexte. Die IDs werden in der Zielmatrix wiederverwendet. Erreichbarkeit und Rechte beziehen sich auf die untersuchten Seiten und Felder, nicht auf pauschale Freigaben ganzer Websites.

| ID | Quelle | Festgestellte Aussage und Verwendung | Nutzungsgrenze für einen späteren Katalog |
|---|---|---|---|
| MB-LIST | [MusicBrainz Genre list](https://musicbrainz.org/genres) | Referenz für tatsächlich geführte Musikgenre-Namen; beliebige Tags sind damit nicht automatisch Genres. | Kein Massenimport ausgeführt; Begriffe, IDs und jeweilige Datenherkunft einzeln dokumentieren. |
| MB-DATA | [Offizielle MusicBrainz-Datenbankdokumentation](https://musicbrainz.readthedocs.io/en/latest/musicbrainz_database/) | Führt Genre-Stammdaten mit Namen, Alias, Unterscheidung und MBID unter Kerndaten; Zuordnungs-Tags stehen bei Zusatzdaten. | Dokumentiert CC0 für Kerndaten und CC BY-NC-SA 3.0 für Zusatzdaten; Datenart vor Übernahme unterscheiden. |
| MB-DUMPS | [MetaBrainz-Datensätze](https://metabrainz.org/datasets/postgres-dumps) | Bestätigt unterschiedliche Lizenzen für Kern-/Zusatzdaten der PostgreSQL-Exporte. | Kein Dump geladen. Bereitstellungsweg, Datensatzversion und konkret benötigte Felder vor Import festlegen. |
| MB-HISTORY | [MetaBrainz: Einführung der Genres, 2018](https://musicbrainz.wordpress.com/2018/11/02/musicbrainz-introducing-genres/) | Historischer Bezug zwischen Genres und Tags. | Historische pauschale Lizenzbeschreibung ist keine aktuelle Freigabe; heutige Unterscheidung in MB-DATA beachten. |
| DC-GENRE | [Discogs: Genres / Styles, Regel 9](https://support.discogs.com/hc/en-us/articles/360005055213-Database-Guidelines-9-Genres-Styles) | Obergruppen und musikalische Unterstile werden unterschieden. | Discogs-„Style“ wird fachlich der Kategorie Genres zugeordnet, nicht automatisch unserem Feld Stil. |
| DC-TERMS | [Discogs API Terms of Use](https://support.discogs.com/hc/en-us/articles/360009334593-API-Terms-of-Use) | Unterscheidet CC0-Daten, eingeschränkte Daten und API-Bedingungen. | Keine API-Anbindung oder Datennutzung beschlossen. Keine pauschale CC0-Zusage für Genrelisten, Seitentexte oder Bilder; konkreten Datenweg und Felder vor Übernahme klären. |
| ARD-FORM | [ARD Sounds: Hörspiel](https://www.ardsounds.de/rubrik/hoerspiel-112/) | Praktische Trennung von Stoffbereichen wie Krimi/Science-Fiction, Serien und Komödie; belegt Bedarf jenseits von Musikgenres. | Nur Strukturbeleg. Keine Audios, Sendungsbeschreibungen, Titel oder Bilder übernommen; keine offene Wiederverwendungslizenz festgestellt. |
| EBU-GENRE | [EBUCore: Genre](https://www.ebu.ch/metadata/ontologies/ebucore/ebucore_Genre.html) | Unterscheidet Begriffstext und Verweis auf ein Klassifikationssystem. | Methodischer Bezug für Quell-ID und fachlichen Typ; keine Ontologie oder Vokabelliste übernommen. |

Die direkten MusicBrainz-Dokumentationsseiten unter `musicbrainz.org/doc/` lieferten HTTP 429. Ihre Inhalte wurden nicht als erfolgreich abgerufen ausgegeben. Die offizielle Dokumentationsfassung auf Read the Docs und die MetaBrainz-Datensatzseite waren lesbar. Eine Discogs-Einzelstilseite lieferte HTTP 403 und ist kein Beleg. Keine Zugriffssperre umgangen. Die ältere Blogaussage und die neuere Unterscheidung von Genre-Stammdaten/Genrezuordnungen werden ausdrücklich auseinandergehalten.

## Begriffe und feste Kategorien

Ein **Profil** ist ein passend zusammengestellter Arbeitsbereich; es muss selbst kein Genre sein. **Chill** ist beispielsweise eine stimmungsbezogene Auswahl, **Film/Spielmusik** eine Verwendung. Eine **Kategorie** bestimmt, welche Art Information ein Eintrag enthält. Ein **Wert** beschreibt genau ein fachliches Konzept in dieser Profil-Kategorie-Kombination.

| Speichername, unverändert | Fachliche Bedeutung und zulässige Beispiele | Abgrenzung |
|---|---|---|
| Genres | Musikalische Gattung/Untergattung, z. B. Ambient; bei gesprochenen Inhalten Stoffgattung oder Format, z. B. Krimi oder Interview. | Jeder neue Katalogeintrag erhält einen Typ: `music_genre`, `content_genre` oder `spoken_format`. Kein Stimmungswort, Instrument oder Effekt als Musikgenre. |
| Stimmungen | Beabsichtigte emotionale Wirkung, z. B. angespannt oder gelassen. | Keine behauptete Diagnose, keine Genre- oder Geschwindigkeitsangabe allein. |
| Stil | Hörbare Gestaltung und Darstellungsweise, z. B. dialogbetont oder sparsam instrumentiert. | Kein bloß umbenanntes Genre; Discogs-Unterstile gehören nicht automatisch hierher. |
| Stimme | Klang und Vortrag, z. B. geflüstert oder mehrstimmig gesungen. | Sprecherrolle, Produktionsmodus und stimmlicher Vortrag getrennt typisieren. „Instrumental“ ist der Modus ohne Stimme, keine menschliche Stimmqualität. |
| Besonderheiten | Konkrete strukturelle, klangliche oder produktionstechnische Merkmale, z. B. wiederkehrendes Leitmotiv. | Nicht als Restablage für Genres, Stimmungen oder Synonyme verwenden. |

Beispiele erläutern die Regeln und werden nicht als geprüfter Standardkatalog gezählt. Überlieferte Mischfälle wie „Erzähler“ in Stimme, „warm“ in Stil oder „Lo-Fi“ in Genres bleiben lesbar und unverändert. Sie brauchen eine kontextbezogene redaktionelle Entscheidung vor Aufnahme in einen neuen Katalog; kein automatisches Verschieben, Löschen oder Umbenennen.

## Zielprofile und ihre Grenzen

Alle zwölf Profile verwenden dieselben fünf Speicher-Kategorien. Die Kombinationen sind fachlich nutzbar; daraus folgt nicht, dass für jede schon 100 sinnvolle Werte belegbar sind. Profilnamen mit Schrägstrich bleiben reine Datennamen, niemals Dateipfade. Die Plan-IDs dienen nur der Dokumentation und ändern keine Laufzeitkennungen.

| Plan-ID | Profilname | Arbeitsbereich / Grenze | Status |
|---|---|---|---|
| P01 | HardTechno | Harte technoorientierte Musik; Unterbereich elektronischer Musik, keine Erfindung zusätzlicher Untergenres zur Mengenerfüllung. | Vorhandener Name erhalten |
| P02 | Chill | Ruhige/entspannte Auswahl über mehrere Musikgattungen; Profilname nicht als Genrebeleg zählen. | Vorhandener Name erhalten |
| P03 | HipHop/Rap | Hip-Hop/Rap mit rhythmischem Sprechgesang und zugehörigen Produktionsweisen. | Vorhandener Name erhalten |
| P04 | Hörspiele | Fiktionale inszenierte Audiostoffe; Stoffgenre und Erzählform von Musikgenre unterscheiden. | Vorhandener Name erhalten |
| P05 | Elektronische Musik | Breites elektronisches Arbeitsprofil; Überschneidung mit P01/P02 erlaubt und dokumentiert. | Geplant |
| P06 | Pop/Rock | Pop- und rockorientierte Songs; feinere Untergattungen in Genres statt zusätzliche Wirkungsprofile. | Geplant |
| P07 | Jazz/Blues | Jazz-/Blues-orientierte Musik; echte Traditions-/Gattungsunterschiede erhalten. | Geplant |
| P08 | Akustik/Folk | Akustisch/folkgeprägte Musik; Instrumentierung allein begründet kein neues Genre. | Geplant |
| P09 | Klassik/Orchester | Kunstmusik und orchestrale Gestaltung; Ensemble, Epoche und Gattung auseinanderhalten. | Geplant |
| P10 | Film/Spielmusik | Musik für filmische/szenische/Spiel-Verwendung; Nutzungskontext kein eigener Beleg eines Musikgenres. | Geplant |
| P11 | Satire/Comedy | Satirische und komische Audio-/Textproduktionen; Vortrag, Format und Wirkung getrennt halten. | Geplant |
| P12 | Sprache/Podcast | Nichtfiktionale gesprochene Formate; Ausspielweg Podcast ist kein Musikgenre. | Geplant |

Dies ist eine projektspezifische Arbeitstaxonomie, keine behauptete universelle Musikklassifikation. Eine automatische Zuordnung vorhandener Nutzerprofile erfolgt nicht. Sprach-, Satire- und Produktionsmerkmale können in mehreren Profilen sinnvoll sein; solche Überschneidungen sind erlaubt, aber innerhalb einer Kombination darf ein Konzept nur einmal zählen.

## Vollständige Matrix und ehrliche Mengenzählung

Die JSON-Datei führt **60 Kombinationen** einzeln auf: 12 Profile × 5 Kategorien. Pflichtziel laut Auftrag: 100 fachlich unterschiedliche Werte je Kombination, insgesamt **6.000**. Die fünf Spalten dieser Übersicht entsprechen den fünf festen Kategorien; jede Zeile verweist auf fünf konkrete JSON-Matrixeinträge.

| Profil | Genres | Stimmungen | Stil | Stimme | Besonderheiten | Altbestand gesamt |
|---|---:|---:|---:|---:|---:|---:|
| HardTechno | 4 | 4 | 4 | 3 | 3 | 18 |
| Chill | 4 | 4 | 4 | 3 | 3 | 18 |
| HipHop/Rap | 4 | 4 | 4 | 4 | 3 | 19 |
| Hörspiele | 6 | 5 | 4 | 4 | 4 | 23 |
| Elektronische Musik | 0 | 0 | 0 | 0 | 0 | 0 |
| Pop/Rock | 0 | 0 | 0 | 0 | 0 | 0 |
| Jazz/Blues | 0 | 0 | 0 | 0 | 0 | 0 |
| Akustik/Folk | 0 | 0 | 0 | 0 | 0 | 0 |
| Klassik/Orchester | 0 | 0 | 0 | 0 | 0 | 0 |
| Film/Spielmusik | 0 | 0 | 0 | 0 | 0 | 0 |
| Satire/Comedy | 0 | 0 | 0 | 0 | 0 | 0 |
| Sprache/Podcast | 0 | 0 | 0 | 0 | 0 | 0 |

Die **78 eingebetteten Altwerte** wurden im Source gezählt, keine persönlichen Dateien gelesen. Rechnerisch fehlen gegenüber 6.000 zunächst 5.922 Einträge. Für den neuen Herkunfts-/Qualitätsvertrag sind bislang **0 Katalogeinträge einzeln freigegeben**, daher sind **6.000 Plätze fachlich noch unbestätigt**. Das erklärt den Unterschied zwischen Bestandsmenge und geprüfter Abdeckung; vorhandene Profile bleiben nutzbar. Für die bisherigen 20 Kombinationen bleibt das alte Mengendefizit 1.922 nachvollziehbar. Keine dieser Zahlen ist ein Importnachweis.

Besonders bei engen Genres und Stimmmerkmalen ist das 100er-Ziel nicht vorab als erreichbar nachgewiesen. Ein zu kleiner belegter Wortschatz bleibt ein offener Fehlbestand. Keine künstlichen Adjektivketten, Rechtschreibvarianten oder Kombinationen zweier bekannter Werte als zusätzliche Konzepte zählen. Eine Zieländerung wird getrennt dokumentiert; das Ziel wird hier nicht stillschweigend reduziert.

## Qualitätsvertrag für spätere Inhalte

1. **Herkunft:** Jeder neue Katalogeintrag erhält Plan-Profil, Kategorie, fachlichen Typ, bevorzugten Namen, kurze eigene Bedeutungsbeschreibung, Quell-ID/Datensatzversion, Abrufdatum und dokumentierte Rechtebasis. Ohne Nachweis bleibt er Kandidat und wird nicht importiert oder gezählt. Die Metadaten gehören zunächst in den Katalogentwurf, nicht als neue Schlüssel in die heutige Profildatei.
2. **Sprache und Detailtiefe:** Verständliche deutsche Beschreibungen; etablierte Genre-Eigennamen in Originalschreibweise möglich. Eine Angabe muss allein einen brauchbaren Unterschied beschreiben. Gegenbeispiel: „ruhig“, „sehr ruhig“ und „besonders ruhig“ sind ohne belegte Bedeutungsgrenze kein Dreierbestand. Kombinationen entstehen später im Generator, nicht zur künstlichen Katalogvermehrung.
3. **Technischer Vergleich:** Bestehenden [Eingabevertrag](PROFIL_EINGABEREGELN.md) weiterverwenden: Leerraum bereinigen, NFC und Casefold, danach nochmals NFC. Pro Profil/Kategorie eindeutig; Umlaute erhalten, keine Akzententfernung. Zitierte Kommas über den vorhandenen Parser. Keine Sonderbehandlung zur automatischen Umschreibung alter Daten.
4. **Synonyme und Aliase:** Aliase verweisen im Katalogentwurf auf genau ein bevorzugtes Konzept und zählen nicht zusätzlich. Redaktionelle Prüfung mit Bedeutungsbegründung; Schreibähnlichkeit allein reicht nicht. Beispielsweise kann eine Übersetzung ein Alias sein, zwei benachbarte Subgenres dürfen jedoch nicht pauschal verschmolzen werden. Aliaszyklen und ungeklärte Mehrfachzuordnungen blockieren die Freigabe. Aktuelle Profildateien behalten Textlisten; keine neue Aliasauflösung in dieser Iteration.
5. **Kontext und Mehrdeutigkeit:** Derselbe Text in verschiedenen Profilen oder Kategorien ist nicht automatisch eine Dublette. Innerhalb einer Kombination werden verschiedene Konzepte mit eigener Erklärung unterschieden oder ein eindeutigerer Name gewählt. „Dunkel“ als Stimmung und Klangbeschreibung erfordert jeweils eine klare Bedeutung; nicht ungeprüft beides übernehmen.
6. **Redaktionelle Freigabe:** Pro Kombination vollständige Liste, Quellenprüfung, exakter Vergleich, Synonym-/Bedeutungsprüfung und Mengenbericht. Abgelehnte Einträge mit Grund erhalten; keine pauschale Freigabe aller 78 Altwerte. Status: `candidate` → `reviewed` → `accepted`; `rejected` mit Begründung. Automatische Dublettenfreiheit ersetzt keine fachliche Prüfung.
7. **Sicherer Transfer:** Späteres Katalogpaket versioniert und auf ausdrückliche Auswahl importieren; Vorschau mit Profil/Kategorie, Neu-/Dubletten-/Fehlerzahlen, unveränderten Altwerten, atomarem Schreiben und erneutem Import ohne zusätzliche Werte. Vorher Paket G und Speichergates prüfen. Diese Regeln beschreiben spätere Akzeptanz, keine bereits implementierte Katalogfunktion.

## Status, Nachweise und nächste Iteration

UI-13.01: Strukturrecherche und Nutzungsgrenzen dokumentiert, keine allgemeine Wiederverwendungsfreigabe. UI-13.02: Begriffe und Kategorien definiert. UI-13.03: zwölf abgegrenzte Zielprofile. UI-13.04: 60 vollständige Kombinationen. UI-13.05: Sprach-, Detailtiefen-, Alias- und Eindeutigkeitsregeln. Das Paket umfasst **fünf fachliche Planungsnachweise**, keine fünf neuen Laufzeitfunktionen. UI-13.06–13.11 und die 6.000 fachlich noch unbestätigten Plätze bleiben offen. Integration und aktuelle CI werden im zugehörigen PR nachgewiesen.

Lokale Prüfung: JSON-Struktur, eindeutige Plan-IDs, Mengen, vollständiges Kreuzprodukt, Source-Übereinstimmung der 78 Altwerte, Quellverweise, Auslieferungsausschluss der Planungsdateien und interne Markdown-Verweise. Dazu bestehende Dokumentations-/Manifest-/Profilprüfungen. Keine neuen Tests für unveränderten Anwendungscode. Die vollständige Repository-CI mit Wayland, Restore und ZIP bleibt vor Integration sowie erneut auf main Pflicht. Automatische CI bestätigt keine fachliche Wahrheit aller zukünftigen Inhalte.

Recovery: autorisierter Schreibscope ausschließlich dieses Dokument, JSON-Zielmatrix, Verweise im Plan/Wegweiser, TODO, Änderungsverlauf und Manifest. Ausgangsbaum entspricht main-Dateibaum `9c61a0e34be78f1f6e261164695d3d97b3e0b7ad`; Sicherung vor Änderung im Arbeitsbereich mit SHA-256. Keine Anwendung, Texte oder Daten geändert. Rücknahme durch Entfernen des Dokumentationspatches; keine Datenmigration rückgängig zu machen.

Fünf Folgeaufgaben: gemeinsame gefilterte Modul-API (**priorisierte Empfehlung**, voraussichtlich 1 Logikdatei, 1 Testdatei und Dokumentation), Dashboard-Schnelleingabe, Profilverwaltung vervollständigen, geprüfte Katalogeinträge pro Kombination, optionalen Katalogtransfer abnehmen. UI-05.12 ist seit PR #166 auf main mit eigener CI integriert und wird nicht erneut implementiert.
