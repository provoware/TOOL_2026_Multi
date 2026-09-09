"""Vollprojekt-ZIP erstellen, SHA prüfen, isoliert wiederherstellen und abnehmen."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

from app.atomic_io import atomic_write_text

EXCLUDED = {".git", ".venv", "backups", "logs", "berichte", "tmp", "release", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_members(archive: zipfile.ZipFile) -> list[zipfile.ZipInfo]:
    members = archive.infolist()
    for info in members:
        path = PurePosixPath(info.filename)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Unsicherer ZIP-Pfad: {info.filename}")
    return members


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


def _commit_archive(temporary: Path, out: Path) -> None:
    """Synchronisiert ein validiertes ZIP und veröffentlicht es anschließend atomar."""
    with temporary.open("rb") as handle:
        os.fsync(handle.fileno())
    os.replace(temporary, out)
    _fsync_directory(out.parent)


def build_zip(root: Path, out: Path) -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{out.name}.", suffix=".tmp", dir=out.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    count = 0
    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(root.rglob("*")):
                rel = path.relative_to(root)
                if any(part in EXCLUDED for part in rel.parts):
                    continue
                if path.is_file() and path.resolve() != out.resolve():
                    archive.write(path, rel.as_posix())
                    count += 1
        with zipfile.ZipFile(temporary) as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise RuntimeError(f"Beschädigter ZIP-Eintrag: {bad_member}")
            safe_members(archive)
        _commit_archive(temporary, out)
    finally:
        temporary.unlink(missing_ok=True)
    return count


def run_checked(command: list[str], cwd: Path) -> None:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=120)
    if result.returncode:
        raise RuntimeError(
            f"Befehl fehlgeschlagen ({result.returncode}): {' '.join(command)}\n"
            f"{result.stdout[-3000:]}\n{result.stderr[-3000:]}"
        )


def restore_and_verify(root: Path, output_dir: Path) -> dict[str, object]:
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    version = manifest["tool"]["version"]
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"TOOL_2026_Multi_{version}_ITERATION_{stamp}.zip"
    file_count = build_zip(root, archive)
    expected_sha = sha256(archive)
    sha_file = archive.with_suffix(archive.suffix + ".sha256")
    atomic_write_text(sha_file, f"{expected_sha}  {archive.name}\n")
    if sha256(archive) != expected_sha:
        raise RuntimeError("SHA-256 stimmt nach dem Schreiben nicht überein.")

    restore_root = output_dir / "restore_test" / archive.stem
    if restore_root.exists():
        shutil.rmtree(restore_root)
    restore_root.mkdir(parents=True)
    with zipfile.ZipFile(archive) as zipped:
        members = safe_members(zipped)
        zipped.extractall(restore_root, members=members)

    restored_manifest = json.loads((restore_root / "MANIFEST.json").read_text(encoding="utf-8"))
    if restored_manifest != manifest:
        raise RuntimeError("Wiederhergestelltes Manifest weicht vom Quellmanifest ab.")

    run_checked(["bash", "scripts/pruefen.sh", "--full"], restore_root)
    run_checked([sys.executable, "-m", "app.main", "--headless-check"], restore_root)
    report = {
        "restore_status": "OK", "archive": str(archive), "sha256": expected_sha,
        "restore_dir": str(restore_root), "files": file_count,
        "manifest_version": version, "full_check": "OK", "headless_start": "OK",
    }
    report_path = output_dir / f"{archive.stem}_RESTORE.json"
    atomic_write_text(report_path, json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output_dir or (root / "backups")).resolve()
    try:
        report = restore_and_verify(root, output)
    except Exception as error:
        print(f"🔴 Restore-Prüfung fehlgeschlagen: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(f"🟢 Restore-Status: {report['restore_status']}")
    print(f"🟢 SHA-256: {report['sha256']}")
    print(f"🟢 Wiederhergestellt: {report['restore_dir']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
