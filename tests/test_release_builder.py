import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.veroeffentlichen import build_release, release_files


class ReleaseBuilderTests(unittest.TestCase):
    def test_only_release_true_files_are_packaged(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "keep.txt").write_text("betrieb", encoding="utf-8")
            (root / "internal.txt").write_text("intern", encoding="utf-8")
            manifest = {
                "tool": {"name": "Probe", "version": "1.0.0"},
                "files": [
                    {"path": "keep.txt", "release": True},
                    {"path": "internal.txt", "release": False}
                ],
                "release_build": {"output_dir": "release"}
            }
            (root / "MANIFEST.json").write_text(json.dumps(manifest), encoding="utf-8")
            archive, _ = build_release(root)
            with zipfile.ZipFile(archive) as handle:
                self.assertEqual(handle.namelist(), ["keep.txt"])

    def test_release_path_cannot_escape_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = {"files": [{"path": "../outside.txt", "release": True}]}
            with self.assertRaises(ValueError):
                release_files(root, manifest)


if __name__ == "__main__":
    unittest.main()
