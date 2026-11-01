# Profil mit Abhängigkeitsschutz löschen

Stand 01.11.2026 · UI-05.03 · Ausgangs-main `fe0d3d0730971513235a3ba7d624994fbc7e6dcc`.

## Bedienung

1. In **Profile & Vorgaben verwalten** das gewünschte Profil wählen und **Profil löschen…** öffnen. Es wurde noch nichts entfernt.
2. **Prüfen** zeigt den exakten Profilnamen, die Zahl bekannter Werte je Kategorie, zusätzliche Feldnamen, verbleibende Profile sowie Favoritenzuordnungen und Verlaufseinträge.
3. Nur ohne solche Bezüge und mit mindestens einem verbleibenden Profil wird **Löschen bestätigen** freigegeben. Auch leere Favoritenzuordnungen und gleichwertige Unicode-/Leerraum-/Großschreibungsvarianten schützen das Profil.
4. Die Folgen lesen, **Löschen bestätigen** aktivieren und ausdrücklich **Profil löschen** wählen. Das entfernt das Profil mit allen enthaltenen Feldern. Im Programm gibt es danach keine Rückgängig-Funktion. Favoriten und Verlauf werden niemals mitgelöscht.

Abbrechen und Escape ändern nichts, auch nach gesetzter Bestätigung. Enter auf der Bestätigung löscht nicht. Erneutes Prüfen setzt die Bestätigung zurück. Ändert sich zwischen Vorschau und Ausführung eine der drei Dateien, muss erneut geprüft und bestätigt werden. Das letzte Profil bleibt geschützt; zuerst ein anderes Profil anlegen. Beschädigte oder mehrdeutige Bestände werden nicht bereinigt oder ersatzweise gelöscht.

Löschen und Schließen bleiben im Editor auch bei hohem Zoom sichtbar. Das Formular scrollt bei Platzmangel. Nach Erfolg aktualisieren sich Editor, Dashboard und sichtbarer Generator. Eine gelöschte Auswahl wechselt auf ein verbleibendes Profil; andere Auswahlen, Generatorfilter und Eingabeentwürfe bleiben erhalten. Die Dashboard-Eingabevorschau wird bei einem geänderten Ziel ungültig. Nicht gespeicherte Eingaben werden nicht automatisch auf dem neuen Ziel gespeichert.

## Daten- und Wiederherstellungsvertrag

`preview_profile_delete(root, name)` liefert einen unveränderlichen, schreibfreien Plan mit Speicherort, exaktem Profilnamen, drei SHA-256-Leseständen, Kategorie-/Feldübersicht, verbleibenden Profilen und Bezugzahlen. Fehlende Profildatei bedeutet den vorhandenen Standardbestand; Vorschau erzeugt keine Dateien. `delete_profile(root, plan)` liest erneut, akzeptiert nur denselben Plan am selben Ort und prüft die Sperren nochmals selbst.

Nur der exakte Profil-Schlüssel wird aus `db_profile.json` entfernt. Alle anderen Rohwerte, unbekannten Felder und Profile bleiben semantisch unverändert. Favoriten und Verlauf bleiben bytegleich. Die Profildatei selbst wird nicht entfernt; so erscheinen gelöschte Standardprofile beim nächsten Start nicht wieder. Bei vorher fehlender Datei wird der verbleibende Standardbestand erstmals gespeichert. Das letzte Profil wird unabhängig vom Inhalt geschützt.

Die bestehenden begrenzten Leser prüfen die drei Dateien auf gültiges UTF-8/JSON, Format, doppelte Schlüssel, reguläre Dateien bis16 MiB und sichere Pfade. Mehrdeutige ausgewählte Profilnamen sowie abweichender Leerraum im gespeicherten Zielschlüssel sperren den Vorgang. Bezüge werden mit NFC, vereinheitlichtem Leerraum und unabhängig von Groß-/Kleinschreibung verglichen. Andere Inhalte wie Songtexte verwenden bisher Werte, keinen Profilnamen als Fremdschlüssel; es gibt keine kaskadierende Löschung.

Die vorhandene [Profiltransaktion](PROFIL_UMBENENNEN.md#abbruchschutz-und-wiederherstellung) erhält Vor-/Nachherbytes vor dem Bestandswechsel. Ein gewöhnlicher Fehler nimmt den Vorgang zurück. Nach einem Prozessabbruch sperrt ein offenes Journal die gemeinsamen Profilzugriffe, bis der reguläre Neustart unter Einzelinstanzschutz vor dem Dashboard den gesicherten Vorzustand wiederherstellt. Fremde Bytes werden vor Recovery erkannt und nicht überschrieben. Bei gesperrter Rücknahme bleiben Journal und Daten erhalten; Journal nicht löschen. Der bestehende Journalname bleibt zur Kompatibilität unverändert.

Das Journal dient der Rücknahme unvollständiger Vorgänge und wird am erfolgreichen Commitpunkt entfernt. Es ist kein Papierkorb oder dauerhafter Wiederherstellungspunkt. Bei erfolgreichem Löschen ist nur eine vorher selbst erstellte Datensicherung ein Rückweg. Der API-Aufrufer benötigt weiterhin den regulären Einzelinstanzschutz. Der vorhandene zusätzliche Transaktionslock und Lesestandvergleich schützen kooperierende Writer; keine neue Garantie gegen beliebige Fremdprogramme oder Hardwarefehler.

Unerwartete Datei-/Schreibfehler erhalten Ereigniskennung, JSONL und TXT. Ein nicht vollständig zurückgenommener Zustand wird ehrlich als gesperrt beschrieben. Bestätigung und Löschfreigabe werden bei jedem Fehler aufgehoben. Falls auch das Protokoll fehlschlägt, bleiben Primärfehler und ehrlicher Zusatzhinweis sichtbar. Start-Recovery und die erneute Prüfaufforderung sprechen nun allgemein von einer Profiländerung, damit beide Operationsarten korrekt bezeichnet sind.

## Frozen Plan, Evidenz und Recovery

1. Schreibfreien Löschplan mit allen Namensbezügen, Lastprofil- und Lesestandschutz ergänzen.
2. Bewussten Dialog, erreichbare Editoraktion und Aktualisierung sichtbarer Module anbinden; vorhandene Transaktion nutzen.
3. Daten-/Fehler-/Abbruch-/GUI-/Layoutprüfungen, zentrale Texte, Manifest und Repository-Gates nachweisen.

Sicherung vor Änderung: `/workspace/work/profile-delete-before.tar`, SHA-256 `851d3b565d5638016473c954afc8210dc83c1a88e2a55a4e301c4ce876321a41`. Zehn neue Logik- und acht GUI-Regressionen. Darin40 Dialogkombinationen über zwei Größen, fünf Zoomstufen und vier Themes. Editoraktion bei100/200% geprüft, zuerst abgeschnittene Aktion durch scrollbar erreichbaren Formularbereich und feste untere Aktionen behoben; keine Prüfgrenze abgeschwächt. Ausschließlich isolierte Testdaten verwendet.

Technischer Abschluss erst nach vollständiger aktueller PR- und eigener main-CI, Wayland, UI-Log, Restore und ZIP. Damit ist das Abnahmekriterium UI-05.03 für Anlegen/Auswählen/Umbenennen und abhängigkeitssicheres Löschen umgesetzt; keine pauschale Fertigstellung der gesamten Profil-/Katalogplanung. Nächste Queue: Suchansicht, Katalogprüfung, Kachelabgleich, allgemeines800×600-Layout. Öffentliche Veröffentlichung und abschließende reale Kubuntu-Gesamtabnahme bleiben zurückgestellt.
