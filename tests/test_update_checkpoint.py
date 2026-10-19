"""Sicherungen nur außerhalb des Programms, prüfbare Rückkehrkopie."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from app import update_checkpoint as ck
from app import update_staging as stage
from app.atomic_io import atomic_write_json


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.active = self.root / "aktiv"
        self.active.mkdir()
        self.staging = self.root / "staging"
        self.staging.mkdir()
        self.backups = self.root / "checkpoints"
        self.backups.mkdir()
        self.restore = self.root / "restore"
        self.restore.mkdir()
        entries = {
            "requirements.txt": "PySide6==6.11.2\n",
            "schnellstart.sh": "#!/bin/bash\nexit 0\n",
            "app/main.py": "print('START')\n",
        }
        for name, text in entries.items():
            destination = self.active / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(text)
        (self.active / "daten").mkdir()
        (self.active / "daten/personen.txt").write_text("Geheim")
        current = {"tool": {"name": "TOOL_2026_Multi",
                             "repository": "provoware/TOOL_2026_Multi",
                             "version": "0.18.5"},
                   "files": [{"path": name, "release": True}
                             for name in ["MANIFEST.json", *entries]]}
        atomic_write_json(self.active / "MANIFEST.json", current)
        candidate = {"tool": {**current["tool"], "version": "0.18.6"},
                     "files": current["files"]}
        package = self.root / "paket.zip"
        with zipfile.ZipFile(package, "w") as archive:
            archive.writestr("MANIFEST.json", json.dumps(candidate))
            for name, content in entries.items():
                archive.writestr(name, content)
        self.owned, _ = stage.stage_update(self.active, package,
            stage.sha256(package), stage.sha256(self.active / "MANIFEST.json"), self.staging)

    def test_create_verify_restore_never_changes_active(self):
        backup, receipt = ck.create_checkpoint(self.active, self.owned, self.backups)
        self.assertEqual(ck.verify_checkpoint(backup), receipt)
        self.assertFalse((backup / "release/daten").exists())
        self.assertFalse(receipt["activation_allowed"])
        new = ck.restore_to_new_slot(backup, self.restore, self.active)
        self.assertEqual((new / "release/MANIFEST.json").read_bytes(),
                         (self.active / "MANIFEST.json").read_bytes())
        self.assertFalse(json.loads((new / "restore-report.json").read_text())["activation_allowed"])
        self.assertEqual((self.active / "daten/personen.txt").read_text(), "Geheim")

    def test_corrupt_and_symlink_rejected(self):
        backup, _ = ck.create_checkpoint(self.active, self.owned, self.backups)
        original = (backup / "release/app/main.py").read_bytes()
        (backup / "release/app/main.py").write_text("HACK")
        with self.assertRaises(ValueError):
            ck.verify_checkpoint(backup)
        (backup / "release/app/main.py").write_bytes(original)
        (backup / "release/app/main.py").unlink()
        (backup / "release/app/main.py").symlink_to(self.active / "app/main.py")
        with self.assertRaises(ValueError):
            ck.verify_checkpoint(backup)

    def test_protect_active_and_cleanup_partial_backup(self):
        with self.assertRaises(ValueError):
            ck.create_checkpoint(self.active, self.owned, self.active / "daten")
        original = (self.active / "MANIFEST.json").read_bytes()
        with patch.object(ck, "_copy_regular", side_effect=OSError("Datenträger voll")):
            with self.assertRaises(OSError):
                ck.create_checkpoint(self.active, self.owned, self.backups)
        self.assertEqual(list(self.backups.iterdir()), [])
        self.assertEqual((self.active / "MANIFEST.json").read_bytes(), original)

    def test_refuse_restoring_into_checkpoint_tree(self):
        backup, _ = ck.create_checkpoint(self.active, self.owned, self.backups)
        with self.assertRaises(ValueError):
            ck.restore_to_new_slot(backup, backup / "release", self.active)
        with self.assertRaises(ValueError):
            ck.restore_to_new_slot(backup, self.active / "daten", self.active)
