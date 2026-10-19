"""Abgeschirmte Laufzeitprobe für bereits statisch geprüfte Updatepakete.

Führt KEINEN Paketcode direkt auf dem Host aus und aktiviert niemals ein Update.
Ein tatsächlicher Lauf findet nur mit Linux-bubblewrap in getrennten Namensräumen statt.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess

from app.atomic_io import atomic_write_json
from app.update_staging import identity, safe_name, sha256, version

LIMIT_SECONDS = 25
HEX = re.compile(r"[a-f0-9]{64}\Z")
_PROBE = (
    "import sys;"
    "sys.path.insert(0, '/work');"
    "from app.main import headless_check;"
    "raise SystemExit(headless_check())"
)


def _receipt(path):
    if not path.is_file() or path.is_symlink() or path.stat().st_size > 300_000:
        raise ValueError("Staging-Nachweis fehlt oder ist zu groß.")
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise ValueError("Ungültiger Staging-Nachweis.")
    return document


def verify_candidate(active_root, staging_folder):
    """Prüft Quell- und Kandidatenbindung erneut vor dem isolierten Start."""
    active = Path(active_root).resolve(strict=True)
    folder = Path(staging_folder).resolve(strict=True)
    if (not folder.name.startswith("provoware-update-")
            or folder.is_relative_to(active) or active.is_relative_to(folder)):
        raise ValueError("Updateprüfbereich muss getrennt vom aktiven Projekt liegen.")
    report = _receipt(folder / "stage-report.json")
    if (report.get("status") != "STATICALLY_VERIFIED_NOT_ACTIVATABLE"
            or report.get("activation_allowed") is not False
            or report.get("candidate_code_executed") is not False
            or report.get("runtime_tests") != "NOT_RUN"):
        raise ValueError("Die Ausgangsprüfung ist nicht unverändert.")
    hashes = report.get("files")
    if not isinstance(hashes, dict) or not hashes or len(hashes) > 1000:
        raise ValueError("Dateiliste ist ungültig.")
    for key in ("basis_manifest_sha256", "package_sha256"):
        if not isinstance(report.get(key), str) or not HEX.fullmatch(report[key]):
            raise ValueError("Prüfsummenformat ist ungültig.")
    if sha256(active / "MANIFEST.json") != report["basis_manifest_sha256"]:
        raise ValueError("Die aktive Ausgangsversion hat sich verändert.")
    candidate = folder / "candidate"
    if candidate.is_symlink() or not candidate.is_dir():
        raise ValueError("Der Updatekandidat fehlt.")
    found = set()
    for path in candidate.rglob("*"):
        if path.is_symlink() or not path.is_file() and not path.is_dir():
            raise ValueError("Kandidat enthält einen Link oder eine Spezialdatei.")
        if path.is_file():
            found.add(path.relative_to(candidate).as_posix())
    if found != set(hashes):
        raise ValueError("Kandidat enthält zusätzliche oder fehlende Dateien.")
    for name, checksum in hashes.items():
        if (not isinstance(name, str) or safe_name(name).as_posix() != name
                or not isinstance(checksum, str) or not HEX.fullmatch(checksum)):
            raise ValueError("Ungültiger Dateinachweis.")
        if sha256(candidate / name) != checksum:
            raise ValueError("Kandidat wurde nach der statischen Prüfung verändert.")
    manifest = json.loads((candidate / "MANIFEST.json").read_text(encoding="utf-8"))
    current = json.loads((active / "MANIFEST.json").read_text(encoding="utf-8"))
    if (identity(manifest)["version"] != report.get("to_version")
            or identity(current)["version"] != report.get("from_version")
            or version(report["to_version"]) <= version(report["from_version"])):
        raise ValueError("Manifest-Versionen stimmen nicht mit dem Staging überein.")
    return active, folder, candidate, report


def _sandbox_command(binary, candidate):
    # Der Host-Projektordner, das HOME-Verzeichnis und der Netznamensraum
    # werden gerade NICHT eingebunden.
    command = [
        binary, "--unshare-all", "--die-with-parent", "--new-session",
        "--cap-drop", "ALL", "--clearenv",
    ]
    for directory in ("/usr", "/lib", "/lib64"):
        if Path(directory).exists():
            command.extend(("--ro-bind", directory, directory))
    command.extend([
        "--ro-bind", str(candidate), "/work",
        "--tmpfs", "/tmp", "--dev", "/dev", "--proc", "/proc",
        "--chdir", "/work",
        "--setenv", "HOME", "/tmp",
        "--setenv", "PATH", "/usr/bin",
        "--setenv", "PYTHONDONTWRITEBYTECODE", "1",
        "--setenv", "PYTHONNOUSERSITE", "1",
        "--setenv", "QT_QPA_PLATFORM", "offscreen",
        "--", "/usr/bin/python3", "-I", "-c", _PROBE,
    ])
    return command


def run_isolated(active_root, staging_folder):
    """Fail-closed: ohne Bubblewrap keine Ausführung und keine Erfolgsmeldung."""
    active, folder, candidate, report = verify_candidate(active_root, staging_folder)
    result = {
        "schema_version": 1, "status": "NOT_RUN",
        "runtime_tests": "NOT_RUN", "sandbox": "bubblewrap",
        "candidate_code_executed_on_host": False,
        "activation_allowed": False,
        "basis_manifest_sha256": report["basis_manifest_sha256"],
        "candidate_manifest_sha256": report["files"]["MANIFEST.json"],
    }
    binary = shutil.which("bwrap")
    if not binary or not Path("/usr/bin/python3").is_file():
        result["status"] = "ISOLATION_UNAVAILABLE"
    else:
        try:
            finished = subprocess.run(
                _sandbox_command(binary, candidate), cwd="/",
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL, timeout=LIMIT_SECONDS,
                check=False, close_fds=True,
            )
            result["runtime_tests"] = "PASS" if finished.returncode == 0 else "FAIL"
            result["status"] = ("ISOLATED_PROBE_PASSED_NOT_ACTIVATABLE"
                                if finished.returncode == 0 else "ISOLATED_PROBE_FAILED")
            result["exit_code"] = finished.returncode
        except subprocess.TimeoutExpired:
            result["runtime_tests"], result["status"] = "TIMEOUT", "ISOLATED_PROBE_TIMED_OUT"
        except OSError:
            result["status"] = "ISOLATION_START_FAILED"
    # Staging darf nie automatisch in die Anwendung übernommen werden.
    if sha256(active / "MANIFEST.json") != report["basis_manifest_sha256"]:
        raise ValueError("Ausgangsmanifest während der isolierten Probe verändert.")
    atomic_write_json(folder / "sandbox-report.json", result)
    return result
