# TODO – TOOL_2026_Multi

Stand: 2026-09-08

## Ampel
🟢 erledigt und geprüft · 🟡 teilweise · 🔴 offen · ⚫ blockiert

## Iteration 7 – Dashboard-Schnellspeicher und Songtexteditor

- 🟢 einzeiliges Entwickler-Schnellinfofeld im Dashboardheader mit Enter/Schaltfläche und append-only Zeitstempeldatei.
- 🟢 Songtexteditor mit Titel, optionalem Genre, optionalem Sonstiges, auswählbaren Songbereichen und Vorschau.
- 🟢 Songtexte werden atomar unter `daten/songtexte/<Titel>.txt` gespeichert; Titelwechsel löscht keinen alten Stand.
- 🟢 Autosave alle 5 Minuten sowie bei Fokusverlust und beim Schließen ergänzt.
- 🟢 Logout speichert offene Songeditoren und beendet die Sitzung nur nach erfolgreicher Speicherung.

## 2 verbleibende nächste Schritte

1. 🟡 erster Fachworkflow „Songtexte“ vorhanden; weitere geplante Module/Arbeitsabläufe des Multitools noch ergänzen und priorisieren.
2. 🔴 reale Kubuntu-Endprüfung einschließlich echtem Crash-/Signaltest, Songeditor-Endabnahme sowie sichtbarer Fokus-/Zoom-Prüfung dokumentieren.
