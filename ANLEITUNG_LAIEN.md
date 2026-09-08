# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Der Schnellstart richtet bei Bedarf die abgeschirmte Python-Umgebung ein, installiert die festgelegte PySide6-Version, prüft den Start und öffnet anschließend das Programm unter Prozesswache.

## Zoom und Schriftgröße
Die Oberfläche kann ohne Einstellungsdialog vergrößert oder verkleinert werden:
- `Strg` gedrückt halten und das **Mausrad nach oben** drehen: größer.
- `Strg` gedrückt halten und das **Mausrad nach unten** drehen: kleiner.
- unten in der Statusleiste stehen zusätzlich **A−** und **A+**.
- `Strg+0` setzt wieder auf 100 % zurück.

Verfügbare Stufen: **100 %, 125 %, 150 %, 175 % und 200 %**.

Die Einstellung gilt gemeinsam für Dashboard, offene Songeditoren, Songbibliothek und Recovery. Dadurch gibt es nicht mehrere widersprüchliche Schriftgrößen.

## Reale Kubuntu/X11-Endabnahme
Für die echte Endprüfung auf dem Zielrechner gibt es einen eigenen Assistenten:

```bash
bash kubuntu_abnahme.sh
```

Er prüft zuerst automatisch:
- Linux,
- eine echte X11-Sitzung,
- KDE/Plasma,
- den Prozesswächter mit einem echten `SIGTERM`-Signal.

Der Signaltest läuft ausschließlich in einem temporären Ordner und verändert keine Song- oder Nutzerdaten.

Danach öffnen Sie über den Assistenten das Dashboard und bestätigen drei sichtbare Punkte:
1. Dark-Orange-Referenzlayout, linke Navigation, Schnellkacheln und 2×2-Hauptkarten sind korrekt sichtbar.
2. Der Tastaturfokus ist beim Wechsel mit `Tab` deutlich sichtbar und logisch.
3. Die Zoomstufen 100/125/150/175/200 % bleiben lesbar und schneiden die Hauptbedienung nicht ab.

Ein Bericht wird nur dann als **OK** markiert, wenn sowohl die automatischen Prüfungen als auch alle drei sichtbaren Punkte bestanden sind. Andernfalls steht ausdrücklich `NICHT_VOLLSTAENDIG` im Bericht.

Die Berichte liegen unter:

```text
berichte/KUBUNTU_X11_ABNAHME_*.txt
berichte/KUBUNTU_X11_ABNAHME_*.json
```

Wenn beim Start gemeldet wird, dass keine X11-Sitzung aktiv ist, bei der Anmeldung **Plasma (X11)** wählen und die Prüfung erneut starten. Wayland wird nicht still als X11 akzeptiert.

## Das neue Dashboard
Das Hauptfenster heißt **Provoware-Datenbank-Dashboard 2026**.

Die Oberfläche ist in fünf leicht erkennbare Bereiche gegliedert:
1. oben der kompakte Kopfbereich mit Suche und Logout,
2. darunter die Schnellkacheln,
3. links die Navigation,
4. in der Mitte vier große Arbeitskarten,
5. unten die Statusleiste.

Die linke Navigation kann mit **☰** schmal und wieder breit geschaltet werden.

Noch nicht freigegebene Bereiche wie Hörspiele oder Reimfinder sind bereits sichtbar. Beim Anklicken erscheint nur ein Hinweis. Sie verändern keine Dateien.

## Recovery
Recovery befindet sich bewusst nur an einer Stelle:

**Navigation → Werkzeug → Recovery**

Dort können Ereignisse nach Schweregrad und Bereich gefiltert werden. Technische Angaben bleiben zunächst eingeklappt.

## Schnellinfo
Im Dashboard gibt es das Feld **Entwicklerinfo**.

1. Kurze Information eingeben.
2. `Enter` drücken oder **Speichern** anklicken.
3. Die Information wird mit Zeitstempel an `Entwicklerinformation.txt` angehängt.

Vorhandene Einträge werden nicht überschrieben.

## Zuletzt bearbeitete Songs
Unter der Entwicklerinfo erscheinen bis zu fünf zuletzt bearbeitete Songs als kleine Schnellkacheln. Ein Klick öffnet den vorhandenen Song direkt im Songtexteditor.

Mit **Alle Songs** oder der Kachel **Songtexte** öffnen Sie die vollständige Songbibliothek.

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
Der Editor enthält:
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

Vor der Wiederherstellung sichert das Programm den aktuellen Song automatisch noch einmal als neuen Versionsstand. Erst danach wird die gewählte alte Version eingesetzt.

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

## Tastatur
- `Tab` – zum nächsten bedienbaren Element,
- `Enter` – Eingabe bestätigen oder ausgewählten Eintrag öffnen,
- `F5` – Bibliothek oder Recovery aktualisieren,
- `Ctrl+S` – Song manuell speichern,
- `Ctrl++` / `Ctrl+-` – Anzeige größer/kleiner,
- `Ctrl+Mausrad` – Anzeige größer/kleiner,
- `Ctrl+0` – zurück auf 100 Prozent,
- `Ctrl+R` – Recovery öffnen,
- `Escape` – untergeordnete Fenster schließen.

## Vollprüfung
```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung prüft die bestehende Fachlogik, Recovery, Songbibliothek, Suche/Filter, Favoriten, Status, Versionswiederherstellung, Exporte, die echten PySide6-Oberflächenwege, Zoom/Schriftgrößensteuerung, die Struktur des Referenzdashboards und die automatisierbare Kubuntu-Abnahmelogik.

## Bestehende Schutzfunktionen
- atomare Songdatei-Speicherung,
- automatische Versionssicherung vor geänderten Überschreibungen,
- Sicherung des aktuellen Songs vor einer Wiederherstellung,
- Pfadprüfung für Versionsstände,
- Logrotation und Quarantäne,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- echter SIGTERM-Wächtertest nur in Tempdaten,
- Schreibfehler-Simulation ohne echten Datenträgerverbrauch,
- vollständige ZIP-/SHA-/Restore-Prüfung.
