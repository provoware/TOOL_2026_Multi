# Iteration 32 – Managed-Window-Registry zentralisieren

**Version:** 0.16.1  
**Datum:** 2026-09-10  
**Hauptziel:** Die Menge der vom Dashboard verwalteten Fenster als gemeinsame Quelle für Erkennung, Zoom-Verteilung und selektiven Refresh zentralisieren, ohne sichtbares Nutzerverhalten zu verändern.

## 1. Ausgangsbefund

Nach der Lebenszyklus-Zentralisierung aus Iteration 31 blieb eine strukturelle Doppelung in `app/ui.py`: dieselbe Gruppe aus Songeditoren, Songbibliothek, Recovery, Profilverwaltung, Todo und Kalender wurde an mehreren Stellen erneut zusammengesetzt. Betroffen waren insbesondere `_is_managed_widget()`, `set_zoom()` und Teile von `refresh()`.

Das war funktional korrekt, erhöhte aber das Risiko, dass ein später ergänztes Fenster nur in einem dieser Pfade registriert wird.

## 2. Qualitätsziele

- **Single Source of Truth:** eine zentrale Registry beschreibt die aktuell verwalteten Nebenfenster,
- **Kohäsion:** gemeinsame Fensteraktionen verwenden denselben Bestand,
- **Explizite Semantik:** Zoom- und Refresh-Verhalten werden je Registry-Eintrag klar beschrieben,
- **Semantikerhalt:** bisherige Sonderbehandlung der Songeditoren und der selektive Dashboard-Refresh bleiben erhalten,
- **Regression Safety:** Registry-Vollständigkeit und Wirkung werden automatisiert geprüft.

## 3. Umsetzung

- `_managed_window_registry()` als zentrale Quelle der aktuell verwalteten Dashboard-Fenster eingeführt.
- `_is_managed_widget()` verwendet ausschließlich diese Registry für Ctrl+Mausrad-/Zoom-Zuordnung.
- `set_zoom()` verteilt die Zoomstufe über dieselben Registry-Einträge statt die Fenster erneut einzeln zusammenzustellen.
- `refresh()` nutzt den Registry-Vertrag mit explizitem `refresh_when_visible`; automatisch aktualisiert werden wie zuvor ausschließlich Recovery, Todo und Kalender.
- Songeditoren behalten ihren speziellen Zoom-Adapter, weil sie ihre Zoomwirkung über `zoom_percent` plus `apply_global_style()` erhalten.
- Drei neue GUI-Regressionen prüfen Registry-Vollständigkeit, Zoom-Verteilung und unveränderten Refresh-Scope.

## 4. Schutzgrenzen

Unverändert bleiben:

- sichtbare Texte, Layouts, Themes und Bedienwege,
- Song-, Profil-, Todo- und Kalenderdaten,
- Speicher-, Backup-, Restore- und Release-Fachlogik,
- externe Abhängigkeiten.

## 5. Abnahme

Geprüfter Head: `873401955bfb4805b4cdfc09c836de6818601709`.

**Grundprüfung #638** vollständig erfolgreich:

- 🟢 96 Logik-/Regressionstests,
- 🟢 62 PySide6-GUI-Tests,
- 🟢 39 freigegebene Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 nativer Qt-Wayland-Smoke (`wayland`),
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `64c3d081f652abcb29623375336c4d71b5ffd55ebce72e2c33cae64e83cef51b`.

PR #42 wurde anschließend sicher per Squash-Merge übernommen. Resultierender Main-Commit: `a0032bc7977e21d830297828610d9b6d3ac68ea3`.

## 6. Wirkung

Fenstererkennung, Zoom-Verteilung und gemeinsamer sichtbarer Refresh können für denselben verwalteten Fensterbestand nicht mehr unbemerkt auseinanderlaufen. Das senkt den Wartungsaufwand bei späteren Fensterergänzungen und macht die beabsichtigten Sonderfälle im Code explizit nachvollziehbar.
