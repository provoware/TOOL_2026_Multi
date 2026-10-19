# Modulbaukasten – Entwürfe ohne fremde Programmausführung

Über das obere Modulmenü **„Modulbaukasten · Entwürfe“** oder **Strg+Alt+E** öffnet sich ein eigener lokaler Editor. Hier lassen sich ein Titel, eine Beschreibung und bis zu zwölf Feldbezeichnungen festlegen, außerdem nur ausdrücklich angebotene Funktionen: Bearbeiten, Suchen, Import und Export. Über die Vorschau erscheint ein schreibgeschütztes Formular. Alle Entwürfe werden atomar in `daten/modulentwuerfe/bestand.json` gespeichert; Export und Import verwenden dieselben Schutzregeln wie das Wiki. Ein Import ergänzt Kopien und verändert vorhandene Vorlagen nicht.

**Sicherheitsgrenzen:** Es handelt sich um **deklarative Vorlagen**, nicht um ausführbare Plugins. Eine JSON-Datei kann niemals selbst Python-Code ausführen, Programme starten, Netzwerke öffnen oder Dateien löschen. `preview_definition()` liefert ausschließlich validierte Strukturdaten, keine Dateipfade oder Programmaufrufe. Für spätere echte Fremdplugins sind ein eigener geprüfter Ausführungskontext, Sandbox und explizite Berechtigungszustimmung erforderlich.

Die bestehenden Modul- und Oberflächenstandards (Tastatur, Zoom, Theme, Bestätigung ungespeicherter Entwürfe, JSON-Import/Export) bleiben erhalten. Die Gesamt-Kubuntu-Abnahme erfolgt erst nach vollständigem Modulaufbau.
