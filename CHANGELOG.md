# Änderungsverlauf

Alle relevanten Änderungen werden hier in einfacher Sprache festgehalten.

## 0.3.0 – 2026-09-08 – Regression, Start, Standards und Release

### Behoben
- `LOG-FEHLER-001`: `EventLogger.recent(0)` gab wegen Python-Slicing `[-0:]` unerwartet alle Ereignisse zurück.
- `REG-LOG-001` sichert den Fehler dauerhaft ab; der unmittelbare Nachbarweg `recent(1)` besitzt einen eigenen Test.
- Der Rückfallfall wechselt im Register nachvollziehbar von **OFFEN** auf **BEHOBEN**.

### Hinzugefügt
- globale Oberflächenstandards für Farben, Abstände, Schriften und Ampellogik,
- grafische Startanzeige mit fünf echten Checkpoints und Konsolenfallback,
- getrennte Prüfmodi `--runtime` und `--full`,
- manifestgesteuerter Release-Builder, der ausschließlich `release: true` markierte Dateien übernimmt,
- Pfadschutz, ZIP-Inhaltsprüfung und SHA-256 für Veröffentlichungen,
- `INFO_DATEIEN_AGENT` für belegabhängige Aktualisierung der zentralen Informationsdateien,
- Release- und Regressionstests im vollständigen Prüfablauf.

### Effizienz
- `pip` wird nicht mehr bei jedem Start aufgerufen, wenn `requirements.txt` keine externen Pakete enthält,
- bei späteren externen Anforderungen wird ein unveränderter Requirements-Stand über Prüffingerabdruck wiederverwendet,
- der normale Schnellstart führt nur die Laufzeitprüfung aus; Entwicklertests bleiben dem vollständigen Prüfweg vorbehalten.

## 0.2.0 – 2026-09-08 – Debug/Log und Rückfallschutz

### Hinzugefügt
- ausführbares Dashboard mit den letzten fünf Ereignissen,
- Menüpunkt **Debug/Log** mit verständlicher Detailansicht,
- eindeutige Ereigniskennungen und parallele JSONL-/TXT-Ausgabe,
- zentrale Ausnahmebehandlung für Start und Oberfläche,
- datensparsame Erkennung wiederkehrender Fehlermuster,
- gezielte automatische Rückfalltests.

### Schutzgrenzen
- keine automatische Veränderung von Nutzerdaten oder Programmcode,
- beschädigte einzelne Protokollzeilen blockieren die Anzeige nicht,
- harte Prozessabbrüche benötigen später einen getrennten Wächter.

## 0.1.0 – 2026-09-08 – Entwicklungsgrundlage

### Hinzugefügt
- verbindliches autonomes Entwicklungsregelwerk,
- klare Trennung von Anwendung, Basisdaten, Texten, Tests, Dokumentation, Protokollen und Sicherungen,
- Sicherungs- und Wiederherstellungsregeln mit Prüfsumme,
- Regeln für Fehlerprävention, Fehlerbehandlung und Rückfalltests,
- endlicher lokaler Prüfablauf,
- vorbereitetes Schnellstart-Skript,
- maschinenlesbares Manifest,
- versionierte Textregistrierung,
- GitHub-Prüfablauf für strukturelle Grundprüfungen.
