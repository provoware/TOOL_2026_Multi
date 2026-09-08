"""Einzelinstanz-Schutz für schreibende Dashboard-Prozesse."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import QLockFile

CONTROLLED_ALREADY_RUNNING_EXIT = 10


@dataclass
class InstanceGuard:
    lock: QLockFile
    path: Path

    def release(self) -> None:
        if self.lock.isLocked():
            self.lock.unlock()


def acquire_instance_guard(root: Path) -> InstanceGuard | None:
    """Erlaubt pro Projektordner genau eine schreibende Programminstanz."""
    lock_path = root / "logs" / "provoware_dashboard.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = QLockFile(str(lock_path))
    # Nach einem echten Absturz darf eine eindeutig verwaiste Sperre zeitnah entfernt werden.
    lock.setStaleLockTime(5000)
    if not lock.tryLock(0):
        return None
    return InstanceGuard(lock=lock, path=lock_path)
