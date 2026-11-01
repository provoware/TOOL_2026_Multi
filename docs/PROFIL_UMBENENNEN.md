# Profil sicher umbenennen

Stand 01.11.2026 · UI-05.03 (Teilumfang) · Ausgangs-main der Bezugserweiterung `34fd6d6d0b5331e32a6b9fa6ac58693fbb0e4c0b`.

## Bedienung

1. In **Profile & Vorgaben verwalten** das Profil auswählen und **Umbenennen** öffnen.
2. Neuen Namen eingeben und **Prüfen** wählen. Enter prüft ebenfalls und speichert nichts.
3. Die Vorschau zeigt alten/neuen Namen, bekannte Werte und Favoriten-/Verlaufsbezüge. Ohne Bezüge genügt **Umbenennen**.
4. Bei Bezügen zum exakten alten Namen bewusst **Bezüge übertragen** aktivieren und erneut prüfen. Die Vorschau erklärt die gemeinsame Übertragung. Erst **Umbenennen** speichert.

Das Übertragen ist zunächst ausgeschaltet. Änderung des Namens oder der Freigabe entwertet die Vorschau. Ein inzwischen veränderter Datenbestand erfordert ebenfalls eine neue Prüfung. Abbrechen und Escape schreiben nichts. Eine Rückbenennung ist später mit demselben geprüften Ablauf möglich, sofern der ursprüngliche Zielname dann frei ist.

Bezüge zu einer anderen Schreibweise des alten Namens oder zum neuen Zielnamen bleiben gesperrt. Hier wäre eine automatische Zuordnung mehrdeutig. Es werden weder Profile noch Favoritenbestände zusammengeführt. Das gilt auch für leere Favoritenzuordnungen und Unicode-/Leerraum-/Großschreibungsvarianten.

Dashboard, Editor und sichtbarer Generator behalten das ausgewählte Profil und gewählte Dashboard-Kategorienwerte. Generatorfilter sowie vorhandene Wert-/Anlegeentwürfe bleiben erhalten. Eine Dashboard-Eingabevorschau wird beim geänderten Ziel ungültig.

## Datenvertrag

Die Qt-freie API `preview_profile_rename(root, old_name, new_name, *, transfer_links=False)` liefert einen unveränderlichen Plan mit Speicherort, drei SHA-256-Leseständen, Freigabe und Bezug-/Wertzahlen. Vorschau schreibt nicht und erzeugt keine Standarddateien. Ohne ausdrückliche Bezugfreigabe bleibt der bisherige Schutzvertrag bestehen. `rename_profile(root, plan)` akzeptiert nur einen erneut identisch geprüften Plan.

Geprüft werden `db_profile.json`, `genre_favoriten.json` und `zufallsverlauf.json`. Je Datei höchstens16 MiB, reguläre UTF-8/JSON-Dateien ohne doppelte Schlüssel und gültige bestehende Formate. Verknüpfungen, FIFOs, beschädigte/mehrdeutige Bestände und Kollisionen sperren die Änderung. Neue Namen erhalten Unicode-NFC und vereinheitlichten Leerraum; vorhandene Werte bleiben unverändert. Altschlüssel mit abweichendem Leerraum werden nicht stillschweigend bereinigt.

Nur der exakte Profilname sowie ausdrücklich freigegebene exakte Favoritenschlüssel und `profile`-Felder historischer Einträge ändern sich. Werte, Zusatzfelder, Zeitstempel, Mengen und bisherige Zufallsergebnisse bleiben semantisch erhalten. Dateien ohne betroffene Bezüge bleiben bytegleich. Geänderte Dateien dürfen eine andere JSON-Formatierung erhalten. Unverknüpfte Umbenennung nutzt weiterhin die vorhandene atomare Einzeldateiersetzung.

## Abbruchschutz und Wiederherstellung

Bei verknüpften Umbenennungen erhält der feste Profilordner vor dem ersten Bestandswechsel ein vollständig atomar veröffentlichtes, privates Wiederherstellungsjournal `.profile-rename-journal.json`. Es enthält Speicherort, feste Dateinamen, exakte Vor-/Nachherbytes als Base64 und SHA-256; Größe höchstens140 MiB. Ein zusätzlicher nicht wartender Linux-Dateilock verhindert einen zweiten kooperierenden Transaktionswriter. Der stabile Lock-Dateiname `.profile-rename.lock` bleibt nach Abschluss bestehen; seine Existenz bedeutet keine aktive Sperre.

Normale Schreibfehler führen sofort zur exakten Rücknahme. Ein Prozessabsturz lässt das Journal zurück. Solange es vorhanden ist, sperren die gemeinsamen Profil-/Favoriten-/Verlaufsleser und der zentrale Schreibweg weitere Zugriffe auf diese drei Dateien. Beim regulären Neustart wird **nach** Erwerb des vorhandenen Einzelinstanzschutzes und **vor** dem Dashboard eine offene Transaktion konservativ zurückgenommen. Erst danach darf die Anwendung Profile verwenden. Ein Warnereignis dokumentiert die erfolgreiche Rücknahme.

Vor einer Rücknahme werden alle drei aktuellen Zustände gegen die gesicherten Vor-/Nachherbytes geprüft. Unbekannte fremde Änderungen, falscher Speicherort, manipulierte Prüfsummen oder unsichere Pfade werden nicht überschrieben. Bei Konflikt bleibt der Start gesperrt. Schlägt eine Rücknahme selbst fehl, bleiben Journal und gesicherte Daten erhalten; ein weiterer Neustart kann sie fortsetzen. **Journal nicht manuell löschen.** Bei erneutem Fehler Dateien/Schreibrechte und den Ereignisbericht prüfen.

Der Commitpunkt ist das Entfernen des Journals nach allen erfolgreichen Dateiersetzungen. Es gibt keine atomare Mehrdateienoperation des Dateisystems: Der Schutz entsteht aus Journal, Zugriffssperre und Wiederherstellung. Jede Datei verwendet den bestehenden atomaren Tempdatei-/fsync-Schreibweg; Verzeichnis-fsync bleibt entsprechend dessen Plattformgrenzen bestmöglich. Es wird keine zusätzliche Garantie gegen Hardware-/Dateisystemfehler oder beliebige externe Programme behauptet. Reguläre Aufrufer benötigen weiterhin den Einzelinstanzschutz; externe Datenkopien nur bei geschlossenem Programm und ohne offenes Journal erstellen.

Unerwartete Fehler erhalten Kennung, JSONL und TXT. Ein unvollständiger Rücknahmezustand wird ausdrücklich als gesperrt bezeichnet; die Oberfläche behauptet dann keinen unveränderten Gesamtbestand. Namensvorschlag und Freigabe bleiben erhalten. Bei zusätzlichem Protokollfehler erscheint ein ehrlicher Hinweis.

## Planung und Nachweis

1. Bezugübertragung auf exakte alte Namen begrenzen; Ziel-/Aliasbezüge sperren.
2. Rücknehmbaren Dateiwechsler, Zugriffsschutz und Wiederherstellung vor Dashboardstart integrieren.
3. Bewusste Freigabe, zentrale Texte, Manifest und Daten-/Prozess-/GUI-/Repository-Gates nachweisen.

Sicherung vor dieser Erweiterung: `/workspace/work/profile-linked-before.tar`, SHA-256 `a2757aee61842adbc60e8ddbc7fa4f11719d9e5e4c65fa3a97a48cb828f01d91`. Nur isolierte Testdaten verändert. Zwölf neue Transaktions- und vier GUI-/Startregressionen einschließlich echter harter Prozessbeendigung und frischem Wiederherstellungsprozess. Vorhandene40 Dialogkombinationen prüfen zusätzlich die neue Freigabe. Vollständige CI und eigener main-Lauf bleiben Integrationsgates.

Historischer Vorgänger: unverknüpfte Umbenennung PR #170, main `34fd6d6`, PR-CI41349637821 und main-CI41350313900 grün. Dessen Review-Rückfall für exklusive Dashboard-Kategorienwerte bleibt erhalten. Vorheriger Sicherungspunkt `/workspace/work/profile-rename-before.tar`, SHA256 `37e6b507c54b55d1856e3a2b727f20ab0eeb983a970886d361a19916465250fc`.

Offen bleibt abhängigkeitssicheres Löschen; UI-05.03 ist insgesamt noch nicht abgeschlossen. Öffentliche Veröffentlichung, abschließende reale Kubuntu-Gesamtabnahme und allgemeine800×600-Dashboard-Freigabe bleiben zurückgestellt.

Erweiterung: Der vorhandene Transaktions-/Recoveryweg wird auch für [geschütztes Löschen](PROFIL_LOESCHEN.md) genutzt. Gemeinsame Startmeldungen sprechen deshalb allgemein von einer Profiländerung. Das bisher offene Löschkriterium wird durch dessen eigene PR-/main-Abnahme abgeschlossen.
