"""Sichere Programmsicherung für spätere Updates; keine Produktivaktivierung.

Ein Checkpoint enthält ausschließlich explizit freigegebene Betriebsdateien.
Die Wiederherstellung erzeugt immer ein neues, separat geprüftes Verzeichnis.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

from app.atomic_io import atomic_write_json
from app.update_sandbox import verify_candidate
from app.update_staging import safe_name, sha256, identity

MAX_FILES = 1000
MAX_SINGLE = 8 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
SHA = re.compile(r"[0-9a-f]{64}\Z")


def _safe_parent(parent, active=None):
    target = Path(parent).resolve(strict=True)
    if not target.is_dir():
        raise ValueError("Ziel ist kein Verzeichnis.")
    if active is not None and (target.is_relative_to(active) or active.is_relative_to(target)):
        raise ValueError("Sicherung und Projekt müssen getrennte Verzeichnisse sein.")
    return target


def _released(manifest):
    if not isinstance(manifest.get("files"), list):
        raise ValueError("Freigabeverzeichnis im Programmmanifest fehlt.")
    result = []
    for entry in manifest["files"]:
        if not isinstance(entry, dict) or type(entry.get("release")) is not bool:
            raise ValueError("Ungültiger Freigabeeintrag.")
        if entry["release"]:
            path = entry.get("path")
            if not isinstance(path, str):
                raise ValueError("Ungültiger Dateiname im Manifest.")
            result.append(safe_name(path).as_posix())
    if (not result or len(result) > MAX_FILES
            or len({s.casefold() for s in result}) != len(result)
            or "MANIFEST.json" not in result):
        raise ValueError("Unvollständiger oder doppelter Releasebestand.")
    return sorted(result)


def _copy_regular(source, target):
    source = Path(source)
    target = Path(target)
    if source.is_symlink() or any(part.is_symlink() for part in source.parents):
        raise ValueError("Quelldatei liegt hinter einer Verknüpfung.")
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_SINGLE:
            raise ValueError("Keine reguläre oder eine zu große Datei.")
        digest = hashlib.sha256()
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with os.fdopen(fd, "rb", closefd=False) as input_file, target.open("xb") as output:
            os.chmod(target, 0o600)
            amount = 0
            for block in iter(lambda: input_file.read(1024 * 1024), b""):
                amount += len(block)
                if amount > MAX_SINGLE:
                    raise ValueError("Quelldatei wurde während der Sicherung zu groß.")
                digest.update(block)
                output.write(block)
            output.flush()
            os.fsync(output.fileno())
        later = os.fstat(fd)
        if (later.st_size != info.st_size or later.st_mtime_ns != info.st_mtime_ns
                or later.st_ino != info.st_ino or amount != info.st_size):
            raise ValueError("Quelldatei wurde während der Sicherung verändert.")
    finally:
        os.close(fd)
    result = digest.hexdigest()
    if sha256(target) != result:
        raise ValueError("Sicherung stimmt nicht mit dem Original überein.")
    return {"size": amount, "sha256": result}


def create_checkpoint(active_root, staging_folder, checkpoint_parent):
    active, folder, _candidate, report = verify_candidate(active_root, staging_folder)
    parent = _safe_parent(checkpoint_parent, active)
    current = json.loads((active / "MANIFEST.json").read_text(encoding="utf-8"))
    paths = _released(current)
    checkpoint = Path(tempfile.mkdtemp(prefix="provoware-checkpoint-", dir=parent))
    try:
        captured = {}
        total = 0
        for relative in paths:
            value = _copy_regular(active / relative, checkpoint / "release" / relative)
            total += value["size"]
            if total > MAX_TOTAL:
                raise ValueError("Gesamtgröße der Sicherung überschritten.")
            captured[relative] = value
        if sha256(active / "MANIFEST.json") != report["basis_manifest_sha256"]:
            raise ValueError("Aktive Version hat sich während der Sicherung verändert.")
        if captured["MANIFEST.json"]["sha256"] != report["basis_manifest_sha256"]:
            raise ValueError("Gesicherte Manifestversion stimmt nicht.")
        receipt = {
            "schema_version": 1, "status": "CHECKPOINT_VERIFIED_NOT_ACTIVATED",
            "version": identity(current)["version"],
            "basis_manifest_sha256": report["basis_manifest_sha256"],
            "files": captured, "total_bytes": total,
            "activation_allowed": False, "active_project_changed": False,
        }
        atomic_write_json(checkpoint / "checkpoint.json", receipt)
        verify_checkpoint(checkpoint)
        return checkpoint, receipt
    except BaseException:
        shutil.rmtree(checkpoint)
        raise


def verify_checkpoint(folder):
    root = Path(folder).resolve(strict=True)
    receipt_path = root / "checkpoint.json"
    if receipt_path.is_symlink() or not receipt_path.is_file() or receipt_path.stat().st_size > 400_000:
        raise ValueError("Sicherungsnachweis fehlt oder ist ungültig.")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (not isinstance(receipt, dict) or set(receipt) != {
            "schema_version", "status", "version", "basis_manifest_sha256",
            "files", "total_bytes", "activation_allowed", "active_project_changed"}
            or receipt["schema_version"] != 1
            or receipt["status"] != "CHECKPOINT_VERIFIED_NOT_ACTIVATED"
            or receipt["activation_allowed"] is not False
            or receipt["active_project_changed"] is not False):
        raise ValueError("Unbekannte oder manipulierte Sicherungsstruktur.")
    manifesthash = receipt["basis_manifest_sha256"]
    files = receipt["files"]
    if (not isinstance(manifesthash, str) or not SHA.fullmatch(manifesthash)
            or not isinstance(files, dict) or not files or len(files) > MAX_FILES):
        raise ValueError("Sicherungsdateiliste ist ungültig.")
    base = root / "release"
    if base.is_symlink() or not base.is_dir():
        raise ValueError("Sicherungsinhalt fehlt.")
    found = set()
    for node in base.rglob("*"):
        if node.is_symlink() or not (node.is_file() or node.is_dir()):
            raise ValueError("Sicherungsbestand enthält Links oder Spezialdateien.")
        if node.is_file():
            found.add(node.relative_to(base).as_posix())
    if found != set(files):
        raise ValueError("Sicherungsbestand und Dateiliste unterscheiden sich.")
    total = 0
    for relative, record in files.items():
        if (not isinstance(relative, str) or safe_name(relative).as_posix() != relative
                or not isinstance(record, dict) or set(record) != {"size", "sha256"}
                or type(record["size"]) is not int or record["size"] < 0
                or record["size"] > MAX_SINGLE or not isinstance(record["sha256"], str)
                or not SHA.fullmatch(record["sha256"])):
            raise ValueError("Ungültiger Dateieintrag.")
        path = base / relative
        if path.stat().st_size != record["size"] or sha256(path) != record["sha256"]:
            raise ValueError("Sicherungsdatei beschädigt.")
        total += record["size"]
    if total > MAX_TOTAL or type(receipt["total_bytes"]) is not int or total != receipt["total_bytes"]:
        raise ValueError("Sicherungsgröße stimmt nicht.")
    if files["MANIFEST.json"]["sha256"] != manifesthash:
        raise ValueError("Gesichertes Manifest stimmt nicht.")
    manifest = json.loads((base / "MANIFEST.json").read_text(encoding="utf-8"))
    if identity(manifest)["version"] != receipt["version"] or _released(manifest) != sorted(files):
        raise ValueError("Sicherung passt nicht zum Releasevertrag.")
    return receipt


def restore_to_new_slot(checkpoint_folder, destination_parent, active_root):
    """Erzeugt eine unveränderliche, isolierte Rückkehrkopie, nie eine aktive Installation."""
    checkpoint = Path(checkpoint_folder).resolve(strict=True)
    active = Path(active_root).resolve(strict=True)
    parent = _safe_parent(destination_parent, active)
    if parent.is_relative_to(checkpoint) or checkpoint.is_relative_to(parent):
        raise ValueError("Rückkehrkopie muss getrennt von der Sicherung liegen.")
    receipt = verify_checkpoint(checkpoint)
    target = Path(tempfile.mkdtemp(prefix="provoware-restore-slot-", dir=parent))
    try:
        for relative, row in receipt["files"].items():
            value = _copy_regular(checkpoint / "release" / relative, target / "release" / relative)
            if value != row:
                raise ValueError("Rückkehrkopie weicht von der Sicherung ab.")
        atomic_write_json(target / "restore-report.json", {
            "schema_version": 1, "status": "RESTORED_TO_NEW_SLOT_NOT_ACTIVE",
            "origin_manifest_sha256": receipt["basis_manifest_sha256"],
            "activation_allowed": False, "active_project_changed": False,
        })
        return target
    except BaseException:
        shutil.rmtree(target)
        raise
