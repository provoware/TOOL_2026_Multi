"""Aktiviert nur eine geprüfte, unabhängige PROGRAMMKOPIE, niemals das Altprogramm.

Der produktive Schnellstart und sämtliche Altbestände bleiben unangetastet.
Ein eigener Starter entsteht erst nach ausdrücklicher Zustimmung und
erfolgreicher Prüfung des separaten Programm-Slots.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import stat
import subprocess
import sys

from app.atomic_io import atomic_write_json
from app.managed_bootstrap import validate_installation
from app.runtime_roots import VARIABLE, runtime_root


def activate_independent_copy(root, *, approved=False, runner=None):
    if approved is not True:
        raise PermissionError("Start der neuen Kopie ist nicht ausdrücklich freigegeben.")
    if runner is None:
        runner = subprocess.run
    install = Path(root).resolve(strict=True)
    if not install.is_dir() or (install / "daten").exists():
        raise ValueError("Keine isolierte neue Programmkopie.")
    pointer = install / "current"
    starter = install / "verwaltet_starten.sh"
    if pointer.exists() or pointer.is_symlink() or starter.exists() or starter.is_symlink():
        raise ValueError("Programmverweis oder Starter existiert bereits.")
    report_file = install / "migration-report.json"
    if report_file.is_symlink() or not report_file.is_file() or report_file.stat().st_size > 16384:
        raise ValueError("Der Migrationsnachweis fehlt.")
    report = json.loads(report_file.read_text(encoding="utf-8"))
    if (not isinstance(report, dict)
            or report.get("schema_version") != 1
            or report.get("status") != "COPY_VERIFIED_NOT_ACTIVATED"
            or report.get("activation_allowed") is not False
            or report.get("old_installation_changed") is not False):
        raise ValueError("Kopie ist nicht als unveränderte Ausgangsbasis nachgewiesen.")
    slot = install / "slots" / "base"
    if slot.is_symlink() or not slot.is_dir() or (slot / "daten").exists():
        raise ValueError("Der Programm-Slot ist nicht unabhängig von Nutzerdaten.")
    data = install / "persistent"
    if runtime_root(slot, {VARIABLE: str(data)}) != data.resolve():
        raise ValueError("Die unabhängige Nutzerdatenablage ist nicht sicher.")
    if Path(report["data_path"]).resolve(strict=True) != (data / "daten").resolve(strict=True):
        raise ValueError("Der Migrationsbericht verweist auf andere Nutzerdaten.")
    manifest = slot / "MANIFEST.json"
    if manifest.is_symlink() or not manifest.is_file() or manifest.stat().st_size > 300000:
        raise ValueError("Das Programmmanifest ist beschädigt.")
    details = json.loads(manifest.read_text(encoding="utf-8"))
    if details.get("runtime", {}).get("external_data_root") is not True:
        raise ValueError("Diese Programmversion unterstützt den externen Datenstart nicht.")
    bootstrap = slot / "scripts" / "managed_start.py"
    if bootstrap.is_symlink() or not bootstrap.is_file():
        raise ValueError("Der geprüfte verwaltete Programmstart fehlt oder ist verknüpft.")
    env = dict(os.environ)
    env[VARIABLE] = str(data.resolve())
    try:
        result = runner([sys.executable, "-m", "app.main", "--headless-check"],
                        cwd=slot, env=env, timeout=35, check=False,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Die Startvorprüfung der neuen Kopie ist gescheitert.") from exc
    if result.returncode != 0:
        raise ValueError("Die neue Programmkopie besteht die Startvorprüfung nicht.")
    script = (
        "#!/usr/bin/env bash\n"
        "set -Eeuo pipefail\n"
        'INSTALL="$(cd -- "$(dirname -- "$0")" && pwd -P)"\n'
        '[[ -L "$INSTALL/current" ]] || { echo "Programmzeiger fehlt." >&2; exit 1; }\n'
        'exec python3 "$INSTALL/current/scripts/managed_start.py" "$INSTALL"\n'
    )
    created = False
    try:
        os.symlink("slots/base", pointer)
        created = True
        validated = validate_installation(install)
        if validated[2] != slot:
            raise ValueError("Der vorbereitete Programmzeiger ist inkonsistent.")
        with starter.open("x", encoding="utf-8") as stream:
            stream.write(script)
            stream.flush()
            os.fsync(stream.fileno())
        starter.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
        atomic_write_json(report_file, {
            **report,
            "status": "INDEPENDENT_COPY_STARTABLE",
            "activation_allowed": False,
            "old_installation_changed": False,
            "separate_start_file": "verwaltet_starten.sh",
        })
        return starter
    except BaseException:
        if starter.exists():
            starter.unlink()
        if created and pointer.is_symlink() and os.readlink(pointer) == "slots/base":
            pointer.unlink()
        raise
