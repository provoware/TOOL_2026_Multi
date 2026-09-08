# Iteration 12 – Reale Kubuntu/X11-Endabnahme

## Hauptziel
Die reale Endabnahme unter Kubuntu/KDE X11 so weit wie möglich automatisieren, ohne Nutzerdaten zu gefährden und ohne eine Offscreen-CI fälschlich als reale Desktop-Abnahme auszugeben.

## Umsetzung
- neuer Klickstart `kubuntu_abnahme.sh`,
- neuer PySide6-Abnahmeassistent `scripts/kubuntu_abnahme.py`,
- Vorprüfung auf Linux, echte X11-Sitzung und KDE/Plasma,
- echter SIGTERM-/Prozesswächtertest in einem temporären Verzeichnis,
- sichtbare Bestätigung für Referenzlayout, Tastaturfokus und Zoom,
- TXT- und JSON-Bericht unter `berichte/`,
- Status `OK` nur, wenn automatische Prüfungen und alle sichtbaren Bestätigungen grün sind.

## Daten- und Fehlerschutz
Der Signaltest benutzt ausschließlich ein temporäres Verzeichnis. Songdateien, Exporte, Versionen und andere Nutzerdaten werden nicht geöffnet, verändert oder kopiert. Ein fehlendes X11-Display wird als Blocker behandelt. Wayland wird nicht still als X11 akzeptiert.

## Bedienung
Unter Kubuntu in einer echten Plasma-X11-Sitzung:

```bash
bash kubuntu_abnahme.sh
```

Der Assistent führt die automatischen Prüfungen aus. Danach kann das Dashboard über eine Schaltfläche geöffnet werden. Die drei sichtbaren Punkte werden erst durch bewusste Bestätigung als bestanden dokumentiert.

## Abnahme dieser Iteration
Automatisierbar und in CI prüfbar:
- Erkennung X11/KDE,
- Blockade von Wayland/fehlendem Display,
- echter SIGTERM-Wächterpfad in Tempdaten,
- Berichtsstatus bleibt ohne Sichtbestätigung unvollständig,
- Grünstatus nur bei vollständiger automatischer und sichtbarer Bestätigung.

Nicht durch CI ersetzbar:
- tatsächliche visuelle Kubuntu/KDE-X11-Darstellung auf dem Zielrechner.

Diese letzte reale Sichtprüfung bleibt absichtlich ein lokaler Schritt und darf nicht aus Offscreen-CI abgeleitet werden.
