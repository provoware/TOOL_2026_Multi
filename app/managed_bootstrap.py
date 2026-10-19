"""Getrennter, fehlerschützender Start vorbereiteter Versions-Slots.

Nur Installationen mit ausdrücklich aktiviertem externen Datenvertrag.
Der normale Schnellstart bleibt für Altinstallationen unverändert.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

from app.atomic_io import atomic_write_json
from app.runtime_roots import runtime_root, VARIABLE
from app import update_slots


def validate_installation(install):
    root = Path(install).resolve(strict=True)
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Der verwaltete Installationsordner fehlt.")
    root, _slots, _pointer, slot_id, slot = update_slots._managed(root)
    persistent = root / "persistent"
    if runtime_root(slot, {VARIABLE: str(persistent)}) != persistent.resolve():
        raise ValueError("Getrennter Datenordner wurde nicht bestätigt.")
    manifest_file = slot / "MANIFEST.json"
    if manifest_file.is_symlink() or not manifest_file.is_file():
        raise ValueError("Manifest des aktiven Programm-Slots fehlt.")
    manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
    if manifest.get("runtime", {}).get("external_data_root") is not True:
        raise ValueError("Die Programmversion unterstützt noch keine sichere Datentrennung.")
    launcher = slot / "schnellstart.sh"
    if launcher.is_symlink() or not launcher.is_file():
        raise ValueError("Der geprüfte Schnellstart fehlt.")
    return root, slot_id, slot, persistent.resolve()


def run_managed(install, *, runner=None):
    if runner is None:
        runner = subprocess.run
    root = Path(install).resolve(strict=True)
    with update_slots._exclusive(root):
        journal = update_slots._journal(root)
        if journal and journal["state"] == "SWITCH_PENDING":
            update_slots._recover_pending_locked(root)
        root, current, slot, persistent = validate_installation(root)
        env = dict(os.environ)
        env[VARIABLE] = str(persistent)
        completed = runner(["bash", str(slot / "schnellstart.sh")],
                           cwd=slot, env=env, check=False)
        code = completed.returncode
        if type(code) is not int:
            raise ValueError("Schnellstart lieferte keinen gültigen Rückgabecode.")
        if code != 0:
            journal = update_slots._journal(root)
            if journal and journal["state"] == "ACTIVE_VERIFIED" and journal["new"] == current:
                # Der alte Slot bleibt unverändert. Keine Daten werden zurückkopiert
                # oder mit einer älteren Datenversion überschrieben.
                update_slots._atomic_pointer(root, journal["old"])
                atomic_write_json(root / update_slots.JOURNAL,
                                  {**journal, "state": "ROLLED_BACK"})
        return code
