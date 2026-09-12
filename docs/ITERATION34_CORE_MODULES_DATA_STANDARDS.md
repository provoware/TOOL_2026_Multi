# Iteration 34 – Charakterfibel, Texteditor und gemeinsame Daten-/UI-Standards

## Ziel

Zwei neue produktive Module bereitstellen und gleichzeitig wiederverwendbare Standards für Eingaben, Kontrast, Datenbanklisten, Importhilfe und Startordner etablieren.

## Umgesetzt

1. **Charakterfibel** mit atomarem JSON-Bestand, stabilen IDs, Such-/Bearbeitungsoberfläche und Feldern für konsistente Charaktere.
2. **Texteditor** mit Titel→Dateiname, Haupttext, Abschlussnotizen, Versionierung/Autosave und Charakterreferenzen.
3. **Komma-Normalisierung** für Genres, Stimmungen, Stil, Stimme und Besonderheiten: trimmen, leere Werte verwerfen, case-insensitive Dubletten vermeiden, einzeln speichern.
4. **Eigene Songbereiche** zusätzlich zu Standardbereichen; Namen werden normalisiert und validiert.
5. **JSON-Importhilfe** mit exakter Struktur und kopierbarer Vorlage; zusätzliche Vorlagendatei im Projekt.
6. **Startvalidierung**: fehlende Arbeitsordner nur nach sichtbarer Zustimmung erstellen, danach Schreibbarkeit prüfen.
7. **UI-Standard**: Eingaben/Auswahlfelder erhalten themeweit einen kontrastierenden Hintergrund; bestehende Zoom-/Theme-/Accessibility-Engine wird weiterverwendet.
8. **Todo-Backlog**: neun Modulvorhaben plus 48 separat abhakbare Unteraufgaben idempotent ergänzt.

## Sicherheitsgrenzen

- Bestehende Nutzerdateien werden nicht gelöscht.
- Neue Datenbestände nutzen atomare Schreibwege.
- Backlog-Ergänzung arbeitet mit stabilen IDs und respektiert aktive sowie archivierte Aufgaben.
- Das spätere Updatemodul wird nicht als unkontrollierter Selbstüberschreiber implementiert; vorgesehen ist ZIP-Prüfung → Integrität/Manifest → Checkpoint → Staging → Tests → Aktivierung → Nachprüfung → Rollback.
- Keine neue externe Laufzeitabhängigkeit.

## Technische Abnahme vor Versionssync

- Branch-Head: `8b5525541cff430f9e820a02adf44f469acc43a7`
- GitHub-Grundprüfung: **#685 – success**
- Logik-/Regressionstests: **104**
- PySide6-GUI-Tests: **74**
- Release-Betriebsdateien: **46**
- Headless-Start: **OK**
- nativer Qt-Wayland-Smoke: **OK** (`QApplication.platformName() = wayland`)
- Vollprojekt-Restore: **OK**
- Restore-SHA-256: `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`

Die sichtbare reale Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme bleibt separat erforderlich; Offscreen-/Weston-CI ersetzt keine reale Sichtprüfung.

## Release-Schritt

Die Version wird mit diesem Synchronisationslauf auf **0.17.0** gesetzt. Danach muss der vollständig synchronisierte Head nochmals Vollprüfung, 100–200-%-GUI-Regression, nativen Wayland-Smoke und Restore-Gate bestehen, bevor PR #45 gemergt werden darf.
