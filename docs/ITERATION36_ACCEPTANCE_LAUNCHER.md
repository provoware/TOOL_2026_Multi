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
- Die Vollprüfung führt diese Regression künftig automatisch mit aus.

## Sicherheitsgrenzen

- keine Nutzerdaten werden verändert,
- keine Systemkonfiguration wird geändert,
- keine Installation außerhalb der bereits bestehenden virtuellen Projektumgebung,
- keine Änderung am fachlichen Datenformat,
- die reale Sichtbestätigung bleibt bewusst eine Nutzeraktion am Zielrechner.

## Abnahmeziel

Erst wenn die CI inklusive Restore und ZIP-Erzeugung grün ist und das neue Vollprojekt-ZIP `kubuntu_abnahme.sh` als ausführbar enthält, gilt diese Härtung als abgeschlossen.
