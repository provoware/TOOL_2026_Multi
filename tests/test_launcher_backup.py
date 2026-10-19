"""Echter Kopiertest, Manipulation, fehlende Zustimmung und Erhalt des Originals."""
import tempfile
import unittest
from pathlib import Path
from app import launcher_backup as b

class LauncherBackupTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        base = Path(self.t.name)
        self.root = base / "legacy"
        self.root.mkdir()
        self.target = base / "external"
        self.target.mkdir()
        self.script = self.root / "schnellstart.sh"
        self.script.write_text("#!/usr/bin/env bash\necho 'alte Version'\n")
    def test_original_preserved_and_backup_checked(self):
        before = self.script.read_bytes()
        with self.assertRaises(PermissionError):
            b.prepare_launcher_backup(self.root, self.target)
        folder = b.prepare_launcher_backup(self.root, self.target, approved=True)
        self.assertEqual(b.verify_launcher_backup(folder)["status"], "BACKED_UP_NOT_ACTIVATED")
        self.assertEqual(self.script.read_bytes(), before)
        self.assertFalse((self.root / "start").exists())
    def test_modified_backup_or_original_fails_closed(self):
        folder = b.prepare_launcher_backup(self.root, self.target, approved=True)
        (folder / "schnellstart.sh").chmod(0o700)
        (folder / "schnellstart.sh").write_text("manipuliert")
        with self.assertRaises(ValueError):
            b.verify_launcher_backup(folder)
        folder2 = b.prepare_launcher_backup(self.root, self.target, approved=True)
        self.script.write_text("Original inzwischen verändert")
        with self.assertRaises(ValueError):
            b.verify_launcher_backup(folder2)
    def test_symlink_and_nested_target_refused(self):
        with self.assertRaises(ValueError):
            b.prepare_launcher_backup(self.root, self.root, approved=True)
        self.script.unlink()
        target = self.target / "outside"
        target.write_text("fake")
        self.script.symlink_to(target)
        with self.assertRaises(ValueError):
            b.prepare_launcher_backup(self.root, self.target, approved=True)
