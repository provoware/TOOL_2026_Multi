# TODO – TOOL_2026_Multi

Stand: 2026-09-08

## Ampel
🟢 erledigt und geprüft · 🟡 teilweise · 🔴 offen · ⚫ blockiert

## Iteration 9 – Songbibliothek vervollständigen

- 🟢 freie Suche über Titel, Genre, Stimmung, Stil, Stimme und Tags.
- 🟢 kombinierbare Filter für Genre, Stimmung, Stil, Stimme, Tags, Status und Favoriten.
- 🟢 Favoriten im Songeditor speicherbar und in der Bibliothek filterbar.
- 🟢 Bearbeitungsstatus Idee, Entwurf, Überarbeitung, Fertig integriert.
- 🟢 Sortierung nach zuletzt bearbeitet, Titel, Genre, Tags und Status; Gruppierung nach Genre, Tags und Status.
- 🟢 Versionswiederherstellung nur nach Vorschau; aktueller Stand wird unmittelbar davor automatisch als neuer Versionsstand gesichert.
- 🟢 fremde Versionspfade werden abgewiesen; ältere 0.7.0/0.8.0-Songs bleiben lesbar.

## 3 nächste Schritte

1. 🔴 kleine separate Wartungsiteration: `actions/checkout@v4` wegen Node-20-Abkündigungswarnung auf aktuell unterstützte Version aktualisieren und CI/Restore erneut prüfen.
2. 🟡 Songworkflow ist als erster Fachbereich belastbar vorhanden; weitere geplante Module/Arbeitsabläufe des Multitools priorisieren und einzeln ergänzen.
3. 🔴 reale Kubuntu-Endprüfung einschließlich echtem Crash-/Signaltest, Songbibliothek-/Editor-Endabnahme sowie sichtbarer Fokus-/Zoom-Prüfung dokumentieren.
