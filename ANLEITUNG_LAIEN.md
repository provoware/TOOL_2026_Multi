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

### Für Kubuntu 26.04

Das offizielle Zielsystem ist **Kubuntu 26.04 LTS mit KDE Plasma unter Wayland**. Du musst für den normalen Start **keine technische Anzeigevariable einstellen**. `schnellstart.sh` lässt Qt die aktive Plasma-Sitzung selbst verwenden.

Die besondere Zielsystem-Prüfung startest du erst nach dem normalen Funktionstest mit:

```bash
bash kubuntu_abnahme.sh
```

Falls diese Prüfung meldet, dass keine Wayland-Sitzung aktiv ist, melde dich ab und wähle beim Anmelden **Plasma (Wayland)**. Ein ausdrücklich auf `xcb`/X11 gezwungenes Qt zählt nicht als native Wayland-Abnahme.

---

## Woran erkenne ich, was schon funktioniert?

**Fertige Bereiche** sehen normal aus und können direkt benutzt werden.

**Noch nicht fertige Bereiche** sind mit **„In Planung“** markiert und gestrichelt dargestellt. Ein Klick zeigt nur einen Hinweis. Dabei wird **nichts gespeichert, gelöscht oder verändert**.

Aktuell direkt nutzbar sind vor allem:

- **Songtexte**
- **Charakterfibel**
- **Texteditor**
- **Genres & Vorgaben**
- **Todo-Liste**
- **Kalender**
- **Hilfe & Fehlerhilfe**

---

## Das Dashboard verstehen

### Oben

- **Songs durchsuchen …** durchsucht nur die Songbibliothek. Das Feld ist deshalb bewusst nicht mehr als allgemeine Suche beschriftet.
- **Programm beenden** speichert zuerst offene Songtexte und beendet danach Provoware.

### Schnellkacheln

Direkter Zugriff auf wichtige Bereiche. Noch nicht fertige Kacheln tragen sichtbar **„In Planung“**.

### Linke Navigation

Die Navigation ist bewusst in zwei einfache Teile gegliedert.

Unter **Direkt nutzbar** stehen zuerst die Bereiche, mit denen du sofort arbeiten kannst:

- **Songtexte**
- **Texteditor**
- **Charakterfibel**
- **Genres & Vorgaben**
- **Todo-Liste**
- **Kalender**
- **Hilfe & Fehlerhilfe**

Darunter steht **Noch nicht fertig**. Die geplanten Bereiche sind normalerweise eingeklappt, damit das Menü ruhig und übersichtlich bleibt.

Mit **Geplante Bereiche anzeigen (10)** kannst du sie bei Bedarf öffnen. Dort sind sie in **Kreativ & Inhalte**, **Dateien & Werkzeuge** und **Projekte** gruppiert. Mit **Geplante Bereiche ausblenden (10)** klappst du sie wieder zu.

Auf kleinen Laptop-Bildschirmen sowie bei 175/200 % Zoom kann Provoware diese optionale Planung automatisch ausblenden, damit die fertigen Funktionen genügend Platz behalten.

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

### Neuen Song anfangen

Auch bei einer komplett leeren Bibliothek gibt es oben den sichtbaren Knopf:

**＋ Neuen Song schreiben**

Dieser öffnet einen leeren Songtexteditor. Vorhandene Songs werden dadurch nicht verändert.

Oben kann gesucht werden nach:

- Titel
- Genre
- Stimmung
- Stil
- Stimme
- Tags

Zusätzlich können Filter kombiniert werden. Auf kleineren Fenstern oder bei höherem Zoom werden **Filter, Sortierung und Gruppierung** platzsparend eingeklappt. Mit **Filter** kannst du sie jederzeit wieder öffnen.

**Wichtig:** Suchen, Filtern, Sortieren und Gruppieren verändern keine Songdatei.

### Einen vorhandenen Song öffnen

1. Song in der Liste markieren.
2. **Ausgewählten Song öffnen** anklicken oder doppelklicken.

Ist nichts markiert, erscheint jetzt ein verständlicher Hinweis statt einer Aktion ohne sichtbare Reaktion.

## Songtext schreiben

Der Editor zeigt oben eine einfache Schrittfolge:

1. Titel eintragen.
2. Songbereich wählen oder hinzufügen.
3. Text schreiben.

Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro. Du kannst zusätzlich einen eigenen Namen eintippen, zum Beispiel **Pre-Drop** oder **Gesprochenes Outro**. Ungültige/leere Namen werden nicht übernommen.

### Charakter aus der Charakterfibel einsetzen

1. Oben bei **Charakterfibel** eine Figur auswählen.
2. **In Songbereich einfügen** anklicken.
3. Provoware setzt die Referenz an die aktuelle Schreibposition und speichert den Song anschließend.

Die Referenz sieht zum Beispiel so aus: `«Charakter: Nora (Erzählerin)»`. Die besonderen Klammern sind absichtlich gewählt, damit die Referenz nicht mit Songbereichen wie `[Strophe]` verwechselt wird.

Rechts steht die **Gesamtvorschau**.

**Weitere Angaben:** Stil, Stimme, Besonderheiten und Tags sind optional. Auf kleinen Fenstern oder ab 150 % Zoom klappt Provoware diesen Bereich automatisch ein, damit mehr Platz zum Schreiben bleibt. Du kannst ihn jederzeit mit **Weitere Angaben** wieder öffnen.

Wenn du einen Song aus der Bibliothek öffnest, wird die Bibliothek bewusst ausgeblendet. Nach dem Schließen des letzten Songeditors erscheint sie automatisch wieder. Fenstergröße, Position und „maximiert“ werden getrennt von deinen Songdaten gespeichert; ungültige Positionen auf einem nicht mehr vorhandenen Monitor werden nicht blind wiederhergestellt.

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

**Direkt nutzbar → Genres & Vorgaben**

oder über die Genres-Kachel.

Ablauf:

1. Profil wählen.
2. Bereich wählen.
3. Vorhandene Werte ansehen.
4. Einen oder mehrere Werte eingeben und **Wert hinzufügen** anklicken. Mehrere Werte mit Komma trennen, zum Beispiel `düster, treibend, melodisch`. Jeder Begriff wird einzeln gespeichert; Dubletten werden übersprungen.

Beim Entfernen eines Wertes wird vorher nachgefragt.

Eigene Profildaten werden gespeichert unter:

```text
daten/profile/db_profile.json
```

---

---

# Charakterfibel

Öffnen über **Direkt nutzbar → Charakterfibel**. Hier pflegst du Figuren zentral, damit spätere Schreibmodule auf denselben Bestand zugreifen können. Gespeichert werden unter anderem Name, Rolle, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen. Jeder Charakter erhält intern eine stabile Kennung.

---

# Texteditor

Öffnen über **Direkt nutzbar → Texteditor**. Der Titel bestimmt einen sicheren Dateinamen. Darunter liegen die große Schreibfläche und ein separates Abschlussnotizenfeld. Texte werden atomar gespeichert und können auf Charaktere aus der Charakterfibel verweisen. `Strg+S` speichert sofort.

# Aufgaben / Todo-Liste

Öffnen über:

**Direkt nutzbar → Todo-Liste**

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

**Direkt nutzbar → Kalender**

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

# Hilfe & Fehlerhilfe

Öffnen über:

**Direkt nutzbar → Hilfe & Fehlerhilfe**, `F1` oder `Strg+R`.

Oben gibt es zwei Reiter:

1. **Schnellhilfe** – tippe ein einfaches Wort wie `speichern`, `Songtexte`, `Daten`, `Fehler` oder `Wayland` ein. Links wählst du ein Thema, rechts stehen die konkreten Schritte.
2. **Fehlermeldungen** – zeigt verständlich **Was ist passiert?**, **Was wurde geschützt?**, **Was soll ich jetzt tun?** und **Wie oft ist das passiert?**

Technische Details bleiben zunächst ausgeblendet und können bei Bedarf geöffnet werden. Mit **JSON-Importvorlage** kannst du zusätzlich die exakte Struktur für extern vorbereitete Songtexte anzeigen und in die Zwischenablage kopieren. Dieselbe Vorlage liegt unter `vorlagen/songtext_import_vorlage.json`.

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

Bei **175 % und 200 %** schaltet das Dashboard automatisch auf eine platzsparende Hochzoom-Darstellung. Schrift bleibt groß; redundante Planungsübersichten werden vorübergehend ausgeblendet. Beim Zurückzoomen erscheinen sie automatisch wieder.

---

# Farben und Barrierefreiheit

Unten im Dashboard befindet sich das Auswahlfeld **Farben**. Dort stehen vier Darstellungen zur Verfügung:

- **Amber** – dunkles Standardtheme mit gelb-orangefarbenem Akzent
- **Türkis** – dunkles Theme mit türkisfarbenem Akzent
- **Lila** – dunkles Theme mit violettem Akzent
- **Kontrast** – besonders kontrastreiche Schwarz-Weiß-Darstellung mit gelbem Akzent und stärkerem Fokusrahmen

Ein Farbwechsel gilt sofort für alle geöffneten Provoware-Fenster. Die Auswahl gilt nur für die laufende Sitzung und **verändert keine Song-, Todo-, Kalender- oder Profildaten**.

Für die Bedienung ohne Maus:

- `Tab` bewegt den Fokus zum nächsten bedienbaren Element.
- Der aktuell fokussierte Bereich erhält einen deutlich sichtbaren Rahmen.
- Eingaben, Schaltflächen, Listen und Auswahlfelder sind für Tastaturfokus freigegeben.
- Zentrale Bedienelemente erhalten zusätzliche Namen und Beschreibungen für Screenreader.
- Status wird nicht nur über Farbe vermittelt: Text, Symbole und gestrichelte Konturen bleiben zusätzlich vorhanden.

Die Kernfarben aller vier Themes werden automatisch auf einen Kontrast von mindestens **4,5:1** gegen den Hintergrund geprüft.

---

# Tastatur

- `Tab` – zum nächsten bedienbaren Element
- `Enter` – Eingabe bestätigen
- `F1` – Hilfe & Fehlerhilfe öffnen
- `F5` – aktuelle Liste / Fehlermeldungen aktualisieren
- `Strg+S` – Song sofort speichern
- `Strg+R` – Hilfe & Fehlerhilfe öffnen
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


## Wenn benötigte Arbeitsordner fehlen

Fehlt beim Start ein benötigter Tool-/Datenordner, legt Provoware ihn nicht still im Hintergrund an. Es zeigt den vorgesehenen Pfad und Zweck und fragt zuerst nach Zustimmung. Bei **Nein** wird nichts erstellt. Bei **Ja** wird der Ordner angelegt und anschließend auf Schreibbarkeit geprüft. Schlägt das fehl, bekommst du eine verständliche Fehlermeldung statt eines halbfertigen Starts.

---

# Kubuntu 26.04 / Wayland prüfen

Nach einem normalen Funktionstest kannst du die Zielsystem-Abnahme starten:

```bash
bash kubuntu_abnahme.sh
```

Die automatische Vorprüfung kontrolliert:

- Linux,
- Ubuntu/Kubuntu-Basis **26.04**,
- KDE/Plasma,
- echte Wayland-Sitzung,
- vorhandene Wayland-Anzeige,
- dass Qt nicht ausdrücklich auf X11/XWayland gezwungen wurde,
- den tatsächlich verwendeten Qt-Plattformnamen,
- den sicheren Prozesswächtertest ausschließlich in einem Tempordner.

Danach bestätigst du sichtbar:

- 1366×768 bei 125/150 % ohne Überlagerungen,
- 175/200 % mit erreichbarer Hauptbedienung,
- Tastaturfokus und Theme **Kontrast**,
- Fenster, Menüs und Eingabefokus unter Wayland.

Nur wenn **alle automatischen und sichtbaren Punkte** bestätigt sind, bekommt der Bericht den Status `OK`. Die Abnahme verändert dabei keine Song-, Todo-, Kalender- oder Profildaten.

---

# Technische Prüfung für Entwickler

Für kleine Änderungen zuerst:

```bash
bash scripts/pruefen.sh --quick
```

Vor Merge/Release immer vollständig:

```bash
bash scripts/pruefen.sh --full
```

Neue Testdateien mit Namen `tests/test_*.py` beziehungsweise `*_gui.py` werden automatisch erkannt.


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
- Hilfe & Fehlerhilfe,
- Zoom und Tastaturwege,
- Farbthemes, Screenreader-Grundwerte und Fokus,
- Laienführung, Menü-Hierarchie und sichtbare Statushinweise,
- Kubuntu-26.04-/Wayland-Prüflogik,
- Kontraste der Kernfarben aller Themes,
- Repository-Hygiene,
- vollständige Wiederherstellung aus einem Projekt-ZIP.

GitHub Actions prüft zusätzlich einen **echten nativen Qt-Wayland-Start** gegen einen isolierten headless Wayland-Compositor. Diese technische Prüfung ist wichtig, ersetzt aber nicht die sichtbare Abnahme auf einem echten Kubuntu-26.04-/Plasma-Rechner.
