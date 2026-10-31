# Provoware-Datenbank-Dashboard 2026

> **Version:** 0.18.5 (Entwicklungskandidat) · **Dokumentationsstand:** 31.10.2026 · **Status:** nutzbarer Desktop-Kern; kein fertiges Release. Abschließende Kubuntu-Abnahme erst nach Fertigstellung aller Module.

Provoware ist ein erweiterbares Desktop-Dashboard für Songtexte, kreative Vorgaben, Aufgaben, Kalender und sichere Projektverwaltung. Die Oberfläche ist auf **einfache Bedienung ohne technisches Vorwissen**, dynamische Größenanpassung und barrierearme Tastatur-/Screenreader-Nutzung ausgelegt.


[![Version: 0.18.5](https://img.shields.io/badge/Version-0.18.5-175a98?style=flat-square)](MANIFEST.json)
[![Status: Entwicklungskandidat](https://img.shields.io/badge/Status-Entwicklungskandidat-a84b00?style=flat-square)](docs/MODULPLAN_2026.md)
[![System: Kubuntu 26.04 LTS](https://img.shields.io/badge/System-Kubuntu_26.04_LTS-40569b?style=flat-square)](#zielsystem-und-schnellstart)
[![Grundprüfung auf main](https://github.com/provoware/TOOL_2026_Multi/actions/workflows/qualitaet.yml/badge.svg?branch=main)](https://github.com/provoware/TOOL_2026_Multi/actions/workflows/qualitaet.yml)

> **Statusfarben:** 🟢 **Direkt nutzbar** · 🟡 **In Entwicklung / noch nicht freigegeben** · 🔴 **Gesperrt oder fehlgeschlagen**. Die Kennzeichnung steht immer auch als Text dabei; Farbe allein ist keine Information. Die Prüfplakette zeigt den **jeweiligen aktuellen GitHub-Prüfstatus** und ersetzt keine abschließende Prüfung am eigenen Kubuntu-Rechner.

## 🧭 Schnellnavigation

| Ich möchte … | Hier geht es weiter |
|---|---|
| 🟢 **Das Programm starten** | [Schnellstart](#zielsystem-und-schnellstart) · [Anleitung für Einsteiger](ANLEITUNG_LAIEN.md) |
| 🟢 **Songtexte, Bücher oder Aufgaben bearbeiten** | [Direkt nutzbare Bereiche](#direkt-nutzbar) |
| 🟢 **Meine Dateien schützen** | [Datensicherung](docs/DATENSICHERUNG.md) · [Datensicherheit](#datensicherheit) |
| 🟡 **Geplante und noch fehlende Funktionen ansehen** | [Verbindlicher Modulplan](docs/MODULPLAN_2026.md) · [Aufgaben](TODO.md) |
| 🟡 **Entwicklung und Fehler verfolgen** | [Offene Aufgaben](https://github.com/provoware/TOOL_2026_Multi/issues) · [Änderungsanträge](https://github.com/provoware/TOOL_2026_Multi/pulls) · [Prüfläufe](https://github.com/provoware/TOOL_2026_Multi/actions) |

**Wichtig:** 🟡 *Entwicklungskandidat* bedeutet nicht, dass alle Module fertig sind. Automatische Prüfungen sichern Zwischenstände ab; die einmalige praktische Kubuntu-Gesamtabnahme folgt nach Abschluss der vereinbarten Module.


## Das Wichtigste auf einen Blick

| Deine Frage | Einfache Antwort |
|---|---|
| **Was ist Provoware?** | Ein Programm für Songtexte, eigene Texte, Figuren, Aufgaben und Termine. |
| **Wie starte ich?** | Projektordner öffnen, Terminal starten und `bash schnellstart.sh` eingeben. |
| **Was funktioniert?** | Songtexte, Texteditor, Charakterfibel, Buchwerkstatt, Wiki, Modulbaukasten, Entwicklungspool, Audioplayer, Bildvorschau, einfache FFmpeg-Diashows, Aufgaben, Kalender, Profile und Dateisuche. |
| **Was fehlt noch?** | Reimfinder, vollständige automatische Update-Aktivierung samt Rollback, Drittplugin-Laden und weitere geplante Module; die statische und isolierte Updateprüfung ist bereits verfügbar. |
| **Wie sichere ich meine Arbeit?** | Programm schließen und die [eigenständige Datensicherung](docs/DATENSICHERUNG.md) nutzen. |
| **Wo finde ich Hilfe?** | [Schritt-für-Schritt-Anleitung](ANLEITUNG_LAIEN.md) oder im Programm die Taste `F1`. |
| **Was wurde zuletzt verbessert?** | Zusätzliche Schutzmaßnahmen für Dateien, gespeicherte Daten und Diagnoseprotokolle; frühere Modulergänzungen sind im [Änderungsverlauf](CHANGELOG.md) dokumentiert. |
| **Was ist technisch noch offen?** | Spätere einmalige Kubuntu-Gesamtabnahme, Weiterentwicklung noch fehlender Module und endgültige Veröffentlichung. |

**Vollständiger Entwicklungsumfang:** [Verbindlicher Modulplan](docs/MODULPLAN_2026.md). [Medienmodule](docs/MEDIENMODULE.md) · [Entwicklungspool](docs/ENTWICKLUNGSPOOL.md) · [Modulentwürfe](docs/MODULENTWURF.md) · [Update-Slots](docs/UPDATE_SLOTS.md). Nachweis PR #97/#98 (CI #1031/#1033/#1035): [Wikimodul](docs/WIKI.md), [Update-Checkpoint](docs/UPDATE_CHECKPOINT.md), [Modulbaukasten](docs/MODULBAUKASTEN.md). Neu in 0.18.5: [rechte Link-Schnellstarter-Leiste](docs/SCHNELLSTARTER.md) mit lokal gespeicherten Webadressen, Gruppen und bewusstem Browserstart.

**Für die normale Nutzung brauchst du nur diese Übersicht und die [einfache Anleitung](ANLEITUNG_LAIEN.md).** Ausführliche technische Informationen stehen getrennt im [Dokumentenwegweiser](docs/README.md). Der folgende Abschnitt enthält zusätzliche Einzelheiten für Interessierte.

---

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

## Neu in 0.18.1: lokale Leistungsdiagnose

Unter **Hilfe & Fehlerhilfe → Leistung & Verbesserung** lassen sich technische Tagesaggregate freiwillig einschalten, ansehen, auswählen, exportieren und löschen. Erfasst werden Ladezeiten, logische Schreibzugriffe und unveränderte gültige Speicherversuche. Inhalte und Dateipfade werden nicht gespeichert, und es gibt keine automatische Übertragung. [Bedienung und Grenzen](docs/LEISTUNGSDIAGNOSE.md).

## Neu in 0.18.0: Textbuttons und Buchwerkstatt

**Repository-Status 0.18.0:** [PR #84](https://github.com/provoware/TOOL_2026_Multi/pull/84) wurde nach ausdrücklicher Freigabe mit main zusammengeführt; der anschließende Hauptzweig-Lauf ist erfolgreich. 0.18.1 ist die nachfolgende abgegrenzte Leistungsdiagnose. Code-/Layoutnachweis: [CI #1007](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39127077853), 188 Logik- und 144 GUI-Tests, UI-Shadow ohne Fehler/Warnungen, Wayland und Restore erfolgreich. Neuere Informationsänderungen benötigen ihren eigenen PR-Nachweis.

Textbaustein-Buttons bieten Workflow-Reiter, Kategorien, Platzhalter, Unterversionen, Monatsstatistik und flexible Darstellung. Die Buchwerkstatt bietet Vorlagen für Hörspiel, Satire, Sachtext und Tutorial mit Kapiteln, Unterkapiteln, Notizen und Manuskriptexport. Beide nutzen gemeinsame Import-/Export- und Schutzfunktionen. Öffnen über die oberen Kacheln, das Menü oder Strg+Alt+T / Strg+Alt+B. Details: [Anleitung](ANLEITUNG_LAIEN.md) und [Abnahme](docs/TEXTBUTTONS_UND_BUCHWERKSTATT.md).

## Direkt nutzbar

- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen
- 🟢 **Charakterfibel** – konsistente Figuren zentral speichern, suchen und für andere Schreibmodule referenzierbar halten
- 🟢 **Texteditor** – allgemeine Texte mit Titel/Dateiname, Haupttext, Abschlussnotizen, Versionen und Charakterbezug bearbeiten
- 🟢 **Ältere Songversionen** – Vorschau und bestätigte Wiederherstellung; aktueller Stand wird vorher gesichert
- 🟢 **Profile & Vorgaben** – Genres, Stimmungen, Stil, Stimme und Besonderheiten je Profil verwalten
- 🟢 **Todo-Liste** – Aufgaben mit optionalem Termin anlegen und erledigte Aufgaben sicher archivieren
- 🟢 **Kalender** – Tag/Woche/Monat/Jahr, Termine und Erinnerungen
- 🟢 **Hilfe & Fehlerhilfe** – durchsuchbare Schritt-für-Schritt-Hilfe plus verständliche Fehlermeldungen, Schutzmaßnahme und nächster Schritt
- 🟢 **Zoom 100–200 %** – gemeinsam für alle Hauptfenster
- 🟢 **Farbthemes** – Amber, Türkis, Lila und Kontrast

- 🟢 **Textbuttons** – Textfragmente, Platzhalter, Varianten und Monatsstatistik
- 🟢 **Buchwerkstatt** – Vorlagen, Kapitel und Manuskripte
- 🟢 **Genre-Zufall und GitHub-Projekte** – profilbasierter Generator sowie lokale Projektübersicht

Die linke Navigation stellt diese fertigen Wege – einschließlich **Texteditor** und **Charakterfibel** – zuerst unter **Direkt nutzbar** bereit. Die acht noch nicht fertigen Bereiche stehen getrennt unter **Noch nicht fertig** und sind standardmäßig eingeklappt. So bleibt das Menü ruhig; wer die geplanten Bereiche sehen möchte, kann sie mit einem einzigen Schalter einblenden.

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

Die normale Responsive-Logik unterscheidet zwischen kompakter, normaler und breiter Fensterdarstellung. Auf typischen kleinen Laptop-Bildschirmen wie **1366×768** wird bei **125/150 %** zusätzlich ein reversibler Laptop-Kompaktmodus verwendet: redundante reine Planungselemente verschwinden vorübergehend, während Songtexte, Vorgaben, Todo, Kalender, Hilfe & Fehlerhilfe, Zoom und Farbtheme erreichbar bleiben. Ab **1450 px Breite** wird automatisch wieder die vollständige große Darstellung verwendet.

Seit 0.16.1 werden Laptop-, Breit- und Hochzoomzustand zusätzlich über eine **zentrale Qt-unabhängige Präsentationspolicy** klassifiziert. Navigation und Laptoplayout greifen damit auf dieselbe deterministische Zustandsentscheidung zurück, statt private Hilfsfunktionen oder doppelte Schwellenwerte zu verwenden. Die sichtbare Bedienung bleibt dabei unverändert; verbessert wurden Wartbarkeit, Testbarkeit und Regressionsschutz.

### Farbthemes

Unten im Dashboard befindet sich die Auswahl **Farben**:

- **Amber** – dunkles Standardtheme mit gelb-orangefarbenem Akzent
- **Türkis** – dunkles Theme mit türkisem Akzent
- **Lila** – dunkles Theme mit violettem Akzent
- **Kontrast** – Schwarz/Weiß mit gelbem Akzent und stärkerem Fokusrahmen

Der Theme-Wechsel gilt sofort für alle geöffneten Provoware-Fenster. Die Auswahl ist **sitzungsbezogen** und erzeugt bewusst keinen neuen Nutzerdaten- oder Konfigurationsschreibweg.

Die Kernfarben jedes Themes werden automatisch mit mindestens **4,5:1** Kontrast gegen den jeweiligen Hintergrund geprüft.

## Schnellüberblick: Was kann das Programm heute?

**Fertig:** Songtexte schreiben und verwalten, Charakterfibel, allgemeiner Texteditor, Genre-/Stimmungs-/Stilprofile, Aufgabenliste, Kalender, Erinnerungen während das Hauptprogramm läuft sowie Hilfe & Fehlerhilfe.

**Noch nicht fertig:** Reimfinder, Suche über alle Dateien, Duplikatprüfung, automatische GitHub-Verwaltung, eigenständige Blog-/Podcast-/Hörspielproduktion und automatisches Update. Genre-Zufall und lokale GitHub-Projektliste sind bereits nutzbar. Ein sichtbarer Planungsbereich bedeutet **nicht**, dass die Funktion bereits arbeitet.

**Die wichtigsten drei Schritte zum Start:**
1. Projektordner öffnen.
2. Terminal im Projektordner öffnen und `bash schnellstart.sh` eingeben.
3. Im Dashboard **Songtexte**, **Texteditor**, **Todo-Liste** oder **Kalender** wählen.

**Wo liegen meine Daten?** Im Ordner `daten/`. Eine Sicherung dieses Ordners auf ein getrenntes Laufwerk ist sinnvoll. Ein automatisch erzeugtes Projekt-ZIP ist **kein nachgewiesener Ersatz für eine unabhängige Sicherung der persönlichen Arbeitsdateien**. Vor einer Wiederherstellung immer zuerst eine zusätzliche Kopie anlegen.

**Was ist zuletzt verbessert worden?** Im Oktober wurden Schutzabfragen gegen ungespeicherte Textänderungen, Konfliktprüfungen bei Dateinamen und die Anzeige bei hohem Zoom ergänzt. Die automatische Hauptzweig-Prüfung umfasst 60 Kombinationen; zuletzt 0 Fehler und 0 Warnungen (GitHub-Arbeitsablauf [#39065993768](https://github.com/provoware/TOOL_2026_Multi/actions/runs/39065993768)). Dies ersetzt keine sichtbare Prüfung am eigenen Bildschirm.

**Brauchst du Hilfe?** Öffne `ANLEITUNG_LAIEN.md`. Bei Problemen nutze zuerst **Hilfe & Fehlerhilfe** oder `F1`; technische Einzelheiten stehen in `docs/`.

## Orientierung im Repository

| Datei oder Ordner | Einfach erklärt |
|---|---|
| `schnellstart.sh` | Normaler Start des Programms. |
| `ANLEITUNG_LAIEN.md` | Bedienung Schritt für Schritt. |
| `README.md` | Übersicht, Funktionen und Einstieg. |
| `TODO.md` | Was erledigt ist und was noch fehlt. |
| `CHANGELOG.md` | Chronologische Übersicht der Änderungen. |
| `MANIFEST.json` | Technische Liste der Dateien und Regeln, die das Programm benötigt. |
| `app/` | Eigentlicher Programmcode. |
| `daten/` | Persönliche Arbeitsdaten; **vor Änderungen und Wiederherstellungen sichern**. |
| `tests/` | Automatische Prüfungen für Entwickler. |
| `docs/` | Ausführliche technische Unterlagen und frühere Entwicklungsberichte. |
| `scripts/` | Zusätzliche Prüf- und Hilfsprogramme. |

**Ältere Abschnitte weiter unten dokumentieren den damaligen Entwicklungsstand.** Ihre historischen Testzahlen und Zwischenstände beschreiben nicht automatisch die neueste Version.

## Neu in 0.17.4 – automatische UI-Abnahme im Shadow-Modus

Die wiederkehrende Oberflächenprüfung wird erstmals systematisch automatisiert. Ein neuer **UI-Shadow-Gate** prüft die kritischen Fenster gegen zentrale Verträge für Raster, Geometrie, Mindesthöhen, Accessibility und Kontrast. Pull Requests nutzen eine kompakte 8-Fall-Matrix; `main` nutzt 60 Kombinationen aus 1366×768 bis 1920×1080, 100–200 % Zoom und allen vier Themes.

Auffälligkeiten erzeugen eine maschinenlesbare JSON-Evidenz und – wo sinnvoll – Diagnosebilder mit 8-Pixel-Raster. Gespeicherte Fensterpositionen werden zusätzlich mit deterministischen Problemfällen gefuzzt. Der Gate läuft in Iteration 39 bewusst **nicht blockierend**, damit seine Regeln zuerst kalibriert werden können. Die vorhandenen Logik-, GUI-, Wayland-, Restore- und ZIP-Gates bleiben weiterhin die verbindliche Freigabe.

Wichtig: CI-Evidenz wird als separates Artefakt erzeugt und nicht nachträglich in das Quell-Manifest geschrieben. Dadurch entsteht kein endloser Kreislauf, bei dem ein Evidenz-Commit selbst wieder einen neuen Evidenz-Commit erfordert.

## Neu in 0.17.3 – Fensterführung und kleine Displays

- **Klare Song-Arbeitsfolge:** Beim Öffnen eines Songs aus der Bibliothek wird die Bibliothek vorübergehend ausgeblendet; nach dem Schließen des letzten Songeditors kehrt sie kontrolliert zurück.
- **Bildschirmsicher:** Songeditor und Songbibliothek werden auf die aktuelle Arbeitsfläche begrenzt und bei ungültiger alter Position neu zentriert.
- **Portable Fensterzustände:** Größe, Position und Maximiert-Status liegen getrennt von Songdaten in `daten/ui/fenster.json`.
- **Kompakter Songeditor:** Stil, Stimme, Besonderheiten und Tags liegen unter **Weitere Angaben** und werden bei knapper Fläche oder ab 150 % Zoom automatisch eingeklappt.
- **Kompakte Songbibliothek:** Filter, Sortierung und Gruppierung können gemeinsam eingeklappt werden; auf kleinen Ansichten bekommt die Songtabelle Vorrang.
- **Eingabefokus:** normal = neutraler Rand, Fokus = Theme-Akzent, Fehler = Rot, gültiger Zustand = Grün. Platzhalter wurden kontrastreicher gemacht.
- **Qt-Ampersand:** `Hilfe & Fehlerhilfe` wird sichtbar korrekt gezeichnet; der Screenreader-Name bleibt unverändert.
- **Sicherheitsgrenze:** keine Song-, Profil-, Todo- oder Kalenderformate wurden verändert.

## Neu in 0.17.2 – Wartbarkeit, Entwicklungseffizienz und Hilfe

- **Hilfe & Fehlerhilfe:** F1 öffnet jetzt ein eigenes Hilfezentrum mit durchsuchbaren Alltagsthemen und einem getrennten Reiter für Fehlermeldungen.
- **Schnellere Entwicklung:** `bash scripts/pruefen.sh --quick` prüft Syntax, JSON, alle automatisch gefundenen Logiktests, Schreibfehlersimulation und Headless-Start ohne den langsameren GUI-/Release-Block.
- **Weniger Pflegeaufwand:** `--full` findet neue `tests/test_*.py` und `*_gui.py` automatisch; die freigegebenen Betriebsdateien kommen direkt aus `MANIFEST.json`. Neue Tests müssen nicht mehr in mehreren Shell-Listen nachgetragen werden.
- **Repo-Hygiene:** einmalige Migrations-/Finalisierungshilfen wie `scripts/_iter…`, `scripts/finalize_…` oder temporäre Finalizer-Workflows werden künftig automatisch als Überrest blockiert.
- **Bereinigung:** der nicht mehr benötigte Einmal-Helfer `scripts/_iter33_docs_apply.py` wurde entfernt.
- **Versionsdisziplin:** der vollständig grüne Main-Lauf #750 bleibt der unveränderte Referenzstand für 0.17.1/Iteration 36; diese Wartungsrunde wird getrennt als 0.17.2/Iteration 37 geführt.
- **Technischer Gate:** Grundprüfung #769 bestätigte 113 Logiktests, 77 GUI-Tests, 47 Release-Dateien, nativen Wayland-Start, Restore `OK` und ZIP-Erzeugung; der versionierte 0.17.2-Head wird vor Merge erneut vollständig geprüft.

## Neu in 0.17.1 – Charakterzugriff in Schreibmodulen

- **Einheitliche Charakterauswahl:** Texteditor und Songtexteditor beziehen Figuren über dieselbe zentrale, stabile Charakter-ID-Logik.
- **Songtexteditor:** Figuren aus der Charakterfibel können direkt an der aktuellen Schreibposition eingefügt werden.
- **Sicherer Referenzmarker:** `«Charakter: Name (Rolle)»` kollidiert nicht mit Songbereichen wie `[Strophe]` oder `[Refrain]`.
- **Regressionsschutz:** ein erster Prüflauf deckte genau diese Kollision auf; nach der Korrektur sind 106 Logiktests und 76 GUI-Tests grün.
- **Vollständiges Projekt-ZIP:** ein erfolgreicher CI-Lauf erzeugt nach Vollprüfung, nativem Wayland-Smoke und Restore zusätzlich ein vollständiges Git-Projekt-ZIP samt SHA-256.

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

Optional kann direkt darunter ein Charakter aus der **Charakterfibel** gewählt und mit **In Songbereich einfügen** an der aktuellen Schreibposition eingesetzt werden. Die sichtbare Referenz hat die Form `«Charakter: Name (Rolle)»`.

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

## Hilfe & Fehlerhilfe

Öffnen über **Direkt nutzbar → Hilfe & Fehlerhilfe**, `F1` oder weiterhin `Strg+R`.

Der erste Reiter **Schnellhilfe** enthält durchsuchbare Themen wie Start, Songtexte, Texteditor/Charakterfibel, Daten, Fehler, Kubuntu/Wayland sowie Zoom/Tastatur. Jedes Thema nennt konkrete Schritte, eine Alternative und – wo nötig – einen Sicherheitshinweis.

Der zweite Reiter **Fehlermeldungen** behält die Recovery-Funktionen bei und zeigt zuerst:

- Was ist passiert?
- Was wurde geschützt?
- Was soll ich jetzt tun?
- Wie oft ist es passiert?

Technische Details bleiben zunächst ausgeblendet.

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
- `F1` = Hilfe & Fehlerhilfe öffnen
- `Strg+R` = Hilfe & Fehlerhilfe öffnen
- `F5` = aktuelle Liste/Ansicht neu laden

## Automatische Qualitätsprüfung

Für schnelle Entwicklungsrunden:

```bash
bash scripts/pruefen.sh --quick
```

`--quick` prüft Manifest-Dateien, Shell-/JSON-/Python-Syntax, **alle automatisch gefundenen Logik-/Regressionstests**, die Schreibfehlersimulation und den Headless-Start. So muss für kleine Änderungen nicht jedes Mal der deutlich langsamere GUI-/Release-Block laufen.

Vor Merge oder Release bleibt zwingend:

```bash
bash scripts/pruefen.sh --full
```

`--full` ergänzt automatisch **alle `*_gui.py`-Tests**, Release-Vollständigkeit und die komplette Entwicklerprüfung. Neue Testdateien werden über ihr Namensschema entdeckt; eine manuelle Testliste in `scripts/pruefen.sh` ist nicht mehr nötig. Die Runtime-Dateien stammen direkt aus `MANIFEST.json`, damit Manifest, Prüfung und Release nicht auseinanderlaufen.

Die Vollprüfung deckt unter anderem Fachlogik, Datensicherheit, Restore, Song-/Text-/Charakterfunktionen, Todo/Kalender, Hilfe & Fehlerhilfe, Zoom/Fokus, Themes/Kontraste, Navigation, Kubuntu-/Wayland-Erkennung, Release-Publish und Repository-Hygiene ab. Ein Hygiene-Rückfalltest blockiert zusätzlich bekannte lokale Artefakte und einmalige Entwicklungshelfer, bevor sie dauerhaft im Projekt bleiben.

**Referenz vor Iteration 37:** Main-Grundprüfung **#750** auf `d34e5fd643d086f6737eb42448a9a126a6bd3214` war vollständig grün: **111 Logik-/Regressionstests**, **76 GUI-Tests**, **46 Release-Betriebsdateien**, nativer Qt-Wayland-Start und Restore `OK`. Restore-SHA-256: `7b519b36dcb610c125a87d632bfe61ab05131b3c7e99912798f46071fe0804c2`.

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
- `docs/ITERATION35_WRITING_CONTEXT.md` – standardisierter Charakterzugriff, Songeditor-Integration und ZIP-Artefakt-Gate

## Noch offen

1. Reale sichtbare Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme auf dem Zielrechner durchführen, besonders 1366×768 bei 125/150 %, zusätzlich 175/200 % und Theme `Kontrast`.
2. Anschließend nur einzeln priorisierte Produktfunktionen aus den sichtbar als `In Planung` markierten Bereichen freigeben.

Die detaillierte Versionshistorie steht bewusst **nicht mehrfach in der README**, sondern im `CHANGELOG.md` und den Iterationsdokumenten.


## Entwicklungsqualität und weitere Messung

Die [Sitzungsauswertung](docs/ENTWICKLUNGSREVIEW_2026_10_18.md) unterscheidet echte Fehler, notwendige Prüfungen und vermeidbare Umwege. Die [Entwicklungsregeln](docs/ENTWICKLUNGSREGELN.md) wurden um konkrete Vorprüfungen und einen begrenzten Lernkreislauf ergänzt. Der [Messplan](docs/DIAGNOSE_MESSPLAN.md) beschreibt Ladezeiten, Schreibzugriffe, Cache und sichere Diagnoseweitergabe als nächste Planung. Die erste lokale Ausbaustufe ist in 0.18.1 umgesetzt; weitere Messgrößen bleiben geplant. Automatischer Versand ist nicht implementiert.


Eigenständige persönliche Datensicherung: [Anleitung](docs/DATENSICHERUNG.md). Vorher Programm schließen; Wiederherstellung erfolgt ausschließlich in einen neuen Ordner.


Versionskennung und vorbereitete Freigabeunterlagen: [0.18.3](docs/FREIGABE_0_18_3.md). Der Kandidatenstatus ist keine Veröffentlichung.

Zentrale gespeicherte Text-/Dateisuche: [Bedienung und Grenzen](docs/DATEISUCHE.md). Über Dateisuche-Kachel, Kopfsuchfeld oder Strg+Umschalt+F erreichbar.

Update-Pakete getrennt statisch prüfen: [Update-Staging](docs/UPDATE_STAGING.md). Aktivierung und Ausführung von Paketcode bleiben gesperrt.

Neu im 0.18.4-Prüfkandidaten: [Ideenarchiv und Kontometadaten](docs/IDEEN_UND_KONTEN.md), [Prozessstartmessung und Strukturhilfen](docs/STARTMESSUNG_UND_STRUKTUR.md). Weitere Module über das Symbol oben links öffnen.

Aktuelle vorbereitete Versionsunterlagen: [0.18.4](docs/FREIGABE_0_18_4.md).
