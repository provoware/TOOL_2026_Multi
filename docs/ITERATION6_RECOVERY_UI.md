# Iteration 6 – Recovery-Oberfläche

## Ziel
Die vorhandene Debug-/Fehleransicht wird zu einer laienfreundlichen Recovery-Zentrale erweitert, ohne neue fachliche Produktmodule einzuführen.

## Bedienweg
- Filter nach **Schweregrad** und **Bereich**.
- Ereignisdetails per **Doppelklick**, **Enter** oder Schaltfläche.
- Wiederholungszähler und **erstes Auftreten** direkt in den Details.
- technische Angaben sind standardmäßig eingeklappt.
- Anzeigegröße: **100 / 125 / 150 / 175 / 200 %**.
- Tastaturkürzel: `Enter`, `F5`, `Ctrl++`, `Ctrl+-`, `Ctrl+0`, `Escape`.

## Fokus und Barrierearmut
Alle interaktiven Filter, Tabelle und Schaltflächen sind in die Tk-Fokusreihenfolge aufgenommen. Die Vollprüfung führt die Oberfläche unter einer echten Tk-Sitzung aus: bevorzugt über `xvfb-run`, alternativ in einer vorhandenen grafischen Sitzung. Ohne beides gilt die GUI-Prüfung als **nicht bestanden**.

## Schreibfehler-Simulation
`scripts/schreibfehler_simulieren.py` simuliert ausschließlich in einem temporären Testordner:
- `ENOSPC` – kein Speicherplatz mehr,
- `EROFS` – Datenträger nur lesbar.

Es wird kein Datenträger gefüllt und kein echter Nutzdatenpfad verändert. Der Test gilt nur als erfolgreich, wenn der vorhandene Bestand unverändert bleibt und eine teilweise temporäre Datei entfernt wird.

## Abnahme
1. Python-/Shell-/JSON-Syntax.
2. vorhandene Rückfall-, Release-, Sicherheits-, Restore- und Diagnosetests.
3. Recovery-Logiktests.
4. ENOSPC-/EROFS-Simulation.
5. echte Tk-GUI-Prüfung für Tastatur, Fokus, Detailansicht und Zoom.
6. Headless-Start.
7. vollständiges Restore-Gate der Iterationssicherung.

## Nicht Bestandteil
- fachliche Hauptmodule,
- reale Kubuntu-Endabnahme mit echtem Prozesssignal/Crash.
