from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: erwartet 1 Fundstelle, gefunden {count}")
    return text.replace(old, new, 1)


# MANIFEST: finalen, bereits nachgewiesenen Release-Stand ergänzen.
path = ROOT / "MANIFEST.json"
manifest = json.loads(path.read_text(encoding="utf-8"))
validation = manifest["validation"]
validation.update({
    "iteration34_final_pr_ci_run": 696,
    "iteration34_final_pr_ci_result": "success",
    "iteration34_final_logic_tests": 104,
    "iteration34_final_gui_tests": 74,
    "iteration34_final_release_files": 46,
    "iteration34_final_native_wayland_smoke": True,
    "iteration34_final_restore_gate": True,
    "iteration34_final_restore_status": "OK",
    "iteration34_final_restore_sha256": "7b1e9365f6326359ca7e927b0d639c4af922ff46ebfce16e266316580634f2ff",
    "iteration34_final_tested_head_sha": "9d9b608b55a72311d65d627dbe274ab400a2c79d",
    "iteration34_feature_merged_main_sha": "f3fafe411f48a67e8eff83c07f7caf9e2ea753c7",
    "iteration34_main_ci_run": 697,
    "iteration34_main_ci_result": "success",
    "iteration34_main_logic_tests": 104,
    "iteration34_main_gui_tests": 74,
    "iteration34_main_release_files": 46,
    "iteration34_main_native_wayland_smoke": True,
    "iteration34_main_restore_gate": True,
    "iteration34_main_restore_status": "OK",
    "iteration34_main_restore_sha256": "25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04",
    "iteration34_final_head_gate": "success",
})
validation["targeted_tests"] = (
    "python3 -m unittest tests.test_presentation_policy tests.test_repo_hygiene "
    "tests.test_event_management tests.test_release_builder tests.test_security_watch "
    "tests.test_restore tests.test_diagnostics_logging tests.test_recovery_ui_logic "
    "tests.test_song_logic tests.test_song_library tests.test_song_library_controls "
    "tests.test_profile_store tests.test_todo_store tests.test_calendar_store "
    "tests.test_process_consistency tests.test_iteration34_core tests.test_kubuntu_acceptance "
    "tests.test_wayland_smoke; QT_QPA_PLATFORM=offscreen python3 -m unittest "
    "tests.test_layman_ux_gui tests.test_navigation_ux_gui tests.test_recovery_ui_gui "
    "tests.test_song_gui tests.test_song_library_gui tests.test_song_library_controls_gui "
    "tests.test_dashboard_reference_gui tests.test_zoom_controls_gui tests.test_profile_gui "
    "tests.test_todo_gui tests.test_calendar_gui tests.test_iteration34_gui"
)
managed = manifest["ui"].setdefault("zoom_managed_windows", [])
for name in ("character_fibel", "text_editor"):
    if name not in managed:
        managed.append(name)
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# TODO: Zwischenstatus durch tatsächliche Abschlussnachweise ersetzen.
text = read("TODO.md")
old = """### Technische Abnahme vor Versionssync

- 🟢 bereinigter Feature-Head `8b5525541cff430f9e820a02adf44f469acc43a7` in Grundprüfung **#685** vollständig erfolgreich.
- 🟢 **104 Logik-/Regressionstests** und **74 PySide6-GUI-Tests** erfolgreich.
- 🟢 **46 Release-Betriebsdateien**, Headless-Start und nativer Qt-Wayland-Smoke erfolgreich.
- 🟢 Vollprojekt-Restore `OK`, SHA-256 `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`.
- 🟡 finale v0.17.0-Versions-/Dokumentationssynchronisierung wird anschließend erneut vollständig geprüft.
"""
new = """### Finale technische Abnahme und Release

- 🟢 synchronisierter PR-Head `9d9b608b55a72311d65d627dbe274ab400a2c79d` in Grundprüfung **#696** vollständig erfolgreich.
- 🟢 **104 Logik-/Regressionstests**, **74 PySide6-GUI-Tests** und **46 Release-Betriebsdateien** erfolgreich; Headless-Start und nativer Qt-Wayland-Smoke ebenfalls grün.
- 🟢 PR #45 SHA-geschützt gemergt; Produkt-Main `f3fafe411f48a67e8eff83c07f7caf9e2ea753c7`.
- 🟢 gemergter Main in Grundprüfung **#697** erneut vollständig erfolgreich: 104 Logiktests, 74 GUI-Tests, 46 Release-Dateien, nativer Wayland-Smoke und Restore `OK`.
- 🟢 Main-Restore-SHA-256 `25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04`.
- 🟢 Version **0.17.0** freigegeben; reale sichtbare Kubuntu-/Plasma-Wayland-Abnahme bleibt als separater manueller Schritt bestehen.
"""
text = replace_once(text, old, new, "TODO Evidence")
write("TODO.md", text)


# CHANGELOG: finale statt ausstehende Freigabe dokumentieren.
text = read("CHANGELOG.md")
old = """- bereinigter Feature-Head `8b5525541cff430f9e820a02adf44f469acc43a7` in Grundprüfung **#685** vollständig grün: **104 Logiktests**, **74 GUI-Tests**, **46 Release-Dateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`,
- Restore-SHA-256 `1f1f46f35d5e733385c77e39c45366a812ce6b92f5a0786faaf948dbfddb4d41`,
- finale v0.17.0-Synchronisierung wird vor Merge erneut vollständig geprüft.
"""
new = """- synchronisierter PR-Head `9d9b608b55a72311d65d627dbe274ab400a2c79d` in Grundprüfung **#696** vollständig grün: **104 Logiktests**, **74 GUI-Tests**, **46 Release-Dateien**, Headless-Start, nativer Qt-Wayland-Smoke und Restore `OK`,
- PR #45 SHA-geschützt gemergt; Produkt-Main `f3fafe411f48a67e8eff83c07f7caf9e2ea753c7`,
- gemergter Main in Grundprüfung **#697** erneut vollständig grün; Restore-SHA-256 `25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04`,
- Version **0.17.0** technisch freigegeben; reale sichtbare Kubuntu-/Plasma-Wayland-Abnahme bleibt separat.
"""
text = replace_once(text, old, new, "CHANGELOG Evidence")
write("CHANGELOG.md", text)


# Iterationsbericht: vollständige Abschlusskette abbilden.
text = read("docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md")
start = text.index("## Technische Abnahme vor Versionssync")
replacement = """## Technische Abnahme und Freigabe

### Vor Versionssync

- Feature-Head: `8b5525541cff430f9e820a02adf44f469acc43a7`
- Grundprüfung **#685 – success**
- 104 Logik-/Regressionstests, 74 PySide6-GUI-Tests, 46 Release-Betriebsdateien
- nativer Qt-Wayland-Smoke und Restore `OK`

### Final synchronisierter PR-Head

- Head: `9d9b608b55a72311d65d627dbe274ab400a2c79d`
- Grundprüfung **#696 – success**
- **104/104 Logik-/Regressionstests**
- **74/74 PySide6-GUI-Tests**, einschließlich Zoom-/Layoutregressionen für 100–200 %
- **46 Release-Betriebsdateien**
- Headless-Start: **OK**
- nativer Qt-Wayland-Smoke: **OK** (`QApplication.platformName() = wayland`)
- Vollprojekt-Restore: **OK**
- Restore-SHA-256: `7b1e9365f6326359ca7e927b0d639c4af922ff46ebfce16e266316580634f2ff`

### Merge und Main-Nachprüfung

- PR #45 SHA-geschützt als Squash-Merge freigegeben.
- Produkt-Main: `f3fafe411f48a67e8eff83c07f7caf9e2ea753c7`
- Grundprüfung **#697 – success**
- erneut **104 Logiktests**, **74 GUI-Tests**, **46 Release-Dateien**, Headless-Start und nativer Wayland-Smoke erfolgreich
- Main-Restore: **OK**
- Main-Restore-SHA-256: `25a9ee8d06ae39a48d712ebf5c98c3451fe92b88abb4937705d7c17a18f1ab04`

Die sichtbare reale Kubuntu-26.04-/KDE-Plasma-Wayland-Abnahme bleibt separat erforderlich; Offscreen-/Weston-CI ersetzt keine reale Sichtprüfung.

## Release-Ergebnis

Version **0.17.0** ist technisch freigegeben. Dieser nachgelagerte Evidence-Sync ändert ausschließlich Status-/Nachweisdokumentation und das maschinenlesbare MANIFEST; der bereits zweifach grün geprüfte Laufzeitcode bleibt unverändert.
"""
text = text[:start] + replacement
write("docs/ITERATION34_CORE_MODULES_DATA_STANDARDS.md", text)
