# TODO – TOOL_2026_Multi

Stand: 2026-09-08

## Ampel
🟢 erledigt und geprüft · 🟡 teilweise · 🔴 offen · ⚫ blockiert

## Iteration 5 – Diagnose- und Logging-Härtung

- 🟢 Diagnosepaket mit automatischer Datenschutzprüfung ergänzt.
- 🟢 Logrotation mit Größenlimit 2 MiB, Alterslimit 30 Tage und maximal 5 Archiven ergänzt.
- 🟢 beschädigte JSONL-Zeilen werden bereinigt in `logs/quarantaene/` gesichert und gültige Zeilen atomar erhalten.
- 🟢 kontrolliertes Programmende wird als eigenes `ENDE`-Ereignis protokolliert.

## 9 verbleibende nächste Schritte

1. 🔴 fachlichen Hauptzweck und echte Arbeitsabläufe festlegen.
2. 🔴 Filter nach Schweregrad und Bereich im Debug/Log ergänzen.
3. 🔴 Ereignisdetails direkt aus der Dashboard-Zeile öffnen.
4. 🔴 Wiederholungszähler und ersten Zeitpunkt anzeigen.
5. 🔴 Schreibfehler bei vollem Datenträger gezielt simulieren.
6. 🔴 Tastaturbedienung und sichtbaren Fokus vollständig prüfen.
7. 🟡 hohe Kontraste vorhanden; Nutzer-Zoom/Schriftgrößenumschaltung fehlt.
8. 🔴 technische Details in der Oberfläche standardmäßig einklappen.
9. 🔴 reale Kubuntu-Endprüfung einschließlich echtem Crash-/Signaltest dokumentieren.
