# Provoware-Datenbank-Dashboard 2026

> **Version:** 0.14.0 · **Stand:** 09.09.2026 · **Status:** ausführbarer Kern, automatische Prüfungen aktiv, reale Kubuntu/KDE-X11-Sichtabnahme noch offen

Provoware ist ein erweiterbares Desktop-Dashboard für Songtexte, kreative Vorgaben, Aufgaben, Kalender und sichere Projektverwaltung. Die Oberfläche ist auf **einfache Bedienung ohne technisches Vorwissen** ausgelegt.

## Schnellstart

Im Projektordner:

```bash
bash schnellstart.sh
```

Der Schnellstart richtet die benötigte Umgebung bei Bedarf selbst ein, prüft den Projektstart in sechs Schritten und öffnet danach das Dashboard.

Für eine ausführliche Bedienanleitung siehe:

```text
ANLEITUNG_LAIEN.md
```

## Was ist direkt nutzbar?

- 🟢 **Songtexte** – neue Songs schreiben, vorhandene Songs suchen, filtern, sortieren und öffnen
- 🟢 **Ältere Songversionen** – erst Vorschau, dann bestätigte Wiederherstellung; aktueller Stand wird vorher gesichert
- 🟢 **Profile & Vorgaben** – Genres, Stimmungen, Stil, Stimme und Besonderheiten je Profil verwalten
- 🟢 **Todo-Liste** – Aufgaben mit optionalem Termin anlegen und erledigte Aufgaben sicher archivieren
- 🟢 **Kalender** – Tag/Woche/Monat/Jahr, Termine und Erinnerungen
- 🟢 **Fehlerhilfe (Recovery)** – einfache Erklärung, Schutzmaßnahme und nächster Schritt; technische Details nur bei Bedarf
- 🟢 **Zoom 100–200 %** – gemeinsam für alle Hauptfenster

## Was ist noch geplant?

Noch nicht fertige Bereiche werden in der Oberfläche ausdrücklich mit **„In Planung“** gekennzeichnet und gestrichelt dargestellt. Ein Klick verändert keine Daten.

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

Darum wurden technische Primärbegriffe aus der normalen Bedienung entfernt oder erklärt. Beispiele:

- Dashboard-Suche heißt **„Songs durchsuchen“**, weil sie tatsächlich nur die Songbibliothek durchsucht.
- **„Programm beenden“** ersetzt die missverständliche Bezeichnung „Logout“.
- **„Projekt-Notiz“** ersetzt die technische Oberflächenbezeichnung „Entwicklerinfo“; das bestehende Dateiformat bleibt kompatibel.
- Geplante Funktionen sehen nicht mehr wie fertige Funktionen aus.
- Aktionen ohne Auswahl zeigen einen verständlichen Hinweis statt still nichts zu tun.

## Songtexte

### Neuen Song beginnen

**Songtexte** öffnen und oben **„＋ Neuen Song schreiben“** anklicken.

Im Editor:

1. Titel eintragen.
2. Songbereich wählen oder hinzufügen.
3. Text schreiben.

Änderungen werden automatisch gespeichert. Zusätzlich steht **„Jetzt speichern“** bzw. `Strg+S` zur Verfügung.

### Sicheres Entfernen und Wiederherstellen

- Ein Songbereich wird erst nach einer Sicherheitsfrage entfernt.
- Eine ältere Songversion wird erst nach Vorschau und zusätzlicher Bestätigung wiederhergestellt.
- Vor einer Wiederherstellung sichert Provoware den aktuellen Stand automatisch.

### Songdaten

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

Ein Profil bündelt zusammenpassende Werte, zum Beispiel für **HardTechno**, **HipHop/Rap** oder **Hörspiele**.

Eigene Profildaten:

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

Der Kalender bietet echte Tages-, Wochen-, Monats- und Jahresbereiche. Erinnerungen funktionieren, solange das **Hauptprogramm geöffnet** ist; das Kalenderfenster selbst darf geschlossen sein.

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

Sie prüft unter anderem:

- Syntax und Startfähigkeit
- Fachlogik und bekannte Rückfälle
- Datensicherheit und Restore
- Songeditor und Songbibliothek
- Profile, Todo und Kalender
- Fehlerhilfe
- reale PySide6-Bedienwege im Offscreen-Test
- Zoom und Fokus
- Laienführung, wahrheitsgemäße Beschriftungen und Nicht-Silent-Fail-Verhalten
- wichtige Textkontraste mit mindestens 4,5:1
- Repository-Hygiene

Vollständiges Restore-Gate:

```bash
python3 scripts/iteration_restore.py
```

## Reale Kubuntu/KDE-X11-Abnahme

Die automatische CI ersetzt keine echte sichtbare Prüfung auf dem Zielrechner. Dafür gibt es:

```bash
bash kubuntu_abnahme.sh
```

Diese reale Sichtabnahme bleibt der nächste Freigabeschritt nach erfolgreicher Iteration 21.

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
- `docs/ITERATION21_LAIEN_UX.md` – Befund und Abnahme der aktuellen UX-Iteration

## Noch offen

1. Iteration 21 nur nach grüner Vollprüfung und grünem Restore-Gate in `main` übernehmen.
2. Danach reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner durchführen.
3. Anschließend verbleibende direkte Berichtsschreiber separat auditieren; Append-Logs nicht unnötig auf Dateiersatz umstellen.

Die detaillierte Versionshistorie steht bewusst **nicht mehr doppelt in der README**, sondern ausschließlich im `CHANGELOG.md` und den Iterationsdokumenten.
