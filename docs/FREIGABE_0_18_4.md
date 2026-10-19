# Provoware 0.18.4 – vorbereitete Versionsunterlagen

TOOL_2026_Multi / provoware/TOOL_2026_Multi. Kandidat, nicht veröffentlicht; Basis ist der geprüfte Stand von PR #88 (lokaler Baum b3272f7). Manuelle Zielrechner-Abnahmen bleiben zurückgestellt.

Fünf Aufträge in der vorgegebenen Reihenfolge:

1. Update-Staging: Runtime-ZIPs mit Paket-/Basis-SHA, Identität, Version und Manifest prüfen, ausschließlich in einen neuen getrennten Ordner entpacken und statisch prüfen. Kein Ausführen und keine Aktivierung von Paketcode.
2. Ideenarchiv: Fragmente, Tags, Herkunft, Suche, Import/Export und Komposition als Kopie. Neue Textdateien verwenden den vorhandenen Kollisionsschutz. Eigener Schutz ungespeicherter Kompositionen.
3. Accountmetadaten: URL, optionaler Profilname, E-Mail, Merkhilfe, Gruppe, Notizen und eigene Tabellenfelder. Kein Passwortfeld oder verschlüsselter Tresor; bekannte Geheimnisfelder/-URLs werden abgewiesen, Metadatenexport verlangt eine Datenschutzbestätigung.
4. Prozessstartmessung: tatsächlicher Programmeinstieg in neuen Prozessen mit eigenen synthetischen Projektordnern, ersten und wiederholten Starts sowie fester Zeitgrenze. Betriebssystem-Kaltstart bleibt unbewiesen.
5. Strukturhilfen: abschaltbare Theme-Farben für Überschriften/Aufgaben/Code und begrenzte Gliederung im Texteditor. Keine Veränderung gespeicherter Klartextzeichen oder künstliche Markierung als geändert.

Moduleinstieg: kleines Menü am Symbol oben links, zusätzlich Strg+Alt+I / Strg+Alt+A. Keine zusätzliche Sidebar-Zeile. Keine neue Bibliothek und keine persönliche Datenmigration. Die neuen regulären Modulbestände unter daten/ werden von der vorhandenen eigenständigen Datensicherung erfasst. Deren Integration wird durch isoliertes Wiederherstellen beider Bestände geprüft.

Technische Nachweise werden nach Abschluss am zugehörigen PR für den exakten Head geführt: gezielte Schutztests, Vollprüfung, große lokale Oberflächenmatrix, native Wayland-Prüfung in CI, isolierte Wiederherstellung und ZIP-Artefakte. Frühere Prüfergebnisse gehören zu ihrem damaligen Stand.

Bekannte Grenzen: kein vollständiger Update-Manager, kein Aktivierungs-/Rollbackweg, keine echte Sandbox-Ausführung von Updatecode, keine Passwortverschlüsselung oder allgemeine Geheimniserkennung in Freitext, keine kontrollierte OS-Dateicache-Leerung und keine reale Kubuntu-Abnahme. Staging-Berichte sind keine Aktivierungstickets. Persönliche Daten und Sicherungsarchive gehören nicht in den Quellcode-PR.

Ein späterer Wechsel bleibt manuell: geschlossenes Programm, persönliche Datensicherung auf getrenntem Datenträger, neue Version in einen neuen Ordner entpacken, alten Programm-/Datenbestand erhalten. Bestehende Datenordner nicht blind überschreiben.
