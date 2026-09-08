# Iteration 9 – Songbibliothek vervollständigen

## Ziel
Den bestehenden Songworkflow ohne zweites internes Datenformat um Suche/Filter, Favoriten, Bearbeitungsstatus, Sortierung/Gruppierung und eine geschützte Wiederherstellung alter Versionsstände erweitern.

## Datenbestand
Kanonische Arbeitsdatei bleibt:

```text
daten/songtexte/<Titel>.txt
```

Neue Kopfzeilen:
- `STATUS: Idee|Entwurf|Überarbeitung|Fertig`
- `FAVORIT: Ja|Nein`

Ältere Dateien ohne diese Felder bleiben lesbar. Sichere Standardwerte sind `Idee` und `Nein`.

## Suche und Filter
Freie Suche über:
- Titel,
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags.

Kombinierbare Filter:
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags,
- Status,
- nur Favoriten.

Diese Operationen verändern keine Datei.

## Sortierung und Gruppierung
Sortierung:
- zuletzt bearbeitet,
- Titel,
- Genre,
- Tags,
- Status.

Gruppierung:
- keine,
- Genre,
- Tags,
- Status.

Gruppen sind reine Ansichtscontainer in der Tabelle.

## Versionswiederherstellung
Schutzfolge:
1. Aktuellen Song wählen.
2. Versionsfenster öffnen.
3. Alten Stand auswählen und ausschließlich in der Vorschau prüfen.
4. Explizit `Diese Version wiederherstellen` auslösen.
5. Prüfen, dass aktuelle Songdatei direkt im erlaubten Songordner liegt.
6. Prüfen, dass die Version exakt im zugehörigen `.versionen/<Titel>/`-Ordner liegt.
7. Aktuellen Inhalt atomar als neuen Versionsstand sichern.
8. Gewählten alten Inhalt atomar als aktuellen Song schreiben.
9. Bibliothek neu einlesen.

Fremde Versionspfade werden vor jedem Schreibvorgang abgewiesen.

## Abnahme
- Rückwärtslesen alter Dateien ohne Status/Favorit.
- Status/Favorit speichern und wieder einlesen.
- kombinierte Suche/Filter.
- Sortier- und Gruppierlogik.
- Restore erzeugt vorher einen neuen aktuellen Sicherungsstand.
- fremde Versionspfade ändern den aktuellen Song nicht.
- echte Tk-Prüfung für Filter, Gruppierung, Editorstatus/Favorit und Restore-Schaltfläche.
- gesamte bestehende Recovery-/Diagnose-/Restore-Kette bleibt grün.

## Nicht Teil dieser Iteration
- neue fachliche Module außerhalb Songtexte,
- reale Kubuntu-Endabnahme,
- CI-Actions-Wartung. Die `actions/checkout`-Aktualisierung erfolgt bewusst als getrennte kleine Wartungsiteration.
