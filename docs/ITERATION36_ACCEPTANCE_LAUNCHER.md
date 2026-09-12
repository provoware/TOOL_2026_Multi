# Iteration 36 – Kubuntu-Abnahmestart und Release-Rechte absichern

## Ausgangslage

Nach der grünen Main-Abnahme von Version 0.17.1 wurde das erzeugte Vollprojekt-ZIP zusätzlich lokal entpackt und auf Startfähigkeit geprüft.

Dabei wurde ein konkreter Verpackungsfehler sichtbar: `kubuntu_abnahme.sh` war im Repository und damit auch im Release nicht als ausführbar markiert (`0644`). `schnellstart.sh` war dagegen korrekt ausführbar (`0755`).

## Ziel

Die reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme soll ohne unnötigen Terminal-Vorbereitungsschritt startbar sein. Gleichzeitig muss ein automatischer Test verhindern, dass der Ausführungsstatus später unbemerkt wieder verloren geht.

## Umsetzung

- `kubuntu_abnahme.sh` wird im Git-Baum auf Modus `100755` gesetzt.
- Ein neuer Regressionstest prüft die Ausführbarkeit der nutzerseitigen Shell-Starter.
- Der Test prüft zusätzlich, dass ein ZIP-Archiv das Ausführungsbit des Abnahmestarters übernimmt.
- `scripts/iteration_restore.py` stellt beim Entpacken die im ZIP gespeicherten normalen Unix-Dateirechte (`0o777`) wieder her.
- Sonderbits wie SUID/SGID werden nicht übernommen.
- Symbolische Links im Restore-ZIP werden als zusätzliche Sicherheitsgrenze abgewiesen.
- Die Vollprüfung führt die neuen Launcher- und Restore-Regressionen künftig automatisch mit aus.

## Während der Prüfung gefundener zweiter Fehler

Der erste Iteration-36-Lauf **#736** bestand die direkte Vollprüfung und den nativen Wayland-Test, wurde aber korrekt im Restore-Gate gestoppt. Ursache: Python `zipfile.extractall()` stellt Unix-Ausführungsrechte nicht zuverlässig wieder her. Dadurch waren im wiederhergestellten Testprojekt sowohl `schnellstart.sh` als auch `kubuntu_abnahme.sh` wieder nur `0644`.

Der Test wurde bewusst nicht abgeschwächt. Stattdessen wurde die Restore-Logik repariert und um eine gezielte Regression ergänzt: Eine Datei, die mit `0755` gesichert wird, muss nach dem Restore wieder `0755` besitzen.

## Technische Abnahme

Korrigierter Prüfstand in Grundprüfung **#740**:

- 🟢 111 Logik-/Regressionstests,
- 🟢 76 PySide6-GUI-Tests,
- 🟢 46 freigegebene Release-Betriebsdateien,
- 🟢 nativer Qt-Wayland-Start,
- 🟢 Vollprojekt-Restore `OK`,
- 🟢 Restore-SHA-256 `6e26a5a397454e202f895ed77cfdf7fdc0b5aaeebdd35d3b4f1e61a08e1c95db`,
- 🟢 Runtime-Release-ZIP erzeugt; SHA-256 `2453c506986d6b0cfca770cecfc49ce96a26c18bf483c4ed69a4656a3895469a`,
- 🟢 geprüfte ZIP-Pakete als CI-Artefakt hochgeladen.

## Sicherheitsgrenzen

- keine Nutzerdaten werden verändert,
- keine Systemkonfiguration wird geändert,
- keine Installation außerhalb der bereits bestehenden virtuellen Projektumgebung,
- keine Änderung am fachlichen Datenformat,
- keine Übernahme gefährlicher ZIP-Sonderbits,
- die reale Sichtbestätigung bleibt bewusst eine Nutzeraktion am Zielrechner.

## Abnahmeziel

Die technische Härtung gilt als abgeschlossen, wenn nach dem Merge auch der Main-Lauf inklusive Restore und ZIP-Erzeugung grün ist. Danach bleibt als separater Schritt nur noch die reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme am Zielrechner.
