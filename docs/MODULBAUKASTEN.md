# Modulbaukasten: verbindlicher Vertrag (Iteration 57)

**Stand:** Entwicklungskandidat, noch kein dynamischer Plugin-Loader.

Das neue Modulregister trennt in Code geprüfte Moduldefinitionen von den persönlich gespeicherten Einstellungen unter `daten/modulbaukasten/katalog.json`. Jedes Modul besitzt feste Kennung, deutsche Bezeichnung, dreiteilige Version, Schnittstellenversion 1 und eine begrenzte Liste benannter Funktionen. Mehrfache Kennungen, fremde Dateipfade, unerlaubte Felder und unbekannte Versionen werden abgewiesen. Das Modulverzeichnis wird atomar geschrieben. Keine Anmeldung und keine Cloud.

**Sehr wichtig:** `set_registered(..., enabled=True)` bedeutet ausschließlich, dass eine bereits bekannte Kennung im Register für spätere Erweiterungen markiert wird. Es werden keine Python-Pakete geladen, keine fremden Plugins ausgeführt und keine vorhandenen Modulbuttons deaktiviert. Diese Sicherheitsgrenze verhindert, dass manipulierter JSON-Inhalt als ausführbarer Code interpretiert wird.

Der Interface-Vertrag `ModuleInterface` fordert später `refresh()` und `set_zoom(percent)` von angebundenen Oberflächen. Die tatsächliche Verbindung zu Navigation, Rechteverwaltung, Modul-Lebenszyklus, separater Testumgebung und dynamischem Laden wird erst in späteren geprüften Iterationen vorgenommen. Vor allem dürfen nicht geprüfte Fremdmodule **niemals** allein durch Eintragung in eine JSON-Datei aktiviert werden.

Schutztests prüfen Versionsgrenzen, Doppelungen, unbekannte IDs, unerlaubte Pfade, Links und Schreibfehler. Automatische CI-Prüfungen bleiben verpflichtend; die komplette sichtbare Kubuntu-Abnahme findet am Projektende statt.
