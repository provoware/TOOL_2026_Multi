# Provoware-Datenbank-Dashboard 2026

> **Version:** 0.17.0 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit Charakterfibel und Texteditor; automatische Voll-/Restore- und native Wayland-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen

Provoware ist ein erweiterbares Desktop-Dashboard für Songtexte, kreative Vorgaben, Aufgaben, Kalender und sichere Projektverwaltung. Die Oberfläche ist auf **einfache Bedienung ohne technisches Vorwissen**, dynamische Größenanpassung und barrierearme Tastatur-/Screenreader-Nutzung ausgelegt.

## Zielsystem und Schnellstart

Offizielles Linux-Zielsystem ist **Kubuntu 26.04 LTS mit KDE Plasma unter Wayland**. Der normale Programmstart bleibt bewusst backend-neutral: Provoware setzt `QT_QPA_PLATFORM` nicht künstlich auf Wayland oder X11, sondern lässt Qt die aktive Desktop-Sitzung verwenden.

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
- 🟢 **Charakterfibel** – konsistente Figuren zentral speichern, suchen und für andere Schreibmodule referenzierbar halten
- 🟢 **Texteditor** – allgemeine Texte mit Titel/Dateiname, Haupttext, Abschlussnotizen, Versionen und Charakterbezug bearbeiten
- 🟢 **Ältere Songversionen** – Vorschau und bestätigte Wiederherstellung; aktueller Stand wird vorher gesichert
- 🟢 **Profile & Vorgaben** – Genres, Stimmungen, Stil, Stimme und Besonderheiten je Profil verwalten
- 🟢 **Todo-Liste** – Aufgaben mit optionalem Termin anlegen und erledigte Aufgaben sicher archivieren
- 🟢 **Kalender** – Tag/Woche/Monat/Jahr, Termine und Erinnerungen
- 🟢 **Fehlerhilfe (Recovery)** – einfache Erklärung, Schutzmaßnahme und nächster Schritt
- 🟢 **Zoom 100–200 %** – gemeinsam für alle Hauptfenster
- 🟢 **Farbthemes** – Amber, Türkis, Lila und Kontrast

Die linke Navigation stellt diese fertigen Wege – einschließlich **Texteditor** und **Charakterfibel** – zuerst unter **Direkt nutzbar** bereit. Die zehn noch nicht fertigen Bereiche stehen getrennt unter **Noch nicht fertig** und sind standardmäßig eingeklappt. So bleibt das Menü ruhig; wer die geplanten Bereiche sehen möchte, kann sie mit einem einzigen Schalter einblenden.

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

Seit 0.16.1 werden Laptop-, Breit- und Hochzoomzustand zusätzlich über eine **zentrale Qt-unabhängige Präsentationspolicy** klassifiziert. Navigation und Laptoplayout greifen damit auf dieselbe deterministische Zustandsentscheidung zurück, statt private Hilfsfunktionen oder doppelte Schwellenwerte zu verwenden. Die sichtbare Bedienung bleibt dabei unverändert; verbessert wurden Wartbarkeit, Testbarkeit und Regressionsschutz.

### Farbthemes

Unten im Dashboard befindet sich die Auswahl **Farben**:

- **Amber** – dunkles Standardtheme mit gelb-orangefarbenem Akzent
- **Türkis** – dunkles Theme mit türkisem Akzent
- **Lila** – dunkles Theme mit violettem Akzent
- **Kontrast** – Schwarz/Weiß mit gelbem Akzent und stärkerem Fokusrahmen

Der Theme-Wechsel gilt sofort für alle geöffneten Provoware-Fenster. Die Auswahl ist **sitzungsbezogen** und erzeugt bewusst keinen neuen Nutzerdaten- oder Konfigurationsschreibweg.

Die Kernfarben jedes Themes werden automatisch mit mindestens **4,5:1** Kontrast gegen den jeweiligen Hintergrund geprüft.

## Neu in 0.17.0 – Charaktere, Texteditor und gemeinsame Standards

- **Charakterfibel:** eigener atomarer Datenbestand mit stabilen Charakter-IDs und wiederverwendbaren Feldern für Schreibmodule.
- **Texteditor:** eigener Arbeitsbereich mit sicherem Titel/Dateinamen, Haupttext, Abschlussnotizen, Versionierung und Charakterreferenzen.
- **Genres & Vorgaben:** Komma-Eingaben wie `düster, treibend, melodisch` werden bereinigt und als einzelne Datenbankwerte gespeichert; Dubletten werden vermieden.
- **Songtexte:** neben Standardbereichen können eigene validierte Bereichsnamen angelegt werden.
- **JSON-Hilfe:** die Fehlerhilfe zeigt eine exakte Songtext-Importvorlage; zusätzlich liegt `vorlagen/songtext_import_vorlage.json` im Projekt.
- **Startschutz:** fehlen benötigte Arbeitsordner, zeigt Provoware Ziel und Zweck und fragt vor dem Erstellen ausdrücklich nach Zustimmung; anschließend wird Schreibbarkeit validiert.
- **Eingabekontrast:** Eingabe- und Auswahlfelder verwenden themeweit einen eigenen Kontrasthintergrund mit kontrastgeprüfter Schrift.
- **Projektplanung:** neun größere Modulvorhaben wurden mit einzeln abhakbaren Unteraufgaben in den Todo-Bestand aufgenommen.

## Was ist noch geplant?

Noch nicht fertige Bereiche werden sichtbar mit **„In Planung“** und gestrichelter Darstellung von fertigen Funktionen getrennt. In der linken Navigation sind sie zusätzlich unter **Noch nicht fertig** gesammelt und standardmäßig eingeklappt. Ein Klick auf einen geplanten Bereich verändert keine Daten.

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
2. Standard-Songbereich wählen oder einen eigenen Bereichsnamen eingeben.
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

Mehrere Werte können mit Komma eingegeben werden. Jeder bereinigte Begriff wird einzeln gespeichert; vorhandene Dubletten werden nicht erneut angelegt.

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

Die Fehlerhilfe befindet sich unter **Direkt nutzbar → Fehlerhilfe (Recovery)**.

Sie zeigt zuerst:

- Was ist passiert?
- Was wurde geschützt?
- Was soll ich jetzt tun?
- Wie oft trat es auf?

Technische Details bleiben standardmäßig ausgeblendet. Über **JSON-Importvorlage** lässt sich zusätzlich die exakte Struktur für extern vorbereitete Songtexte anzeigen und kopieren.

## Datensicherheit

Wichtige Schutzmechanismen:

- zentraler atomarer Schreibweg für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien
- zentraler atomarer Publish-Schritt für fertig erzeugte Diagnose- und Release-Dateien
- atomare Status-, Rückfall-, Quarantäne-, Ereignis-, Wächter- und Kubuntu-Abnahmeberichte
- eindeutige Tempdateien
- Datei-`fsync`, atomarer Replace und bestmöglicher Verzeichnis-`fsync`
- Einzelinstanz-Schutz pro Projektordner
- automatische Songversionssicherung
- Pfadprüfung vor Versionswiederherstellung
- geschützte Backup-/Restore-Kette mit ZIP-Prüfung und SHA-256
- Diagnose- und Log-Bereinigung
- Append-only-Protokolle bleiben bewusst Append-only statt unnötig per Dateiersatz umgebaut zu werden
- ENOSPC-/EROFS-Schreibfehlersimulation ohne echten Datenträgerverbrauch
- Repository-Hygiene-Test
- automatischer Release-Invariant: jedes produktive `app/*.py`-Modul muss im Release-Manifest enthalten sein

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
- Profile, Charakterfibel, Texteditor, Todo und Kalender
- Komma-Eingaben, freie Songbereiche, JSON-Importstruktur und Startordner-Validierung
- Fehlerhilfe
- PySide6-Bedienwege im Offscreen-Test
- Zoom, Fokus und Hochzoom
- reine deterministische Präsentationspolicy und ihre Grenzwerte
- Laptop-Kompaktmodus und Rückkehr zur großen Ansicht
- Farbthemes und Screenreader-Grundwerte
- Kontraste aller Theme-Kernfarben mit mindestens 4,5:1
- Laienführung und Nicht-Silent-Fail-Verhalten
- Menü-Hierarchie, Planungs-Aufklappzustand und Rückkehr aus Laptop-/Hochzoom-Modi
- responsive Breiten- und Tabellenverteilung
- Vollständigkeit aller produktiven `app/*.py`-Module im Release
- direkte Startbarkeit wichtiger Skripte
- Kubuntu-26.04-/Wayland-Erkennung und Abnahmeberichte
- tatsächlichen nativen Qt-Wayland-Start in einem isolierten headless Wayland-Compositor
- Release-/Diagnose-Publish-Fehler und Temp-Cleanup
- Repository-Hygiene

Iteration 27 wurde mit dem finalen 0.15.3-Head `9cd8101ba19c5e28b41fa7793d35860462d38864` in **Grundprüfung #554** vollständig abgenommen: **81 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **38 Release-Betriebsdateien**, Headless-Start und Restore `OK`; Restore-SHA-256 `add4af04204e694427aa2332edea4136c2816e0c196676391a5763e044be3718`. PR #34 wurde danach sicher gemergt; Main-Commit `e7027e57c3c8709263b73543fd2b01be84e6639d`.

Der technische Iteration-28-Head `a7f2c168ecc3f0a2310fbff874cea33d30793d25` bestand **Grundprüfung #567** mit **86 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **38 Release-Betriebsdateien**, Headless-Start, einem echten nativen Qt-Wayland-Smoke (`QApplication.platformName() = wayland`) und Vollprojekt-Restore `OK`. Restore-SHA-256: `1283f1399a5d4a675bdc06720ebf5435df38fccbf36d64fb74fd5e1e9748b579`. Der CI-Compositor läuft isoliert und ersetzt ausdrücklich nicht die reale sichtbare Kubuntu-26.04-/Plasma-Endabnahme.

Der korrigierte technische Iteration-29-Head `117aa0eee4e3422804506d9bc1c1fc50f75d4591` bestand **Grundprüfung #600** mit **94 Logik-/Regressionstests**, **56 PySide6-GUI-Tests**, **39 Release-Betriebsdateien**, Headless-Start, nativem Qt-Wayland-Smoke und Vollprojekt-Restore `OK`. Restore-SHA-256: `064caec2bca6423922ae7bed63fe7d2684a403c69f03a3c5674e3708b5f86624`. Zuvor hatte der neu eingeführte Release-Vollständigkeitstest den fehlenden Manifest-Eintrag für `app/presentation_policy.py` korrekt blockiert.

Vollständiges Restore-Gate:

```bash
python3 scripts/iteration_restore.py
```

## Reale Kubuntu 26.04 / Plasma-Wayland-Abnahme

Für die offizielle Zielsystem-Abnahme auf **Kubuntu 26.04 LTS**:

```bash
bash kubuntu_abnahme.sh
```

Die Abnahme verlangt eine echte **Plasma-Wayland-Sitzung**, prüft die Betriebssystembasis 26.04, `WAYLAND_DISPLAY`, KDE/Plasma und zusätzlich den tatsächlich von Qt verwendeten Plattformnamen. Ein erzwungenes `QT_QPA_PLATFORM=xcb`/XWayland zählt nicht als native Wayland-Abnahme.

Besonders sichtbar zu prüfen sind **1366×768 bei 125/150 %**, zusätzlich 175/200 %, das Theme **Kontrast**, Tastaturfokus sowie Fenster-, Menü- und Eingabeverhalten. Automatische CI kann diesen echten Plasma-Bildschirm nicht vollständig ersetzen.

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
- `docs/ITERATION26_RELEASE_IO_HARDENING.md` – Release-/Bericht-I/O-Audit und Abnahme
- `docs/ITERATION27_NAVIGATION_UX.md` – Menü-Hierarchie, Laiennavigation und Abnahme
- `docs/ITERATION28_KUBUNTU_2604_WAYLAND.md` – Kubuntu-26.04-/Wayland-Umstellung und Plattformabnahme
- `docs/ITERATION29_PRESENTATION_POLICY.md` – Architekturhärtung, zentrale Präsentationspolicy und Release-Vollständigkeit
- `docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md` – Charakterfibel, Texteditor, gemeinsame Daten-/UI-Standards und Abnahme

## Noch offen

1. Reale sichtbare Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme auf dem Zielrechner durchführen, besonders 1366×768 bei 125/150 %, zusätzlich 175/200 % und Theme `Kontrast`.
2. Anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

Die detaillierte Versionshistorie steht bewusst **nicht mehrfach in der README**, sondern im `CHANGELOG.md` und den Iterationsdokumenten.
