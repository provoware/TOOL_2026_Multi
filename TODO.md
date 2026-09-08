# TODO – TOOL_2026_Multi

Stand: 2026-09-08

## Ampellegende

- 🟢 erledigt und geprüft
- 🟡 geplant / teilweise vorbereitet
- 🔴 offen
- ⚫ blockiert

## Iteration 1 – Entwicklungsgrundlage

- 🟢 Projektregeln zentral definiert.
- 🟢 Ordnertrennung festgelegt.
- 🟢 Sicherungskonzept definiert.
- 🟢 Fehler- und Rückfallmanagement definiert.
- 🟢 Prüfskript angelegt.
- 🟢 Schnellstart-Grundgerüst angelegt.
- 🟢 Textregistrierung vorbereitet.
- 🟢 GitHub-Prüfablauf vorbereitet.

## Iteration 2 – Debug/Log und Rückfallschutz

- 🟢 ausführbaren Dashboard-Kern bereitgestellt.
- 🟢 zentrale Ereignisprotokollierung als wiederverwendbares Modul umgesetzt.
- 🟢 verständlichen TXT-Bericht und maschinenlesbare JSON-Zeile erzeugt.
- 🟢 zentrale Start- und Oberflächenfehler abgefangen.
- 🟢 wiederkehrende Fehlermuster datensparsam erkannt.
- 🟢 letzte fünf Ereignisse im Dashboard dargestellt.
- 🟢 gezielte Rückfalltests in den begrenzten Prüfablauf eingebunden.

## Iteration 3 – Regression, Start, Standards und Release

- 🟢 `LOG-FEHLER-001` reproduziert: `recent(0)` lieferte wegen `[-0:]` fälschlich alle Ereignisse.
- 🟢 `REG-LOG-001` ergänzt; nichtpositive Grenzen liefern jetzt eine leere Liste.
- 🟢 Nachbarweg `recent(1)` separat geprüft und unverändert korrekt.
- 🟢 Rückfallregister führt `REG-LOG-001` mit Statuswechsel **OFFEN → BEHOBEN**.
- 🟢 globale Farben, Abstände, Schriften und Ampeldarstellung in `app/ui_standards.py` zentralisiert.
- 🟢 Schnellstart um fünf echte Checkpoints, grafische Statusanzeige und Konsolenfallback erweitert.
- 🟢 unnötigen Paketabgleich vermieden: ohne externe Anforderungen wird `pip` nicht aufgerufen.
- 🟢 Veröffentlichungsweg auf ausschließlich `release: true` markierte Manifest-Dateien begrenzt und getestet.
- 🟢 `INFO_DATEIEN_AGENT` für belegabhängige Pflege von Manifest, Changelog, TODO, README, Anleitung und Doku angelegt.

## 17 verbleibende nächste Schritte

1. 🔴 fachlichen Hauptzweck und echte Arbeitsabläufe festlegen.
2. 🔴 separate Prozesswache für harte Programmabbrüche ergänzen.
3. 🔴 Diagnosepaket mit bewusster Datenschutzfreigabe exportieren.
4. 🔴 Filter nach Schweregrad und Bereich im Debug/Log ergänzen.
5. 🔴 Protokollrotation mit fester Größen- und Altersgrenze umsetzen.
6. 🔴 Ereignisdetails direkt aus der Dashboard-Zeile öffnen.
7. 🔴 Wiederholungszähler und ersten Zeitpunkt anzeigen.
8. 🔴 sensible Werte vor dem Protokollieren automatisch ausblenden.
9. 🔴 beschädigte Protokolle getrennt sichern und verständlich melden.
10. 🔴 Schreibfehler bei vollem Datenträger gezielt simulieren und testen.
11. 🔴 Tastaturbedienung und sichtbaren Fokus vollständig prüfen.
12. 🟡 hohe Kontraste und größere Standards sind vorhanden; Nutzer-Zoom und Schriftgrößenumschaltung fehlen noch.
13. 🔴 Wiederherstellungsprüfung des vollständigen Iterations-ZIP automatisieren.
14. 🔴 Startprüfung ohne sichtbare Oberfläche ergänzen.
15. 🔴 kontrolliertes Beenden als Ereignis erfassen.
16. 🔴 technische Details in der Oberfläche standardmäßig einklappen.
17. 🔴 reale Kubuntu-Endprüfung dokumentieren.
