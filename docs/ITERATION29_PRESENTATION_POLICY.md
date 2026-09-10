# Iteration 29 – Präsentationspolicy und Architekturhärtung

**Version:** 0.16.1  
**Datum:** 2026-09-10  
**Hauptziel:** Darstellungszustände des Dashboards deterministisch, Qt-unabhängig und mit geringer Kopplung klassifizieren sowie die Vollständigkeit des Runtime-Releases automatisch erzwingen.

## 1. Ausgangsbefund

Die visuelle Härtung der vorangegangenen Iterationen war funktional regressionsgeprüft, verteilte die Entscheidung über Darstellungszustände jedoch auf mehrere UI-Schichten:

- `app/ui_standards.py` verwaltet globale Responsive-/Zoom-Regeln,
- `app/laptop_layout.py` klassifizierte den Laptop-Kompaktmodus über private Hilfsfunktionen,
- `app/navigation_ux.py` importierte eine dieser privaten Hilfsfunktionen und ergänzte zusätzlich eine eigene Hochzoom-Bedingung.

Damit bestand **verdeckte Kopplung**: Die Navigation war von einem privaten Implementierungsdetail des Laptopmoduls abhängig. Gleichzeitig waren einzelne Schwellenwerte und Zustandsentscheidungen an Qt-Ereignisse und Modulgrenzen gekoppelt. Funktional war dieser Zustand abgesichert, architektonisch erhöhte er jedoch die Wahrscheinlichkeit späterer Divergenzen bei neuen Bildschirmgrößen, Zoomstufen oder Wayland-Skalierungsfällen.

## 2. Qualitätsmodell

Die Bewertung orientiert sich an etablierten Software-Engineering-Prinzipien:

- **Separation of Concerns:** Klassifikation des Darstellungszustands getrennt von Qt-Manipulationen.
- **Information Hiding:** Kein Modul soll private Hilfsfunktionen eines anderen UI-Moduls als Vertrag verwenden.
- **Low Coupling / High Cohesion:** Eine einzige kohärente Policy entscheidet über Laptop-, Breit- und Hochzoomzustand.
- **Determinismus:** Gleiche Messwerte müssen unabhängig von der Reihenfolge von Qt-Ereignissen denselben Zustand ergeben.
- **Single Source of Truth:** Benannte Grenzwerte statt mehrfach verteilter Zahlenwerte.
- **Testability:** Die Kernentscheidung muss ohne QApplication und ohne Eventloop testbar sein.
- **Release Completeness:** Jedes produktive Python-Modul unter `app/*.py` muss im Release-Manifest enthalten sein.

## 3. Umsetzung

### 3.1 Reine Präsentationspolicy

Neu ist `app/presentation_policy.py`. Das Modul enthält **keine Qt-Imports** und bildet Bildschirmbreite, Bildschirmhöhe, Mindestgröße und Zoom auf einen unveränderlichen `PresentationState` ab.

Zentrale benannte Grenzwerte:

- Zoom: 100–200 %,
- Laptop-Kompaktmodus: 125/150 %,
- Hochzoom ab 175 %,
- breite Dashboard-Ansicht ab 1450 px,
- Laptop-Höhengrenze 820 px,
- effektive Höhengrenze 700 px.

Der Zustand enthält explizit:

- `wide`,
- `high_zoom`,
- `laptop_compact`,
- `restricted_navigation` als abgeleitete Eigenschaft.

### 3.2 Abhängigkeiten entkoppelt

`app/laptop_layout.py` und `app/navigation_ux.py` verwenden nun dieselbe öffentliche Policy. Die Navigation importiert keine private `_is_laptop_compact()`-Funktion mehr und dupliziert die Grenze `zoom >= 175` nicht mehr.

Die bisherigen privaten Laptop-Helfer bleiben vorerst nur als kleine Kompatibilitätsadapter erhalten. Damit wird unnötiger API-Bruch vermieden, während die eigentliche Entscheidung bereits vollständig zentralisiert ist.

### 3.3 Reine Grenzwerttests

`tests/test_presentation_policy.py` prüft ohne GUI:

- sichere Zoomnormalisierung,
- 1366×768 bei 125 % als Laptop-Kompaktfall,
- 1594×926 bei 125 % als große Ansicht,
- die 1450-px-Breitengrenze,
- 175 % als Hochzoom ohne Laptop-Kompaktmodus,
- Mindestgrößen in der Klassifikation,
- Ausschluss des Dashboard-Laptopmodus für andere Fensterklassen.

Die bestehenden 56 GUI-Regressionsprüfungen bleiben unverändert als zweite Ebene bestehen. Damit werden reine Zustandslogik und tatsächliche Qt-Wirkung getrennt geprüft.

### 3.4 Release-Vollständigkeit als Invariant

Die Analyse zeigte zusätzlich eine Lücke im bisherigen Release-Gate: `scripts/veroeffentlichen.py` prüfte zuverlässig alle **im Manifest genannten** Release-Dateien, konnte aber nicht erkennen, wenn ein neues produktives `app/*.py`-Modul versehentlich gar nicht in `MANIFEST.json` eingetragen wurde.

Dafür wurde `test_all_runtime_app_modules_are_release_listed` ergänzt. Die erste CI-Ausführung blockierte dadurch korrekt, weil das neue `app/presentation_policy.py` noch nicht im Manifest stand. Erst nach Aufnahme in den Release-Bestand wurde das Gate grün.

Dieser Test schützt künftig nicht nur Iteration 29, sondern jede spätere Runtime-Erweiterung gegen denselben Verpackungsfehler.

## 4. Gefundener Fehler und Korrektur

**Erste Grundprüfung #598:** erwartungsgemäß rot ausschließlich wegen der neu eingeführten Release-Vollständigkeitsregel.

Befund:

```text
Runtime-App-Module fehlen im Release-Manifest: app/presentation_policy.py
```

Gleichzeitig bestanden bereits alle **56 GUI-Tests**. Der Fehler lag daher nicht in der sichtbaren Oberfläche, sondern in der Release-Metadatenkonsistenz.

Korrektur:

- `app/presentation_policy.py` als produktive Release-Datei aufgenommen,
- `tests/test_presentation_policy.py` als Entwicklungs-/Testdatei registriert,
- gezielte Testkommando- und Policy-Metadaten synchronisiert,
- Release-Vollständigkeitstest dauerhaft im Vollprüfpfad belassen.

## 5. Technische Abnahme vor finalem Versionssync

**Grundprüfung #600** auf dem korrigierten technischen Stand:

- 🟢 94 Logik-/Regressionstests,
- 🟢 56 PySide6-GUI-Tests,
- 🟢 39 freigegebene Betriebsdateien,
- 🟢 Headless-Start,
- 🟢 nativer Qt-Wayland-Smoke (`wayland`),
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`.

Technischer geprüfter Head: `117aa0eee4e3422804506d9bc1c1fc50f75d4591`.

## 6. Schutzgrenzen

Unverändert bleiben:

- Song-, Profil-, Todo- und Kalenderdaten,
- Datenformate und Speicherorte,
- atomare Schreibpfade,
- Backup-/Restore-Fachlogik,
- normaler backend-neutraler Start,
- Kubuntu-26.04-/Wayland-Abnahme,
- bestehende Nutzerführung und sichtbare Produktfunktionen.

Iteration 29 ist eine **interne Architektur- und Qualitätshärtung**, keine neue Produktfunktion.

## 7. Erwartete Wirkung

Die Änderung senkt vor allem das zukünftige Änderungsrisiko:

- Bildschirm-/Zoomgrenzen sind an einer Stelle nachvollziehbar,
- reine Zustandslogik kann ohne Qt-Ereignisreihenfolge geprüft werden,
- Navigation und Laptopmodus können nicht mehr still unterschiedliche Regeln entwickeln,
- ein neues Runtime-Pythonmodul kann nicht mehr unbemerkt aus dem Release herausfallen.

Die reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt trotz automatischer Tests ein separater Zielsystem-Gate.

## 8. Finales Gate

Nach Version-/Doku-/Manifest-Synchronisierung wird **derselbe vollständige Prüfweg erneut** ausgeführt. Erst bei erneut grünem Volltest, nativem Wayland-Smoke und Restore darf PR #37 gemergt werden.
