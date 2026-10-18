# Genres-Favoriten und GitHub-Projektübersicht

Stand: 18.10.2026 · TOOL_2026_Multi · offline / nur ein Nutzer

## A. Genres-Zufall und Monatsauswertung

**Dieser Bereich ist ausschließlich für Genres, Stimmungen, Stil, Stimme und Besonderheiten gedacht.** Er ist vollständig unabhängig von den GitHub-Projekten.

1. Im Genre-Zufall das Profil und die Kategorie wählen.
2. In der alphabetischen Liste einen Begriff markieren und mit **☆ / ★ Favorit** kennzeichnen. Ein erneuter Klick entfernt den Stern. Sterne gehören zum jeweiligen Profil und zur Kategorie.
3. **★ Nur Favoriten für die Zufallsauswahl verwenden** aktivieren. Mengen pro Kategorie wie gewohnt einstellen. Fehlen ausreichende Favoriten, erscheint eine verständliche Fehlermeldung; es werden weder Begriffe erfunden noch Protokolleinträge angelegt.
4. Bei jeder erfolgreichen Ziehung bleibt die **Suno-kompatible, kommagetrennte Ausgabe** erhalten, wird automatisch kopiert und mit Zeitstempel, Profil, Mengen und „Favoritenmodus ja/nein“ im bestehenden Zufallsverlauf gespeichert.
5. Unter **Genres-Statistik · Monatsauswertung** einen Stichtag auswählen. Mit **ⓘ Auswertung erklärt** erscheint ein Hilfefenster, mit **Monat ansehen** die TXT-Vorschau und mit **Monat als TXT exportieren** die Dateiauswahl. Das Programm schreibt den Bericht nur nach ausdrücklicher Auswahl eines Speicherorts.

Die Monatsauswertung zählt ausschließlich die Ziehungen vom Monatsanfang bis einschließlich Stichtag, inklusive Profil-, Kategorie- und Favoritenmodus-Statistik sowie häufig gezogener Begriffe. Bei rückblickenden Favoritenzählungen wird auf den **heutigen Favoritenstand** hingewiesen, weil frühere Sterne nicht rückwirkend zuverlässig rekonstruiert werden können.

Speicherorte: `daten/profile/genre_favoriten.json`, bestehender Zufallsverlauf `daten/profile/zufallsverlauf.json`. TXT-Berichte werden in der vom Nutzer ausdrücklich gewählten Datei gespeichert. Beschädigte Favoriten verhindern Änderungen, statt die Datei zu überschreiben.

## B. GitHub-Projekte (separates Modul)

Das GitHub-Modul ist **nur ein lokales Verzeichnis**. Es erstellt, synchronisiert oder löscht **keine** GitHub-Repositories online. Eine GitHub-Anmeldung ist nicht erforderlich.

- **Eingabefelder:** Projektname, GitHub-Name im Format `Eigentümer/Repository`, vollständige `https://github.com/Eigentümer/Repository`-Adresse, freie Notizen, Status **Offen/Fertig**.
- **Optionale Aufgaben:** einzeln eingeben, abhaken oder entfernen. Die Aufgaben sind *nur* diesem Projekt zugeordnet.
- **Übersicht:** Liste aller Projekte, Suchfeld, Filter Alle/Offen/Fertig und aktuelle Zähler. Auswahl lädt den Eintrag in die Eingabemaske; Speichern aktualisiert ihn.
- **Kopieren:** Eigene Schaltflächen für Projektname, Repository-Name und URL.
- **Import/Export:** JSON-Dateien; Import validiert erst den gesamten Inhalt. Bekannte Projekte werden nicht überschrieben, Konflikte brechen ohne Teilübernahme ab, Duplikate und falsche URLs werden abgelehnt.
- **Sicherheit:** Atomare Speicherung unter `daten/github_projekte.json`, Bestätigung bei Löschung und Rückfrage beim Verlassen ungespeicherter Änderungen.

Das Grundformat ist einfach und für spätere optionale Projektfelder erweiterbar. **Es enthält keine monatliche Statistik und keine automatische GitHub-Abfrage.**

## Technische und praktische Freigabe

Logik- und GUI-Rückfalltests prüfen Favoriten, Ausgabe, Monatsbericht, Import-Validierung, Einträge, Status und Zwischenablage. Alle vorherigen Pflichtprüfungen für Wayland, Sicherung/Wiederherstellung und Barrierefreiheit bleiben verbindlich.

Eine vollständige visuelle Praxisabnahme der **beiden neu ergänzten Oberflächen** bei Kubuntu und größerer Schrift ist nach der automatischen Prüfung weiterhin offen.
