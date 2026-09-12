#!/usr/bin/env python3
"""Einmaliger, deterministischer Metadaten-Sync für Iteration 35; löscht sich nach Ausführung selbst."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content, encoding="utf-8")


# MANIFEST
manifest_path = ROOT / "MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["schema_version"] = 28
manifest["tool"]["version"] = "0.17.1"
manifest["tool"]["date"] = "2026-09-12"
manifest["iteration"] = {
    "number": 35,
    "goal": "Charakterzugriff in Schreibmodulen standardisieren und geprüfte Vollprojekt-ZIPs direkt aus CI bereitstellen",
    "completed": 4,
    "open_next": 1,
}
targeted = manifest["validation"]["targeted_tests"]
if "tests.test_iteration35_writing_context" not in targeted:
    targeted = targeted.replace(
        "tests.test_iteration34_core tests.test_kubuntu_acceptance",
        "tests.test_iteration34_core tests.test_iteration35_writing_context tests.test_kubuntu_acceptance",
    )
if "tests.test_iteration35_writing_context_gui" not in targeted:
    targeted = targeted.replace(
        "tests.test_iteration34_gui",
        "tests.test_iteration34_gui tests.test_iteration35_writing_context_gui",
    )
manifest["validation"]["targeted_tests"] = targeted
manifest["validation"].update({
    "iteration35_initial_ci_run": 716,
    "iteration35_initial_ci_result": "failure",
    "iteration35_initial_ci_cause": "Charaktermarker in eckigen Klammern kollidierte mit der Songbereichssyntax und wurde beim erneuten Laden als Bereich statt als Text interpretiert",
    "iteration35_technical_ci_run": 722,
    "iteration35_technical_ci_result": "success",
    "iteration35_technical_logic_tests": 106,
    "iteration35_technical_gui_tests": 76,
    "iteration35_technical_release_files": 46,
    "iteration35_technical_native_wayland_smoke": True,
    "iteration35_technical_restore_gate": True,
    "iteration35_technical_restore_status": "OK",
    "iteration35_technical_restore_sha256": "2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a",
    "iteration35_technical_tested_head_sha": "907e65df46ba31d2d5e7df03d137baf1448742b8",
    "iteration35_ci_full_project_artifact": True,
    "iteration35_release_version": "0.17.1",
})
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# README
readme = text("README.md")
readme = readme.replace(
    "> **Version:** 0.17.0 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit Charakterfibel und Texteditor; automatische Voll-/Restore- und native Wayland-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen",
    "> **Version:** 0.17.1 · **Stand:** 12.09.2026 · **Status:** ausführbarer Kern mit standardisiertem Charakterzugriff in Text- und Songeditor; automatische Voll-/Restore-, native Wayland- und ZIP-Artefakt-Prüfung aktiv, reale Kubuntu-26.04-/Plasma-Wayland-Sichtabnahme noch offen",
)
new_section = """## Neu in 0.17.1 – Charakterzugriff in Schreibmodulen

- **Einheitliche Charakterauswahl:** Texteditor und Songtexteditor beziehen Figuren über dieselbe zentrale, stabile Charakter-ID-Logik.
- **Songtexteditor:** Figuren aus der Charakterfibel können direkt an der aktuellen Schreibposition eingefügt werden.
- **Sicherer Referenzmarker:** `«Charakter: Name (Rolle)»` kollidiert nicht mit Songbereichen wie `[Strophe]` oder `[Refrain]`.
- **Regressionsschutz:** ein erster Prüflauf deckte genau diese Kollision auf; nach der Korrektur sind 106 Logiktests und 76 GUI-Tests grün.
- **Vollständiges Projekt-ZIP:** ein erfolgreicher CI-Lauf erzeugt nach Vollprüfung, nativem Wayland-Smoke und Restore zusätzlich ein vollständiges Git-Projekt-ZIP samt SHA-256.

"""
if new_section not in readme:
    readme = readme.replace("## Neu in 0.17.0 – Charaktere, Texteditor und gemeinsame Standards\n", new_section + "## Neu in 0.17.0 – Charaktere, Texteditor und gemeinsame Standards\n")
readme = readme.replace(
    "3. Text schreiben.\n\nÄnderungen werden automatisch gespeichert.",
    "3. Text schreiben.\n\nOptional kann direkt darunter ein Charakter aus der **Charakterfibel** gewählt und mit **In Songbereich einfügen** an der aktuellen Schreibposition eingesetzt werden. Die sichtbare Referenz hat die Form `«Charakter: Name (Rolle)»`.\n\nÄnderungen werden automatisch gespeichert.",
)
readme = readme.replace(
    "- `docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md` – Charakterfibel, Texteditor, gemeinsame Daten-/UI-Standards und Abnahme",
    "- `docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md` – Charakterfibel, Texteditor, gemeinsame Daten-/UI-Standards und Abnahme\n- `docs/ITERATION35_WRITING_CONTEXT.md` – standardisierter Charakterzugriff, Songeditor-Integration und ZIP-Artefakt-Gate",
)
write("README.md", readme)

# Laienanleitung
anleitung = text("ANLEITUNG_LAIEN.md")
old = "Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro. Du kannst zusätzlich einen eigenen Namen eintippen, zum Beispiel **Pre-Drop** oder **Gesprochenes Outro**. Ungültige/leere Namen werden nicht übernommen.\n\nRechts steht die **Gesamtvorschau**."
new = """Mögliche Bereiche sind zum Beispiel Strophe, Refrain, Intro, Bridge oder Outro. Du kannst zusätzlich einen eigenen Namen eintippen, zum Beispiel **Pre-Drop** oder **Gesprochenes Outro**. Ungültige/leere Namen werden nicht übernommen.

### Charakter aus der Charakterfibel einsetzen

1. Oben bei **Charakterfibel** eine Figur auswählen.
2. **In Songbereich einfügen** anklicken.
3. Provoware setzt die Referenz an die aktuelle Schreibposition und speichert den Song anschließend.

Die Referenz sieht zum Beispiel so aus: `«Charakter: Nora (Erzählerin)»`. Die besonderen Klammern sind absichtlich gewählt, damit die Referenz nicht mit Songbereichen wie `[Strophe]` verwechselt wird.

Rechts steht die **Gesamtvorschau**."""
if old in anleitung:
    anleitung = anleitung.replace(old, new)
write("ANLEITUNG_LAIEN.md", anleitung)

# TODO
TODO_SECTION = """## Iteration 35 – Standardisierter Charakterzugriff in Schreibmodulen

**Hauptziel:** Den letzten offenen Charakterfibel-Punkt aus 0.17.0 klein und rückfallarm abschließen, ohne Song- oder Textdatenformat zu migrieren.

- 🟢 zentrale, UI-unabhängige Charakterauswahl mit stabilen IDs und einheitlicher Beschriftung eingeführt.
- 🟢 allgemeiner Texteditor auf dieselbe Referenzlogik umgestellt.
- 🟢 Songtexteditor kann Charaktere aus der Fibel direkt an der aktuellen Schreibposition einsetzen.
- 🟢 Referenzmarker auf `«Charakter: Name (Rolle)»` festgelegt; dadurch keine Kollision mit `[Strophe]`, `[Refrain]` oder eigenen Songbereichen.
- 🟢 erster Prüflauf #716 hat die ursprüngliche Kollision mit eckigen Klammern korrekt blockiert.
- 🟢 korrigierter technischer Head `907e65df46ba31d2d5e7df03d137baf1448742b8` in Grundprüfung #722 vollständig grün: 106 Logiktests, 76 GUI-Tests, 46 Release-Dateien, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`.
- 🟢 Restore-SHA-256: `2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a`.
- 🟢 CI stellt nach erfolgreichem Restore zusätzlich Runtime- und vollständiges Projekt-ZIP samt SHA-256 als Artefakt bereit.
- 🟡 reale sichtbare Kubuntu-26.04-/Plasma-Wayland-Abnahme bleibt weiterhin ein separater Zielrechner-Schritt.

"""
todo = text("TODO.md").replace("- [ ] Zugriff aus weiteren Schreibmodulen standardisieren", "- [x] Zugriff aus weiteren Schreibmodulen standardisieren")
if TODO_SECTION not in todo:
    todo = todo.replace("## Detaillierter Modul-Backlog zum Abhaken\n", TODO_SECTION + "## Detaillierter Modul-Backlog zum Abhaken\n")
write("TODO.md", todo)

# Changelog
CHANGELOG_ENTRY = """## 0.17.1 – 2026-09-12 – Charakterzugriff in Schreibmodulen und vollständige CI-ZIPs

### Neu
- zentrale UI-unabhängige Charakterauswahl für Schreibmodule mit stabiler ID, einheitlicher Beschriftung und wiederverwendbarer Referenz,
- direkter Charakterfibel-Zugriff im Songtexteditor; ausgewählte Figuren werden an der aktuellen Schreibposition eingesetzt,
- erfolgreicher CI-Lauf erzeugt nach Grundprüfung, nativem Qt-Wayland-Smoke und Restore zusätzlich ein vollständiges Projekt-ZIP sowie SHA-256 und lädt die geprüften Pakete als Artefakt hoch.

### Fehlerbehebung / Schutz
- der erste Iteration-35-Prüflauf **#716** blockierte korrekt: der zunächst verwendete Marker `[Charakter: …]` kollidierte mit der vorhandenen Songbereichssyntax `[Strophe]`, `[Refrain]` usw.,
- der gemeinsame Marker wurde deshalb auf die klar lesbare und songformat-sichere Form `«Charakter: Name (Rolle)»` geändert,
- Song- und Textdatenformate bleiben unverändert; keine Migration und keine neue Laufzeitabhängigkeit,
- keine bestehenden Nutzerdaten gelöscht, konvertiert oder überschrieben.

### Technische Abnahme
- korrigierter Head `907e65df46ba31d2d5e7df03d137baf1448742b8` in Grundprüfung **#722** vollständig grün,
- **106 Logik-/Regressionstests**, **76 PySide6-GUI-Tests**, **46 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich,
- Vollprojekt-Restore `OK`, SHA-256 `2b1dc4413771643c7a83a9e7b991ed56062afd6da259150d64c5d77ea62bca3a`,
- CI-Artefakt mit Runtime-Release-ZIP und vollständigem Projekt-ZIP samt Prüfsummen erfolgreich erzeugt.

"""
changelog = text("CHANGELOG.md")
if CHANGELOG_ENTRY not in changelog:
    changelog = changelog.replace("# Änderungsverlauf\n\n", "# Änderungsverlauf\n\n" + CHANGELOG_ENTRY)
write("CHANGELOG.md", changelog)

# Iterationsdoku
doc = """# Iteration 35 – Standardisierter Charakterzugriff in Schreibmodulen

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
"""
write("docs/ITERATION35_WRITING_CONTEXT.md", doc)

# Vollprüfung kennt die neue Doku.
pruefen = text("scripts/pruefen.sh")
pruefen = pruefen.replace(
    "docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md)",
    "docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md docs/ITERATION35_WRITING_CONTEXT.md)",
)
write("scripts/pruefen.sh", pruefen)

# Das Hilfsskript darf im finalen Projekt nicht liegen bleiben.
Path(__file__).unlink()
