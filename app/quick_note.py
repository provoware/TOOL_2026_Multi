"""Schnelles, append-only Entwicklerinformationsprotokoll."""

from __future__ import annotations

import os
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
    with target.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {clean}\n")
        handle.flush()
        os.fsync(handle.fileno())
    return target
