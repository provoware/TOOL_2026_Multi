import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.iteration_restore import safe_members, sha256


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


if __name__ == "__main__":
    unittest.main()
