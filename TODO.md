# TODO – TOOL_2026_Multi

Stand: 2026-09-08

## Ampel
🟢 erledigt und geprüft · 🟡 teilweise · 🔴 offen · ⚫ blockiert

## Iteration 4 – Recovery-Härtung

- 🟢 Vollprojekt-ZIP automatisiert erzeugt und SHA-256 direkt geprüft.
- 🟢 ZIP-Pfade gegen `..` und absolute Pfade abgesichert.
- 🟢 Wiederherstellung erfolgt ausschließlich in einen neuen Restore-Ordner.
- 🟢 Wiederhergestelltes Manifest wird gegen den Ausgangsstand verglichen.
- 🟢 Vollprüfung und Headless-Start werden im Restore-Ordner ausgeführt.
- 🟢 Headless-Startweg ohne Fenster in `app.main` ergänzt.
- 🟢 separate Prozesswache für fehlerhaften/harten Prozessabschluss ergänzt.
- 🟢 sensible Protokollwerte werden zentral vor Persistierung und Rückfalllernen bereinigt.

## 13 verbleibende nächste Schritte

1. 🔴 fachlichen Hauptzweck und echte Arbeitsabläufe festlegen.
2. 🔴 Diagnosepaket mit bewusster Datenschutzfreigabe exportieren.
3. 🔴 Filter nach Schweregrad und Bereich im Debug/Log ergänzen.
4. 🔴 Protokollrotation mit Größen-/Altersgrenze umsetzen.
5. 🔴 Ereignisdetails direkt aus der Dashboard-Zeile öffnen.
6. 🔴 Wiederholungszähler und ersten Zeitpunkt anzeigen.
7. 🔴 beschädigte Protokolle getrennt sichern und verständlich melden.
8. 🔴 Schreibfehler bei vollem Datenträger gezielt simulieren.
9. 🔴 Tastaturbedienung und sichtbaren Fokus vollständig prüfen.
10. 🟡 hohe Kontraste vorhanden; Nutzer-Zoom/Schriftgrößenumschaltung fehlt.
11. 🔴 kontrolliertes Beenden als eigenes Ereignis erfassen.
12. 🔴 technische Details in der Oberfläche standardmäßig einklappen.
13. 🔴 reale Kubuntu-Endprüfung einschließlich echtem Crash-/Signaltest dokumentieren.
