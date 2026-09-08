#!/usr/bin/env python3
"""Erzeugt ein Release-ZIP ausschließlich aus Manifest-Einträgen mit release=true."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_manifest(root: Path) -> dict:
    return json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))


def release_files(root: Path, manifest: dict) -> list[Path]:
    root_resolved = root.resolve()
    selected: list[Path] = []
    seen: set[str] = set()
    for entry in manifest.get("files", []):
        if entry.get("release") is not True:
            continue
        raw_path = entry.get("path")
        if not isinstance(raw_path, str) or not raw_path.strip():
            raise ValueError("Release-Eintrag ohne gültigen Pfad im Manifest.")
        relative = Path(raw_path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"Unsicherer Release-Pfad im Manifest: {raw_path}")
        normalized = relative.as_posix()
        if normalized in seen:
            raise ValueError(f"Doppelter Release-Pfad im Manifest: {normalized}")
        target = (root / relative).resolve()
        if root_resolved != target and root_resolved not in target.parents:
            raise ValueError(f"Release-Pfad verlässt das Projekt: {raw_path}")
        if not target.is_file():
            raise FileNotFoundError(f"Markierte Betriebsdatei fehlt: {raw_path}")
        selected.append(relative)
        seen.add(normalized)
    if not selected:
        raise ValueError("Das Manifest enthält keine Betriebsdatei mit release=true.")
    return sorted(selected, key=lambda path: path.as_posix())


def verify_archive(archive: Path, expected: list[Path]) -> None:
    with zipfile.ZipFile(archive, "r") as handle:
        names = sorted(handle.namelist())
        wanted = sorted(path.as_posix() for path in expected)
        if names != wanted:
            raise RuntimeError("Release-ZIP enthält nicht exakt die im Manifest freigegebenen Dateien.")
        bad = handle.testzip()
        if bad is not None:
            raise RuntimeError(f"Beschädigter ZIP-Eintrag: {bad}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_release(root: Path, output_dir: Path | None = None) -> tuple[Path, str]:
    manifest = load_manifest(root)
    selected = release_files(root, manifest)
    tool = manifest["tool"]
    output_dir = output_dir or root / manifest.get("release_build", {}).get("output_dir", "release")
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"{tool['name']}_{tool['version']}_release.zip"
    temporary = archive.with_suffix(".zip.tmp")
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as handle:
            for relative in selected:
                handle.write(root / relative, arcname=relative.as_posix())
        verify_archive(temporary, selected)
        os.replace(temporary, archive)
    finally:
        temporary.unlink(missing_ok=True)
    checksum = sha256(archive)
    archive.with_suffix(archive.suffix + ".sha256").write_text(f"{checksum}  {archive.name}\n", encoding="utf-8")
    return archive, checksum


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="nur Manifest-Freigaben prüfen")
    args = parser.parse_args()
    manifest = load_manifest(ROOT)
    selected = release_files(ROOT, manifest)
    if args.check_only:
        print(f"🟢 Release-Manifest gültig: {len(selected)} freigegebene Betriebsdateien.")
        return 0
    archive, checksum = build_release(ROOT)
    print(f"🟢 Release erstellt: {archive}")
    print(f"SHA-256: {checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
