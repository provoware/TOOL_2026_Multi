"""Geprüfte Vorbereitung einer Alt-Schnellstartmigration; Altstart bleibt unverändert.

Eine produktive Ersetzung der regulären schnellstart.sh ist absichtlich NICHT
enthalten. Die separate, schreibgeschützte Originalkopie lässt sich unabhängig
überprüfen und ist Voraussetzung für einen späteren gesondert freizugebenden
atomaren Wrapper-Austausch.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import secrets
import stat

from app.atomic_io import atomic_write_json

MAX_LAUNCHER = 512 * 1024
RECEIPT = "launcher-backup.json"


def _hash(path):
    h = hashlib.sha256()
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_LAUNCHER or info.st_size < 1:
            raise ValueError("Kein zulässiges reguläres Schnellstartskript.")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(MAX_LAUNCHER + 1)
        if len(data) != info.st_size:
            raise ValueError("Schnellstart wurde während der Prüfung verändert.")
        h.update(data)
        return data, h.hexdigest()
    finally:
        os.close(fd)


def prepare_launcher_backup(legacy_root, independent_parent, *, approved=False):
    if approved is not True:
        raise PermissionError("Eine ausdrückliche Sicherungsfreigabe ist erforderlich.")
    legacy = Path(legacy_root).resolve(strict=True)
    parent = Path(independent_parent).resolve(strict=True)
    if (not legacy.is_dir() or not parent.is_dir()
            or legacy == parent or parent.is_relative_to(legacy)
            or legacy.is_relative_to(parent)
            or (legacy / "schnellstart.sh").is_symlink()):
        raise ValueError("Sicherungsziel muss unabhängig und ohne Links sein.")
    original = legacy / "schnellstart.sh"
    source, digest = _hash(original)
    backup = parent / ("provoware-launcher-backup-" + secrets.token_hex(10))
    backup.mkdir(mode=0o700)
    try:
        target = backup / "schnellstart.sh"
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(target, flags, 0o500)
        with os.fdopen(fd, "wb") as out:
            out.write(source)
            out.flush()
            os.fsync(out.fileno())
        _unchanged, copyhash = _hash(target)
        if copyhash != digest or _hash(original)[1] != digest:
            raise ValueError("Prüfsummen unterscheiden sich; Original wurde verändert.")
        atomic_write_json(backup / RECEIPT, {
            "schema_version": 1, "status": "BACKED_UP_NOT_ACTIVATED",
            "original": str(original), "sha256": digest,
            "copy": str(target), "activation_allowed": False,
        })
        return backup
    except BaseException:
        for name in (RECEIPT, "schnellstart.sh"):
            (backup / name).unlink(missing_ok=True)
        backup.rmdir()
        raise


def verify_launcher_backup(backup_folder):
    root = Path(backup_folder).resolve(strict=True)
    receipt = root / RECEIPT
    if receipt.is_symlink() or not receipt.is_file() or receipt.stat().st_size > 4096:
        raise ValueError("Sicherungsprotokoll fehlt.")
    data = json.loads(receipt.read_text(encoding="utf-8"))
    if (not isinstance(data, dict)
            or set(data) != {"schema_version", "status", "original", "sha256", "copy", "activation_allowed"}
            or data["schema_version"] != 1 or data["status"] != "BACKED_UP_NOT_ACTIVATED"
            or data["activation_allowed"] is not False
            or data["copy"] != str(root / "schnellstart.sh")):
        raise ValueError("Ungültiges Sicherungsprotokoll.")
    if _hash(root / "schnellstart.sh")[1] != data["sha256"]:
        raise ValueError("Sicherung wurde beschädigt.")
    if _hash(Path(data["original"]))[1] != data["sha256"]:
        raise ValueError("Original hat sich nach der Sicherung verändert.")
    return data
