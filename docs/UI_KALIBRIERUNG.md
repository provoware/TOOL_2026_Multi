# UI-Shadow-Nachweise auswerten

`python3 scripts/ui_kalibrierung.py lauf1.json lauf2.json lauf3.json` prüft gespeicherte Original-Evidenz aus CI-Artefakten. Die vorhandene Infrastrukturprüfung wird wiederverwendet. Zusätzlich sind vollständige Release-Matrizen, keine Fehler/Warnungen/Befunde, eine GitHub-Laufnummer, ein vollständiger SHA und eine Abschlusszeit mit Zeitzone erforderlich. Höchstens 100 Nachweise pro Auswertung.

Mindestens drei unterschiedliche saubere CI-Läufe verschiedener Quellstände sind Voraussetzung für einen **Prüfkandidaten**. Doppelt übergebene Artefakte, lokale Proben und die kleine PR-Matrix zählen nicht als drei Kalibrierläufe. Ein ungeklärter oder ungültiger übergebener Nachweis verhindert die Empfehlung; bekannte überholte Fehlerstände nicht still ignorieren, sondern ihre Ablösung dokumentieren.

Das Werkzeug aktiviert keine Regel und ändert keinen CI-Gate. Eine fachliche Kalibrierung und die Entscheidung über einzelne Pflichtregeln bleiben eine getrennte Aufgabe. Es beweist keine Echtheit heruntergeladener JSON-Dateien; Original-Artefakte und zugehörige GitHub-Läufe müssen nachvollziehbar sein. Ohne übergebene Evidenz lautet das Ergebnis ausdrücklich 0 Nachweise und keine Freigabeempfehlung.

Drei automatische Schutztests prüfen fehlende Evidenz, echte Eingabestruktur, Dubletten, Befunde trotz grüner Zusammenfassung sowie unvollständige/lokale/PR-Nachweise. Testfixtures sind synthetisch und werden niemals als echte CI-Kalibrierung ausgegeben.
