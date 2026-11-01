# Neue Profilwerte direkt im Dashboard

Stand 01.11.2026 · Ausgangs-main `98933c627708a80b6bf39862b93312f16e39d8b2` · UI-05.06 / PV-UX26-05 im direkten Eingabeumfang.

## Bedienung

1. In der Karte **Vorgaben** das Zielprofil wählen und **Werte ergänzen** öffnen.
2. Den Bereich wählen: Genres, Stimmungen, Stil, Stimme oder Besonderheiten.
3. Mehrere Werte mit Komma eingeben. Ein Begriff mit eigenem Komma steht in Anführungszeichen: `"warm, dunkel", ruhig`.
4. **Prüfen** zeigt neue Werte, bereits vorhandene Werte und Wiederholungen mit Zahl und Wortlaut. Es wird noch nichts gespeichert.
5. **Speichern** übernimmt ausschließlich neue Werte. Die Meldung zählt gespeicherte und übersprungene Werte. Die passende Dashboard-Auswahl und bereits sichtbare Profil-/Generatorfenster werden aktualisiert.

**Zurück zur Auswahl** und Escape erhalten die Eingabe innerhalb der Sitzung. Enter im Eingabefeld prüft; es speichert nicht ungefragt. Tab führt über die Vorschau zu den Aktionen, Leertaste betätigt die fokussierte Schaltfläche. Kategorien und Eingabe besitzen feste Beschriftungen, zusätzliche Hinweise und Namen für Bildschirmleser.

Die Ansicht scrollt nach dem Prüfen zur Vorschau und bei Erfolg oder Fehler zur Rückmeldung. Unerwartete Lese-/Schreibfehler werden über den vorhandenen EventLogger in JSON-Zeilen und TXT-Bericht erfasst; die angezeigte Kennung bleibt beim Weiterbearbeiten als letzter Fehler auffindbar. Eingabefehler werden davon getrennt behandelt und nicht als Speicherdefekt protokolliert. Falls auch das Protokoll nicht geschrieben werden kann, bleibt die ursprüngliche Erklärung erhalten; eine vollständige Aufzeichnung wird dann ausdrücklich nicht behauptet. Eine Änderung an Profil, Bereich oder Eingabe macht die vorherige Vorschau ungültig. Bei einer zwischenzeitlichen Bestandsänderung wird die Vorschau beim Speicherversuch erneuert; danach erneut bewusst **Speichern** wählen. Bei ungültiger Eingabe oder Schreibfehlern bleiben Text und bisheriger Bestand erhalten. Ein nicht zerlegbarer Text wird insgesamt abgewiesen, nicht teilweise gespeichert. Fehlermeldungen erscheinen als Klartext im Formular.

Beim Beenden mit einer begonnenen Eingabe werden die vorhandenen eindeutigen Entscheidungen Speichern/Verwerfen/Weiterarbeiten verwendet. Weiterarbeiten, Escape und Abbrechen schützen den Entwurf. Speichern und schließen gelingt nur mit gültiger Vorschau und erfolgreichem Schreiben; eine ungeprüfte Eingabe führt zurück zum Formular. Ein bewusstes Verwerfen erlaubt das Schließen ohne Schreibvorgang. Die Eingabe ist kein automatisch gespeicherter Entwurf; ein Programmabsturz kann noch nicht gespeicherten Text verlieren.

## Technischer Vertrag und Grenzen

- Wiederverwendbares `ProfileQuickEntry`-Widget in einer scrollbar erreichbaren Dashboard-Ansicht, keine zusätzliche Hauptzeile oder verdeckte Überlagerung. Auch die bisherige Auswahlseite hat bei knappem Platz einen Scrollweg. Schrift und Prüfgrenzen werden nicht verkleinert.
- Einzige Quelle bleibt der bestehende Profil-Store. `preview_values` und `add_values` übernehmen Unicode, Zitate, Dubletten und atomare Speicherung. Der Parser wird nicht im Widget nachgebaut. Alle Altprofile und Altwerte bleiben erhalten; keine Migration oder Katalogbefüllung.
- Der Generator verwendet weiterhin denselben Store und dieselbe Zufallsquelle. Datenänderungen sind nach erfolgreichem Speichern über die gemeinsame Lese-API sofort verfügbar.
- Vor dem Schreiben werden Eingabe und Vorschau erneut abgeglichen. Das ist keine neue prozessübergreifende Sperre: der vorhandene Speichervertrag für mehrere gleichzeitig schreibende Prozesse bleibt unverändert.
- Das Dashboard behält seine bestehende Mindestgröße 1020×650. Diese Iteration behauptet keine allgemeine 800×600-Dashboard-Freigabe; diese Größenanforderung bleibt im bestehenden Bereichs-/Layoutauftrag zu prüfen. Die neue Form selbst bleibt in kleineren Karten scrollbar erreichbar.
- Profile anlegen/umbenennen/löschen, zusätzliche Kategorien, eigene Taxonomie und ein geprüfter 100er-Katalog sind getrennte Aufgaben. Die bestehenden Editorwege bleiben zugänglich.

## Planung, Nachweise und Recovery

1. Wiederverwendbares Formular mit bewusster Vorschau und schreibgeschützter Textanzeige aufbauen.
2. Im Dashboard innerhalb der Vorgaben-Karte einbinden, Auswahl und offene Module aktualisieren, Entwurf beim Zurückgehen/Schließen schützen.
3. Daten-/Fehler-/Tastatur-/Zoom-Regressionen, Oberflächenmatrix, Manifest und die vollständigen PR-/main-Gates prüfen.

Sechzehn neue GUI-Regressionen prüfen echte Aktionen und die bisherigen Store-Funktionen: Vorschau ohne Schreiben, exakte Profil-/Kategoriegrenzen und ein atomarer Schreibvorgang, ungültige Listen, Änderungen am Ziel, veraltete Vorschau, Schreibfehler, Tastatur, Schließschutz, lange Eingabe/Scrollwege, sichtbare Editor-/Generatoraktualisierung, schreibfreie Standardwerte/beschädigter Bestand und bewusstes Verwerfen. Vier zusätzliche Fälle sichern echte Ereignis-/Berichtsdateien bei Lese-/Schreibfehlern, Kennung nach Textänderung, fehlende Protokollschreibrechte und datensparsame Fehlererfassung ohne Eingabeinhalt. Alle Datenproben liegen in temporären Ordnern.

Zusätzlich wurde die geöffnete Form im vollständigen Kreuzprodukt aus drei Größen (1020×650, 1366×768, 1600×900), fünf Zoomstufen (100/125/150/175/200 %) und vier Themes auf erreichbare vollständige Bedienelemente geprüft: 60 Fälle. Der dauerhafte GUI-Rückfalltest deckt dieselben Achsen mit zehn orthogonalen Fällen ab, um die begrenzte Restore-Prüfung nicht mit redundantem Kreuzprodukt zu belasten. Die vollständige bestehende Dashboard-Matrix mit 60 Fällen/180 Fenstern bleibt zusätzlich erhalten; ihr Normalzustand ersetzt keine Prüfung der geöffneten Eingabe.

Der erste Versuch zeigte 20 echte Überlappungen im 200-%-Profil. Scrollbarer Auswahl-Inhalt mit Qt-Mindestgrößen und umbrochene Feldbeschriftungen beseitigen die Ursache. Ein bisheriger Geometrietest vergleicht weiterhin strikt die vertikale Reihenfolge, jetzt in gemeinsamen Dashboard-Koordinaten statt inkompatiblen Elternkoordinaten; keine Prüfgrenze gelockert. Bei 175/200 % konnten zunächst zu breite Feldbeschriftungen nicht vollständig sichtbar werden; Zeilenumbruch behebt das. Die Einstiegsschaltfläche behält ihre natürliche Breite statt überbreit mit dem Inhalt zu wachsen. Die Scroll-Prüfung steuert den gesamten Feldbereich an; bei Qt-Textfeldern ist das vom Ansteuern des Textcursors zu unterscheiden. Endgültige Revision vor Integration vollständig erneut prüfen.

Scope: neues Formular, Dashboard-Anbindung, zentrale Texte, gezielte Regressionen, Manifest und Bedien-/Entwicklerdokumentation. Sicherungspunkt vor Änderungen mit SHA-256 im Arbeitsbericht. Rücknahme als Codepatch möglich, keine Datenmigration. Geprüfter Commit, CI, eigener main-Lauf und ZIP im zugehörigen PR nachweisen; nur dann den direkten Eingabeauftrag technisch abschließen. Reale Kubuntu-Gesamtabnahme und öffentliche Veröffentlichung bleiben zurückgestellt.

Nächste fünf Aufgaben: Profilverwaltung (**priorisierte Empfehlung**, zunächst sichere Umbenennung im bestehenden Datenmodell mit Abhängigkeitsprüfung, Logik-/GUI-Tests und Dokumentation), gemeinsame Datenbank-Suchansicht, Header-/Kachel-Abgleich gemäß Abhängigkeiten, fachlich geprüfte Katalogeinträge, optionaler Katalogtransfer. PV-UX26-05 wird hier nur im bestehenden festen Profil-/Kategorie- und Eingabeumfang bearbeitet; erweiterte Verwaltung und Katalog bleiben getrennt.

Review-Korrektur im selben PR: Der P1-Befund zur fehlenden Fehlerprotokollierung ist durch EventLogger-Injektion aus dem Dashboard, klare Trennung reiner Eingabevalidierung, reale Ereignis-/Berichtstests und einen ehrlichen Notfallpfad bearbeitet. Der verzögerte Scroll-Aufruf ist an den Dashboard-Kontext gebunden und verwendet keine gelöschten Ziele. Eigener vollständiger Prüflauf auf der korrigierten Revision erforderlich.
