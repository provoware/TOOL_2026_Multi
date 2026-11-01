# Gemeinsamer lesender Profilzugriff für Module

Stand: 01.11.2026 · UI-05.14 · Ausgangs-main `fffb1ad10672953e785e93437f2f880fe362b6b0`.

## Abgegrenzter Auftrag

1. Im bestehenden `app.profile_store` einen Qt-unabhängigen Lesevertrag für Profile, Kategorien und Teiltextsuche festlegen.
2. Bestehende lesende Modulwege daran anbinden; Schreib-/Import-/Export-/Favoritenformate und Zufallsquelle erhalten.
3. Profilgrenzen, Fehler, Unicode, aktuelle Werte und bytegleiche Bestände isoliert prüfen; danach PR-CI und eigener main-Lauf.

Scope: zwei zusätzliche Lesefunktionen im bestehenden Store, Dashboard, Profileditor, Genre-Generator/-Archiv und lesende Favoritenauswahl; zentrale Fehlertexte, Tests, Manifest und Dokumentation. Keine zweite Datenbank, kein neuer Hintergrunddienst, kein Cache, keine Migration. Paket B ist über PR #167 integriert; PR-CI #41318751785 und main-CI #41319089428 erfolgreich. Die dort dokumentierten zwölf Zielprofile werden durch diese API nicht aktiviert.

## Schnittstellen

```python
from app.profile_store import profile_names, read_profile

names = profile_names(root)
profile = read_profile(root, "HardTechno")
genres = read_profile(root, "HardTechno", category="Genres")["Genres"]
hits = read_profile(root, "HardTechno", category="Genres", query="TECHNO")
```

`root` ist wie bei den vorhandenen Store-Funktionen ein `pathlib.Path` zum Datenwurzelverzeichnis. Die einzige Profildatei bleibt `daten/profile/db_profile.json` unter dieser Wurzel. Fehlt sie, werden die eingebetteten vier Startprofile ausschließlich im Speicher angeboten; Lesen erstellt keine Datei oder Verzeichnisse.

| Funktion / Eingabe | Verbindliches Ergebnis |
|---|---|
| `profile_names(root)` | Aktuelle Namen, nach `str.casefold` sortiert; Schreibweise erhalten. Keine automatische Zusammenführung ähnlicher oder kanonisch gleichwertiger Alt-Namen. |
| `read_profile(root, profile)` | Neues Wörterbuch mit allen fünf festen Kategorien und unabhängigen Wertelisten aus einem Ladevorgang. |
| `category=None` | Alle Kategorien in `CATEGORIES`-Reihenfolge. |
| `category="Genres"` usw. | Genau eine vorhandene Kategorie als Wörterbuchschlüssel. Die Reihenfolge der gespeicherten Werte bleibt erhalten. |
| `query=""` oder nur Leerraum/Tabulatoren | Alle Werte der gewählten Kategorien. |
| Nichtleerer Suchtext | Wörtlicher Teiltextvergleich über den bestehenden Unicode-Schlüssel: Leerraum bereinigen, Casefold und NFC. Keine regulären Ausdrücke, Kommalisten, Aliasauflösung oder unscharfe Suche. |
| Keine Treffer / leeres bekanntes Profil | Gewählte Kategorien mit leeren Listen; keine Ersatzwerte aus anderen Profilen. |
| Unbekanntes Profil/Kategorie oder falsche Typen | `ValueError`, kein stiller Rückfall auf HardTechno oder eine globale Sammlung. Suchtext mit ASCII-Zeilenumbrüchen/Steuerzeichen wird abgewiesen; Tabulatoren dienen als Leerraum. |
| Beschädigter oder nicht lesbarer Bestand | Fehler des bestehenden Ladewegs wird weitergegeben; keine Reparatur, Überschreibung oder Verdeckung durch Standardwerte. |

Profilname und Kategorie sind **exakte Schlüssel**. So kann ein Aufrufer nicht versehentlich ein ähnlich geschriebenes anderes Profil lesen; eine Auswahl aus `profile_names` liefert die richtigen Schlüssel. Nur die Suche vergleicht unabhängig von Großschreibung und kanonischer Umlautschreibweise. Beispiel: ` DÜST ` findet `Düster`; `warm, dunkel` ist ein einzelner Suchtext, keine Komma-Eingabe.

Die Rückgabe entspricht den Werten des vorhandenen Ladevalidators: keine zusätzliche Umschreibung oder Deduplizierung. Bereits vorhandene NFC-/NFD-Varianten und ihre Reihenfolge bleiben in den Ergebnissen erhalten. Änderungen an Rückgabelisten oder Namenslisten verändern weder spätere Leser noch die Datei. Jeder Aufruf liest erneut, sodass nach einer erfolgreichen Änderung neue Werte sofort sichtbar sind. Mehrere getrennte Aufrufe sind keine gemeinsame Transaktion; zusätzliche prozessübergreifende Sperren werden hier nicht eingeführt.

## Angebundene Wege

- Dashboard und Profileditor verwenden die sortierte Namensliste und den exakten Profil-/Kategorie-Lesezugriff.
- Der Generator liest alle fünf Kategorien mit einem Profilaufruf; Mengenprüfung, `random.SystemRandom` beziehungsweise explizit übergebenes `rng`, Suno-Format und Verlaufsregeln bleiben erhalten.
- Das Generatorarchiv nutzt dieselbe API für seinen Suchtext. Seine Eintragszahl entspricht jetzt den sichtbaren Treffern; die sortierte Anzeige und Sternmarkierungen bleiben erhalten. Eine technische Umlautvariante im Suchtext liefert dieselben Treffer.
- Die lesende Favoritenauswahl nimmt ihre Werte aus derselben Kategorie-API. Favoritenspeicherung und deren bisheriger Vergleichsvertrag bleiben unverändert; keine stillschweigende Änderung alter Favoritendaten.
- Bearbeitung, Export und Import verwenden weiterhin die vorhandenen Gesamtbestand-/Schreibfunktionen. `load_profiles` bleibt für bestehende Aufrufer kompatibel; es wird kein zweiter Speicherweg aufgebaut.

## Nachweise und Grenzen

Neun neue Logikregressionen: schreibfreie Standarddaten/Namensliste, Profil-/Kategorie-/Suchgrenzen, leere Ergebnisse, falsche Schlüssel/Typen/Steuerzeichen, unabhängige Rückgaben und frische Werte, unveränderte Legacy-Unicode-Varianten/Reihenfolge, beschädigte JSON-/UTF-8-/Wertetypen, Generator-/Favoriten-Grenzfälle und echter isolierter Python-Aufruf ohne geladene Qt-Module. Neuer GUI-Fall: Dashboard, Editor und Generator sehen dieselbe neue Eingabe; Unicodefilter und Trefferzahl stimmen, Profilwechsel bringt keine fremden Werte, Lesen lässt Bestandsbytes unverändert.

Die zehn neuen Fälle und bestehende Nachbarprüfungen werden vor Übertragung ausgeführt. Vollständige GitHub-CI einschließlich Wayland, UI-Evidenz, Restore und ZIP auf exakt dem Kandidaten sowie eigener main-Lauf bleiben Integrationsvoraussetzung. Lokal bekannte Umgebungsgrenzen für vollständige Audio-/Bubblewrap-Prüfungen werden nicht als bestanden umgedeutet.

Recovery: lokaler vollständiger Quell-Sicherungspunkt vor Änderung; SHA-256 im Arbeitsbericht. Keine produktiven Bestände für Prüfungen gelesen oder verändert. Änderung bei Bedarf als Codepatch rücknehmbar, kein Datenformat zurückzumigrieren. Die endgültigen CI-/Integrationsnachweise stehen im zugehörigen PR; UI-05.14 wird erst nach erfolgreicher Integration technisch abgeschlossen.

Fünf Folgeaufgaben: Dashboard-Schnelleingabe (**priorisierte Empfehlung**, voraussichtlich ein wiederverwendbares Eingabe-Widget, Dashboard-Anbindung, GUI-Regressionen und Dokumentation), Profilverwaltung vervollständigen, Datenbank-Suchansicht, einzeln geprüfte Kataloginhalte, optionaler Katalogtransfer. UI-05.15 für zusätzliche Profile/Generatorkombinationen bleibt an deren tatsächlichen Bestand gebunden; keine Katalogfreigabe durch einen API-Test.
