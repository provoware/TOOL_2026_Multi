"""Zentraler, rücknehmbarer Schreibweg für lokale Nutzerdaten und Berichte."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def _fsync_directory(directory: Path) -> None:
    """Sichert den Verzeichniseintrag, soweit das Dateisystem dies unterstützt."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(str(directory), flags)
    except OSError:
        return
    try:
        try:
            os.fsync(descriptor)
        except OSError:
            # Einige Dateisysteme/Plattformen unterstützen Verzeichnis-fsync nicht.
            return
    finally:
        os.close(descriptor)


def atomic_publish_file(temporary: Path, target: Path) -> Path:
    """Veröffentlicht eine fertig erzeugte Datei im selben Zielordner atomar."""
    temporary = Path(temporary)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if temporary.parent.resolve() != target.parent.resolve():
        raise ValueError("Temporäre Datei und Ziel müssen im selben Ordner liegen.")
    if not temporary.is_file():
        raise FileNotFoundError(f"Temporäre Datei fehlt: {temporary}")
    try:
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, target)
        _fsync_directory(target.parent)
    finally:
        if temporary.exists():
            temporary.unlink(missing_ok=True)
    return target


def atomic_write_text(target: Path, content: str, *, encoding: str = "utf-8") -> Path:
    """Schreibt erst vollständig in eine eindeutige Tempdatei und ersetzt dann atomar."""
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{target.name}.", suffix=".tmp", dir=str(target.parent)
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding=encoding, newline="") as handle:
            handle.write(content)
            handle.flush()
        atomic_publish_file(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink(missing_ok=True)
    return target


def atomic_write_json(target: Path, payload: Any) -> Path:
    """Schreibt JSON über denselben zentralen Schutzweg."""
    content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return atomic_write_text(target, content)
