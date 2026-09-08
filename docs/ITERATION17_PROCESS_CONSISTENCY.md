# Iteration 17 – Prozess- und Schreibkonsistenz

## Ziel

Alle schreibenden Kernbereiche sollen denselben abgesicherten Dateischreibweg verwenden. Gleichzeitig darf pro Projektordner nur eine schreibende Dashboard-Instanz laufen.

## Befund

Vor dieser Iteration hatten Profil-, Todo-, Kalender- und Songdaten eigene, ähnliche Atomar-Schreibimplementierungen. Sie nutzten feste `.tmp`-Namen und synchronisierten nach `os.replace` den Verzeichniseintrag nicht. Außerdem konnte ein zweites Dashboard denselben Datenbestand gleichzeitig öffnen. Das machte verlorene Änderungen bei Mehrfachstart prinzipiell möglich.

Die bisherige ENOSPC-/EROFS-Simulation prüfte zudem einen separaten Probe-Schreiber und nicht den produktiven Schreibweg.

## Umsetzung

- `app/atomic_io.py` ist der gemeinsame Produktions-Schreibweg.
- jede Speicherung verwendet eine eindeutige Tempdatei im Zielordner,
- Dateiinhalt wird vor dem Ersetzen mit `fsync` gesichert,
- `os.replace` ersetzt erst den vollständig geschriebenen Stand,
- auf POSIX wird danach auch der Verzeichniseintrag mit `fsync` gesichert,
- Tempdateien werden auch bei Fehlern entfernt,
- Profil-, Todo-, Kalender- und Songdateien verwenden denselben Weg.

## Mehrfachstart

`app/process_guard.py` verwendet `QLockFile`. Pro Projektordner ist genau eine schreibende Programminstanz erlaubt. Ein zweiter Start beendet sich kontrolliert mit Rückgabecode 10 und verändert keine Nutzerdaten. Der Prozesswächter behandelt diesen Code ausdrücklich nicht als Absturz.

Eine eindeutig verwaiste Sperre nach einem harten Absturz kann von Qt nach der festgelegten Stale-Zeit wieder entfernt werden.

## Weitere Inkonsistenzen behoben

- Todo-Termine folgen jetzt derselben lokalen, zeitzonenlosen ISO-8601-Semantik wie Kalendertermine.
- beschädigte Profilbestände mit doppelten Werten werden nicht mehr still bereinigt, sondern klar abgewiesen.
- die ENOSPC-/EROFS-Simulation arbeitet jetzt direkt gegen `app.atomic_io.atomic_write_text`.

## Abnahme

1. alte Datei bleibt bei simuliertem Replace-Fehler bytegleich,
2. zwei Schreibversuche verwenden unterschiedliche Tempdateinamen,
3. nach Fehler bleiben keine Tempdateien zurück,
4. zweite Instanz wird blockiert, nach Freigabe ist ein neuer Start möglich,
5. kontrollierter Mehrfachstart erzeugt keinen Absturzbericht,
6. bestehende Profil-, Todo-, Kalender-, Song-, Recovery-, GUI-, Release-, Headless- und Restore-Tests bleiben grün.
