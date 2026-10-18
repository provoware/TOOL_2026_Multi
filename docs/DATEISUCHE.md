# Zentrale Datei- und Textsuche

Iteration 49 · lokaler 0.18.3-Prüfkandidat · Basis 230f562.

1. Rein lesenden Suchscope und feste Schutzgrenzen festlegen.
2. Suche mit kleinen Qt-Zeitgeberschritten, Abbruch und Trefferanzeige umsetzen.
3. Grenzen, Nachbarwege, Darstellung und vollständige Sicherung prüfen; zusammen mit bisherigen lokalen Arbeiten ins Repository übertragen.

Im Dashboard die Kachel **Dateisuche** wählen oder **Strg+Umschalt+F** drücken. Das Kopfsuchfeld öffnet ebenfalls die zentrale Suche und übernimmt seinen Suchtext. Die Songbibliothek behält ihre eigene detaillierte Song-Suche. Die Kartenaktionen Dateisuche, Textinhalt suchen und Trefferliste führen zum selben Suchfenster.

Suchtext eingeben, Dateinamen und/oder Textinhalte auswählen, **Suchen** wählen. Groß-/Kleinschreibung spielt keine Rolle, Unicode wie Straße/STRASSE wird berücksichtigt. Gesucht wird nach einer wörtlichen Zeichenfolge, nicht nach regulären Ausdrücken. Bei Namen wird der relative Pfad durchsucht. Texttreffer enthalten die Zeilennummer der gespeicherten Datei, bei JSON also die Zeile der JSON-Darstellung. Namenstreffer haben keine Zeilennummer. Einen Treffer markieren, um den kopierbaren Klartextausschnitt zu sehen. Der Ausschnitt enthält bis zu 500 Zeichen ab Zeilenanfang, nicht immer die vollständige Fundzeile.

**Abbrechen** oder Escape beendet weitere Suchschritte; bisherige Treffer bleiben sichtbar. Beim Schließen wird die Suche beendet und der offene Verzeichnisiterator geschlossen. Wiederöffnen verwendet dasselbe Fenster. Dashboard-Aktualisierung löst keine automatische neue Suche aus.

Scope: gespeicherte reguläre Dateien ausschließlich unter dem Projektordner `daten/`. Kein Zugriff auf beliebige externe Ordner, keine automatische Dateiöffnung, kein Ausführen von Treffern, kein Schreiben oder Indizieren. Ungespeicherte Texte sind nicht enthalten. Verknüpfungen und Spezialdateien werden nicht gelesen. Versteckte Dateien/Ordner einschließlich `.versionen/` bleiben außerhalb des Suchscopes. Textinhalte werden nur für UTF-8/UTF-8-BOM-Dateien mit Endung txt, md, json oder csv geprüft; ungeeignete Inhalte werden ausgelassen und gemeldet. Namen sonstiger regulärer Dateien bleiben auffindbar.

Grenzen: 200 Treffer, 5000 betrachtete Datei-/Verzeichniseinträge, 1 MiB pro Textdatei, 32 MiB gelesene Textdaten. Bis zu ein zusätzliches Prüfbyte erkennt ein Überschreiten der Bytegrenze. Zeitlimit 10 Sekunden, geprüft zwischen Suchschritten; es ist kein harter Abbruch eines vom Betriebssystem blockierten Dateizugriffs. Jeder Qt-Schritt bearbeitet höchstens eine Datei oder ein Verzeichnis, damit Abbrechen zwischen den Schritten möglich bleibt. Ein einzelner langsamer Dateizugriff kann die Oberfläche vorübergehend verzögern. Es wird kein Hintergrundthread benötigt, der beim Schließen zurückbleiben könnte.

Treffer sind eine Momentaufnahme. Externe Änderungen während des Suchens können zu ausgelassenen oder unterschiedlichen Inhalten führen; erneut Suchen aktualisiert sie. Keine Behauptung eines transaktionalen Gesamt-Snapshots. Suchtexte, Treffer und Vorschau bleiben im Speicher; kein Log, Export oder Upload erfolgt automatisch.

Prüfung: Backend-Schutztests für Unicode, wörtliche Suche, getrennte Suchmodi, unveränderte Dateibytes, Links/Spezialdateien/versteckte Versionen, fremden Datenlink, Treffer-/Zeit-/Eintrags-/Bytegrenzen, große/binäre/ungültige Dateien und fehlende Daten. GUI-Tests prüfen Abbruch/Schließen/Wiederöffnen, Plain-Text-Vorschau, Fehlerhinweise, Dashboard-/Registry-Anbindung sowie getrennte Bedienelemente bei 100/150/200 %.

Ein erster zusätzlicher Sidebar-Eintrag erzeugte in der Release-Matrix 32 Überlappungen. Er wurde entfernt; dieselbe Funktion ist ohne zusätzliche Sidebar-Zeile über Kopf, Kachel und Tastatur zugänglich. Zwei historische UI-Erwartungen zur geplanten Dateisuche wurden an die tatsächlich nutzbare Funktion angepasst. Keine Geometriegrenze gelockert. Finale Zahlen und GitHub-Head werden am Pull Request belegt.

Fortschritt: Implementierung, gezielte Prüfung und Dokumentation; technische Vollprüfung/Übertragung gehören zum Abschluss. Manuelle Kubuntu-Abnahme bleibt zurückgestellt. Nachrangige Folgevorhaben: **priorisiert** sichere Update-Prüfung im isolierten Staging; danach Ideenarchiv, Account-Schutzkonzept, Dashboard-Kaltstartmessung und Abgleich vergleichbarer Entwicklungsiterationen. Keine dieser Funktionen wird mit dieser Suche als fertig markiert.
