#!/usr/bin/env python3
"""Erstellt ein bereinigtes Diagnose-ZIP ohne unveränderte Rohprotokolle."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from app.atomic_io import atomic_write_text
from app.redaction import redact

ROOT = Path(__file__).resolve().parent.parent
TEXT_GLOBS = ("logs/*.jsonl", "logs/*.json", "berichte/*.txt")
ALWAYS = ("MANIFEST.json",)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fsync_directory(directory: Path) -> None:
    """Sichert den Ziel-Verzeichniseintrag, soweit das Dateisystem dies unterstützt."""
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0)
    try:
        descriptor = os.open(str(directory), flags)
    except OSError:
        return
    try:
        try:
            os.fsync(descriptor)
        except OSError:
            return
    finally:
        os.close(descriptor)


def _commit_archive(temporary: Path, archive: Path) -> None:
    """Synchronisiert ein fertiges ZIP und veröffentlicht es erst danach atomar."""
    with temporary.open("rb") as handle:
        os.fsync(handle.fileno())
    os.replace(temporary, archive)
    _fsync_directory(archive.parent)


def _privacy_clean(text: str) -> str:
    cleaned = redact(text)
    if redact(cleaned) != cleaned:
        raise ValueError("Datenschutzprüfung ist nicht idempotent.")
    return cleaned


def source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in ALWAYS:
        path = root / relative
        if path.is_file():
            files.append(path)
    for pattern in TEXT_GLOBS:
        files.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted(set(files))


def build_diagnostic(root: Path = ROOT, output_dir: Path | None = None) -> tuple[Path, Path]:
    root = root.resolve()
    output_dir = (output_dir or root / "diagnose").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    version = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))["tool"]["version"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    archive = output_dir / f"TOOL_2026_Multi_{version}_DIAGNOSE_{stamp}.zip"
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    collected: list[dict[str, object]] = []
    temporary: Path | None = None
    with tempfile.TemporaryDirectory(dir=output_dir) as temp:
        temp_root = Path(temp)
        for source in source_files(root):
            relative = source.relative_to(root)
            try:
                text = source.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            cleaned = _privacy_clean(text)
            target = temp_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(cleaned, encoding="utf-8")
            collected.append({"path": relative.as_posix(), "bytes": len(cleaned.encode("utf-8"))})
        info = {
            "schema_version": 1,
            "created_utc": datetime.now(timezone.utc).isoformat(),
            "privacy_check": "OK",
            "raw_files_included": False,
            "file_count": len(collected),
            "files": collected,
        }
        (temp_root / "DIAGNOSE_INFO.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{archive.name}.", suffix=".tmp", dir=str(output_dir)
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        try:
            with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as handle:
                for path in sorted(temp_root.rglob("*")):
                    if path.is_file():
                        handle.write(path, path.relative_to(temp_root))
            with zipfile.ZipFile(temporary) as handle:
                for name in handle.namelist():
                    data = handle.read(name).decode("utf-8")
                    if redact(data) != data:
                        raise ValueError(f"Datenschutzprüfung fehlgeschlagen: {name}")
            _commit_archive(temporary, archive)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    atomic_write_text(checksum, f"{_sha256(archive)}  {archive.name}\n")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    archive, checksum = build_diagnostic(output_dir=args.output_dir)
    print(f"🟢 Diagnosepaket: {archive}")
    print(f"🟢 Datenschutzprüfung: OK")
    print(f"🟢 SHA-256: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
