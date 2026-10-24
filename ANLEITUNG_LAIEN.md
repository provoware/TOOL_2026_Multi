# Provoware – einfache Anleitung

## Wichtig vor dem ersten Start

**Deine Texte gehören dir.** Sichere den Ordner `daten/` regelmäßig auf einem zweiten Datenträger. Bei Problemen mit Daten oder bei einer Wiederherstellung zuerst eine Kopie des aktuellen `daten/`-Ordners anlegen. Die automatische GitHub-Prüfung kann keine Sicherung deiner persönlichen Dateien ersetzen.

**Neue Sicherheitsfragen im Texteditor:** Wenn du einen veränderten Text verlässt, einen neuen Text beginnst oder das Fenster schließt, fragt das Programm, ob gespeichert, verworfen oder abgebrochen werden soll. **Abbrechen** bringt dich zum bisherigen Text zurück. Haben verschiedene Titel nach Bereinigung denselben Dateinamen, verweigert das Programm ein unbeabsichtigtes Überschreiben.

**Bei stark vergrößerter Schrift:** Die Navigation verwendet kürzere gut lesbare Beschriftungen. Über die eingeblendeten Hinweise und die barrierefreien Namen bleiben die vollständigen Funktionen erkennbar.

## Schnellhilfe: Die sieben häufigsten Fragen

| Was möchtest du tun? | So geht es |
|---|---|
| **Programm starten** | Projektordner öffnen → Terminal öffnen → `bash schnellstart.sh`. |
| **Song schreiben** | Auf der Startkarte **Song schreiben** wählen → Titel und Text eingeben. |
| **Normalen Text schreiben** | **Text schreiben** wählen → Titel und Text eingeben → **Jetzt speichern**. |
| **Aufgabe notieren** | **Aufgabe planen** wählen → Eingabe ergänzen → **Aufgabe anlegen**. |
| **Termin eintragen** | **Termin anlegen** wählen → Titel und Uhrzeit ergänzen → Termin anlegen. |
| **Alles größer machen** | Unten `A+` drücken; bis 200 % möglich. |
| **Problem lösen** | `F1` drücken → **Hilfe & Fehlerhilfe**. |

**Deine wichtigsten Dateien liegen unter `daten/`.** Sichere diesen Ordner regelmäßig auf einem getrennten Datenträger.

**Achtung bei Textänderungen:** Beim Schließen oder Wechseln eines bearbeiteten Textes kannst du **Speichern**, **Verwerfen** oder **Abbrechen** wählen. Mit **Abbrechen** bleibt deine Arbeit offen. Wird ein Dateiname bereits von einer anderen Datei verwendet, verhindert das Programm ein ungewolltes Überschreiben.

**Was ist noch nicht fertig?** Mit **In Planung** gekennzeichnete Funktionen sind keine einsatzbereiten Werkzeuge.

**Mehr Einzelheiten:** Die folgenden Kapitel sind zum Nachschlagen gedacht. Für den normalen Einstieg genügt die Tabelle oben.

---

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

- **Suchtext eingeben …** öffnet die lokale Datei- und Textsuche. Im Suchfenster den gewünschten Ordner auswählen; die Songbibliothek hat zusätzlich ihre eigene Suche.
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

### Karte „Was möchtest du tun?“

Vier gleichwertige Aktionen helfen dir beim Einstieg. Du kannst sie unabhängig voneinander nutzen:

- **Song schreiben:** Öffnet einen neuen Songeditor. Bereits offene Songs bleiben erhalten.
- **Text schreiben:** Beginnt bei geschlossenem Editor einen leeren Text. Ist der Editor bereits offen, arbeitest du im vorhandenen Entwurf weiter; er wird nicht neu geladen oder geleert.
- **Aufgabe planen:** Öffnet die Aufgabenliste und setzt den Fokus in das Eingabefeld. Eine begonnene Eingabe bleibt erhalten.
- **Termin anlegen:** Öffnet den Kalender und setzt den Fokus in den Titel. Begonnene Termineingaben bleiben erhalten.

Bei einer leeren Textliste erklärt ein Hinweis den ersten Schritt: Titel und Text eingeben, dann **Jetzt speichern**. Gespeicherte Texte findest du im Texteditor links unter **Gespeicherte Texte**. Für einen weiteren neuen Text im bereits geöffneten Editor **Neuer Text** wählen; dabei gilt die vorhandene Nachfrage zu ungespeicherten Änderungen.

Ein beim Schließen ausdrücklich verworfener Text wird durch die Startaktion nicht wieder geöffnet. Bücher beginnst oder bearbeitest du weiterhin über **Bücher / Buchwerkstatt** und deren Vorlagenauswahl. Die Songbibliothek bleibt über **Songtexte** erreichbar.

### Projekt-Notiz

Oben im Arbeitsbereich befindet sich **Projekt-Notiz**.

- Text eingeben.
- `Enter` drücken oder **Notiz speichern** anklicken.
- Vorhandene Notizen bleiben erhalten.

Neue Notizen liegen unter `daten/notizen/projekt-notizen.txt` und werden mit dem persönlichen Datenordner gesichert. Bereits gespeicherte Notizen werden beim Ergänzen erhalten.

Gibt es noch die alte Datei `Entwicklerinformation.txt` im Projektstamm, fragt Provoware beim Speichern nach:

- **Ja:** Eine unveränderte Kopie alter Notizen kommt in den Datenordner und damit in künftige persönliche Sicherungen. Das Original bleibt unverändert.
- **Nein:** Nur die neue Notiz wird gespeichert. Die alten Notizen sind weiterhin nicht im persönlichen Daten-ZIP enthalten; ein Hinweis erinnert daran. In dieser Sitzung wird nicht erneut gefragt. Zum späteren Übernehmen das Programm neu starten und erneut eine Notiz speichern.
- **Abbrechen:** Die Eingabe bleibt geöffnet; es wird keine neue Notiz gespeichert.

Identische Altkopien werden nicht doppelt angelegt. Wurde die alte Datei nachträglich verändert, kann beim nächsten Programmstart eine weitere Kopie übernommen werden. Alte und neue Notizen werden nicht automatisch zu einem Text vermischt. Bei Fehlern bleibt deine aktuelle Eingabe erhalten. Notizdateien sind auf jeweils 4 MiB begrenzt; größere Altdateien separat auf einem zweiten Datenträger sichern und über die Fehlerhilfe prüfen lassen.

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

# Charakterfibel

Öffnen über **Direkt nutzbar → Charakterfibel**. Hier pflegst du Figuren zentral, damit spätere Schreibmodule auf denselben Bestand zugreifen können. Gespeichert werden unter anderem Name, Rolle, Aussehen, Persönlichkeit, Motivation, Hintergrund, Beziehungen, Sprache, Stärken, Schwächen, Tags und Notizen. Jeder Charakter erhält intern eine stabile Kennung.

---

# Texteditor

Öffnen über **Direkt nutzbar → Texteditor**. Der Titel bestimmt einen sicheren Dateinamen. Darunter liegen die große Schreibfläche und ein separates Abschlussnotizenfeld. Texte werden atomar gespeichert und können auf Charaktere aus der Charakterfibel verweisen. `Strg+S` speichert sofort.

# Aufgaben / Todo-Liste

Öffnen über:

**Direkt nutzbar → Todo-Liste**

## Persönliche Aufgaben und ältere Entwicklungsplanung

Ein neuer Bestand beginnt mit einer leeren persönlichen Aufgabenliste. Öffnen, Aktualisieren und Vergrößern erzeugen keine Aufgaben und schreiben die Aufgabendatei nicht um.

Falls eine ältere Programmversion automatisch Entwicklungsaufgaben eingetragen hat, erscheinen diese unter **Entwicklungsplanung (Altbestand)**. Der Reiter wird nur angezeigt, wenn solche Einträge vorhanden sind. Offene und erledigte Altaufgaben bleiben dort vollständig erhalten. Unter **Aktiv** und **Archiv** stehen deine persönlichen Aufgaben. Gleiche Titel führen nicht dazu, dass eigene Aufgaben als Entwicklungsaufgaben behandelt werden.

Wenn du eine alte Entwicklungsaufgabe persönlich weiterverfolgen möchtest:

1. **Entwicklungsplanung (Altbestand)** öffnen und einen Eintrag markieren.
2. **Als persönliche Aufgabe kopieren** wählen.
3. Den Hinweis prüfen und **Persönliche Kopie anlegen** bestätigen. **Abbrechen** verändert nichts.
4. Die neue Aufgabe erscheint markiert unter **Aktiv**. Der ursprüngliche Eintrag bleibt im Altbestand; dies gilt auch für zuvor erledigte Altaufgaben.

Jede bestätigte Wiederholung erzeugt eine weitere eigenständige persönliche Aufgabe. Eine noch nicht angelegte Eingabe im Formular bleibt beim Kopieren erhalten. **Als erledigt markieren → Archiv** ist ausschließlich im Reiter **Aktiv** verfügbar.

Alle Einträge liegen weiterhin gemeinsam in `daten/todo/todo.json` und sind Bestandteil der persönlichen Datensicherung. Die Trennung betrifft die Anzeige; vorhandene Aufgaben werden beim Öffnen weder verschoben noch gelöscht.

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

Die reine Startprüfung soll vorhandene Nutzerdaten nicht verändern. Vor umfangreichen Änderungen trotzdem eine eigene Sicherung erstellen.


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

## Textbaustein-Buttons: häufige Texte mit einem Klick kopieren

1. Im Menü **Textbaustein-Buttons** öffnen (oder **Strg+Alt+T**).
2. **Neuen Button anlegen** wählen. Arbeitsbereich, Kategorie, Titel und Text eingeben.
3. Unter Kategorie, Titel und Text liegt jeweils **Aus Zwischenablage einfügen**. Text wird an der Schreibposition eingefügt.
4. Optional Farbe und **Klein / Mittel / Groß** wählen. **Button speichern** drücken.
5. Unter **Buttons verwenden** den Arbeitsbereich wählen und den Textbutton drücken. Danach im Zielprogramm **Strg+V** drücken.

Mit **Workflow ergänzen** kommen weitere Arbeitsbereiche hinzu. Ein bis drei Spalten, Kategorien, Suche sowie **↑ / ↓** helfen beim Ordnen. Die Pfeile verschieben innerhalb derselben Kategorie; zum Umgruppieren **Bearbeiten** nutzen.

**Variante anlegen** erzeugt eine Unterversion derselben Familie. Der Originaltext bleibt erhalten. Bei gleichem Text bietet das Programm auch beim Anlegen eine Unterversion an. Mit `{{Name}}` oder `{{Thema}}` lassen sich ausfüllbare Stellen vorbereiten. Beim Kopieren fragt das Programm die Werte ab; Abbrechen verändert die Zwischenablage nicht.

**Monatliche Verwendungen** zählt Kopiervorgänge im Programm, getrennt nach Button und Monat. Die Nutzung des eingefügten Textes in anderen Programmen kann nicht erfasst werden. Der Monatsbericht lässt sich als Textdatei ausgeben.

## Buchwerkstatt: vom ersten Kapitel zum Manuskript

1. **Buchwerkstatt** öffnen (oder **Strg+Alt+B**).
2. Vorlage **Hörspiel**, **Satire & Geschichte**, **Sachausarbeitung**, **Tutorial** oder **Leer** wählen und **Neues Buch aus Vorlage** drücken.
3. Buchtitel eingeben. Im Kapitelbaum ein Kapitel wählen und schreiben.
4. Über **＋ Kapitel** oder **＋ Unterkapitel** erweitern. Mit den Pfeilen Geschwisterkapitel verschieben; **Eine Ebene höher** löst ein Unterkapitel aus seiner bisherigen Ebene.
5. Passende Textelemente oder Figuren aus der Charakterfibel an der Schreibposition einfügen. Kapitelstatus und Notizen helfen beim Überarbeiten.
6. **Buch jetzt speichern** oder **Strg+S** drücken. Betitelte geänderte Entwürfe werden zusätzlich jede Minute gespeichert.
7. Unter **Bücher & Vorlagen** das **Manuskript als Markdown oder Text exportieren**. Planungs- und Kapitelnotizen bleiben dabei im Buchbestand.

**Planung & Notizen** hält Zielgruppe, Ideen, Quellen und offene Punkte fest. **Aktuelles Buch als neue Fassung kopieren** legt einen neuen Entwurf an; zum Behalten speichern. Bis zu acht Kapitelebenen sind möglich. Die Vorlagen helfen beim Strukturieren und schreiben keine fertigen Inhalte automatisch.

### Gemeinsame Bedienung beider neuer Module

- **Importieren / Exportieren** stehen immer oben. JSON-Export sichert den gespeicherten Bestand des jeweiligen Moduls, einschließlich Varianten beziehungsweise Kapitelstruktur und Notizen.
- Beim Import zuerst die Vorschau prüfen. Neue Kennungen verhindern ein Überschreiben vorhandener Einträge. Wiederholter Import erzeugt weitere Kopien; Monatszähler dieser Kopien starten bei null.
- Ungespeicherte Änderungen werden beim Wechsel oder Schließen abgefragt. **Abbrechen** lässt die Arbeit geöffnet. Das gilt auch beim Beenden des Dashboards.
- **Rechtschreibung prüfen** arbeitet lokal und optional. Benötigt werden die Kubuntu-Pakete **aspell** und **aspell-de**. Unbekannte Namen oder Fachwörter können korrekt sein. Die Prüfung lässt ein Wort auswählen und dessen Schreibweise ausdrücklich ändern.
- Die bestehenden Farbthemes und Zoomstufen gelten auch hier. Bei wenig Platz helfen Rollbalken; der Buchbereich wechselt bei hoher Vergrößerung zur Anordnung untereinander.

Die Daten liegen unter `daten/textbausteine/bestand.json` und `daten/buecher/bestand.json`. Sichere weiterhin den gesamten Ordner `daten/` auf einem getrennten Datenträger.


## Lokale Leistungsdiagnose – freiwillig und ohne Inhaltsaufzeichnung

1. **Hilfe & Fehlerhilfe → Leistung & Verbesserung** öffnen.
2. Bei Bedarf **Lokale Leistungsmessung einschalten** auswählen. Zunächst ist sie aus.
3. Normal arbeiten. Die Messung sammelt feste technische Aktionen, Laufzeiten, Zähler und Bytezahlen – keine Texte, Titel, Zwischenablageinhalte oder Pfade.
4. Aufbewahrung (1–30 Tage), Berichtszeitraum und gewünschte Messgruppen wählen. **Aktualisieren** zeigt neue Werte; die **JSON-Vorschau** zeigt die gewählte Exportauswahl.
5. **Gewählte Messdaten exportieren** speichert nach deiner Dateiauswahl TXT oder JSON. Es wird nichts hochgeladen. Vor einer späteren Weitergabe die Vorschau prüfen.
6. Ausschalten stoppt neue Messungen. **Alle Leistungsdaten löschen und Messung ausschalten** entfernt nach Bestätigung den zusätzlichen Leistungsbestand. Eigene Arbeiten und Fehlerprotokolle bleiben erhalten.

Die Statistik wird gebündelt alle 60 Sekunden und beim normalen Beenden gespeichert. Ein Absturz kann die letzte Minute Statistik verlieren; Arbeitsdateien sind davon unabhängig. Startwerte entstehen erst bei einem folgenden Programmstart mit eingeschalteter Messung. Größenklassen für Cache und tatsächliche SSD-Schreibmengen werden noch nicht gemessen. „Unverändert“ zählt gültige Speicherversuche in Buchwerkstatt, Textbuttons und Texteditor; es bedeutet nicht, dass bereits Schreibzugriffe eingespart werden.


Eigenständige persönliche Datensicherung: [Anleitung](docs/DATENSICHERUNG.md). Vorher Programm schließen; Wiederherstellung erfolgt ausschließlich in einen neuen Ordner.


### Wenn die Startumgebung beschädigt ist

Das Startprogramm prüft nun auch bei vorhandener Installationsmarkierung die tatsächlichen Pakete. Fehlende Programmteile werden mit Zeitgrenze erneut installiert. Bei fehlender Verbindung oder defekter Umgebung startet die Oberfläche nicht. Persönliche Arbeitsdaten bleiben erhalten.

Wenn die Meldung ausdrücklich eine beschädigte `.venv` nennt: Programm schließen, ausschließlich den versteckten Ordner `.venv` in einen noch nicht vorhandenen Namen wie `.venv-alt` umbenennen und `bash schnellstart.sh` erneut starten. `daten/` bleibt erhalten. Vorhandene `.venv-alt` niemals überschreiben. Das Werkzeug benennt keine Ordner automatisch um.


### Dateien und Textstellen wiederfinden

Im Dashboard oben **Dateisuche** wählen oder **Strg+Umschalt+F** drücken. Über **Ordner auswählen …** den lokalen Suchordner wählen oder einen absoluten Pfad eingeben. Suchtext eingeben, Dateinamen und/oder Textinhalte wählen und **Suchen** drücken. Für einen Ordner außerhalb des Standarddatenordners wird der lesende Zugriff ausdrücklich abgefragt; Ablehnen erhält bisherige Treffer. Markiere einen Treffer, um Datei, Zeile und Textausschnitt darunter zu lesen oder zu kopieren. **Abbrechen** beendet weitere Suche, bisherige Treffer bleiben sichtbar. Dateien werden nicht verändert oder automatisch geöffnet. Gesucht wird im gewählten Ordner einschließlich Unterordnern; versteckte Einträge und Verknüpfungen bleiben außen vor. Fehlende Leserechte werden als unvollständige Suche angezeigt; auf Wunsch öffnet sich nach Bestätigung die Betriebssystem-Ordnerauswahl. Ein Bestätigen in Provoware ändert keine Linux-Dateirechte: Zugriff gegebenenfalls im Betriebssystem freigeben lassen, den Ordner erneut wählen und die Suche bestätigen. PDF- und Office-Inhalte werden nicht durchsucht; ihre Dateinamen können gefunden werden. Bei Suchgrenzen den Begriff genauer wählen. [Weitere Grenzen](docs/DATEISUCHE.md).


### Ideen und Kontometadaten

Das Symbol oben links öffnet ein Modulmenü. **Ideenarchiv** (Strg+Alt+I) sammelt Fragmente, Schlagworte und Herkunft. Ziehe ein gespeichertes Fragment als Kopie in die Komposition; daraus lässt sich ein neuer Text speichern, ohne die Ideen zu löschen. **Accountmanager** (Strg+Alt+A) sammelt Kontometadaten und Gruppen. Er ist kein verschlüsselter Passworttresor: keine echten Passwörter oder Tokens eingeben. [Bedienung und Datenschutz](docs/IDEEN_UND_KONTEN.md).

Im Texteditor helfen **Strukturfarben** und die Gliederung bei Überschriften und Abschnitten. Sie verändern keine gespeicherten Textzeichen. [Details](docs/STARTMESSUNG_UND_STRUKTUR.md).
