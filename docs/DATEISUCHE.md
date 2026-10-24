# Zentrale Datei- und Textsuche

**Aktualisierung 24.10.2026:** Lokale Dateisystemsuche mit wählbarem Suchordner; Implementierungskandidat auf Basis `66ba0aef274930578f9232a24b5ea44c4f3543ed`. Historische Iteration 49 wurde unten fachlich korrigiert.

1. Rein lesenden Suchscope und feste Schutzgrenzen festlegen.
2. Suche mit kleinen Qt-Zeitgeberschritten, Abbruch und Trefferanzeige umsetzen.
3. Grenzen, Nachbarwege, Darstellung und vollständige Sicherung prüfen; zusammen mit bisherigen lokalen Arbeiten ins Repository übertragen.

Im Dashboard die Kachel **Dateisuche** wählen oder **Strg+Umschalt+F** drücken. Das Kopfsuchfeld öffnet ebenfalls die zentrale Suche und übernimmt seinen Suchtext. Die Songbibliothek behält ihre eigene detaillierte Song-Suche. Die Kartenaktionen Dateisuche, Textinhalt suchen und Trefferliste führen zum selben Suchfenster.

Unter **Suchordner** einen absoluten lokalen Pfad eingeben oder **Ordner auswählen …** verwenden. Als Ausgangspunkt steht der Datenordner des Programms im Feld; beliebige andere zugängliche lokale Ordner können gewählt werden. Danach Suchtext eingeben, Dateinamen und/oder Textinhalte auswählen und **Suchen** wählen. Groß-/Kleinschreibung spielt keine Rolle, Unicode wie Straße/STRASSE wird berücksichtigt. Gesucht wird nach einer wörtlichen Zeichenfolge, nicht nach regulären Ausdrücken. Bei Namen wird der relative Pfad durchsucht. Texttreffer enthalten die Zeilennummer der gespeicherten Datei, bei JSON also die Zeile der JSON-Darstellung. Namenstreffer haben keine Zeilennummer. Einen Treffer markieren, um den kopierbaren Klartextausschnitt zu sehen. Der Ausschnitt enthält bis zu 500 Zeichen ab Zeilenanfang, nicht immer die vollständige Fundzeile.

**Abbrechen** oder Escape beendet weitere Suchschritte; bisherige Treffer bleiben sichtbar. Beim Schließen wird die Suche beendet und der offene Verzeichnisiterator geschlossen. Wiederöffnen verwendet dasselbe Fenster. Dashboard-Aktualisierung löst keine automatische neue Suche aus.

Suchbereich: gespeicherte reguläre Dateien unter dem ausdrücklich gewählten lokalen Ordner einschließlich Unterordnern. Der vollständige Suchwurzelpfad bleibt sichtbar und wird im Ergebnis genannt. Keine automatische Dateiöffnung, kein Ausführen von Treffern, kein Schreiben oder Indizieren. Ungespeicherte Texte sind nicht enthalten. PDF, DOCX, ODT und andere Binär-/Containerformate werden nicht in Text umgewandelt; ihre Dateinamen bleiben suchbar. Verknüpfungen und Spezialdateien werden nicht gelesen. Versteckte Dateien/Ordner einschließlich `.versionen/` bleiben außerhalb des Suchscopes. Textinhalte werden nur für UTF-8/UTF-8-BOM-Dateien mit Endung txt, md, json, csv, log, ini, cfg, yaml, yml, toml, xml, html, css, js, ts, py, sh, rst oder tex geprüft; ungeeignete Inhalte werden ausgelassen und gemeldet. Namen sonstiger regulärer Dateien bleiben auffindbar.


## Zugriff und Bestätigung

Vor der ersten Suche außerhalb des Standarddatenordners fragt Provoware ausdrücklich nach Zustimmung für den angezeigten Ordner einschließlich seiner Unterordner. **Nein** beginnt keine neue Suche und erhält vorhandene Treffer. Die Freigabe gilt nur im aktuellen Suchfenster für den unveränderten Pfad. Eine Pfadänderung verwirft sie; während einer laufenden Suche ist die Pfadauswahl gesperrt. Die Ordnerauswahl allein startet keine Suche.

Diese Bestätigung erlaubt den lesenden Suchumfang innerhalb von Provoware. Sie vergibt keine Linux-Dateirechte und entsperrt keine geschützten Ordner. Die native Betriebssystem-Ordnerauswahl kann in unterstützten Umgebungen einen systemseitigen Freigabedialog anbieten; dessen tatsächliches Verhalten ist auf dem Zielsystem zu prüfen. Fehlen klassische Leserechte, müssen sie über das Betriebssystem von einer berechtigten Person freigegeben werden. Danach den Suchpfad erneut auswählen und **Suchen** bestätigen. Keine automatische Rechteänderung, kein `sudo`/`pkexec`, keine Administratorsuche.

Nicht lesbare Dateien oder Unterordner werden gezählt; bis zu zehn betroffene Pfade werden im Freigabehinweis genannt. Bei Zugriffsproblemen fragt Provoware, ob die Betriebssystem-Ordnerauswahl geöffnet werden soll. Nur nach Zustimmung wird sie geöffnet; eine neue Suche wird dadurch nicht gestartet. Die bisherige Suchfreigabe wird bei Berechtigungsfehlern zurückgesetzt. Ein dadurch unvollständiger Lauf wird ausdrücklich als solcher angezeigt, auch wenn andere Treffer vorliegen. Bei Treffer-, Zeit- oder Größengrenzen bleibt deren Abbruchgrund sichtbar; die Anzahl fehlender Leseberechtigungen wird zusätzlich genannt. Keine Treffer sind kein Nachweis, dass im nicht lesbaren Teil nichts vorhanden ist.

Grenzen: 200 Treffer, 5000 betrachtete Datei-/Verzeichniseinträge, 1 MiB pro Textdatei, 32 MiB gelesene Textdaten. Bis zu ein zusätzliches Prüfbyte erkennt ein Überschreiten der Bytegrenze. Zeitlimit 10 Sekunden, geprüft zwischen Suchschritten; es ist kein harter Abbruch eines vom Betriebssystem blockierten Dateizugriffs. Jeder Qt-Schritt bearbeitet höchstens eine Datei oder ein Verzeichnis, damit Abbrechen zwischen den Schritten möglich bleibt. Ein einzelner langsamer Dateizugriff kann die Oberfläche vorübergehend verzögern. Es wird kein Hintergrundthread benötigt, der beim Schließen zurückbleiben könnte.

Treffer sind eine Momentaufnahme. Externe Änderungen während des Suchens können zu ausgelassenen oder unterschiedlichen Inhalten führen; erneut Suchen aktualisiert sie. Keine Behauptung eines transaktionalen Gesamt-Snapshots. Suchtexte, Treffer und Vorschau bleiben im Speicher; kein Log, Export oder Upload erfolgt automatisch.

Prüfung: Backend-Schutztests für Unicode, wörtliche Suche, getrennte Suchmodi, unveränderte Dateibytes, Links/Spezialdateien/versteckte Versionen, fremden Datenlink, Treffer-/Zeit-/Eintrags-/Bytegrenzen, große/binäre/ungültige Dateien und fehlende Daten. GUI-Tests prüfen Abbruch/Schließen/Wiederöffnen, Plain-Text-Vorschau, Fehlerhinweise, Dashboard-/Registry-Anbindung sowie getrennte Bedienelemente bei 100/150/200 %.

Ein erster zusätzlicher Sidebar-Eintrag erzeugte in der Release-Matrix 32 Überlappungen. Er wurde entfernt; dieselbe Funktion ist ohne zusätzliche Sidebar-Zeile über Kopf, Kachel und Tastatur zugänglich. Zwei historische UI-Erwartungen zur geplanten Dateisuche wurden an die tatsächlich nutzbare Funktion angepasst. Keine Geometriegrenze gelockert. Finale Zahlen und GitHub-Head werden am Pull Request belegt.

Fortschritt: Implementierung, gezielte Prüfung und Dokumentation; technische Vollprüfung/Übertragung gehören zum Abschluss. Manuelle Kubuntu-Abnahme bleibt zurückgestellt. Nachrangige Folgevorhaben: **priorisiert** sichere Update-Prüfung im isolierten Staging; danach Ideenarchiv, Account-Schutzkonzept, Dashboard-Kaltstartmessung und Abgleich vergleichbarer Entwicklungsiterationen. Keine dieser Funktionen wird mit dieser Suche als fertig markiert.

Neue gezielte Prüffälle: externer Suchordner mit Unterordnern, unveränderte Quelldateien, explizite Zustimmung/Ablehnung, erneute Bestätigung nach Pfadwechsel, abgebrochene Ordnerauswahl, ungültiger Pfad sowie verweigerter Datei-/Verzeichniszugriff mit erhaltenen Teiltreffern. Systemseitige Portal-/Authentifizierungsdialoge wurden nicht durch simulierte GUI-Tests als praktisch geprüft ausgegeben.

## Prüfnachweis des Implementierungskandidaten (24.10.2026)

- 32 gezielte Prüfungen aus `test_data_search`, `test_search_gui` und `test_documentation_consistency` erfolgreich; einschließlich Ablehnung ohne Dateizugriff, Plain-Text-Berechtigungsdialog und Auswahl erst nach Zustimmung.
- 22 angrenzende Prüfungen aus `test_recovery_ui_logic`, `test_recovery_ui_gui` und `test_layman_ux_gui` erfolgreich.
- Release-Manifest: 147 freigegebene Betriebsdateien gültig; JSON und `git diff --check` ohne Befund.
- Lokale Vollprüfung nicht erfolgreich: ein Fehler unter 352 Logiktests in `ActualSandboxTests.test_plugin_cannot_read_host_environment`; derselbe Fehler wurde unverändert in der ursprünglichen Arbeitskopie ohne Suchänderung reproduziert. Keine Abschwächung dieses Tests vorgenommen.
- Anschließende lokale GUI-Gesamtprüfung blieb im Lauf stehen und wurde kontrolliert beendet; kein vollständiges lokales PASS. Die endgültige vollständige Prüfung am übertragenen Commit muss GitHub belegen.
- Native Portal-/Authentifizierungsdialoge und reale Kubuntu-Bedienung bleiben praktisch ungeprüft. Die vorhandene einmalige Gesamtabnahme am Projektende wird nicht vorgezogen.
