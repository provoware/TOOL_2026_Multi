import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from scripts.iteration_restore import build_zip, extract_preserving_modes, safe_members, sha256


class RestoreTests(unittest.TestCase):
    def test_restore_script_direct_invocation_can_import_project_modules(self):
        root = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, "scripts/iteration_restore.py", "--help"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

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

    def test_symbolic_link_member_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            archive_path = Path(temp) / "link.zip"
            info = zipfile.ZipInfo("link")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr(info, "ziel")
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

    def test_restore_preserves_executable_bits_but_not_special_bits(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "projekt"
            restored = base / "restore"
            root.mkdir()
            restored.mkdir()
            launcher = root / "start.sh"
            launcher.write_text("#!/usr/bin/env bash\necho ok\n", encoding="utf-8")
            launcher.chmod(0o755)
            archive_path = base / "backup.zip"

            build_zip(root, archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                info = archive.getinfo("start.sh")
                self.assertTrue(((info.external_attr >> 16) & 0o777) & stat.S_IXUSR)
                extract_preserving_modes(archive, restored)

            restored_mode = (restored / "start.sh").stat().st_mode
            self.assertTrue(restored_mode & stat.S_IXUSR)
            self.assertEqual(stat.S_IMODE(restored_mode), 0o755)
            self.assertFalse(restored_mode & stat.S_ISUID)
            self.assertFalse(restored_mode & stat.S_ISGID)


if __name__ == "__main__":
    unittest.main()
