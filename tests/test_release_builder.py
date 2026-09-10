import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.veroeffentlichen import build_release, release_files


class ReleaseBuilderTests(unittest.TestCase):
    @staticmethod
    def _manifest() -> dict:
        return {
            "tool": {"name": "Probe", "version": "1.0.0"},
            "files": [
                {"path": "keep.txt", "release": True},
                {"path": "internal.txt", "release": False},
            ],
            "release_build": {"output_dir": "release"},
        }

    def test_only_release_true_files_are_packaged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "keep.txt").write_text("betrieb", encoding="utf-8")
            (root / "internal.txt").write_text("intern", encoding="utf-8")
            (root / "MANIFEST.json").write_text(json.dumps(self._manifest()), encoding="utf-8")
            archive, checksum = build_release(root)
            with zipfile.ZipFile(archive) as handle:
                self.assertEqual(handle.namelist(), ["keep.txt"])
            checksum_file = archive.with_suffix(archive.suffix + ".sha256")
            self.assertEqual(checksum_file.read_text(encoding="utf-8"), f"{checksum}  {archive.name}\n")

    def test_release_replace_failure_preserves_existing_archive_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "keep.txt").write_text("betrieb", encoding="utf-8")
            (root / "internal.txt").write_text("intern", encoding="utf-8")
            (root / "MANIFEST.json").write_text(json.dumps(self._manifest()), encoding="utf-8")
            output = root / "release"
            output.mkdir()
            archive = output / "Probe_1.0.0_release.zip"
            archive.write_bytes(b"ALTER FREIGABESTAND")

            with patch("app.atomic_io.os.replace", side_effect=OSError("simuliert")):
                with self.assertRaises(OSError):
                    build_release(root)

            self.assertEqual(archive.read_bytes(), b"ALTER FREIGABESTAND")
            self.assertEqual(list(output.glob("*.tmp")), [])
            self.assertFalse(archive.with_suffix(archive.suffix + ".sha256").exists())

    def test_release_path_cannot_escape_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = {"files": [{"path": "../outside.txt", "release": True}]}
            with self.assertRaises(ValueError):
                release_files(root, manifest)

    def test_all_runtime_app_modules_are_release_listed(self):
        root = Path(__file__).resolve().parent.parent
        manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
        released = {
            entry["path"] for entry in manifest.get("files", [])
            if entry.get("release") is True and isinstance(entry.get("path"), str)
        }
        app_modules = {
            path.relative_to(root).as_posix()
            for path in (root / "app").glob("*.py")
            if path.is_file()
        }
        missing = sorted(app_modules - released)
        self.assertEqual(
            missing,
            [],
            "Runtime-App-Module fehlen im Release-Manifest: " + ", ".join(missing),
        )


if __name__ == "__main__":
    unittest.main()
