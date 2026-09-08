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
Oben in der Songbibliothek können Sie frei suchen. Durchsucht werden:
- Titel,
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags.

Zusätzlich können Sie mehrere Filter gleichzeitig setzen:
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Tags,
- Bearbeitungsstatus,
- **nur Favoriten**.

**Filter zurücksetzen** stellt wieder alle Songs dar.

### Sortieren und gruppieren
Sortierung ist möglich nach:
- zuletzt bearbeitet,
- Titel,
- Genre,
- Tags,
- Status.

Gruppierung ist möglich nach:
- Genre,
- Tags,
- Status.

Suchen, Filtern, Sortieren und Gruppieren verändern keine Songdatei.

## Favoriten und Bearbeitungsstatus
Im Songeditor gibt es:
- **★ Favorit**,
- **Bearbeitungsstatus** mit `Idee`, `Entwurf`, `Überarbeitung` oder `Fertig`.

Beides wird mit dem Song gespeichert und erscheint anschließend in der Bibliothek.

## Songtexteditor
Der Editor enthält weiterhin:
- Titel,
- Genre,
- Stimmung,
- Stil,
- Stimme,
- Besonderheiten,
- Tags,
- Favorit und Bearbeitungsstatus,
- Songbereiche wie Intro, Strophe, Refrain oder Bridge,
- Vorschau,
- Sonstiges.

Die Arbeitsdatei bleibt:

```text
daten/songtexte/<Titel>.txt
```

Alte Songdateien ohne Favorit oder Status können weiterhin geöffnet werden. Sie starten sicher als **Idee** und **nicht favorisiert**.

## Automatisches Speichern und Versionsstände
Gespeichert wird:
- alle 5 Minuten,
- beim Verlassen der Eingabefelder,
- mit `Ctrl+S`,
- beim Schließen des Editors,
- vor Logout.

Wenn sich der Inhalt geändert hat, wird der bisherige Stand vorher automatisch gesichert:

```text
daten/songtexte/.versionen/<Titel>/<Zeitstempel>.txt
```

Identisches Speichern erzeugt keinen neuen Versionsstand.

## Alte Version sicher wiederherstellen
1. In der Songbibliothek einen Song markieren.
2. **Versionsstände / Wiederherstellen** öffnen.
3. Einen alten Stand anklicken.
4. Den Inhalt zuerst in der Vorschau prüfen.
5. Erst dann **Diese Version wiederherstellen** anklicken.

Vor der Wiederherstellung sichert das Programm den aktuellen Song automatisch noch einmal als neuen Versionsstand. Erst danach wird die gewählte alte Version eingesetzt. So bleibt der vorherige aktuelle Inhalt erhalten und kann später wieder zurückgeholt werden.

Eine Versionsdatei aus einem falschen Ordner wird abgewiesen.

## Export
Über **Export** im Songeditor stehen bereit:
- TXT mit Metadaten,
- Markdown,
- JSON,
- Nur Songtext als TXT.

Exporte landen unter:

```text
daten/songtexte/export/
```

Die Arbeitsdatei wird beim Export nicht verändert.

## Logout
**Logout** speichert zuerst alle offenen Songeditoren. Wenn mindestens ein Song nicht gespeichert werden kann, bleibt das Programm geöffnet.

## Debug- und Recovery-Zentrale
Ereignisse können weiterhin nach Schweregrad und Bereich gefiltert werden. Technische Angaben bleiben zunächst eingeklappt.

## Tastatur
- `Tab` – zum nächsten bedienbaren Element,
- `Enter` – Schnellinfo speichern, Song öffnen oder Ereignis öffnen,
- `F5` – Bibliothek oder Recovery-Anzeige aktualisieren,
- `Ctrl+S` – Song manuell speichern,
- `Ctrl++` / `Ctrl+-` – Anzeige größer/kleiner,
- `Ctrl+0` – zurück auf 100 Prozent,
- `Escape` – Detail-, Bibliothek- oder Songeditorfenster schließen.

## Vollprüfung
```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung prüft Recovery-Funktionen, Songbibliothek, Suche/Filter, Favoriten, Status, Versionswiederherstellung, Exporte und echte Tk-Oberflächenwege.

## Bestehende Schutzfunktionen
- atomare Songdatei-Speicherung,
- automatische Versionssicherung vor geänderten Überschreibungen,
- Sicherung des aktuellen Songs vor einer Wiederherstellung,
- Pfadprüfung für Versionsstände,
- Logrotation und Quarantäne,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- Schreibfehler-Simulation ohne echten Datenträgerverbrauch,
- vollständige ZIP-/SHA-/Restore-Prüfung.
