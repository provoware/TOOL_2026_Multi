# Iteration 30 – Codequalität der Log-Wartung

**Version:** 0.16.1  
**Datum:** 2026-09-10  
**Hauptziel:** Die interne Log-Wartung deterministischer, kohärenter und besser testbar machen, ohne das Append-only-Verhalten des normalen Ereignislogs oder fachliche Nutzerdatenpfade zu verändern.

## 1. Ausgangsbefund

`app/log_maintenance.py` vereinte mehrere Verantwortlichkeiten direkt in denselben Abläufen: Rotationsentscheidung, Zeitermittlung, Quarantäne-Serialisierung und Archivsortierung. Funktional war der Bereich abgesichert, die Kopplung erschwerte jedoch isolierte Tests und erhöhte das Risiko inkonsistenter Zeitwerte innerhalb einer einzelnen Operation.

## 2. Qualitätsziele

Die Optimierung orientiert sich an folgenden Software-Engineering-Kriterien:

- **Determinismus:** pro Wartungsoperation genau ein UTC-Zeit-Snapshot,
- **Separation of Concerns:** Rotationsentscheidung als reine, dateisystemunabhängige Logik,
- **Single Write Contract:** strukturierte Quarantänedaten über den vorhandenen atomaren JSON-Schreiber,
- **Robustheit:** Archivsortierung bleibt stabil, auch wenn Dateien zwischen Ermittlung und Sortierung verschwinden,
- **Testbarkeit:** Grenzfälle der Rotation und Zeitkonsistenz werden direkt regressionsgeprüft.

## 3. Umsetzung

- Zeitlogik zentralisiert und pro Operation auf einen gemeinsamen UTC-Snapshot begrenzt.
- Rotationsentscheidung in eine reine Hilfsfunktion ausgelagert.
- Quarantäne-JSON auf den zentralen atomaren JSON-Schreibpfad umgestellt; eigene Serialisierungslogik entfällt.
- Archivsortierung gegen parallel verschwundene Dateien robuster gemacht.
- Regressionen für Rotationsgrenzen und konsistente Quarantäne-Zeitstempel ergänzt.

## 4. Schutzgrenzen

Unverändert bleiben:

- Song-, Profil-, Todo- und Kalenderdaten,
- das normale Append-only-Ereignislog,
- Release-, Backup- und Restore-Fachlogik,
- sichtbare UI und Bedienpfade,
- externe Abhängigkeiten.

Iteration 30 ist ausschließlich eine interne Codequalitäts- und Wartbarkeitsoptimierung.

## 5. Abnahme

Geprüfter Head: `2c76d6a1ec8bd86c00125094809fcedc315775da`.

**Grundprüfung #628** vollständig erfolgreich:

- 🟢 96 Logik-/Regressionstests,
- 🟢 56 PySide6-GUI-Tests,
- 🟢 39 freigegebene Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 nativer Qt-Wayland-Smoke (`wayland`),
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `c45fa475055dfb1b5d3e5904321f4d967c96a3ea5d3f82bba46bdb6538ad574c`.

PR #40 wurde danach sicher per Squash-Merge übernommen. Resultierender Main-Commit: `20a9106616e4f32677c271906f345f02652b7cdd`.

## 6. Wirkung

Die Log-Wartung besitzt jetzt klarere Verantwortungsgrenzen, reproduzierbare Zeitsemantik und weniger duplizierte Schreiblogik. Dadurch sinkt das Risiko, dass spätere Wartungsänderungen Rotation, Quarantäne und Archivverwaltung unbeabsichtigt unterschiedlich behandeln.
