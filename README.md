# Provoware-Datenbank-Dashboard 2026

> **Version:** 0.15.1 · **Stand:** 09.09.2026 · **Status:** ausführbarer Kern, automatische Voll-/Restore-Prüfung aktiv, reale Kubuntu/KDE-X11-Sichtabnahme noch offen

Provoware ist ein erweiterbares Desktop-Dashboard für Songtexte, kreative Vorgaben, Aufgaben, Kalender und sichere Projektverwaltung. Die Oberfläche ist auf **einfache Bedienung ohne technisches Vorwissen**, dynamische Größenanpassung und barrierearme Tastatur-/Screenreader-Nutzung ausgelegt.

## Schnellstart

Im Projektordner:

```bash
bash schnellstart.sh
```

Der Schnellstart richtet die benötigte Umgebung bei Bedarf selbst ein, prüft den Projektstart in sechs verständlichen Schritten und öffnet danach das Dashboard.

Die ausführliche einfache Bedienanleitung steht in:

```text
ANLEITUNG_LAIEN.md
```

## Direkt nutzbar

- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen
- 🟢 **Ältere Songversionen** – Vorschau und bestätigte Wiederherstellung; aktueller Stand wird vorher gesichert
- 🟢 **Profile & Vorgaben** – Genres, Stimmungen, Stil, Stimme und Besonderheiten je Profil verwalten
- 🟢 **Todo-Liste** – Aufgaben mit optionalem Termin anlegen und erledigte Aufgaben sicher archivieren
- 🟢 **Kalender** – Tag/Woche/Monat/Jahr, Termine und Erinnerungen
- 🟢 **Fehlerhilfe (Recovery)** – einfache Erklärung, Schutzmaßnahme und nächster Schritt
- 🟢 **Zoom 100–200 %** – gemeinsam für alle Hauptfenster
- 🟢 **Farbthemes** – Amber, Türkis, Lila und Kontrast

## Erscheinungsbild, Zoom und Barrierefreiheit

Die Oberfläche verwendet zentrale wiederverwendbare UI-Standards statt einzelner Sonderformatierungen:

- gut lesbare systemweite Sans-Serif-Schrift ohne zusätzliche Font-Installation,
- klar sichtbarer Tastaturfokus,
- gleichmäßige Abstände, Rundungen, Eingabehöhen, Tabs, Scrollleisten und Splitter,
- responsive Aufteilung für kompakte, normale und breite Fenster,
- getrennte Schrift- und Geometrieskalierung, damit 175/200 % nicht zu Überlagerungen führen,
- platzsparender Hochzoom-Modus ab 175 %,
- Accessible Names und Beschreibungen für zentrale interaktive Elemente,
- `Qt.StrongFocus` für Buttons, Eingaben, Auswahlfelder, Listen und Tabellen,
- Zustände werden zusätzlich durch Text, Symbole und Konturen vermittelt – nicht nur durch Farbe.

Die normale Responsive-Logik unterscheidet zwischen kompakter, normaler und breiter Fensterdarstellung. Auf typischen kleinen Laptop-Bildschirmen wie **1366×768** wird bei **125/150 %** zusätzlich ein reversibler Laptop-Kompaktmodus verwendet: redundante reine Planungselemente verschwinden vorübergehend, während Songtexte, Vorgaben, Todo, Kalender, Fehlerhilfe, Zoom und Farbtheme erreichbar bleiben. Ab **1450 px Breite** wird automatisch wieder die vollständige große Darstellung verwendet.

### Farbthemes

Unten im Dashboard befindet sich die Auswahl **Farben**:

- **Amber** – dunkles Standardtheme mit gelb-orangefarbenem Akzent
- **Türkis** – dunkles Theme mit türkisem Akzent
- **Lila** – dunkles Theme mit violettem Akzent
- **Kontrast** – Schwarz/Weiß mit gelbem Akzent und stärkerem Fokusrahmen

Der Theme-Wechsel gilt sofort für alle geöffneten Provoware-Fenster. Die Auswahl ist **sitzungsbezogen** und erzeugt bewusst keinen neuen Nutzerdaten- oder Konfigurationsschreibweg.

Die Kernfarben jedes Themes werden automatisch mit mindestens **4,5:1** Kontrast gegen den jeweiligen Hintergrund geprüft.

## Was ist noch geplant?

Noch nicht fertige Bereiche werden sichtbar mit **„In Planung“** und gestrichelter Darstellung von fertigen Funktionen getrennt. Ein Klick auf einen geplanten Bereich verändert keine Daten.

Dazu gehören derzeit unter anderem:

- Hörspiele
- Blogartikel
- Prompts
- Genre-Zufall
- Reimfinder
- Dateisuche
- Textinhalt-Suche
- Trefferliste
- Duplikatprüfer
- GitHub-Repositories als eigenes Dashboardmodul

## Bedienprinzip

Die Oberfläche soll jederzeit beantworten:

1. **Wo bin ich?**
2. **Was kann ich hier tun?**
3. **Was ist fertig und was nur geplant?**
4. **Was passiert nach meinem Klick?**
5. **Was bleibt bei einem Fehler geschützt?**
6. **Was ist der nächste sinnvolle Schritt?**

Darum heißen Funktionen wahrheitsgemäß und laienfreundlich, zum Beispiel **Songs durchsuchen**, **Programm beenden** und **Projekt-Notiz**. Aktionen ohne notwendige Auswahl zeigen einen verständlichen Hinweis statt still nichts zu tun.

## Songtexte

### Neuen Song beginnen

**Songtexte** öffnen und **＋ Neuen Song schreiben** anklicken.

Im Editor:

1. Titel eintragen.
2. Songbereich wählen oder hinzufügen.
3. Text schreiben.

Änderungen werden automatisch gespeichert. Zusätzlich steht **Jetzt speichern** bzw. `Strg+S` zur Verfügung.

### Sicheres Entfernen und Wiederherstellen

- Ein Songbereich wird erst nach einer Sicherheitsfrage entfernt.
- Eine ältere Songversion wird erst nach Vorschau und zusätzlicher Bestätigung wiederhergestellt.
- Vor einer Wiederherstellung sichert Provoware den aktuellen Stand automatisch.

Arbeitsdateien:

```text
daten/songtexte/<Titel>.txt
```

Versionsstände:

```text
daten/songtexte/.versionen/<Titel>/
```

Exporte:

```text
daten/songtexte/export/
```

## Profile & Vorgaben

Ein Profil bündelt zusammenpassende Werte, beispielsweise für **HardTechno**, **HipHop/Rap** oder **Hörspiele**.

```text
daten/profile/db_profile.json
```

Die eingebauten Startprofile werden beim bloßen Start nicht unnötig als Nutzerdatendatei geschrieben.

## Todo-Liste

Aufgaben können mit Titel, Notiz und optionalem Termin angelegt werden. Beim Erledigen wird eine Aufgabe **nicht gelöscht**, sondern vollständig ins Archiv verschoben.

```text
daten/todo/todo.json
```

Aktive Aufgaben und Archiv liegen im selben atomar geschriebenen Datenbestand.

## Kalender

Der Kalender bietet Tages-, Wochen-, Monats- und Jahresbereiche. Erinnerungen funktionieren, solange das **Hauptprogramm geöffnet** ist; das Kalenderfenster selbst darf geschlossen sein.

```text
daten/kalender/termine.json
```

Es läuft bewusst kein versteckter Erinnerungsdienst weiter, wenn Provoware vollständig beendet wurde.

## Fehlerhilfe

Die Fehlerhilfe befindet sich unter:

```text
Hilfe → Fehlerhilfe (Recovery)
```

Sie zeigt zuerst:

- Was ist passiert?
- Was wurde geschützt?
- Was soll ich jetzt tun?
- Wie oft trat es auf?

Technische Details bleiben standardmäßig ausgeblendet.

## Datensicherheit

Wichtige Schutzmechanismen:

- zentraler atomarer Schreibweg für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien
- eindeutige Tempdateien
- Datei-`fsync`, atomarer Replace und bestmöglicher Verzeichnis-`fsync`
- Einzelinstanz-Schutz pro Projektordner
- automatische Songversionssicherung
- Pfadprüfung vor Versionswiederherstellung
- geschützte Backup-/Restore-Kette mit ZIP-Prüfung und SHA-256
- Diagnose- und Log-Bereinigung
- ENOSPC-/EROFS-Schreibfehlersimulation ohne echten Datenträgerverbrauch
- Repository-Hygiene-Test

## Anzeige und Tastatur

Zoomstufen:

```text
100 % · 125 % · 150 % · 175 % · 200 %
```

Bedienung:

- `Tab` = nächstes bedienbares Element
- `A−` / `A+` = Anzeige kleiner / größer
- `Strg + Mausrad`
- `Strg++` / `Strg+-`
- `Strg+0` = 100 %
- `Strg+S` = Song sofort speichern
- `Strg+R` = Fehlerhilfe öffnen
- `F5` = aktuelle Liste/Ansicht neu laden

## Automatische Qualitätsprüfung

Vollprüfung:

```bash
bash scripts/pruefen.sh --full
```

Sie prüft unter anderem:

- Syntax und Startfähigkeit
- Fachlogik und bekannte Rückfälle
- Datensicherheit und Restore
- Songeditor und Songbibliothek
- Profile, Todo und Kalender
- Fehlerhilfe
- PySide6-Bedienwege im Offscreen-Test
- Zoom, Fokus und Hochzoom
- Laptop-Kompaktmodus und Rückkehr zur großen Ansicht
- Farbthemes und Screenreader-Grundwerte
- Kontraste aller Theme-Kernfarben mit mindestens 4,5:1
- Laienführung und Nicht-Silent-Fail-Verhalten
- responsive Breiten- und Tabellenverteilung
- Repository-Hygiene

Der korrigierte Iteration-25-Produktions-/Teststand wurde in **Grundprüfung #468** bereits vollständig grün geprüft: 75 Logik-/Regressionstests, 52 PySide6-GUI-Tests, 37 Release-Betriebsdateien und Vollprojekt-Restore `OK` mit SHA-256 `9ace0f9d3311dbe98fa4875b9c1ed86ed51ef1d48ad50a41b6527be09c160b01`. Der reine Evidence-Sync wird vor Merge nochmals vollständig geprüft.

Vollständiges Restore-Gate:

```bash
python3 scripts/iteration_restore.py
```

## Reale Kubuntu/KDE-X11-Abnahme

Automatische Offscreen-CI ersetzt keine echte sichtbare Prüfung auf dem Zielrechner. Dafür gibt es:

```bash
bash kubuntu_abnahme.sh
```

Besonders zu prüfen sind **1366×768 bei 125/150 %**, zusätzlich 175/200 %, normales und maximiertes Fenster sowie das Theme **Kontrast**.

## Projektstruktur

```text
app/        Programm und Oberfläche
daten/      Nutzerdaten
docs/       Entwicklerdokumentation
scripts/    Prüf-, Start-, Diagnose- und Restore-Werkzeuge
tests/      automatische Tests
texte/      zentrale Nutzertexte
logs/       lokale Laufzeitprotokolle, nicht versioniert
berichte/   lokale Berichte, nicht versioniert
backups/    lokale Sicherungen, nicht versioniert
```

## Dokumentation

- `ANLEITUNG_LAIEN.md` – Bedienung für normale Nutzer
- `AGENTS.md` – verbindliche Entwicklungsregeln
- `TODO.md` – aktueller Entwicklungsstand und offene Freigabepunkte
- `CHANGELOG.md` – Versionshistorie
- `MANIFEST.json` – maschinenlesbarer Projekt- und Freigabestand
- `docs/ITERATION21_LAIEN_UX.md` – Laien-UX-Befund
- `docs/ITERATION22_RESPONSIVE_DESIGN.md` – Responsive Design und Abnahme
- `docs/ITERATION23_ZOOM_HAERTUNG.md` – Hochzoom-Härtung
- `docs/ITERATION24_ACCESSIBILITY_THEMES.md` – Barrierefreiheit, Farbthemes und Kontrastprüfung
- `docs/ITERATION25_LAPTOP_LAYOUT.md` – Laptop-Kompaktmodus, Fehlerkorrektur und Abnahme

## Noch offen

1. Den Evidence-Sync-Head von PR #29 nochmals vollständig per Grundprüfung und Restore prüfen und nur bei Grün übernehmen.
2. Danach reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner durchführen.
3. Anschließend verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs nicht unnötig auf Dateiersatz umstellen.

Die detaillierte Versionshistorie steht bewusst **nicht mehrfach in der README**, sondern im `CHANGELOG.md` und den Iterationsdokumenten.
