# Iteration 11 – PySide6-Referenzdashboard

## Ziel
Die gesamte produktive GUI wird einheitlich mit **PySide6** umgesetzt. Das Dashboard wird in Struktur, Proportion, Dichte, Farbkontrast und visueller Hierarchie an den bereitgestellten Provoware-Referenzentwurf angeglichen.

## Referenzmerkmale
- kompakter Header mit Provoware-Titel und Suche,
- horizontale Schnellkachelleiste,
- links feste, einklappbare Navigation,
- schmale Zeile „Zuletzt bearbeitet“,
- 2×2-Hauptfläche aus gleichwertigen Karten,
- kompakte Statusleiste,
- Dark-Orange-Industrial-Farbwelt,
- dunkles Blau/Schwarz als Grundfläche,
- Orange `#FF9800` als einziger dominanter Akzent,
- feine Konturen statt starker Schatten.

## Wahrheitsgemäße Technikangaben
Der Referenzentwurf nennt PyQt6/PySide. Die reale Anwendung verwendet ausschließlich:

```text
PySide6==6.11.2
```

PyQt6 und PySide6 werden nicht gemischt.

## GUI-Migration
Auf PySide6 umgestellt:
- `app/main.py`,
- `app/ui.py`,
- `app/ui_standards.py`,
- `app/song_editor.py`,
- `app/song_library.py`,
- `app/recovery_center.py`,
- `scripts/start_status.py`.

Die fachliche Song-/Datei-/Recovery-Logik bleibt in den bestehenden framework-unabhängigen Modulen erhalten.

## Recovery
Recovery ist in der Dashboard-Hauptansicht **genau einmal** vorhanden:

```text
Navigation → Werkzeug → Recovery
```

Keine Recovery-Tabelle in der Startansicht, kein zweiter Header-Knopf und kein zusätzliches Debug-Menü.

## Schutz bestehender Funktionen
Die GUI-Migration darf folgende geprüfte Funktionen nicht verlieren:
- Entwickler-Schnellinfo append-only,
- letzte Songs als Schnellkacheln,
- Songbibliothek,
- Suche/Filter/Sortierung/Gruppierung,
- Favoriten und Bearbeitungsstatus,
- Song-Metadaten,
- Autosave alle 5 Minuten,
- Speichern bei Fokusverlust und beim Schließen,
- Versionierung und geschützter Restore,
- TXT/Markdown/JSON/Nur-Songtext-Export,
- Recovery-Filter und Ereignisdetails,
- Zoomstufen 100/125/150/175/200,
- Prozesswache, Logging, Datenschutz und Restore-Gate.

## Referenzprüfung
`tests/test_dashboard_reference_gui.py` prüft unter Qt-Offscreen:
- Fenstertitel,
- Dark-Orange-Akzent,
- linke Sidebar und deren Breiten,
- sieben Schnellkacheln,
- vier 2×2-Hauptkarten,
- annähernd gleiche Kartenabmessungen,
- genau einen Recovery-Dashboardeintrag,
- Ein-/Ausklappen der Navigation,
- keine produktive Tkinter-GUI in den migrierten Dateien.

Zusätzlich laufen alle bisherigen Song-, Recovery-, Sicherheits-, Release- und Restore-Tests weiter.
