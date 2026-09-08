# Anleitung für Laien

## Starten
```bash
bash schnellstart.sh
```

Die sechs Startschritte, die unsichtbare Startprüfung und die Prozesswache bleiben aktiv.

## Schnellinfo im Dashboardheader
Oben im Dashboard gibt es das Feld **Entwickler-Schnellinfo**.

1. Kurze Information eingeben.
2. `Enter` drücken oder **Speichern** anklicken.
3. Die Information wird mit Zeitstempel an `Entwicklerinformation.txt` angehängt.

Vorhandene Einträge werden nicht überschrieben.

## Songtexteditor
Klicken Sie oben auf **Songtexteditor**.

Der Editor enthält:
- **Titel** – unter diesem Namen wird der Song gespeichert,
- **Genre** – optional,
- **Bereich** – zum Beispiel Intro, Strophe, Refrain oder Bridge,
- **Bereich hinzufügen** – fügt einen weiteren Songabschnitt hinzu,
- **Bereich entfernen** – entfernt den aktuell gewählten Abschnitt,
- **Vorschau** – zeigt den gesamten Song fortlaufend,
- **Sonstiges** – optional für zusätzliche Hinweise.

Die Songdatei liegt unter:

```text
daten/songtexte/<Titel>.txt
```

Wenn Sie den Titel ändern, entsteht beim nächsten Speichern ein Stand unter dem neuen Titel. Der alte Songstand wird nicht automatisch gelöscht.

## Automatisches Speichern
Der Songtext wird automatisch gespeichert:
- alle 5 Minuten,
- wenn Sie Titel, Genre, Songtext oder Sonstiges verlassen,
- wenn Sie den Songtexteditor schließen,
- vor einem Logout.

Mit `Ctrl+S` können Sie zusätzlich jederzeit selbst speichern.

## Logout
Die Schaltfläche **Logout** beendet die aktuelle Sitzung. Vorher werden alle offenen Songtexteditoren gespeichert. Wenn ein Songtext nicht gespeichert werden kann, wird der Logout gestoppt, damit kein ungesicherter Text verloren geht.

## Debug- und Recovery-Zentrale
Ereignisse können weiterhin nach Schweregrad und Bereich gefiltert werden. Ereignisdetails lassen sich per Doppelklick, `Enter` oder Schaltfläche öffnen. Technische Angaben bleiben zunächst eingeklappt.

## Tastatur
- `Tab` – zum nächsten bedienbaren Element,
- `Enter` – Schnellinfo speichern oder markiertes Ereignis öffnen,
- `F5` – Recovery-Anzeige aktualisieren,
- `Ctrl+S` – Songtext manuell speichern,
- `Ctrl++` / `Ctrl+-` – Anzeige größer/kleiner,
- `Ctrl+0` – zurück auf 100 Prozent,
- `Escape` – Detail- oder Songeditorfenster schließen.

## Vollprüfung
```bash
bash scripts/pruefen.sh --full
```

Die Vollprüfung prüft Recovery-Funktionen, Songtextlogik und echte Tk-Oberflächenwege. Ohne virtuelle oder echte grafische Sitzung wird der GUI-Teil nicht als bestanden ausgegeben.

## Bestehende Schutzfunktionen
- Logrotation und Quarantäne beschädigter Zeilen,
- Datenschutzbereinigung und Diagnosepaket,
- Headless-Start,
- Prozesswache,
- Schreibfehler-Simulation ohne echten Datenträgerverbrauch,
- vollständige ZIP-/SHA-/Restore-Prüfung.
