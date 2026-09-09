# Iteration 21 – Laien-UX-Konsistenz

Stand: 2026-09-09

## Hauptziel

Das gesamte produktive Projekt aus Sicht eines absoluten Laien prüfen und die Bedienung so vereinheitlichen, dass jederzeit erkennbar ist:

1. Wo bin ich?
2. Was kann ich hier tun?
3. Was ist bereits fertig und was nur geplant?
4. Was passiert nach einem Klick?
5. Was wurde bei einem Fehler geschützt?
6. Was ist der nächste sinnvolle Schritt?

Fachlogik, Speicherformate und Nutzerdatenpfade werden nicht umgebaut.

## Befund vor der Änderung

- Das Suchfeld im Dashboard hieß allgemein `Suchen …`, durchsuchte tatsächlich aber nur Songs.
- `Logout` beendete faktisch das Programm und war daher falsch benannt.
- `Entwicklerinfo` und der sichtbare Dateiname `Entwicklerinformation.txt` waren für normale Nutzer unnötig technisch.
- Geplante Bereiche wirkten teilweise wie fertige Funktionen.
- Mehrere Aktionen reagierten bei fehlender Auswahl gar nicht sichtbar, z. B. Song öffnen oder Versionsstände öffnen.
- Startanzeige und Schnellstart verwendeten Begriffe wie Abhängigkeiten, Headless, PySide6 und Prozesswache als primäre Nutzersprache.
- Songbereiche konnten ohne Sicherheitsfrage entfernt werden.
- Versionswiederherstellung hatte zwar Vorschau und automatische Sicherung, aber keine abschließende Bestätigung.
- Fehlerhilfe verwendete viele Diagnosebegriffe, obwohl die zugrunde liegenden Ereignisse bereits einfache Erklärungen enthalten.
- `ANLEITUNG_LAIEN.md` begann direkt mit Terminal- und Technikdetails statt mit einem kurzen Bedienweg.
- README war beim Versionsstand hinter dem tatsächlichen Projektstand zurück.

## Umgesetzt

### Dashboard

- Suchfeld eindeutig als Song-Suche bezeichnet.
- `Logout` in `Programm beenden` geändert; Tooltip erklärt das vorherige Speichern.
- `Projekt-Notiz` ersetzt die technische Bezeichnung in der Oberfläche; Dateiformat bleibt kompatibel.
- Fertige und geplante Bereiche visuell getrennt; geplante Bereiche tragen ausdrücklich `In Planung`.
- Startkarte mit direkten Schritten zu Songtexte, Todo und Kalender.
- Datenkarte auf tatsächlich nutzbare Profilfelder reduziert; GitHub-Repositories und Prompts werden nur noch als geplant genannt.
- Statusleiste nennt den nächsten sinnvollen Schritt statt Framework-/Theme-Details.

### Songeditor und Songbibliothek

- klare Drei-Schritt-Führung im Editor,
- `Export` zu `Exportieren`, `Autosave` zu verständlicher deutscher Rückmeldung,
- Sicherheitsfrage vor dem Entfernen eines Songbereichs,
- keine stille Aktion mehr bei fehlender Songauswahl,
- deutsche Datumsanzeige in der Bibliothek,
- eindeutige Leer-/Kein-Treffer-Hinweise,
- zusätzliche Bestätigung vor Versionswiederherstellung; automatische Sicherung des aktuellen Stands bleibt aktiv.

### Todo, Kalender und Profile

- Schrittfolgen und eindeutige Statushinweise,
- klarere Bezeichnungen wie `Aufgabe`, `Termin hinzufügen`, `Fällig am`,
- Archivwirkung ausdrücklich erklärt: erledigte Aufgabe wird nicht gelöscht,
- Kalender weist sichtbar darauf hin, dass Erinnerungen nur bei laufendem Hauptprogramm funktionieren,
- Profilbegriff direkt in der Oberfläche erklärt.

### Fehlerhilfe

- Recovery als `Fehlerhilfe (Recovery)` bezeichnet,
- Spalten und Details auf Nutzerfragen umgestellt: `Was ist passiert?`, `Was wurde geschützt?`, `Was soll ich jetzt tun?`,
- technische Details weiterhin verfügbar, aber standardmäßig verborgen.

### Start und Anleitung

- sechs Startschritte in einfache Sprache übersetzt,
- technische Begriffe nur noch in echten Fehlerhinweisen, wenn sie zur Reparatur nötig sind,
- Laienanleitung auf 30-Sekunden-Start, fertige/geplante Bereiche und konkrete Arbeitsabläufe neu strukturiert.

## Automatische Abnahme

Neuer Regressionstest `tests/test_layman_ux_gui.py` prüft unter anderem:

- wahrheitsgemäße Beschriftung der Song-Suche,
- `Programm beenden` statt `Logout`,
- sichtbare Markierung aller geplanten Schnellkacheln,
- klare nächste Schritte in Unterfenstern,
- keine stille Reaktion bei fehlender Songauswahl,
- Bestätigung vor Songbereich-Entfernung,
- Mindestkontrast 4,5:1 für zentrale Text-, Hinweis- und Akzentfarben gegen den Hintergrund.

Der Test ist in `bash scripts/pruefen.sh --full` integriert.

## Schutzgrenzen

- keine Datenmigration,
- keine Änderung der kanonischen Song-, Todo-, Kalender- oder Profildateien,
- keine Änderung der atomaren Speicherlogik,
- keine Änderung der Restore-/Backup-Fachlogik,
- keine neue Hauptfunktion außerhalb des bestehenden Umfangs.

## Gate

Vor Merge erforderlich:

```bash
bash scripts/pruefen.sh --full
python3 scripts/iteration_restore.py
```

Zusätzlich bleibt die reale sichtbare Kubuntu/KDE-X11-Abnahme auf dem Zielrechner offen.
