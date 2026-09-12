#!/usr/bin/env python3
"""Einmaliger deterministischer Manifest-Sync für Iteration 36.

Das Hilfsskript entfernt sich zusammen mit dem temporären Workflow nach erfolgreicher
Anwendung selbst, damit im finalen Projekt keine Einmal-Mechanik zurückbleibt.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"
WORKFLOW = ROOT / ".github" / "workflows" / "finalize-iteration36-manifest.yml"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
manifest["schema_version"] = 29
manifest["iteration"] = {
    "number": 36,
    "goal": "Kubuntu-Abnahmestart und Restore-Dateirechte für Klick-&-Start zuverlässig absichern",
    "completed": 6,
    "open_next": 1,
}
validation = manifest.setdefault("validation", {})
validation.update({
    "iteration36_initial_ci_run": 736,
    "iteration36_initial_ci_result": "failure",
    "iteration36_initial_ci_cause": "Restore verlor Unix-Ausführungsrechte; wiederhergestellte Starter waren 0644",
    "iteration36_corrected_ci_run": 740,
    "iteration36_corrected_ci_result": "success",
    "iteration36_main_merge_sha": "9a5d60cfe2322619ac526854dde29a943c439661",
    "iteration36_main_ci_run": 745,
    "iteration36_main_ci_result": "success",
    "iteration36_main_logic_tests": 111,
    "iteration36_main_gui_tests": 76,
    "iteration36_main_release_files": 46,
    "iteration36_main_native_wayland_smoke": True,
    "iteration36_main_restore_gate": True,
    "iteration36_main_restore_status": "OK",
    "iteration36_main_restore_sha256": "3b1145b912aca1f6fbced4070688ee28177416a8aadce68a0ec82ac7182dc5ef",
    "iteration36_main_runtime_release_sha256": "ec408ed8ba64a05d9a8ba0e2a6d7b1659d2b1dcebc3f6c4f8dce32c4c848c950",
    "iteration36_launcher_modes": "schnellstart.sh=0755;kubuntu_abnahme.sh=0755",
    "iteration36_permissions_restored": True,
    "iteration36_symlink_restore_rejected": True,
})
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Einmal-Helfer vollständig aus dem finalen Branch entfernen.
Path(__file__).unlink()
WORKFLOW.unlink(missing_ok=True)
