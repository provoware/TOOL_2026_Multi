# Iteration 35 – Standardisierter Charakterzugriff in Schreibmodulen

## Ziel

Den offenen Punkt „Zugriff aus weiteren Schreibmodulen standardisieren“ abschließen, ohne bestehende Song- oder Textdatenformate zu verändern.

## Umsetzung

- `app/character_store.py` liefert mit `CharacterOption` eine UI-unabhängige gemeinsame Auswahlrepräsentation.
- Texteditor und Songtexteditor verwenden dieselbe stabile Charakter-ID, Beschriftung `Name — Rolle` und dieselbe Referenzfunktion.
- Der Songtexteditor erhält eine sichtbare Charakterfibel-Auswahl und setzt die Referenz an der aktuellen Schreibposition ein.
- Der sichtbare Marker lautet `«Charakter: Name (Rolle)»`.
- Das Songformat selbst bleibt unverändert. Es werden keine Charakter-IDs in das Song-Schema geschrieben und keine vorhandenen Dateien migriert.

## Gefundener Fehler vor Freigabe

Der erste Marker `[Charakter: …]` sah für den vorhandenen Song-Parser wie ein Songbereich aus, weil Songbereiche absichtlich eckige Klammern verwenden. Grundprüfung #716 hat diesen Rückfall im neuen Persistenztest entdeckt und die Freigabe blockiert.

Die Korrektur verwendet Guillemets (`«…»`). Dadurch bleibt der Verweis sichtbar und lesbar, kann aber nicht mehr als `[Strophe]`-ähnliche Struktur interpretiert werden.

## Regressionen

Neue Tests prüfen:

1. sortierte gemeinsame Charakterauswahl und einheitliche Label-/Referenzregeln,
2. stabile IDs und sauberes Verhalten bei nicht mehr vorhandenen Charakteren,
3. identische Auswahl im Text- und Songeditor,
4. Einfügen, Speichern und erneutes Laden des Markers im Songeditor ohne Schemaänderung.

## CI- und Restore-Gate

Technischer Korrektur-Head `907e65df46ba31d2d5e7df03d137baf1448742b8`, Grundprüfung #722:

- 🟢 106 Logik-/Regressionstests
- 🟢 76 GUI-Tests
- 🟢 46 Release-Betriebsdateien
- 🟢 Headless-Start
- 🟢 nativer Qt-Wayland-Smoke
- 🟢 Vollprojekt-Restore `OK`
- 🟢 Restore-SHA-256 `2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a`
- 🟢 Runtime-Release-ZIP und vollständiges Projekt-ZIP samt SHA-256 als CI-Artefakt erzeugt

## Schutzgrenzen

- keine Löschungen vorhandener Nutzerdaten,
- keine Song-Schemaänderung,
- keine TextDocument-Schemaänderung,
- keine neue Laufzeitabhängigkeit,
- bestehende atomare Speicherwege bleiben erhalten.

## Noch offen

Die reale sichtbare Zielsystemabnahme auf Kubuntu 26.04 / KDE Plasma Wayland bleibt bewusst separat. Nach dieser Abnahme soll nur jeweils **eine** neue Produktfunktion priorisiert werden.
