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


## Suno-kompatible Ausgabe

Der Generator erzeugt für **Suno → Create → Custom → Styles (Style of Music)** einen **reinen, durch Kommas getrennten Stiltext**. Er setzt die Kategorien in der Reihenfolge Genre, Stimmung, Stil, Stimme, Besonderheiten hintereinander – **ohne Kategorienamen**, nummerierte Listen, Markdown-Formatierung oder zusätzliche Klammern.

**Beispiel:** `Hard Techno, Industrial Techno, düster, hypnotisch, verzerrte Stimme, harte Kicks, Acid-Lines`

Die Ausgabe wird automatisch in die Zwischenablage kopiert und mit Zeitstempel protokolliert. Die Begriffe bleiben so erhalten, wie sie im Profilarchiv stehen; es wird keine unbelegte automatische Übersetzung oder musikalische Wirkung versprochen.

**Wichtig:** Anweisungen für die Liedstruktur wie `[Intro]`, `[Verse]`, `[Chorus]`, `[Bridge]` und `[Outro]` gehören in Sunos gesondertes **Lyrics-/Liedtextfeld** und nicht in das Stilfeld. Reine eckige Tags als Archiv-Zufallseintrag werden für die Stil-Ausgabe abgelehnt. Mehr als **1000 Zeichen** werden nicht stillschweigend abgeschnitten: Das Programm bittet um kleinere Mengen oder kürzere Begriffe. Die Grenze ist eine konservative Sicherheitsentscheidung für kopierbare Stiltexte, keine Garantie dafür, welche Eingabegröße eine konkrete Suno-Version zulässt.
