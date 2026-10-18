# Barrierefreiheit: verbindliche Prüfmatrix

**Stand:** 18.10.2026 · **Umfang:** Automatisierte Vorprüfung, keine neue Sichtabnahme.

Die Matrix steht in `app/accessibility_contracts.py` und umfasst folgende acht Kernfenster: Dashboard, Songeditor, Texteditor, Songbibliothek, Kalender, Todo, Charakterfibel und Profileditor.

Jeder Bereich wird gegen sieben Dimensionen geführt: **Tastatur**, **Fokus**, **Beschriftungen**, **Kontrast**, **Zoom**, **Screenreader-Praxistest** sowie **Speichern/Abbrechen/Wiederherstellung**.

## Grenzen der Aussage

Die Matrix sagt aus, **welche Anforderungen geprüft werden sollen**. Sie bedeutet nicht, dass sämtliche Anforderungen schon bestanden wurden. Neue automatische Tests verifizieren beispielhaft konkrete kontrastbezogene Grenzwerte, benannte Dashboard-Schaltflächen mit Tastaturfokus und das sichere Abbrechen ungespeicherter Textänderungen.

Die bereits vorhandene grafische 60-Fälle-Matrix prüft weitere Zoom-/Layoutkonstellationen. Ob ein realer Bildschirmleser sinnvolle Ansagen liefert, eine Tabulatorreihenfolge intuitiv ist und alle Dialoge motorisch uneingeschränkt bedienbar sind, muss getrennt praktisch überprüft werden. **Ein grüner GitHub-Lauf ist keine vollständige Barrierefreiheits-Zertifizierung.**

## Verbindlicher Qualitätsstandard

Für neue oder geänderte Bedienelemente gelten verständlicher sichtbarer Text beziehungsweise technischer Accessible Name, Tastaturfokus, nachvollziehbare Fehlermeldungen, Erhalt ungespeicherter Daten bei Abbruch sowie passende automatische Rückfalltests. Der Kontrast soll für gewöhnliche Schrift mindestens **4,5:1** und für große Schrift mindestens **3:1** erreichen. Die Zielwerte sind Prüfkriterien, kein unbelegter Nachweis sämtlicher heutiger Farben.

**Keine automatische Änderung der Oberfläche:** Auffälligkeiten werden zunächst als Befund dokumentiert. Sichtbare Änderungen erfordern eine gesonderte Entscheidung und gegebenenfalls neue Nutzerabnahme.

## Vorhandene Datensicherheitsprüfungen

Die vorhandenen Tests für Textwechsel, Schließen mit ungespeicherten Daten, Song-Speicherung und Projekt-Wiederherstellung bleiben verbindlich. Die neue Prüfung kontrolliert zusätzlich das Abbrechen beim Anlegen eines neuen Dokuments.


## Ausbaustufe: reale Fenster und Theme-Paare

`tests/test_accessibility_eight_windows_gui.py` instanziiert die acht tatsächlichen Modulfenster mit vorübergehenden lokalen Projektordnern. Für bedienbare Schaltflächen prüft der Test, dass sie einen technischen oder sichtbaren Namen haben, Tastaturfokus zulassen und die Qt-Fokusfolge einen geschlossenen Zyklus bildet. Eine zyklische Fokusfolge allein beweist **keine sinnvolle Reihenfolge für Menschen**; diese muss in einem späteren Praxistest beurteilt werden.

Kontrast wird für alle vier Themes bei sämtlichen fünf freigegebenen Zoomstufen für ausgewählte, tatsächlich konfigurierte Farbpaarungen berechnet, zum Beispiel normale Schrift auf Hintergrund, Fläche und Eingabefeld sowie Platzhaltertext auf Eingabefeld. Das ist keine pixelgenaue Untersuchung aller Dialoge oder Zustände.

### Datensicherheitsregeln

Bestehende Tests für **Speichern, Abbrechen, Dokumentwechsel, Schließen und Wiederherstellung** dürfen nicht entfernt oder abgeschwächt werden. Neue Oberflächentests verwenden temporäre Projektverzeichnisse und dürfen keine echten Benutzerdateien verändern. Datenverluste werden als harte Fehler behandelt.

**Bekannter Befund:** Qt-interne Kalender-Navigationsknöpfe (z. B. `qt_calendar_prevmonth`) haben im automatisierten Test keine auslesbare Schaltflächenbeschriftung. Die neuen Tests prüfen deren Tastaturfokus weiter, schließen sie aber von der *anwendungseigenen* Beschriftungspflicht aus. Ihre tatsächliche Bildschirmleseransage ist weiterhin **offen**, nicht bestanden.


## Nächste Rückfallprüfungen: Kalender, Tastatur und Schreibfehler

Die Monatswechsel-Schaltflächen des Qt-Kalenders bekommen nun reine Zugänglichkeitsnamen. Das verändert keine sichtbare Oberfläche. Der technische Test liest diese Namen direkt aus den tatsächlichen Kalenderknöpfen aus.

Ein zusätzlicher Qt-Test simuliert die **Tabulatortaste** im allgemeinen Texteditor und kontrolliert den Wechsel des aktiven Eingabefeldes. Das bestätigt eine konkrete Tastaturaktion, nicht die Benutzerfreundlichkeit der vollständigen Reihenfolge in jedem Fenster.

Die Datensicherheit wird mit absichtlich ausgelösten Schreibfehlern beim Dokumentwechsel und Schließen geprüft. Dabei müssen offener Editor und noch nicht gespeicherter Text erhalten bleiben und eine Fehlermeldung erscheinen.

Eine echte Bildschirmleserprüfung und die subjektive Reihenfolge der Tastaturbedienung bleiben weiterhin Aufgaben für eine spätere Praxisabnahme.
