# Provoware-Datenbank-Dashboard 2026

> **Version:** 0.14.2 · **Stand:** 09.09.2026 · **Status:** ausführbarer Kern, zoom-sichere Layout-Härtung automatisch geprüft; reale Kubuntu/KDE-X11-Sichtabnahme noch offen

Provoware ist ein erweiterbares Desktop-Dashboard für Songtexte, kreative Vorgaben, Aufgaben, Kalender und sichere Projektverwaltung. Die Oberfläche ist auf **einfache Bedienung ohne technisches Vorwissen** ausgelegt und passt sich gemeinsam an Fenstergröße und Zoomstufe an.

## Schnellstart

Im Projektordner:

```bash
bash schnellstart.sh
```

Der Schnellstart richtet die benötigte Umgebung bei Bedarf selbst ein, prüft den Projektstart in sechs Schritten und öffnet danach das Dashboard.

Die ausführliche Bedienanleitung steht in `ANLEITUNG_LAIEN.md`.

## Direkt nutzbar

- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen
- 🟢 **Ältere Songversionen** – Vorschau und bestätigte Wiederherstellung mit vorheriger Sicherung
- 🟢 **Profile & Vorgaben** – Genres, Stimmungen, Stil, Stimme und Besonderheiten je Profil verwalten
- 🟢 **Todo-Liste** – Aufgaben mit optionalem Termin anlegen und erledigte Aufgaben sicher archivieren
- 🟢 **Kalender** – Tag/Woche/Monat/Jahr, Termine und Erinnerungen
- 🟢 **Fehlerhilfe (Recovery)** – einfache Erklärung, Schutzmaßnahme und nächster Schritt
- 🟢 **Zoom 100–200 %** – gemeinsam für alle Hauptfenster

## Modernes und zoom-sicheres Erscheinungsbild

Die Oberfläche verwendet zentrale, wiederverwendbare UI-Standards statt einzelner Sonderformatierungen:

- ruhiges dunkles Grunddesign mit gezielten Amber-Akzenten,
- systemweite Sans-Serif-Schrift ohne zusätzliche Font-Installation,
- Cyan-Fokus für gut erkennbare Tastaturbedienung,
- einheitliche Abstände, Rundungen und Eingabeelemente,
- adaptive Songbibliothek und dynamischer Songeditor-Splitter,
- Navigation und Dashboard-Karten mit sicherem vertikalem Überlauf statt Überlagerungen,
- automatische Umordnung der Hauptkarten bei zu geringer effektiver Arbeitsbreite.

### Wie der Zoom jetzt berechnet wird

Responsive Grenzen richten sich nicht mehr nur nach der physischen Fensterbreite. Verwendet wird die **effektive Arbeitsbreite**:

```text
effektive Breite = Fensterbreite × 100 / Zoom-Prozent
```

Beispiel: Ein 1.594 Pixel breites Fenster besitzt bei 200 % Zoom nur rund **797 Pixel effektive Arbeitsbreite**. Es wird deshalb nicht mehr fälschlich wie ein breites 1.594-Pixel-Layout behandelt.

Die Schrift wächst weiterhin entsprechend der gewählten Stufe **100 / 125 / 150 / 175 / 200 %**. Abstände, Rundungen, Padding und Mindesthöhen wachsen absichtlich flacher, damit bei 200 % mehr Platz für den eigentlichen Inhalt bleibt.

Wenn die effektive Breite unter **960 px** fällt, wechseln die vier Dashboard-Hauptkarten von **2×2 auf eine Spalte**. Beim Zurückzoomen wird die 2×2-Anordnung automatisch wiederhergestellt. Navigation und Kartenbereich können bei Bedarf vertikal scrollen; Inhalte werden nicht mehr in zu geringe Höhe gepresst.

## Noch geplant

Noch nicht fertige Bereiche werden ausdrücklich mit **„In Planung“** gekennzeichnet und gestrichelt dargestellt. Ein Klick verändert keine Daten.

Dazu gehören derzeit:

- Hörspiele
- Blogartikel
- Prompts
- GitHub-Repositories als eigenes Dashboardmodul
- Genre-Zufall
- Reimfinder
- Dateisuche
- Textinhalt-Suche
- Trefferliste
- Duplikatprüfer

## Bedienprinzip

Die Oberfläche soll jederzeit beantworten:

1. **Wo bin ich?**
2. **Was kann ich hier tun?**
3. **Was ist fertig und was nur geplant?**
4. **Was passiert nach meinem Klick?**
5. **Was bleibt bei einem Fehler geschützt?**
6. **Was ist der nächste sinnvolle Schritt?**

Darum heißt die Dashboard-Suche **„Songs durchsuchen“**, `Logout` wurde durch **„Programm beenden“** ersetzt und die technische `Entwicklerinfo` in der Bedienoberfläche als **„Projekt-Notiz“** bezeichnet. Aktionen ohne Auswahl zeigen einen Hinweis statt still nichts zu tun.

## Songtexte

### Neuen Song beginnen

**Songtexte** öffnen und **„＋ Neuen Song schreiben“** anklicken.

Im Editor:

1. Titel eintragen.
2. Songbereich wählen oder hinzufügen.
3. Text schreiben.

Änderungen werden automatisch gespeichert. Zusätzlich steht **„Jetzt speichern“** beziehungsweise `Strg+S` zur Verfügung.

### Sicheres Entfernen und Wiederherstellen

- Ein Songbereich wird erst nach einer Sicherheitsfrage entfernt.
- Eine ältere Songversion wird erst nach Vorschau und zusätzlicher Bestätigung wiederhergestellt.
- Vor einer Wiederherstellung sichert Provoware den aktuellen Stand automatisch.

Arbeitsdateien: `daten/songtexte/<Titel>.txt`  
Versionsstände: `daten/songtexte/.versionen/<Titel>/`  
Exporte: `daten/songtexte/export/`

## Profile & Vorgaben

Ein Profil bündelt zusammenpassende Werte, zum Beispiel für **HardTechno**, **HipHop/Rap** oder **Hörspiele**.

Eigene Profildaten liegen unter:

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
- eindeutige Tempdateien statt kollisionsanfälliger fester Namen
- Datei-`fsync`, atomarer Replace und bestmöglicher Verzeichnis-`fsync`
- Einzelinstanz-Schutz pro Projektordner
- automatische Songversionssicherung
- Pfadprüfung vor Versionswiederherstellung
- geschützte Backup-/Restore-Kette mit ZIP-Prüfung und SHA-256
- Diagnose- und Log-Bereinigung
- ENOSPC-/EROFS-Schreibfehlersimulation ohne echten Datenträgerverbrauch
- Repository-Hygiene-Test gegen versehentlich eingecheckte Laufzeit- und Temp-Artefakte

## Anzeige und Tastatur

Zoomstufen:

```text
100 % · 125 % · 150 % · 175 % · 200 %
```

Bedienung:

- `A−` / `A+`
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

Sie prüft unter anderem Syntax, Fachlogik, Datensicherheit, Restore, Songeditor, Songbibliothek, Profile, Todo, Kalender, Fehlerhilfe, PySide6-Bedienwege, Zoom, Fokus, Laienführung, Responsive-Verhalten, Kernkontraste und Repository-Hygiene.

Für den konkreten Hochzoom-Rückfall wird zusätzlich geprüft, dass bei **1.594×900 px und 200 %**:

- Navigationseinträge nicht überlappen,
- Profilzeilen nicht kollidieren,
- die Kartenfläche in eine Spalte wechselt,
- Navigation und Karten bei Bedarf sicher scrollen,
- Zurückzoomen auf 100 % wieder die 2×2-Kartenstruktur herstellt.

Technischer Abnahmestand der Iteration 23:

- GitHub-Grundprüfung **#403**: 75 Logik-/Regressionstests + 50 PySide6-GUI-Tests erfolgreich
- Vollprojekt-Restore: **OK**
- Restore-SHA-256: `69e6cc8b3b5f3838b4478e3c0373ba0cb46c86942927d5b523f78a0cdb16214a`

Vollständiges Restore-Gate:

```bash
python3 scripts/iteration_restore.py
```

## Reale Kubuntu/KDE-X11-Abnahme

Die automatische CI ersetzt keine echte sichtbare Prüfung auf dem Zielrechner. Dafür gibt es:

```bash
bash kubuntu_abnahme.sh
```

Die reale Sichtabnahme bei **100/125/150/175/200 %** in normaler und maximierter Fenstergröße bleibt der nächste visuelle Freigabeschritt.

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
- `docs/ITERATION22_RESPONSIVE_DESIGN.md` – Responsive Design- und Screenshot-Befund
- `docs/ITERATION23_ZOOM_LAYOUT.md` – 200-%-Fehleranalyse, Zoom-Härtung und Abnahme

## Noch offen

1. Den reinen Evidence-/Versions-Sync der Iteration 23 noch einmal vollständig durch CI und Restore prüfen und erst danach PR #25 mergen.
2. Danach reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner bei allen fünf Zoomstufen durchführen.
3. Anschließend verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs nicht unnötig auf Dateiersatz umstellen.

Die detaillierte Versionshistorie steht bewusst **nicht mehrfach in der README**, sondern im `CHANGELOG.md` und den Iterationsdokumenten.
