# Genres-Zufallsgenerator – Fach- und Bedienkonzept

**Programm:** TOOL_2026_Multi · **Ziel:** Single User, lokal/offline, PySide6/Kubuntu

## Profile und Archiv
- Die vorhandenen fünf Kategorien werden direkt aus `app.profile_store.CATEGORIES` übernommen: **Genres, Stimmungen, Stil, Stimme, Besonderheiten**.
- Die Beispielprofile **HardTechno, Chill, Hörspiele** gelten für neue Projektprofile; bestehende gespeicherte Profile bleiben unangetastet.
- Ein Komma trennt mehrere Begriffe; jeder Begriff wird einzeln, bereinigt und ohne Dopplungen gespeichert. Vergleiche ignorieren Groß- und Kleinschreibung.
- Archiveinträge können gesucht, alphabetisch angezeigt, hinzugefügt, umbenannt und nach Bestätigung entfernt werden.
- JSON-Import validiert zunächst **alle** Einträge und ergänzt nur neue, einzigartige Werte in einem atomaren Speichervorgang. Ein beschädigter Import verändert keine vorhandenen Profile. Export speichert die aktuelle Sammlung atomar.

## Zufall und Vorlagen
- Ein Profil und die Mengen je Kategorie müssen vor der Generierung feststehen. Ein Mengenwert **0** lässt die entsprechende Kategorie aus.
- Für jede Kategorie stehen die Tasten **3, 6, 9, 12, 15** und eine manuelle Einstellung zur Verfügung.
- Es gibt **drei dauerhaft gespeicherte Mengenvorlagen**. Jede kann geladen oder überschrieben werden.
- Es werden nur vorhandene Werte ausgewählt, **ohne Wiederholung innerhalb der Gesamtausgabe**. Reichen die Werte nicht, folgt ein konkreter Fehler statt eines verfälschten Ergebnisses.
- Jede erfolgreiche Generierung wird mit Ortszeit-Zeitstempel, Profil, Mengen, Kategorien und kommagetrennter Ausgabe unter `daten/profile/zufallsverlauf.json` gespeichert. Das Ergebnis wird zugleich in die Systemzwischenablage kopiert.

## Wiederverwendbarkeit
- `app.genre_random` enthält ausschließlich allgemein verwendbare Funktionen ohne GUI-Abhängigkeit.
- Dashboard und Songeditor öffnen dieselbe Oberfläche `app.genre_random_window.GenreRandomWindow` und verwenden die bestehenden Profilbestände.
- Alle Daten bleiben lokal; keine Anmeldung oder Onlineverbindung.

## Prüfgrenzen
Automatisch geprüft werden: Mengen, Duplikate, Import und Beschädigungsschutz, Vorlagen, dauerhafter Verlauf, Zwischenablage und GUI-Aufruf. Die vollständige **visuelle Praxisabnahme der neuen Oberfläche** (Zoom 100–200 %, Lesbarkeit, Abstände und Bedienfluss) ist weiterhin erforderlich und ausdrücklich nicht durch automatische Tests ersetzt.

Noch nicht enthalten sind eine vollständige JSON-Historienexportoberfläche oder eine frei gestaltbare Mischlogik, die kategoriale Dubletten durch neue Profileinträge automatisch ersetzen könnte. Das System gibt in solchen Fällen einen verständlichen Fehler aus.
