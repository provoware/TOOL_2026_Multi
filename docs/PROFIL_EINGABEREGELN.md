# Profilwerte: Eingabe- und Eindeutigkeitsvertrag

Stand: 01.11.2026 · Basis: `12a3ad80bd096723573287b15c32b8bc2bed5ccc`.

## Abgegrenzter Auftrag

1. Bestehende vier Startprofile und fünf feste Kategorien für diese Korrektur beibehalten: Genres (fachliche Gattungen), Stimmungen (Wirkung), Stil (Gestaltung), Stimme (Vortrag), Besonderheiten (zusätzliche Merkmale). Keine neue fachliche Taxonomie oder ungeprüften Standardinhalte einführen.
2. Neue Wertelisten, Einzelwerte, Umbenennungen und Profilimporte konsistent vergleichen; Speicherung bleibt im vorhandenen JSON-Store atomar.
3. Fehlerpfade und vorhandene Altbestände isoliert prüfen; Dokumentation, Vollprüfung und Integration gemeinsam abschließen.

Scope: Profil-Store, bestehender Import-/Umbenennungsweg, zugehörige Hilfe, Regressionstests und Dokumentation. Risiken: unbemerkte Altbestandsänderungen, Teilimport und falsche Kommatrennung. Sicherungspunkt: vollständiges Git-Archiv mit SHA-256 vor Codeänderung. Persönliche Daten werden nicht für Tests verwendet. Das fachliche Paket B einschließlich Recherche, breiter Taxonomie und Synonymregeln bleibt offen; dieser Vertrag erfüllt nur die technische Voraussetzung für die bestätigten Parserfehler.

## Regeln

- Eingabe als eine Textzeile; Werte durch Komma trennen. Äußere Leerzeichen entfernen, innere Leerraumfolgen zu einem Leerzeichen zusammenfassen. Tabulatoren werden dabei wie Leerzeichen behandelt. Zeilenumbrüche und sonstige ASCII-Steuerzeichen sind in neuen Werten ungültig.
- Ein Komma innerhalb eines Wertes durch doppelte Anführungszeichen schützen: `"warm, dunkel", ruhig` ergibt die zwei Werte `warm, dunkel` und `ruhig`.
- Ein Anführungszeichen innerhalb eines zitierten Wertes verdoppeln: `"Stimme ""nah"", weich"` ergibt `Stimme "nah", weich`. Ein Zitat beginnt am Feldanfang, gegebenenfalls nach Leerzeichen. Anführungszeichen innerhalb unzitierter Begriffe bleiben aus Kompatibilität wörtlich erhalten (`Stimme "nah"`).
- Unvollständige oder falsch abgeschlossene Zitate: ganze Aktion ablehnen, Eingabe und Bestandsdatei erhalten. Leere Teilwerte überspringen; vollständig leere Liste ablehnen.
- Neue Werte in Unicode-NFC speichern: ein Umlaut und sein aus Grundbuchstabe plus Akzent zusammengesetztes Gegenstück sind gleichwertig. Vergleich zusätzlich mit `casefold` und Leerraumbereinigung; keine Akzententfernung, keine Synonym- oder Ähnlichkeitserkennung. `schön` und `schon` bleiben verschiedene Werte.
- Eindeutigkeit gilt innerhalb eines Profils und einer Kategorie. Derselbe Begriff in anderen Profilen oder Kategorien bleibt erlaubt. Gleichwertige neue Profilnamen ablehnen.
- Bestehende Dateien beim Laden nicht nachträglich normalisieren, deduplizieren oder schreiben. Neue Ergänzungen vergleichen auch gegen alte Unicode-Schreibweisen; ein reiner Dublettenversuch schreibt nichts. Bereits vorhandene kanonische Dubletten bleiben lesbar und werden nicht automatisch zusammengeführt.
- Import: gesamten Inhalt vor dem Schreiben prüfen. Mehrdeutige Profilnamen oder Unicode-Dubletten innerhalb einer importierten Kategorie ablehnen; Zielbestand bleibt erhalten. Gleichwertige Werte im Ziel überspringen und vorhandene Schreibweise bewahren. Ein Import ergänzt, ersetzt aber keinen Altbestand. Ein alter Export mit bereits enthaltenen kanonischen Dubletten benötigt bewusste Bereinigung einer Kopie vor erneutem Import.
- Export-/Speicherformat unverändert: JSON, UTF-8, LF-Abschluss, Schema 1 beim bestehenden Profilarchiv. Es findet keine Shell-Ausführung statt.

## Abnahme und Folgequeue

Nachweis: neue Regressionen für NFC/NFD, Casefold, zitierte Kommas/Anführungszeichen, ungültige Zitate/Typen/Steuerzeichen, Profil-/Kategoriegrenzen, bytegleichen Altbestand, Importwiederholung und simuliertes Schreibversagen. Bestehende Profil-/Generator-/GUI-Tests bleiben erhalten. Vollständige GitHub-Prüfung mit eigenem main-Lauf, Wayland, Restore, ZIP und UI-Evidenz vor technischem Abschluss.

Weiterführend: fachliche Zielstruktur (**priorisierte Empfehlung**), Vorschau samt Speicherzahlen, gefilterte gemeinsame API, Dashboard-Schnelleingabe, belegter optionaler Katalogimport. Kein neues Aufgabenregister; IDs UI-05.08–05.11 und UI-05.16 bleiben im bestehenden Plan nachvollziehbar. Semantische Dubletten und Katalogerweiterung sind nicht durch diesen technischen Vergleich erledigt.


## Lokaler Prüfnachweis und Grenze

77 gezielte Logik-/GUI-/Dokumentationsprüfungen erfolgreich, darunter 15 neue Logik- und ein neuer GUI-Rückfalltest. Die lokale Vollprüfung meldete bei 418 Logiktests einen Fehler in der echten Bubblewrap-Probe; derselbe Fehler wurde auf unverändertem main `12a3ad8` reproduziert. Der gesamte lokale GUI-Lauf blieb am PulseAudio-Backend hängen und wurde durch das feste Zeitlimit begrenzt. Kein lokaler Vollprüfungs-PASS; vollständige GitHub-CI bleibt Voraussetzung. Tests und Schutzgrenzen wurden nicht abgeschwächt.
