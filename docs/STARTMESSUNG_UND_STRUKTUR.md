# Prozessstart messen und Textstruktur anzeigen

Version 0.18.4-Prüfkandidat · Iterationen 53/54.

## Echter Programmeinstieg in neuen Prozessen

Das Startmesswerkzeug liegt nur im vollständigen Projektpaket, nicht im Runtime-ZIP. `python3 scripts/startbenchmark.py --rounds 3` startet den tatsächlichen Einstieg `app.main.main()` je Probe in einem neuen Python-Prozess. Dafür werden ausschließlich eigene temporäre Projektordner mit synthetischen Beständen von einem beziehungsweise 100 Songs erzeugt. Aktive Arbeitsdaten werden nicht als Messdaten gelesen. Der interne Worker akzeptiert nur speziell markierte Messordner innerhalb des eigenen temporären Bereichs. Alle Messordner werden danach entfernt.

Gemessen wird vom Startaufruf im Elternprozess bis zum ersten Ereignisschleifen-Callback nach dem tatsächlichen Dashboard-Show/Refresh. Zusätzlich steht die gesamte Prozesslaufzeit einschließlich kontrolliertem Ende im Bericht. **Dies beweist weder eine vollständig gezeichnete reale Anzeige noch bereits beantwortete Nutzereingaben.** Der erste Start einer synthetischen Installation und weitere Starts derselben Installation heißen `first_launch_in_series` und `repeat_launch`. Jeder davon ist ein neuer Prozess; der Betriebssystem-Dateicache wird nicht kontrolliert oder geleert. Damit wird Prozess-Kaltstart messbar, kein sicherer OS-Kaltstart nach Neustart behauptet.

Vorgabe ist Qt-Offscreen. `--qpa wayland` oder `--qpa xcb` setzt eine passende reale Sitzung voraus. Zwei bis zehn Starts je Größenklasse, höchstens 25 Sekunden je Prozess und zusätzliche 10-Sekunden-Ereignisschleifengrenze. Ausgabe ist JSON auf Standardausgabe; keine automatische Übertragung. `--temp-parent` wählt den Datenträger für den privaten Messbereich.

Lokale Entwicklungsprobe mit zwei Starts je Größenklasse: bis zum Callback etwa 288/292 ms bei einem Song und 287/284 ms bei 100 Songs. Die vier Proben unter Offscreen sind keine belastbare Geschwindigkeitsbewertung, keine Zielrechnerabnahme und kein Vergleich zum Aufwand freiwilliger Diagnostik. Rohwerte liegen außerhalb des Quellbaums. Zwei Tests prüfen echte Unterprozesse, Zustände, Messgrenzen und die Erhaltung fremder Dateien.

## Flüchtige Text-Strukturhilfen

Im allgemeinen Texteditor gibt es **Strukturfarben** und eine Gliederungsauswahl. Markiert werden Überschriften mit `#` bis `######`, eigene Bereiche wie `[Szene]`, Aufgaben wie `- [ ] Aufgabe` sowie dreifache Backtick-Codeblöcke. Überschriften sind zusätzlich fett, Aufgaben unterstrichen und Code in einer Monospace-Schrift dargestellt. Die Farbwahl folgt dem aktiven Theme; die Markierungen lassen sich ausschalten.

Die Gliederung springt zur gewählten Überschrift. Sie wird verzögert nach Eingaben aktualisiert und ist auf die ersten 5000 Zeilen beziehungsweise 200 Überschriften begrenzt; eine begrenzte Liste wird ausdrücklich gekennzeichnet. Überschriften innerhalb eines erkannten Codeblocks werden nicht in die Gliederung übernommen.

Die Syntaxfarben liegen nur in der Darstellung. Gespeicherte Dateien bleiben derselbe Klartext; die Hilfen erzeugen weder Markup noch eine Datenmigration, Autospeicherung oder einen geänderten Textstand. Die erkannten Zeichen bleiben im Text sichtbar; dies ist kein umfangreicher Markdown-Renderer. Tests prüfen Klassifizierung, Codezustände, Kontrast in allen Themes, Gliederungssprung, unveränderte gespeicherte Bytes und unveränderten Änderungsstatus beim Umschalten der Hilfen/Themes.
