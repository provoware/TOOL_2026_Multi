# Profil sicher umbenennen

Stand 01.11.2026 · UI-05.03 (Teilumfang) · Ausgangs-main `9cf7c21ef24f22378fa3c054c50c0184496d6bec`.

## Bedienung

1. In **Profile & Vorgaben verwalten** das Profil auswählen und **Umbenennen** öffnen.
2. Neuen Namen eingeben und **Prüfen** wählen. Enter im Namensfeld prüft ebenfalls und speichert nichts.
3. Die Vorschau zeigt alten/neuen Namen, bekannte Werte sowie Favoritenzuordnungen und Verlaufseinträge zum alten oder neuen Namen. Auch eine leere Favoritenzuordnung sperrt die Änderung.
4. Nur ohne solche Bezüge wird **Umbenennen** freigegeben. Der bewusste Klick ändert ausschließlich den Profilnamen. Abbrechen und Escape schreiben nichts.

Ändern der Eingabe entwertet die Vorschau. Ändert sich eine der drei geprüften Dateien, muss erneut geprüft werden. Fehler erhalten den eingegebenen Namen. Unerwartete Datei-/Schreibfehler erscheinen mit Ereigniskennung im bestehenden JSONL-/TXT-Protokoll; bei zusätzlichem Protokollfehler wird dieser ausdrücklich angezeigt. Eingabefehler, Namenskollisionen und veraltete Vorschauen sind sichere Ablehnungen.

Dashboard, Editor und ein bereits sichtbarer Generator behalten nach Erfolg das ausgewählte umbenannte Profil. Andere Auswahlen, der Generatorfilter sowie bestehende Wert-/Anlegeentwürfe bleiben erhalten. Eine Vorschau der Dashboard-Schnelleingabe wird bei geändertem Ziel ungültig.

## Datenvertrag und Grenzen

Die Qt-freie API `preview_profile_rename(root, old_name, new_name)` liefert einen unveränderlichen Plan mit Speicherort, Namen, drei SHA-256-Leseständen und Bezug-/Wertzahlen. Sie schreibt keine Dateien und legt keinen Standardbestand an. `rename_profile(root, plan)` liest alle Dateien erneut und akzeptiert nur den gleichen Plan am gleichen Speicherort.

Geprüft werden `db_profile.json`, `genre_favoriten.json` und `zufallsverlauf.json`. Nur reguläre Dateien bis jeweils 16 MiB, gültiges UTF-8/JSON ohne doppelte Schlüssel und valide bestehende Datenformate sind zulässig. Symbolische Verknüpfungen, Verzeichnisse und FIFOs werden abgewiesen. Alte und neue Referenznamen werden mit vereinheitlichtem Leerraum, Unicode-NFC und Groß-/Kleinschreibung verglichen. Gleichwertige andere Profile, mehrdeutige alte Namen oder abweichender Leerraum im gespeicherten alten Schlüssel sperren die Änderung. Neue Namen werden NFC-normalisiert; reine Schreibweisenänderungen sind ohne Bezüge zulässig.

Nur der exakte alte Schlüssel wird ersetzt. Alle Rohwerte, unbekannten Zusatzfelder und anderen Profile bleiben semantisch unverändert; JSON-Formatierung und Schlüsselreihenfolge dürfen sich ändern. Favoriten und historische Daten bleiben bytegleich. Die vorhandene zentrale atomare Dateiersetzung schützt vor Teilständen und lässt bei fehlgeschlagenem Ersetzen die bisherige Profildatei erhalten. Es gibt keine Mehrdateienmigration.

Der reguläre Programmstart besitzt bereits einen Einzelinstanzschutz für den Datenordner. Der API-Aufrufer muss diesen Schreibschutz einhalten. Der Lesestandvergleich ist keine neue Sperre gegen beliebige externe Programme, die zwischen Prüfung und Dateiersetzung schreiben oder Pfade austauschen. Solche parallelen externen Eingriffe sind nicht Teil dieses Vertrags.

## Planung und Nachweis

1. Namensbezüge bestimmen, schreibfreie Vorschau und atomare Einzeldateiumbenennung umsetzen.
2. Bewussten Dialog mit zugänglichen, bei Zoom erreichbaren Aktionen anbinden; Modul-Auswahlen aktualisieren.
3. Negativ-/Daten-/GUI-Prüfungen, zentrale Texte, Manifest und vollständige Repository-Gates nachweisen.

Sicherung vor Änderung: `/workspace/work/profile-rename-before.tar`, SHA-256 `37e6b507c54b55d1856e3a2b727f20ab0eeb983a970886d361a19916465250fc`. Kein Produktivbestand wurde verändert. Die Regressionen verwenden ausschließlich isolierte Datenordner.

Neun neue Logiktests und acht GUI-Tests prüfen Rohdatenerhalt, Bezüge, Unicode, veraltete/gefälschte Pläne, unsichere/beschädigte Dateien, atomaren Fehlerfall, Enter/Abbrechen, echte Ereignisprotokolle und Modul-Auswahlen. Der neue Dialog wird zusätzlich innerhalb eines Tests in 40 Größen-/Zoom-/Theme-Kombinationen geprüft. Die allgemeine Dashboard-Matrix und vollständige PR-/main-CI bleiben eigenständige Gates.

Offen (REQUIRES diesen Teilumfang): sichere Mehrdateienübertragung verknüpfter Profilnamen und Abhängigkeitsvorschau vor Löschen. UI-05.03 ist damit ausdrücklich nicht insgesamt abgeschlossen. Öffentliche Veröffentlichung, abschließende Kubuntu-Gesamtabnahme und allgemeine 800×600-Dashboard-Freigabe bleiben unverändert offen.

Review-Rückfall: Beim Neuaufbau der Dashboard-Profilliste muss das umbenannte Ziel vor dem ersten Laden der Kategorienwerte ausgewählt sein. Sonst könnte ein Ausweichprofil exklusive aktuelle Werte verwerfen. Der bestehende Modul-/Entwurfstest prüft diesen zunächst reproduzierten Fehlerweg mit.
