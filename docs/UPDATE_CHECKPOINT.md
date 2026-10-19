# Getrennte Programmsicherung und Rückkehrkopie (Iteration 59)

**Entwicklungskandidat, keine automatische Programminstallation.**

Der bestehende Update-Manager prüft ein fremdes ZIP zunächst statisch und kann es optional in Linux-Isolierung testen. Die neue Checkpoint-Stufe ergänzt eine eigene Sicherung **des aktiven Programmcodes**. Dabei werden ausschließlich jene Dateien erfasst, die das aktive `MANIFEST.json` als Betriebsdateien freigibt. Persönliche Ordner wie `daten/` werden nicht erfasst und nicht berührt. Sie haben eine **eigene** Datensicherung.

### Benutzung durch Entwickler

1. Zunächst Update-Staging wie in [UPDATE_STAGING.md](UPDATE_STAGING.md) beschrieben prüfen.
2. Einen **anderen** Sicherungsordner außerhalb des aktiven Projekts auswählen.
3. `python3 scripts/update_checkpoint.py --root . --staging /pfad/provoware-update-... --checkpoint-parent /anderer/ordner`
4. Die Prüfsummen werden gespeichert und anschließend erneut kontrolliert.
5. Optional kann ein **drittes, getrenntes** Rückkehrverzeichnis mit `--restore-parent /dritter/ordner` erstellt werden.

### Sicherheitsvertrag

- Reguläre Dateien mit erlaubten Pfaden, ohne Links oder Spezialdateien; Datei- und Gesamtgrößen begrenzt.
- Während der Sicherung werden veränderte Quelldateien erkannt. Bei Fehlern wird ausschließlich der gerade angelegte Sicherungsordner entfernt.
- Eine Rückkehrkopie entsteht nur in einem **neuen** Verzeichnis und wird vollständig gegen die gesicherten Prüfsummen verglichen.
- Wiederherstellung **niemals** in das aktive Projekt, niemals automatische Datenmigration, niemals Umbenennen/Löschen der alten Installation.
- Statusberichte kennzeichnen immer `activation_allowed=false` und `active_project_changed=false`.
- Ein vollständiger, automatischer Rollback erfordert später eine getrennte, geprüfte Aktivierung mit zwei Versionen und atomarer Umschaltung sowie Nachkontrolle; dieser Schritt ist **noch nicht implementiert**.

Die automatische GitHub-Prüfung ist verbindlich. Die nächste vollständige manuelle Kubuntu-Abnahme erfolgt erst nach Fertigstellung aller vereinbarten Module.
