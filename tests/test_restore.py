import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.iteration_restore import build_zip, safe_members, sha256


class RestoreTests(unittest.TestCase):
    def test_sha256_is_stable(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "a.bin"
            path.write_bytes(b"provoware")
            self.assertEqual(sha256(path), sha256(path))

    def test_zip_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            archive_path = Path(temp) / "bad.zip"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("../escape.txt", "x")
            with zipfile.ZipFile(archive_path) as archive:
                with self.assertRaises(ValueError):
                    safe_members(archive)

    def test_build_zip_keeps_existing_archive_on_replace_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "projekt"
            output = Path(temp) / "out"
            root.mkdir()
            output.mkdir()
            (root / "MANIFEST.json").write_text("{}", encoding="utf-8")
            archive = output / "backup.zip"
            archive.write_bytes(b"ALT")

            with patch("scripts.iteration_restore.os.replace", side_effect=OSError("simuliert")):
                with self.assertRaises(OSError):
                    build_zip(root, archive)

            self.assertEqual(archive.read_bytes(), b"ALT")
            self.assertEqual(list(output.glob(".backup.zip.*.tmp")), [])

    def test_build_zip_creates_valid_archive_without_temp_leftover(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "projekt"
            output = Path(temp) / "out"
            root.mkdir()
            output.mkdir()
            (root / "MANIFEST.json").write_text("{}", encoding="utf-8")
            archive = output / "backup.zip"

            count = build_zip(root, archive)

            self.assertEqual(count, 1)
            self.assertTrue(archive.is_file())
            with zipfile.ZipFile(archive) as zipped:
                self.assertIsNone(zipped.testzip())
                self.assertEqual(zipped.namelist(), ["MANIFEST.json"])
            self.assertEqual(list(output.glob(".backup.zip.*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
