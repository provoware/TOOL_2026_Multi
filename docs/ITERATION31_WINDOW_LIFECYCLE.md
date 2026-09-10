# Iteration 31 – Fenster-Lebenszyklus zentralisieren

**Version:** 0.16.1  
**Datum:** 2026-09-10  
**Hauptziel:** Wiederholte Lebenszykluslogik für Dashboard-Nebenfenster in einen generischen, typisierten Vertrag überführen, ohne sichtbares Verhalten zu verändern.

## 1. Ausgangsbefund

In `app/ui.py` wiederholten Profile, Todo, Kalender, Songbibliothek und Recovery denselben Grundablauf in leicht unterschiedlichen Varianten: vorhandenes Fenster prüfen, sichtbaren Zustand aktivieren und aktualisieren oder ein Fenster erzeugen beziehungsweise bewusst wiederverwenden. Diese Wiederholung erhöhte Änderungsaufwand und Divergenzrisiko.

## 2. Qualitätsziele

- **DRY / Wiederverwendung:** gemeinsamer Lebenszyklus nur an einer Stelle,
- **Typisierung:** gemeinsamer minimaler Fenstervertrag statt unstrukturierter Duplikate,
- **Semantikerhalt:** bestehende Unterschiede ausdrücklich modellieren statt vereinheitlichen, wo sie fachlich beabsichtigt sind,
- **Testbarkeit:** Lebenszyklusentscheidungen deterministisch prüfen.

## 3. Umsetzung

- `_open_managed_window()` als generischen, typisierten Helfer eingeführt.
- Sichtbare Fenster werden zentral vorbereitet, nach vorn geholt, aktiviert und aktualisiert.
- Standardmäßig bleibt die bisherige Semantik erhalten: ein nur verborgenes Profil-, Todo-, Songbibliotheks- oder Recovery-Fenster wird durch den vorgesehenen neuen Zustand ersetzt.
- Der Kalender behält ausdrücklich seine bisherige Hidden-Reuse-Semantik und kann den verborgenen Zustand wieder anzeigen.
- Suchbegriff der Songbibliothek und initiale Profil-Kategorie behalten Reihenfolge und Wirkung.
- Drei deterministische Regressionen prüfen sichtbare Wiederverwendung, standardmäßige Neuerzeugung und bewusste Wiederverwendung eines verborgenen Fensters.

## 4. Schutzgrenzen

Unverändert bleiben:

- sichtbare Texte, Layouts, Themes und Bedienpfade,
- Song-, Profil-, Todo- und Kalenderdaten,
- Speicherformate,
- Backup-, Restore- und Release-Fachlogik,
- externe Abhängigkeiten.

## 5. Abnahme

Geprüfter Head: `6f69c163b88f3d024b670298d70c755a0c1bb82d`.

**Grundprüfung #633** vollständig erfolgreich:

- 🟢 96 Logik-/Regressionstests,
- 🟢 59 PySide6-GUI-Tests,
- 🟢 39 freigegebene Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 nativer Qt-Wayland-Smoke (`wayland`),
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `8d6f15df599d92ad60be71fab18c171243cbdfbf5fb55e4d236d23cbec79819a`.

PR #41 wurde anschließend sicher per Squash-Merge übernommen. Resultierender Main-Commit: `c4df362e8518acab07d4aac987ce08b5ff7e60b6`.

## 6. Wirkung

Der gemeinsame Lebenszyklus reduziert Duplikation und macht beabsichtigte Unterschiede explizit. Neue Fensterpfade können sich künftig an denselben Vertrag halten, ohne bestehende Zustands- und Wiederverwendungsregeln still auseinanderlaufen zu lassen.
