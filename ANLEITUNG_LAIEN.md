# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Die Startprüfung, Prozesswache und Recovery-Schutzwege bleiben aktiv.

## Schnellinfo im Dashboardheader
Oben im Dashboard gibt es das Feld **Entwickler-Schnellinfo**.

1. Kurze Information eingeben.
2. `Enter` drücken oder **Speichern** anklicken.
3. Die Information wird mit Zeitstempel an `Entwicklerinformation.txt` angehängt.

Vorhandene Einträge werden nicht überschrieben.

## Zuletzt bearbeitete Songs
Unter dem Dashboardheader erscheinen bis zu fünf zuletzt bearbeitete Songs als Schnellkacheln. Ein Klick öffnet den vorhandenen Song direkt im Songtexteditor.

Mit **Alle Songs** oder **Songbibliothek** öffnen Sie die vollständige Songliste.

## Songbibliothek
Die Bibliothek zeigt:
- Titel,
- Genre,
- letzte Bearbeitungszeit,
- Anzahl älterer Versionsstände.

Ein Song lässt sich per Doppelklick, `Enter` oder **Song öffnen** bearbeiten.

Mit **Versionsstände ansehen** öffnen Sie ältere Stände nur zur Ansicht. Der aktuelle Song wird dadurch nicht verändert.

## Songtexteditor
Der Editor enthält:
- **Titel** – bestimmt den Namen der Arbeitsdatei,
- **Genre** – optional,
- **Stimmung** – optional,
- **Stil** – optional,
- **Stimme** – optional,
- **Besonderheiten** – optional,
- **Tags** – optional, durch Kommas getrennt,
- Songbereiche wie Intro, Strophe, Refrain oder Bridge,
- **Vorschau** des vollständigen Songs,
- **Sonstiges** für zusätzliche Hinweise.

Die Arbeitsdatei liegt weiterhin unter:

```text
daten/songtexte/<Titel>.txt
```

Alte Songdateien aus Version 0.7.0 können weiterhin geöffnet werden.

## Automatisches Speichern und Versionsstände
Gespeichert wird:
- alle 5 Minuten,
- beim Verlassen der Eingabefelder,
- mit `Ctrl+S`,
- beim Schließen des Editors,
- vor Logout.

Wenn sich der Inhalt seit dem letzten Speichern geändert hat, wird der bisherige Stand vorher automatisch gesichert:

```text
daten/songtexte/.versionen/<Titel>/<Zeitstempel>.txt
```

Wenn sich nichts geändert hat, entsteht kein unnötiger Versionsstand.

## Export
Über **Export** im Songeditor stehen bereit:
- **TXT mit Metadaten**,
- **Markdown**,
- **JSON**,
- **Nur Songtext (TXT)** ohne Titel-, Genre- oder andere Metadaten.

Exporte landen unter:

```text
daten/songtexte/export/
```

Die Arbeitsdatei wird beim Export nicht verändert.

## Logout
**Logout** speichert zuerst alle offenen Songeditoren. Wenn mindestens ein Song nicht gespeichert werden kann, bleibt das Programm geöffnet.

## Debug- und Recovery-Zentrale
Ereignisse können weiterhin nach Schweregrad und Bereich gefiltert werden. Ereignisdetails lassen sich per Doppelklick, `Enter` oder Schaltfläche öffnen. Technische Angaben bleiben zunächst eingeklappt.

## Tastatur
- `Tab` – zum nächsten bedienbaren Element,
- `Enter` – Schnellinfo speichern, Song öffnen oder Ereignis öffnen,
- `F5` – Recovery-Anzeige aktualisieren,
- `Ctrl+S` – Song manuell speichern,
- `Ctrl++` / `Ctrl+-` – Anzeige größer/kleiner,
- `Ctrl+0` – zurück auf 100 Prozent,
- `Escape` – Detail-, Bibliothek- oder Songeditorfenster schließen.

## Vollprüfung
```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung prüft Recovery-Funktionen, Songbibliothek, Metadaten, Versionen, Exporte und echte Tk-Oberflächenwege. Ohne virtuelle oder echte grafische Sitzung wird der GUI-Teil nicht als bestanden ausgegeben.

## Bestehende Schutzfunktionen
- atomare Songdatei-Speicherung,
- automatische Versionssicherung vor geänderten Überschreibungen,
- Logrotation und Quarantäne beschädigter Zeilen,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- Schreibfehler-Simulation ohne echten Datenträgerverbrauch,
- vollständige ZIP-/SHA-/Restore-Prüfung.
