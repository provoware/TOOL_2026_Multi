# Ordnerstruktur – einfach erklärt

Stand der Dokumentation: 17.10.2026

Diese Übersicht erklärt, welche Dateien zum Programm gehören und welche Ordner persönliche Daten enthalten.

| Ordner / Datei | Bedeutung | Empfehlung |
|---|---|---|
| `app/` | Hier steht der eigentliche Programmcode. | Nicht ändern, wenn du nur das Programm benutzen möchtest. |
| `daten/` | Hier speichert das Programm Texte, Songtexte, Profile, Aufgaben und Termine. | **Regelmäßig separat sichern.** |
| `daten/notizen/` | Neue Projekt-Notizen und ausdrücklich bestätigte Altkopien. | Mit dem gesamten Datenordner sichern. |
| `Entwicklerinformation.txt` | Möglicher alter Notizbestand im Projektstamm. | Erst bestätigte Kopien unter `daten/notizen/` sind im Daten-ZIP; Original erhalten. |
| `texte/` | Allgemeine sichtbare Texte des Programms. | Für normalen Betrieb unverändert lassen. |
| `vorlagen/` | Vorgefertigte Beispiele, zum Beispiel für Songtexte. | Nach Bedarf als Vorlage verwenden. |
| `scripts/` | Werkzeuge für Prüfung, Diagnose und Veröffentlichung. | Nur bei Bedarf benutzen. |
| `tests/` | Automatische Kontrollen für Entwickler. | Für normale Nutzung nicht nötig. |
| `docs/` | Technische Informationen und ältere Entwicklungsberichte. | Als Nachschlagewerk nutzen. |
| `agents/` | Regeln zur Pflege der Projektinformationen. | Für die Weiterentwicklung bestimmt. |
| `logs/` | Lokale technische Protokolle. | Bei Fehlern hilfreich, nicht öffentlich hochladen. |
| `berichte/` | Lokal erzeugte Diagnoseergebnisse. | Können private Informationen enthalten. |
| `backups/` | Lokal erzeugte Sicherungen. | Auf einem *zweiten* Datenträger zusätzlich sichern. |
| `.venv/` | Automatisch eingerichtete Python-Umgebung. | Nicht selbst bearbeiten. |
| `tmp/` | Vorübergehende Arbeitsdateien. | Nicht als persönliche Sicherung verwenden. |
| `schnellstart.sh` | Normaler Programmeinstieg. | Mit `bash schnellstart.sh` starten. |
| `ANLEITUNG_LAIEN.md` | Einfache Bedienanleitung. | Bei Unsicherheit hier anfangen. |
| `MANIFEST.json` | Technische Liste der zum Programm gehörenden Dateien. | Nicht manuell ändern. |

## Was kommt in eine Veröffentlichung?

Nur die für den Betrieb notwendigen Dateien. Tests, Entwicklerberichte, lokale Protokolle und private Nutzerdaten gehören normalerweise **nicht** in öffentlich verteilte Programmpakete. Welche Dateien tatsächlich im Betriebspaket enthalten sind, bestimmt `MANIFEST.json`; ein veröffentlichtes Projekt-Gesamt-ZIP kann einen anderen Zweck haben.

## Was darf ich aufräumen?

**Nicht blind löschen:** `daten/`, `backups/`, `berichte/` und `logs/`. Dort könnten persönliche Texte, Sicherungen oder wichtige Fehlerspuren liegen.

Historische Berichte unter `docs/ITERATION*.md` bleiben erhalten. Sie dokumentieren Entscheidungen und Prüfergebnisse. Ihr Alter allein ist **kein Grund zum Löschen**.

## Persönliche Daten sichern

1. Programm beenden.
2. Den kompletten Ordner `daten/` kopieren.
3. Die Kopie außerhalb des Projektordners auf einem zweiten Datenträger ablegen.
4. Stichprobenartig prüfen, ob deine wichtigen Texte in der Kopie vorhanden sind.

Eine erfolgreiche automatische Projekt-ZIP-Prüfung beweist nicht, dass die gerade vorhandenen privaten Texte unabhängig gesichert wurden.
