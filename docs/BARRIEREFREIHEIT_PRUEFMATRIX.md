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
