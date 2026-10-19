"""Konservativer Prototyp zum isolierten Aufruf fremder Erweiterungen.

Kein Laden in den Hauptprozess, kein HOME-/Daten-Mount, kein Netzwerk.
Ausführung nur nach ausdrücklich erteilter Zustimmung.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

ALLOWED = {"read_input", "write_stdout"}
MAX_CODE = 128 * 1024


def validate_package(folder):
    path = Path(folder).resolve(strict=True)
    if not path.is_dir():
        raise ValueError("Erweiterungsverzeichnis fehlt.")
    spec = path / "plugin.json"
    script = path / "main.py"
    for entry in (spec, script):
        if entry.is_symlink() or not entry.is_file() or not stat.S_ISREG(entry.stat().st_mode):
            raise ValueError("Nur reguläre Paketdateien sind erlaubt.")
    if spec.stat().st_size > 8192 or script.stat().st_size > MAX_CODE:
        raise ValueError("Erweiterung zu groß.")
    info = json.loads(spec.read_text(encoding="utf-8"))
    if not isinstance(info, dict) or set(info) != {"schema_version", "name", "capabilities"}:
        raise ValueError("Unbekanntes Erweiterungsmanifest.")
    if info["schema_version"] != 1 or not isinstance(info["name"], str) or not 1 <= len(info["name"]) <= 80:
        raise ValueError("Ungültige Paketkennung.")
    caps = info["capabilities"]
    if (not isinstance(caps, list) or len(caps) != len(set(caps))
            or any(not isinstance(v, str) or v not in ALLOWED for v in caps)):
        raise ValueError("Unbekannte Berechtigung.")
    for entry in path.iterdir():
        if entry.name not in ("plugin.json", "main.py"):
            raise ValueError("Paket enthält nicht freigegebene Dateien.")
    return info


def run_isolated_package(folder, *, approved=False, input_text="", timeout=8):
    if approved is not True:
        raise PermissionError("Vor der Ausführung ist eine ausdrückliche Zustimmung nötig.")
    info = validate_package(folder)
    if type(input_text) is not str or len(input_text.encode("utf-8")) > 8192:
        raise ValueError("Eingabe zu groß.")
    if input_text and "read_input" not in info["capabilities"]:
        raise PermissionError("Eingaben sind für diese Erweiterung nicht freigegeben.")
    if type(timeout) is not int or not 1 <= timeout <= 20:
        raise ValueError("Zeitgrenze ungültig.")
    sandbox = shutil.which("bwrap")
    if not sandbox or not Path("/usr/bin/python3").is_file():
        raise RuntimeError("Linux-Isolierung fehlt; Erweiterung bleibt gesperrt.")
    package = Path(folder).resolve(strict=True)
    cmd = [sandbox, "--die-with-parent", "--unshare-all",
           "--new-session", "--clearenv", "--setenv", "PATH", "/usr/bin",
           "--setenv", "HOME", "/nonexistent",
           "--tmpfs", "/tmp", "--dir", "/work",
           "--ro-bind", str(package), "/work",
           "--ro-bind", "/usr", "/usr", "--proc", "/proc", "--dev", "/dev"]
    for library in ("/lib", "/lib64", "/bin"):
        if Path(library).exists():
            cmd += ["--ro-bind", library, library]
    cmd += ["--chdir", "/work", "/usr/bin/python3", "-I", "-S", "/work/main.py"]
    try:
        finished = subprocess.run(cmd, input=input_text.encode("utf-8"),
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=timeout, check=False, cwd="/")
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Isolierte Erweiterung hat nicht korrekt beendet.") from exc
    if len(finished.stdout) > 16384 or len(finished.stderr) > 16384:
        raise RuntimeError("Erweiterung überschreitet Ausgabelimits.")
    if finished.returncode:
        raise RuntimeError("Isolierte Erweiterung hat einen Fehler gemeldet.")
    return finished.stdout.decode("utf-8", "replace")
