# Iteration 39 – Autonomous UI Quality Gate PRO (Shadow Mode)

## Ziel

Wiederkehrende lokale Sichttests sollen weitgehend durch reproduzierbare automatische Prüfungen ersetzt werden. Iteration 39 führt dafür einen **nicht blockierenden Shadow-Gate** ein. Er sammelt bereits echte Evidenz, darf aber noch keinen Release wegen neu kalibrierter UI-Regeln stoppen.

## Architektur

### 1. Qt-unabhängige UI-Verträge

`app/ui_quality_contracts.py` definiert zentral:

- 8-Pixel-Hauptraster und 4-Pixel-Feinraster,
- sichere Arbeitsflächenränder,
- harte und empfohlene Mindesthöhen für Bedienelemente,
- WCAG-Kontrastberechnung,
- kritische PR-Matrix mit 8 Fällen,
- vollständige Release-Matrix mit 60 Fällen,
- deterministische Fensterzustands-Fuzzfälle,
- reproduzierbare Kriterien für eine spätere Hochstufung zum Pflicht-Gate.

Die Regeln sind bewusst ohne Qt implementiert, damit sie auch ohne grafische Sitzung geprüft werden können.

### 2. Shadow-Gate

`scripts/ui_shadow_gate.py` startet im CI echte PySide6-Fenster im Offscreen-Modus und prüft zunächst die drei kritischsten Arbeitsfenster:

- Dashboard,
- Songbibliothek,
- Songeditor.

Pro Matrixfall werden unter anderem Sichtbarkeit, Abschneiden, Geschwister-Überlappungen, Screenreader-Namen, Mindesthöhen und Rastertreue untersucht. Theme-Kontrast sowie gespeicherte Fensterpositionen werden zusätzlich unabhängig gefuzzt.

### 3. Automatische Diagnose

Der Gate erzeugt in jedem Lauf:

- `ui_shadow_evidence.json` – maschinenlesbare Evidenz,
- `ui_shadow_summary.md` – kurze menschenlesbare Zusammenfassung,
- bei Auffälligkeiten Screenshots mit 8-Pixel-Raster und markierten Problemgeometrien.

Fehler des Prüfsystems selbst werden als `infrastructure-error` gespeichert statt still zu verschwinden.

### 4. Zwei Matrizen

**Pull Requests:** 8 harte repräsentative Kombinationen.
**Main/Release:** 3 Bildschirmgrößen × 5 Zoomstufen × 4 Themes = **60 Kombinationen**.

Damit bleiben normale Änderungen schnell, während `main` die breite Matrix erhält.

### 5. Shadow statt sofortigem Hard-Gate

Der neue Schritt läuft in GitHub Actions mit `continue-on-error`. Ein roter Shadow-Befund macht also die vorhandene Iteration-39-Freigabe noch nicht rot. Die bestehenden harten Logik-, GUI-, Wayland-, Restore- und ZIP-Gates bleiben unverändert.

Die Hochstufung zum Pflicht-Gate erfolgt frühestens nach mehreren reproduzierbar sauberen Läufen, ohne bestätigte Fehlalarme und mit vollständiger Erkennung absichtlich eingebauter Testfehler.

## Sicherheitsgrenzen

- keine Änderung von Song-, Profil-, Todo- oder Kalenderformaten,
- keine automatische Änderung oder Akzeptanz von Screenshot-Baselines,
- keine automatische Reparatur produktiver Dateien,
- keine neue lokale Systeminstallation,
- Shadow-Evidenz wird als CI-Artefakt erzeugt und nicht in das Quell-Manifest zurückgeschrieben; damit entsteht kein zirkulärer Evidenz-Commit.

## Nächste Stufe

Iteration 40 soll nach Kalibrierung ergänzen:

1. tolerante visuelle Referenzvergleiche,
2. Fokus-/Tab-Reihenfolge als eigener Vertrag,
3. automatische Historienauswertung der Shadow-Evidenz,
4. Hochstufung ausgewählter Regeln zum verbindlichen Gate.
