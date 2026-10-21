"""Schnelles, append-only Entwicklerinformationsprotokoll."""

from __future__ import annotations

import os
import stat
from datetime import datetime, timezone
from pathlib import Path


def append_developer_info(root: Path, text: str) -> Path:
    """Hängt eine einzeilige Entwicklerinformation mit UTC-Zeitstempel an."""
    clean = " ".join(str(text).splitlines()).strip()
    if not clean:
        raise ValueError("Die Schnelleingabe ist leer.")
    target = root / "Entwicklerinformation.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    # NOFOLLOW schützt auch bei einem Linktausch unmittelbar vor dem Öffnen.
    # NONBLOCK verhindert Hänger durch versehentlich angelegte benannte Pipes.
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK
    descriptor = os.open(target, flags, 0o600)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        info = os.fstat(handle.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise PermissionError("Die Projekt-Notiz muss eine normale Datei ohne weitere Verknüpfungen sein.")
        handle.write(f"[{timestamp}] {clean}\n")
        handle.flush()
        os.fsync(handle.fileno())
    return target
