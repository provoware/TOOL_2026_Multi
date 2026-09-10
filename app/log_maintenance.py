"""Begrenzte Logrotation und sichere Quarantäne beschädigter JSONL-Zeilen."""

from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.atomic_io import atomic_write_json, atomic_write_text
from app.redaction import redact

DEFAULT_MAX_BYTES = 2 * 1024 * 1024
DEFAULT_MAX_AGE_DAYS = 30
DEFAULT_KEEP = 5
_SECONDS_PER_DAY = 24 * 60 * 60


def _utc_now() -> datetime:
    """Liefert einen einzigen, zeitzonenbewussten UTC-Zeitpunkt pro Operation."""
    return datetime.now(timezone.utc)


def _needs_rotation(*, size: int, modified_at: float, now: datetime,
                    max_bytes: int, max_age_days: int) -> bool:
    """Entscheidet ohne Dateisystemzugriff, ob Größen- oder Altersgrenze überschritten ist."""
    age_seconds = max(0.0, now.timestamp() - modified_at)
    too_large = max_bytes >= 0 and size > max_bytes
    too_old = max_age_days >= 0 and age_seconds > max_age_days * _SECONDS_PER_DAY
    return too_large or too_old


def _archive_mtime(path: Path) -> float:
    """Liefert eine robuste Sortierzeit; parallel verschwundene Archive landen hinten."""
    try:
        return path.stat().st_mtime
    except OSError:
        return float("-inf")


def quarantine_corrupt_jsonl(path: Path, quarantine_dir: Path) -> int:
    """Entfernt nur ungültige Zeilen und bewahrt eine bereinigte Beweiskopie auf."""
    if not path.exists():
        return 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return 0
    valid: list[str] = []
    corrupt: list[dict[str, object]] = []
    for number, line in enumerate(lines, start=1):
        try:
            json.loads(line)
            valid.append(line)
        except json.JSONDecodeError:
            cleaned = redact(line, limit=2000)
            corrupt.append({
                "line": number,
                "sha256": hashlib.sha256(line.encode("utf-8", errors="replace")).hexdigest(),
                "content_redacted": cleaned,
            })
    if not corrupt:
        return 0

    now = _utc_now()
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f")
    quarantine = quarantine_dir / f"{path.stem}_BESCHAEDIGT_{stamp}.json"
    payload = {
        "schema_version": 1,
        "source": path.name,
        "created_utc": now.isoformat(),
        "corrupt_count": len(corrupt),
        "items": corrupt,
    }
    atomic_write_json(quarantine, payload)
    atomic_write_text(path, "\n".join(valid) + ("\n" if valid else ""))
    return len(corrupt)


def rotate_log(path: Path, *, max_bytes: int = DEFAULT_MAX_BYTES,
               max_age_days: int = DEFAULT_MAX_AGE_DAYS, keep: int = DEFAULT_KEEP) -> Path | None:
    """Rotiert nur bei Größen- oder Altersgrenze und hält eine feste Zahl Archive."""
    if not path.exists() or keep < 1:
        return None

    stat = path.stat()
    now = _utc_now()
    if not _needs_rotation(
        size=stat.st_size,
        modified_at=stat.st_mtime,
        now=now,
        max_bytes=max_bytes,
        max_age_days=max_age_days,
    ):
        return None

    archive_dir = path.parent / "archiv"
    archive_dir.mkdir(parents=True, exist_ok=True)
    stamp = now.strftime("%Y%m%d_%H%M%S_%f")
    target = archive_dir / f"{path.stem}_{stamp}{path.suffix}"
    os.replace(path, target)

    archives = sorted(
        archive_dir.glob(f"{path.stem}_*{path.suffix}"),
        key=_archive_mtime,
        reverse=True,
    )
    for old in archives[keep:]:
        old.unlink(missing_ok=True)
    return target
