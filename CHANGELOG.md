# Änderungsverlauf

## 0.14.0 – 2026-09-09 – Laien-UX-Konsistenz

### Geändert
- gesamtes produktives Projekt aus Sicht eines Nutzers ohne technisches Vorwissen auf Einstieg, Sprache, Navigation, Rückmeldung, Fehlermeldungen und Sackgassen geprüft,
- Dashboard-Suche wahrheitsgemäß als Song-Suche bezeichnet und `Logout` durch `Programm beenden` ersetzt,
- technische Oberflächenbezeichnung `Entwicklerinfo` zu `Projekt-Notiz` vereinfacht, ohne das bestehende Speicherformat zu ändern,
- geplante Bereiche sichtbar mit `In Planung` und gestricheltem Zustand von fertigen Bereichen getrennt,
- echte Startwege zu Songtexte, Todo-Liste und Kalender in der Dashboard-Startkarte ergänzt,
- Erstnutzer-Sackgasse in der leeren Songbibliothek durch `＋ Neuen Song schreiben` geschlossen,
- Songbibliothek gegen stille Nicht-Reaktionen bei fehlender Auswahl gehärtet und Datumsanzeige auf deutsches Format umgestellt,
- Songeditor mit Drei-Schritt-Führung, verständlicher Speicheranzeige und Sicherheitsfrage vor dem Entfernen eines Songbereichs ergänzt,
- Wiederherstellung älterer Songversionen zusätzlich nach Vorschau bestätigungspflichtig gemacht; automatische Sicherung des aktuellen Stands bleibt bestehen,
- Todo, Kalender und Profilverwaltung mit eindeutiger Schrittfolge und nächstem sinnvollen Schritt vereinheitlicht,
- Recovery als `Fehlerhilfe (Recovery)` auf einfache Nutzerfragen ausgerichtet; technische Details bleiben standardmäßig verborgen,
- Schnellstart und grafische Startanzeige auf sechs verständliche Prüfschritte umgestellt,
- `ANLEITUNG_LAIEN.md` auf schnellen Einstieg und konkrete Arbeitsabläufe neu strukturiert,
- README auf den aktuellen Stand 0.14.0 synchronisiert und von doppelter Versionshistorie befreit.

### Prüfung / Schutz
- neuer Regressionstest `tests/test_layman_ux_gui.py` prüft wahrheitsgemäße Beschriftungen, sichtbare Planungszustände, Erstnutzer-Songstart, Nicht-Silent-Fail-Verhalten und Sicherheitsbestätigungen,
- Kernkontraste für normalen Text, Hinweistext und Akzent gegen den Hintergrund werden automatisiert auf mindestens 4,5:1 geprüft,
- Laien-UX-Test ist in `bash scripts/pruefen.sh --full` integriert,
- keine Datenmigration, keine Änderung der Song-/Todo-/Kalender-/Profilformate und keine Änderung der atomaren Speicher- oder Restore-Fachlogik,
- finale GitHub-Grundprüfung und Restore-Gate stehen für den vollständigen Iteration-21-Branch noch aus.

## 0.13.4 – 2026-09-09 – Repository-Hygiene

### Geändert
- unreferenziertes Root-Artefakt `ChatGPT Image 8. Sept. 2026, 02_16_14.png` mit 2.056.107 Bytes aus dem Repository entfernt,
- `.gitignore` um typische unsortierte ChatGPT-/Screenshot-Bildexporte ausschließlich im Repository-Root ergänzt,
- neuen Regressionstest `tests/test_repo_hygiene.py` ergänzt,
- Vollprüfung um automatische Kontrolle auf versionierte Laufzeit-/Temp-Artefakte, lokale Root-Screenshots und übergroße Root-Dateien erweitert,
- veralteten, nicht mergebaren PR #2 als überholt geschlossen.

### Schutz / Abnahme
- keine Anwendungs-, Speicher-, Backup-, Restore- oder UI-Fachlogik verändert,
- keine Nutzerdaten verändert oder gelöscht,
- reguläre Projektbilder in passenden Unterordnern bleiben weiterhin versionierbar,
- Grundprüfung #335 zeigte einen Restore-spezifischen Rückfall: der Git-Hygienetest erwartete im entpackten Restore irrtümlich `.git`,
- der Test wurde auf seinen tatsächlichen Geltungsbereich begrenzt; das Restore-Gate selbst blieb unverändert aktiv,
- Grundprüfung #337 war anschließend vollständig erfolgreich, einschließlich Vollprüfung und Restore-Gate,
- geprüfter Head `caefca0d51b158ac9a3c8cfedc6fb18e0899a580` wurde als PR #21 per Squash-Merge übernommen; resultierender Main-Commit `aa66dc5ed106e470a533c4dd9f65cf80b726b05c`.

## 0.13.3 – 2026-09-09 – Backup-/Restore-I/O-Konsistenz

### Geändert
- Backup-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- validiertes ZIP wird vor Veröffentlichung per Datei-`fsync` synchronisiert, atomar ersetzt und der Verzeichniseintrag bestmöglich synchronisiert,
- Tempdateien werden auch bei Fehlern bereinigt,
- SHA-256-Begleitdatei und RESTORE-JSON-Bericht verwenden `app.atomic_io.atomic_write_text`,
- Backup-Dateinamen enthalten Mikrosekunden gegen schnelle Mehrfachlauf-Kollisionen,
- `ZipFile.testzip()` wird explizit ausgewertet und meldet beschädigte Einträge,
- Restore-Regressionen für Altbestandsschutz bei Replace-Fehler und Temp-Cleanup ergänzt.

### Schutz / Abnahme
- Restore-Pfadprüfung, Manifestvergleich, Vollprüfung und Headless-Start bleiben unverändert,
- Append-only Ereignislogs und Nutzerdaten wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #315 war erfolgreich; Vollprüfung und Restore-Gate sind grün bestätigt,
- geprüfter PR-Head `ca6ff3a7eb29a6bbf237a81199a8a8764280784a` wurde als PR #19 per Squash-Merge in `main` übernommen; resultierender Main-Commit `72719acbef5be379c1340b5771962a81fb40fc85`.

## 0.13.2 – 2026-09-09 – Diagnose-I/O-Konsistenz

### Geändert
- Diagnose-ZIP verwendet eindeutige Tempdateien im Zielordner statt eines festen `.tmp`-Namens,
- ZIP-Datei wird vor Veröffentlichung per `fsync` synchronisiert und anschließend atomar ersetzt,
- bestmöglicher Verzeichnis-`fsync` und Temp-Cleanup bei Fehlern ergänzt,
- SHA-256-Begleitdatei auf `app.atomic_io.atomic_write_text` umgestellt,
- Diagnose-Dateinamen um Mikrosekunden ergänzt, damit schnelle Mehrfachexporte nicht kollidieren,
- gezielte Regression für eindeutige Exportnamen und Replace-Fehler ergänzt.

### Schutz / Abnahme
- bestehende Datenschutz- und ZIP-Inhaltsprüfungen bleiben unverändert aktiv,
- Append-only Ereignislogs, Nutzerdaten, Restore-Logik, Backup-Skript und sonstige Berichtsschreiber wurden bewusst nicht verändert,
- GitHub Actions `Grundprüfung` Run #294 war erfolgreich und führte sowohl `bash scripts/pruefen.sh --full` als auch `python3 scripts/iteration_restore.py` aus,
- damit sind Vollprüfung und Restore-Gate für den geprüften Produktionspatch grün nachgewiesen.

## 0.13.1 – 2026-09-08 – Prozess- und Schreibkonsistenz

### Geändert
- zentralen Produktions-Schreibweg `app/atomic_io.py` für Profil-, Todo-, Kalender-, Song-, Versions- und Exportdateien eingeführt,
- feste `.tmp`-Dateinamen durch eindeutige Tempdateien im jeweiligen Zielordner ersetzt,
- Datei-`fsync`, atomaren `os.replace` und bestmöglichen Verzeichnis-`fsync` vereinheitlicht,
- pro Projektordner einen `QLockFile`-basierten Einzelinstanz-Schutz eingeführt,
- Todo-Termine auf dieselbe lokale, zeitzonenlose ISO-8601-Semantik wie Kalendertermine vereinheitlicht,
- ENOSPC-/EROFS-Simulation auf den echten Produktionsschreiber umgestellt,
- gezielte Prozesskonsistenz-Regressionstests ergänzt.

### Schutz / Fehlerbehebung
- ein zweiter schreibender Dashboard-Prozess wird kontrolliert beendet, bevor er Nutzerdaten oder Laufzeitlogs öffnet,
- der Prozesswächter behandelt den kontrollierten Mehrfachstart-Code 10 nicht als Absturz,
- ein Replace-Fehler erhält den vorherigen Datenbestand und hinterlässt keine Tempdatei,
- unterschiedliche Schreibversuche kollidieren nicht mehr über denselben Tempnamen,
- nicht unterstützter Verzeichnis-`fsync` erzeugt nach bereits erfolgreichem Dateiersatz keinen falschen Speicherfehler,
- beschädigte Profilbestände mit doppelten Werten werden nicht mehr still bereinigt, sondern klar abgewiesen,
- die erste CI-Prüfung deckte drei Rückfälle in Testimport, Qt-Testdouble und direktem Simulationsstart auf; alle wurden ursächlich behoben und in der folgenden Vollprüfung verifiziert.

## 0.13.0 – 2026-09-08 – Kalender und Erinnerungen

### Hinzugefügt
- eigenes PySide6-Kalendermodul unter `Planung → Kalender`,
- echte Tages-, Wochen-, Monats- und Jahresbereiche für den gewählten Kalendertag,
- Termine mit Titel, optionaler Notiz, Beginn und Ende,
- Erinnerungen zum Terminbeginn sowie 5/15/30/60 Minuten oder 1 Tag vorher,
- 30-Sekunden-Erinnerungsprüfung als Kind des laufenden Dashboards, auch bei geschlossenem Kalenderfenster,
- gezielte Logik- und GUI-Rückfalltests für Bereichsgrenzen, Mehrtagestermine, Termineingabe, Einmal-Erinnerung, Dashboardbetrieb und Zoom.

### Schutz
- Beginn und Ende verwenden lokale Rechnerzeit ohne erfundene Zeitzonenumrechnung,
- Ende muss nach Beginn liegen; ungültige Termine werden vor dem Schreiben abgewiesen,
- Kalenderdaten werden atomar unter `daten/kalender/termine.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- eine Erinnerung wird erst nach erfolgreicher Anzeige atomar als erinnert markiert,
- Wiedereintritt während einer geöffneten Erinnerung wird blockiert,
- bei vollständig beendetem Dashboard wird bewusst kein separater Hintergrunddienst gestartet,
- keine destruktive Terminlöschung in dieser Iteration,
- bestehende Todo-, Profil-, Song-, Recovery-, Referenz-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.12.0 – 2026-09-08 – Todo-Liste mit Termin und Archiv

### Hinzugefügt
- eigenes PySide6-Todo-Modul unter `Planung → Todo-Liste`,
- Aufgaben mit Pflicht-Titel, optionaler Notiz und optionalem Datum/Uhrzeit-Termin,
- getrennte Ansichten für aktive Aufgaben und Archiv,
- Abhaken verschiebt die vollständige Aufgabe ins Archiv und setzt einen Abschlusszeitpunkt,
- zentrale Zoom-/Schriftsteuerung gilt auch im Todo-Fenster,
- gezielte Logik- und GUI-Rückfalltests für Terminierung, Abhaken, Archiv und Zoom.

### Schutz
- aktive Aufgaben und Archiv liegen zusammen in `daten/todo/todo.json`, damit beim Abhaken kein Zwischenzustand zwischen zwei Dateien entstehen kann,
- Speicherung erfolgt atomar über Tempdatei, `fsync` und `os.replace`,
- ein simulierter Fehler beim atomaren Ersetzen erhält den vorherigen Bestand,
- Abhaken löscht keine Aufgabe; der Eintrag wird vollständig ins Archiv verschoben,
- ungültige Termine und leere Titel werden vor dem Schreiben abgewiesen,
- bestehende Song-, Profil-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.11.0 – 2026-09-08 – profilbasierte DB-Eingaben

### Hinzugefügt
- Profile `HardTechno`, `HipHop/Rap` und `Hörspiele` mit Startwerten,
- getrennte Kategorien Genres, Stimmungen, Stil, Stimme und Besonderheiten,
- PySide6-Profilverwaltung zum Anlegen von Profilen und Werten,
- Profilauswahl direkt in der Dashboard-Karte `DB-Eingaben`,
- sofortige Aktualisierung der Dashboard-Auswahlfelder nach Profiländerungen,
- gezielte Logik- und GUI-Rückfalltests für Profilisolation, Duplikate und Dashboardbefüllung.

### Schutz
- Startprofile liegen bis zur ersten eigenen Änderung nur im Programmbestand und schreiben nicht beim Start,
- eigene Profildaten werden atomar unter `daten/profile/db_profile.json` gespeichert,
- ein simulierter Fehler beim atomaren Ersetzen lässt die vorherige Datei unverändert,
- doppelte Werte werden ohne Beachtung der Groß-/Kleinschreibung abgewiesen,
- Entfernen eines Werts verlangt eine ausdrückliche Bestätigung,
- bestehende Song-, Recovery-, Zoom-, Kubuntu- und Restore-Gates bleiben aktiv.

## 0.10.2 – 2026-09-08 – Zoom und Schriftgrößensteuerung

### Hinzugefügt
- `Strg + Mausrad` für zentrale Zoom-/Schriftgrößenänderung,
- sichtbare `A−`-/`A+`-Schaltflächen mit Prozentanzeige in der Statusleiste,
- Weitergabe der Zoomstufe an Dashboard, offene Songeditoren, Songbibliothek und Recovery,
- gezielter PySide6-GUI-Rückfalltest für Mausrad, Zoomgrenzen und sichtbare Bedienung.

### Schutz
- bestehende Zoomstufen 100/125/150/175/200 % bleiben unverändert,
- kein zweites Schriftgrößensystem eingeführt,
- keine Nutzerdaten verändert,
- globaler Ereignisfilter wird beim Schließen des Dashboards wieder entfernt.

## 0.10.1 – 2026-09-08 – Kubuntu/X11-Endabnahme vorbereitet

### Hinzugefügt
- neuer Klickstart `kubuntu_abnahme.sh`,
- neuer PySide6-Abnahmeassistent `scripts/kubuntu_abnahme.py`,
- Vorprüfung auf Linux, echte X11-Sitzung und KDE/Plasma,
- echter SIGTERM-/Prozesswächtertest ausschließlich in Tempdaten,
- sichtbare Bestätigung für Referenzlayout, Tastaturfokus und Zoomstufen 100/125/150/175/200 %,
- TXT- und JSON-Abnahmeberichte unter `berichte/`,
- gezielte Tests für X11/KDE-Erkennung, Signalprobe und Berichtsstatus.

### Schutz
- Wayland oder fehlendes `DISPLAY` werden nicht still als X11 akzeptiert,
- der Signaltest verändert keine Song-, Versions- oder sonstigen Nutzerdaten,
- `OK` wird nur vergeben, wenn automatische Prüfungen und alle sichtbaren Bestätigungen erfolgreich sind,
- Offscreen-CI wird ausdrücklich nicht als reale Kubuntu/KDE-X11-Sichtabnahme gewertet.

## 0.10.0 – 2026-09-08 – PySide6-Referenzdashboard

### Geändert
- gesamte produktive Oberfläche einheitlich auf **PySide6 6.11.2** migriert,
- Dashboardtitel auf `Provoware-Datenbank-Dashboard 2026` gesetzt,
- Dashboard nach dem bereitgestellten Dark-Orange-Referenzentwurf neu strukturiert: kompakter Header, Schnellkachelleiste, einklappbare linke Navigation, schmale „Zuletzt bearbeitet“-Zeile, 2×2-Hauptkarten und Statusleiste,
- zentrale Qt/QSS-Standards für Farben, Abstände, Schriftgrößen, Fokus und Zoom eingeführt,
- Songeditor, Songbibliothek, Recovery-Zentrale und grafische Startanzeige auf PySide6 umgestellt,
- Recovery aus der Dashboard-Hauptfläche entfernt und als einzelner Navigationspunkt `Werkzeug → Recovery` geführt,
- GitHub-CI auf Qt-Offscreen-Prüfung und die für PySide6 benötigte `libegl1`-Systembibliothek umgestellt.

### Schutz
- bestehendes Song-Textformat und alle Nutzerdatenpfade bleiben unverändert,
- Autosave, Fokusverlust-Speicherung, Versionierung, Restore-Sicherung, Favoriten/Status, Metadaten und Exporte bleiben erhalten,
- geplante noch nicht freigegebene Dashboardbereiche verändern keine Daten,
- zusätzlicher Referenzlayout-Test prüft Kartenstruktur/-proportionen, Sidebarbreiten, Schnellkacheln, Dark-Orange-Akzent und exakt einen Recovery-Eintrag,
- produktive GUI-Dateien werden auf unerlaubte Tkinter-Reste geprüft,
- bestehende Logik-, Sicherheits-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Gates bleiben verbindlich.

## 0.9.1 – 2026-09-08 – CI-Wartung

### Geändert
- GitHub Actions Checkout von `actions/checkout@v4` auf **`v7.0.1`** aktualisiert.

### Schutz
- keine fachliche Funktion, Songdatei oder Laufzeitlogik verändert,
- vollständige bestehende Logik-, Tk-GUI-, ENOSPC-/EROFS-, Release-, Headless- und Restore-Prüfung bleibt unverändert verbindlich.

## 0.9.0 – 2026-09-08 – Songbibliothek vervollständigt

### Hinzugefügt
- freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags,
- kombinierbare Filter nach Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten,
- Favoritenkennzeichnung im Editor und Favoritenfilter in der Bibliothek,
- Bearbeitungsstatus `Idee`, `Entwurf`, `Überarbeitung`, `Fertig`,
- Sortierung nach letzter Bearbeitung, Titel, Genre, Tags und Status,
- Gruppierung nach Genre, Tags und Status,
- Versionswiederherstellung aus der schreibgeschützten Vorschau heraus,
- gezielte Logik- und Tk-GUI-Tests für Suche, Filter, Gruppierung, Status/Favorit und Restore.

### Schutz
- ältere Songdateien ohne Status/Favorit bleiben lesbar und erhalten nur sichere Standardwerte,
- Filtern, Sortieren und Gruppieren sind reine Ansichtsoperationen,
- vor jeder tatsächlichen Versionswiederherstellung wird der aktuelle Song erneut als Versionsstand gesichert,
- die Restore-Funktion akzeptiert nur die direkte Arbeitsdatei und den zugehörigen `.versionen/<Titel>/`-Pfad,
- fremde Versionspfade werden vor Schreibzugriff abgewiesen,
- Arbeitsdatei und Sicherungsstand werden atomar geschrieben,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.8.0 – 2026-09-08 – Songbibliothek und Versionsverwaltung

### Hinzugefügt
- Songbibliothek mit Titel, Genre, letzter Bearbeitung und Versionsanzahl,
- direktes Öffnen vorhandener Songs per Doppelklick, Enter oder Schaltfläche,
- bis zu fünf zuletzt bearbeitete Songs als Schnellkacheln im Dashboard,
- Song-Metadaten Stimmung, Stil, Stimme, Besonderheiten und Tags,
- automatische Versionsschnappschüsse vor geänderten Überschreibungen,
- schreibgeschützte Vorschau älterer Versionsstände,
- Exporte als TXT, Markdown, JSON und Nur-Songtext-TXT,
- Rückwärtslesen der bisherigen 0.7.0-Textdateien,
- gezielte Logik- und Tk-GUI-Tests für Bibliothek, Metadaten, Versionen, Kacheln und Exporte.

### Schutz
- das bestehende `.txt`-Arbeitsformat bleibt kanonisch; kein paralleles internes Songformat,
- identische Speicherungen erzeugen keinen Versionsmüll,
- Versionsstände werden getrennt unter `.versionen/` gesichert und nicht still überschrieben,
- Versionsansicht ist zunächst schreibgeschützt,
- Exporte verändern weder Arbeitsdatei noch Versionshistorie,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.7.0 – 2026-09-08 – Dashboard-Schnellspeicher und Songtexteditor

### Hinzugefügt
- einzeilige Entwickler-Schnelleingabe im Dashboardheader mit Enter- und Schaltflächenbestätigung,
- append-only Speicherung mit Zeitstempel in `Entwicklerinformation.txt`,
- Songtexteditor mit Titel, optionalem Genre, optionalem Sonstiges und Live-Vorschau,
- auswählbare Bereiche Intro, Strophe, Pre-Chorus, Refrain, Hook, Bridge, Outro, Spoken und Instrumental,
- atomare Speicherung unter `daten/songtexte/<Titel>.txt`,
- Autosave alle fünf Minuten sowie bei Fokusverlust und beim Schließen,
- Logout-Schaltfläche mit Speichern aller offenen Songeditoren vor Sitzungsende,
- gezielte Logik- und Tk-GUI-Tests für Schnelleingabe, Speicherpfad, Bereichswechsel, Autosave und Logout.

### Schutz
- Schnellinfos überschreiben vorhandene Informationen nicht,
- Songdateien werden über eine temporäre Datei atomar ersetzt,
- ein Titelwechsel löscht keinen vorherigen Songstand,
- Logout wird gestoppt, wenn ein offener Songtext nicht gespeichert werden kann,
- bestehende Recovery-, Diagnose-, Datenschutz-, Wächter- und Restore-Gates bleiben aktiv.

## 0.6.0 – 2026-09-08 – Debug- und Recovery-Zentrale

### Hinzugefügt
- kombinierbare Filter nach Schweregrad und Bereich,
- Ereignisdetails per Doppelklick, Enter oder Schaltfläche,
- Wiederholungszähler und dauerhaft gespeichertes erstes Auftreten,
- zentrale Zoomstufen 100/125/150/175/200 Prozent,
- standardmäßig eingeklappte technische Details,
- gefahrlose `ENOSPC`-/`EROFS`-Simulation ohne echten Datenträgerverbrauch,
- automatisierte Tk-GUI-Prüfung für Tastatur, Fokus, Detailansicht und Zoom.

### Bedienung
- `F5` aktualisiert,
- `Ctrl++` und `Ctrl+-` ändern die Anzeigegröße,
- `Ctrl+0` setzt auf 100 Prozent,
- `Escape` schließt Detailfenster,
- interaktive Filter, Tabelle und Schaltflächen sind in der Fokusreihenfolge.

### Schutz
- Schreibfehlersimulation arbeitet ausschließlich in temporären Testpfaden,
- vorhandener Bestand muss bei simuliertem Fehler unverändert bleiben,
- ohne echte Tk-Sitzung wird die GUI-Prüfung nicht als bestanden gewertet,
- vorhandene Restore-, Diagnose-, Redaktions- und Wächter-Gates bleiben aktiv.

## 0.5.0 – 2026-09-08 – Diagnose- und Logging-Härtung

### Hinzugefügt
- Größen-/Altersrotation für das Ereignislog mit maximal fünf Archiven,
- Quarantäne beschädigter JSONL-Zeilen mit bereinigter Beweiskopie,
- datenschutzgeprüftes Diagnosepaket mit SHA-256,
- eigenes `ENDE`-Ereignis bei kontrolliertem Programmabschluss,
- gezielte Tests für Rotation, Quarantäne, Diagnoseexport und normales Programmende.

### Schutz
- beschädigte Logzeilen werden nicht mehr still verworfen,
- gültige Logzeilen bleiben beim Bereinigen atomar erhalten,
- Diagnosepakete enthalten nur bereinigte Textkopien und keine unveränderten Rohprotokolle,
- Datenschutzprüfung läuft unmittelbar vor ZIP-Übernahme erneut,
- vorhandene Restore-, Headless- und Wächter-Gates bleiben aktiv.

## 0.4.0 – 2026-09-08 – Recovery-Härtung

### Hinzugefügt
- vollständige Iterations-ZIP-/Restore-Kette mit SHA-256, sicherem Entpacken, Manifestvergleich, Vollprüfung und Headless-Start,
- fensterlose Startabnahme über `python3 -m app.main --headless-check`,
- separate Prozesswache `scripts/process_watch.py`,
- zentrale Log-Bereinigung `app/redaction.py`,
- gezielte Sicherheits-, Wächter- und Restore-Tests,
- sechsten Start-Checkpoint für Prozesswache/Headless-Gate,
- CI-Restore-Gate auf jedem Push und Pull Request.

## 0.3.0 – 2026-09-08 – Regression, Start, Standards und Release
- `REG-LOG-001` behebt `recent(0)`.
- globale UI-Standards, Start-Checkpoints und manifestgesteuerter Releasefilter ergänzt.
