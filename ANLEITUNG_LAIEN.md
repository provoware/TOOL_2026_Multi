# Provoware – einfache Anleitung

## In 30 Sekunden starten

1. Projektordner öffnen.
2. `schnellstart.sh` starten.
3. Die automatische Startprüfung abwarten.
4. Im Dashboard mit **Songtexte**, **Todo-Liste** oder **Kalender** beginnen.

Falls ein Doppelklick auf `schnellstart.sh` die Datei nur als Text öffnet: Rechtsklick → **Ausführen**. Alternativ im Projektordner ein Terminal öffnen und eingeben:

```bash
bash schnellstart.sh
```

Beim ersten Start können benötigte Programmteile eingerichtet werden. Danach öffnet sich das **Provoware-Datenbank-Dashboard 2026**.

---

## Woran erkenne ich, was schon funktioniert?

**Fertige Bereiche** sehen normal aus und können direkt benutzt werden.

**Noch nicht fertige Bereiche** sind mit **„In Planung“** markiert und gestrichelt dargestellt. Ein Klick zeigt nur einen Hinweis. Dabei wird **nichts gespeichert, gelöscht oder verändert**.

Aktuell direkt nutzbar sind vor allem:

- **Songtexte**
- **Genres / Profile & Vorgaben**
- **Todo-Liste**
- **Kalender**
- **Fehlerhilfe (Recovery)**

---

## Das Dashboard verstehen

### Oben

- **Songs durchsuchen …** durchsucht nur die Songbibliothek. Das Feld ist deshalb bewusst nicht mehr als allgemeine Suche beschriftet.
- **Programm beenden** speichert zuerst offene Songtexte und beendet danach Provoware.

### Schnellkacheln

Direkter Zugriff auf wichtige Bereiche. Noch nicht fertige Kacheln tragen sichtbar **„In Planung“**.

### Linke Navigation

Die Navigation ist nach einfachen Aufgaben gegliedert:

- **Schreiben**
- **Daten & Vorgaben**
- **Funktionen**
- **Dateien & Werkzeuge**
- **Planung**
- **Hilfe**

Mit **☰** kann die linke Navigation schmal oder breit geschaltet werden.

### Karte „So startest du“

Für den schnellen Einstieg gibt es drei direkte Wege:

1. **Songtexte öffnen**
2. **Todo-Liste öffnen**
3. **Kalender öffnen**

### Projekt-Notiz

Oben im Arbeitsbereich befindet sich **Projekt-Notiz**.

- Text eingeben.
- `Enter` drücken oder **Notiz speichern** anklicken.
- Vorhandene Notizen bleiben erhalten.

Die technische Datei dahinter heißt weiterhin `Entwicklerinformation.txt`, damit bestehende Daten kompatibel bleiben.

---

# Songtexte

## Songbibliothek

Über **Songtexte** öffnet sich die Songbibliothek.

Oben kann gesucht werden nach:

- Titel
- Genre
- Stimmung
- Stil
- Stimme
- Tags

Zusätzlich können Filter kombiniert werden.

**Wichtig:** Suchen, Filtern, Sortieren und Gruppieren verändern keine Songdatei.

### Einen Song öffnen

1. Song in der Liste markieren.
2. **Ausgewählten Song öffnen** anklicken oder doppelklicken.

Ist nichts markiert, erscheint jetzt ein verständlicher Hinweis statt einer Aktion ohne sichtbare Reaktion.

## Songtext schreiben

Der Editor zeigt oben eine einfache Schrittfolge:

1. Titel eintragen.
2. Songbereich wählen oder hinzufügen.
3. Text schreiben.

Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro.

Rechts steht die **Gesamtvorschau**.

## Speichern

Änderungen werden automatisch gespeichert:

- nach Änderungen an Eingabefeldern,
- beim Verlassen größerer Textfelder,
- alle 5 Minuten,
- beim Schließen,
- beim Beenden des Programms.

Zusätzlich kann jederzeit **Jetzt speichern** oder `Strg+S` verwendet werden.

Kann nicht gespeichert werden, bleibt der bisherige gespeicherte Stand geschützt und Provoware meldet verständlich, was passiert ist.

## Songbereich entfernen

Ein Bereich wird nicht mehr still entfernt.

1. Bereich links auswählen.
2. **Bereich entfernen** anklicken.
3. Sicherheitsfrage bestätigen.

Erst danach wird der Bereich aus dem aktuellen Arbeitsstand entfernt.

## Ältere Version wiederherstellen

1. Song in der Bibliothek markieren.
2. **Ältere Version ansehen / wiederherstellen** öffnen.
3. Alte Version auswählen.
4. Vorschau prüfen.
5. **Diese Version wiederherstellen** anklicken.
6. Sicherheitsfrage bestätigen.

Vor der Wiederherstellung wird der aktuelle Stand automatisch als neue Version gesichert.

## Exportieren

Über **Exportieren** können zusätzliche Dateien erzeugt werden:

- TXT mit Angaben
- Markdown
- JSON
- nur Songtext als TXT

Der aktuelle Song wird durch einen Export nicht verändert.

---

# Profile & Vorgaben

Ein **Profil** ist eine Sammlung passender Vorgaben.

Beispiel: Im Profil **HardTechno** können eigene Werte für Genre, Stimmung, Stil, Stimme und Besonderheiten liegen.

Öffnen über:

**Navigation → Daten & Vorgaben**

oder über die Genres-Kachel.

Ablauf:

1. Profil wählen.
2. Bereich wählen.
3. Vorhandene Werte ansehen.
4. Neuen Wert eingeben und **Wert hinzufügen** anklicken.

Beim Entfernen eines Wertes wird vorher nachgefragt.

Eigene Profildaten werden gespeichert unter:

```text
daten/profile/db_profile.json
```

---

# Aufgaben / Todo-Liste

Öffnen über:

**Navigation → Planung → Todo-Liste**

## Aufgabe anlegen

1. Aufgabe eingeben.
2. Optional eine Notiz ergänzen.
3. Optional **Termin hinzufügen** aktivieren.
4. **Aufgabe anlegen** anklicken.

## Aufgabe erledigen

1. Unter **Aktiv** eine Aufgabe markieren.
2. **Als erledigt markieren → Archiv** anklicken.

Die Aufgabe wird **nicht gelöscht**. Sie wird vollständig ins Archiv verschoben.

Daten liegen unter:

```text
daten/todo/todo.json
```

---

# Kalender & Termine

Öffnen über:

**Navigation → Planung → Kalender**

Links kann ein Datum gewählt und ein neuer Termin angelegt werden. Rechts gibt es:

- **Tag**
- **Woche**
- **Monat**
- **Jahr**

## Termin anlegen

1. Titel eingeben.
2. Optional Notiz ergänzen.
3. Beginn wählen.
4. Ende wählen.
5. Optional Erinnerung wählen.
6. **Termin anlegen** anklicken.

Das Ende muss nach dem Beginn liegen.

## Erinnerungen

Erinnerungen funktionieren, solange das **Hauptprogramm geöffnet** ist. Der Kalender selbst darf dabei geschlossen sein.

Wenn Provoware komplett beendet wurde, läuft kein versteckter Hintergrunddienst.

Kalenderdaten liegen unter:

```text
daten/kalender/termine.json
```

---

# Fehlerhilfe (Recovery)

Öffnen über:

**Navigation → Hilfe → Fehlerhilfe (Recovery)**

Die Fehlerhilfe zeigt zuerst einfache Informationen:

- **Was ist passiert?**
- **Was wurde geschützt?**
- **Was soll ich jetzt tun?**
- **Wie oft ist das passiert?**

Technische Details bleiben zunächst ausgeblendet und können bei Bedarf geöffnet werden.

Falls eine Meldung ausgewählt werden muss und nichts markiert ist, erscheint ein verständlicher Hinweis.

---

# Anzeige vergrößern

Die gesamte Oberfläche kann gemeinsam vergrößert oder verkleinert werden.

- **A−** = kleiner
- **A+** = größer
- `Strg + Mausrad`
- `Strg++`
- `Strg+-`
- `Strg+0` = zurück auf 100 %

Stufen:

**100 %, 125 %, 150 %, 175 %, 200 %**

---

# Tastatur

- `Tab` – zum nächsten bedienbaren Element
- `Enter` – Eingabe bestätigen
- `F5` – Liste / Fehlerhilfe aktualisieren
- `Strg+S` – Song sofort speichern
- `Strg+R` – Fehlerhilfe öffnen
- `Strg+0` – Anzeige auf 100 %
- `Escape` – untergeordnetes Fenster schließen

---

# Wenn Provoware schon läuft

Pro Projektordner wird nur ein schreibendes Hauptfenster gleichzeitig zugelassen.

Wird Provoware versehentlich zweimal gestartet, erscheint ein Hinweis. Das zweite Fenster wird nicht geöffnet. Das bereits laufende Fenster arbeitet normal weiter.

---

# Wenn der Start fehlschlägt

Die Startanzeige zeigt sechs Schritte. Ein roter Schritt enthält eine einfache Fehlerbeschreibung.

Typische Ursachen:

- Python 3 fehlt.
- Unter Ubuntu/Kubuntu fehlt `python3-venv`.
- benötigte Programmteile konnten nicht eingerichtet werden.
- eine Projektdatei fehlt oder ist beschädigt.

Vorhandene Nutzerdaten werden durch die reine Startprüfung nicht absichtlich verändert.

---

# Technische Prüfung für Entwickler

Die vollständige automatische Prüfung lautet:

```bash
bash scripts/pruefen.sh --full
```

Sie prüft unter anderem:

- Start und Syntax,
- Daten- und Speicherlogik,
- Songbibliothek und Songeditor,
- Profile,
- Todo und Kalender,
- Fehlerhilfe,
- Zoom und Tastaturwege,
- Laienführung und sichtbare Statushinweise,
- Kontraste wichtiger Texte,
- Repository-Hygiene,
- vollständige Wiederherstellung aus einem Projekt-ZIP.

Die reale sichtbare Kubuntu/KDE-X11-Endabnahme bleibt zusätzlich möglich mit:

```bash
bash kubuntu_abnahme.sh
```
