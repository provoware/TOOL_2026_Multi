"""Vollprojekt-ZIP erstellen, SHA prüfen, isoliert wiederherstellen und abnehmen."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath

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


def build_zip(root: Path, out: Path) -> int:
    out.parent.mkdir(parents=True, exist_ok=True)
    temporary = out.with_suffix(out.suffix + ".tmp")
    count = 0
    with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            rel = path.relative_to(root)
            if any(part in EXCLUDED for part in rel.parts):
                continue
            if path.is_file() and path.resolve() != out.resolve():
                archive.write(path, rel.as_posix())
                count += 1
    with zipfile.ZipFile(temporary) as archive:
        archive.testzip()
        safe_members(archive)
    os.replace(temporary, out)
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
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"TOOL_2026_Multi_{version}_ITERATION_{stamp}.zip"
    file_count = build_zip(root, archive)
    expected_sha = sha256(archive)
    sha_file = archive.with_suffix(archive.suffix + ".sha256")
    sha_file.write_text(f"{expected_sha}  {archive.name}\n", encoding="utf-8")
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
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
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
