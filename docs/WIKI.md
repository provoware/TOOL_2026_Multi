# Lokales Wikimodul – Iteration 58

**Status:** eigener Entwicklungszweig; noch keine Veröffentlichung und keine abgeschlossene praktische Gesamtabnahme.

Das Wiki verwaltet mehrere benannte Wissenssammlungen und bis zu 2000 Artikel im lokalen Bestand `daten/wiki/bestand.json`. Jeder Artikel enthält Titel, Klartext, Schlagworte, geprüfte Verweise auf andere Artikel und bis zu 20 frühere Textfassungen. Der gesamte Bestand wird atomar geschrieben. Fehlerhaftes JSON bleibt zur manuellen Reparatur erhalten, statt still überschrieben zu werden.

**Bedienung:** Menü oben links → „Wiki · Wissenssammlungen“ oder Strg+Alt+W. Sammlung auswählen oder neu anlegen. Links die Artikelliste durchsuchen, rechts Titel, Text, Schlagworte und Verweise bearbeiten. Speichern sichert Änderungen; beim Wechsel oder Schließen erscheint die vorhandene Rückfrage. Eine ältere Fassung lässt sich als *ungespeicherter* Entwurf laden und bewusst erneut speichern.

**Schutz:** Doppelte Artikeltitel innerhalb derselben Sammlung werden abgelehnt. Verknüpfte Seiten dürfen nicht unbemerkt gelöscht werden. JSON-Import prüft zunächst das gesamte Archiv, übernimmt neue Kopien mit neuen Kennungen und remappt interne Links auf die Kopien. Originale bleiben unverändert. Exporte dürfen keine internen Dateien überschreiben. Keine Online-Synchronisation, keine Speicherung von Zugangsdaten, keine ausführbaren Wiki-Markups.

**Grenzen:** Keine grafische Netzwerkansicht, keine Wiki-Syntax-Auswertung, keine Mehrbenutzerverwaltung. Das Modul nutzt die bestehenden Theme-/Zoom-/Import-/Export-Standards. Die technische Prüfung läuft automatisch; eine neue manuelle Kubuntu-Abnahme folgt erst am Ende des gesamten Projektaufbaus.
