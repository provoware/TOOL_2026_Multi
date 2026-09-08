# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Der Schnellstart richtet bei Bedarf die abgeschirmte Python-Umgebung ein, installiert die festgelegte PySide6-Version, prüft den Start und öffnet anschließend das Programm unter Prozesswache.

### Wenn Provoware schon läuft
Pro Projektordner darf nur ein schreibendes Dashboard gleichzeitig laufen. Wird Provoware versehentlich ein zweites Mal gestartet, erscheint ein verständlicher Hinweis und der zweite Start wird beendet. Der bereits geöffnete Stand läuft unverändert weiter. Dadurch können zwei Prozesse nicht gegenseitig neuere Änderungen überschreiben.

### Einheitlicher Speicherschutz
Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien verwenden denselben geschützten Schreibweg. Neue Daten werden zuerst vollständig in eine eindeutige temporäre Datei geschrieben und geprüft. Erst danach ersetzt das Programm den bisherigen Stand atomar. Ein Fehler vor diesem letzten Schritt lässt den vorherigen Bestand erhalten. Temporäre Reste werden entfernt.

## Zoom und Schriftgröße
Die Oberfläche kann ohne Einstellungsdialog vergrößert oder verkleinert werden:
- `Strg` gedrückt halten und das **Mausrad nach oben** drehen: größer.
- `Strg` gedrückt halten und das **Mausrad nach unten** drehen: kleiner.
- unten in der Statusleiste stehen zusätzlich **A−** und **A+**.
- `Strg+0` setzt wieder auf 100 % zurück.

Verfügbare Stufen: **100 %, 125 %, 150 %, 175 % und 200 %**.

Die Einstellung gilt gemeinsam für Dashboard, offene Songeditoren, Songbibliothek, Recovery, Profilverwaltung, Todo-Liste und Kalender. Dadurch gibt es nicht mehrere widersprüchliche Schriftgrößen.

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

Unter **Planung** finden Sie jetzt **Todo-Liste** und **Kalender**.

Noch nicht freigegebene Bereiche wie Hörspiele oder Reimfinder sind bereits sichtbar. Beim Anklicken erscheint nur ein Hinweis. Sie verändern keine Dateien.

## Kalender
Öffnen über:

**Navigation → Planung → Kalender**

Links sehen Sie einen Kalender zum Auswählen des Bezugsdatums und darunter die Eingabe für neue Termine. Rechts stehen vier Ansichten:
- **Tag** – nur der gewählte Tag,
- **Woche** – Montag bis zum folgenden Montag,
- **Monat** – der vollständige gewählte Monat,
- **Jahr** – das vollständige gewählte Jahr.

Ein Termin über Mitternacht erscheint in allen Zeitbereichen, die er tatsächlich berührt.

### Termin anlegen
1. Titel eingeben. Der Titel ist Pflicht.
2. Optional eine Notiz eintragen.
3. Beginn mit Datum und Uhrzeit wählen.
4. Ende mit Datum und Uhrzeit wählen. Das Ende muss nach dem Beginn liegen.
5. Optional eine Erinnerung wählen.
6. **Termin anlegen** anklicken.

Zur Auswahl stehen:
- keine Erinnerung,
- zum Terminbeginn,
- 5 Minuten vorher,
- 15 Minuten vorher,
- 30 Minuten vorher,
- 1 Stunde vorher,
- 1 Tag vorher.

Kalenderdaten liegen unter:

```text
daten/kalender/termine.json
```

### Erinnerungen
Solange das Provoware-Dashboard läuft, prüft es etwa alle 30 Sekunden auf fällige Erinnerungen. Das funktioniert auch, wenn das Kalenderfenster gerade geschlossen ist.

Nach dem Anzeigen wird die Erinnerung im Kalenderbestand als bereits angezeigt markiert. Dadurch erscheint derselbe Hinweis nicht immer wieder.

Wichtig: Wenn das **gesamte Dashboard geschlossen** ist, läuft kein versteckter Linux-Hintergrunddienst. Erinnerungen bei vollständig geschlossenem Programm sind in dieser Version bewusst nicht enthalten.

In dieser Iteration gibt es außerdem keine Terminlöschung. Dadurch wird kein destruktiver Weg eingeführt, der nicht verlangt wurde.

## Profilbasierte DB-Eingaben
In der Karte **DB-Eingaben** wählen Sie zuerst ein Profil, zum Beispiel:
- HardTechno,
- HipHop/Rap,
- Hörspiele.

Danach werden die passenden Werte für folgende Felder geladen:
- Genres,
- Stimmungen,
- Stil,
- Stimme,
- Besonderheiten.

Über **Bearbeiten …** oder die passenden Punkte in der linken Navigation öffnen Sie die Profilverwaltung. Dort können Sie eigene Profile und Werte ergänzen.

Eigene Änderungen werden gespeichert unter:

```text
daten/profile/db_profile.json
```

Die eingebauten Startprofile erzeugen beim bloßen Programmstart noch keine Datei. Erst wenn Sie etwas ändern, wird gespeichert. Wenn eine vorhandene Profildatei widersprüchliche doppelte Werte enthält, wird sie nicht still verändert. Das Programm meldet den Fehler stattdessen.

## Todo-Liste
Öffnen über:

**Navigation → Planung → Todo-Liste**

### Aufgabe anlegen
1. Titel eingeben. Der Titel ist Pflicht.
2. Optional eine Notiz eintragen.
3. Wenn ein Termin gewünscht ist, **Termin verwenden** aktivieren.
4. Datum und Uhrzeit wählen.
5. **Aufgabe anlegen** anklicken.

Aktive Aufgaben stehen in der Registerkarte **Aktiv**. Aufgaben mit Termin werden nach Termin einsortiert. Todo- und Kalenderzeiten verwenden einheitlich die lokale Rechnerzeit, ohne stille Umrechnung in eine andere Zeitzone.

### Aufgabe abhaken
1. Eine aktive Aufgabe markieren.
2. **Ausgewählte Aufgabe abhaken** anklicken.
3. Die Aufgabe verschwindet aus **Aktiv** und erscheint vollständig unter **Archiv**.

Beim Abhaken wird die Aufgabe **nicht gelöscht**. Aktive Aufgaben und Archiv befinden sich gemeinsam in:

```text
daten/todo/todo.json
```

Dadurch kann die Aufgabe nicht zwischen zwei getrennten Dateien verloren gehen. Die Datei wird über den gemeinsamen geschützten Schreibweg atomar ersetzt.

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

Die Vollprüfung prüft die bestehende Fachlogik, Recovery, Songbibliothek, Suche/Filter, Favoriten, Status, Versionswiederherstellung, Exporte, Profilverwaltung, Todo, Kalender und Erinnerungen, den gemeinsamen Produktions-Schreibweg, Mehrfachstart-Schutz, die echten PySide6-Oberflächenwege, Zoom/Schriftgrößensteuerung, die Struktur des Referenzdashboards und die automatisierbare Kubuntu-Abnahmelogik.

## Bestehende Schutzfunktionen
- gemeinsamer atomarer Schreibweg für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien,
- eindeutige temporäre Dateien statt kollisionsanfälliger fester `.tmp`-Namen,
- Einzelinstanz-Schutz pro Projektordner,
- automatische Versionssicherung vor geänderten Überschreibungen,
- Sicherung des aktuellen Songs vor einer Wiederherstellung,
- Pfadprüfung für Versionsstände,
- einmalige Kalender-Erinnerungsmarkierung erst nach Anzeige,
- Logrotation und Quarantäne,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- echter SIGTERM-Wächtertest nur in Tempdaten,
- ENOSPC-/EROFS-Simulation gegen den echten Produktionsschreiber ohne echten Datenträgerverbrauch,
- vollständige ZIP-/SHA-/Restore-Prüfung.
