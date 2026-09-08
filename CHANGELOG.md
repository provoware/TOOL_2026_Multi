# Änderungsverlauf

Alle relevanten Änderungen werden hier in einfacher Sprache festgehalten.

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

### Bewusst nicht umgesetzt
- keine Werkzeugfunktion erfunden,
- kein bestehender Programmcode umgebaut, da noch keiner vorhanden ist,
- kein komplexes Fehlerprotokollmodul vorgezogen, bevor eine echte Anwendung existiert.
