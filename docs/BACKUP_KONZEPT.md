# Sicherungs- und Wiederherstellungskonzept

Version 1.0 · 2026-09-08

## Ziel

Der letzte brauchbare Stand muss aus mehreren voneinander unabhängigen Wegen rekonstruierbar sein.

## Drei Ebenen

### A. Git-Verlauf
Quellcode und Entwicklungsdokumente werden in nachvollziehbaren Commits gesichert.

### B. lokaler Vorher-Sicherungspunkt
Vor riskanten Änderungen wird ein ZIP erzeugt. Es enthält den Projektbestand, aber keine virtuellen Umgebungen, Protokolle, lokalen Nutzerdaten, Transferdaten, temporären Dateien oder ältere Sicherungen.

### C. Iterations-ZIP
Nach erfolgreicher Iteration entsteht ein vollständiges ZIP mit Versions- und Statusangabe sowie SHA-256-Prüfsumme.

## Aufbewahrung lokal

Empfohlene begrenzte Rotation:
- letzte 5 Iterationssicherungen immer behalten,
- zusätzlich je 1 Tagesstand der letzten 7 Tage,
- zusätzlich je 1 Wochenstand der letzten 4 Wochen.

Die Rotation wird erst automatisiert, wenn genügend reale Sicherungen vorhanden sind; bis dahin löscht das Grundskript nichts automatisch.

## Sicherungsprüfung

Jedes ZIP erhält eine `.sha256`-Datei. Vor Wiederherstellung:
1. Prüfsumme vergleichen.
2. in neuen Ordner entpacken.
3. `scripts/pruefen.sh` ausführen.
4. erst danach den Stand als brauchbar markieren.

## Wichtiger Unterschied

Quellcode-Sicherung ersetzt keine Sicherung späterer Nutzerdaten. Sobald TOOL_2026_Multi Nutzerdaten erzeugt, erhält `nutzerdaten/` eine eigene transaktionale Sicherungsstrategie mit Wiederherstellungsprüfung.
