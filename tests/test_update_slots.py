"""Negativtests: Slot-Update, Umschalt-Fehler und Rückkehr nach Abbruch."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from app import update_slots as slots
from app import update_staging as stage
from app import update_checkpoint as ck
from app.atomic_io import atomic_write_json


class SlotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.deploy = self.root / "install"
        self.old = self.deploy / "slots/old"
        self.old.mkdir(parents=True)
        self.deploy.joinpath("current").symlink_to("slots/old")
        self.entries = {"requirements.txt": "PySide6==6.11.2\n",
                        "schnellstart.sh": "#!/bin/bash\n",
                        "app/main.py": "print('probe')\n"}
        self.manifest = {"tool": {"name": "TOOL_2026_Multi",
                                 "repository": "provoware/TOOL_2026_Multi",
                                 "version": "0.18.5"},
                         "files": [{"path": k, "release": True}
                                   for k in ["MANIFEST.json", *self.entries]]}
        for name, data in self.entries.items():
            path = self.old / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data)
        atomic_write_json(self.old / "MANIFEST.json", self.manifest)
        candidate = {**self.manifest,
                     "tool": {**self.manifest["tool"], "version": "0.18.6"}}
        self.zip = self.root / "update.zip"
        with zipfile.ZipFile(self.zip, "w") as z:
            z.writestr("MANIFEST.json", json.dumps(candidate))
            for name, data in self.entries.items():
                z.writestr(name, data)
        staging_parent = self.root / "stages"
        staging_parent.mkdir()
        self.stage, _ = stage.stage_update(
            self.old, self.zip, stage.sha256(self.zip),
            stage.sha256(self.old / "MANIFEST.json"), staging_parent)
        backup_parent = self.root / "backups"
        backup_parent.mkdir()
        self.backup, _ = ck.create_checkpoint(self.old, self.stage, backup_parent)

    def _do(self, results):
        with patch.object(slots, "run_isolated",
                          return_value={"runtime_tests": "PASS",
                                        "status": "ISOLATED_PROBE_PASSED_NOT_ACTIVATABLE"}), patch.object(
                              slots, "_health_check", side_effect=results):
            return slots.activate_managed(self.deploy, self.stage, self.backup)

    def test_switch_keeps_prior_slot_and_never_deletes_data(self):
        result = self._do([True, True])
        self.assertEqual(result["status"], "ACTIVE_VERIFIED")
        self.assertEqual(self.deploy.joinpath("current").resolve().name, result["new"])
        self.assertTrue((self.old / "MANIFEST.json").is_file())
        self.assertEqual(slots._journal(self.deploy)["state"], "ACTIVE_VERIFIED")

    def test_failed_post_activation_health_restores_old_pointer(self):
        with self.assertRaisesRegex(ValueError, "Startnachprüfung"):
            self._do([True, False])
        self.assertEqual(self.deploy.joinpath("current").resolve(), self.old)
        self.assertEqual(slots._journal(self.deploy)["state"], "ROLLED_BACK")

    def test_failed_before_switch_never_touches_pointer(self):
        with self.assertRaisesRegex(ValueError, "Startprüfung"):
            self._do([False])
        self.assertEqual(self.deploy.joinpath("current").resolve(), self.old)
        self.assertFalse((self.deploy / slots.JOURNAL).exists())

    def test_untrusted_legacy_install_and_missing_probe_refused(self):
        with self.assertRaises(ValueError):
            slots.activate_managed(self.old, self.stage, self.backup)
        with self.assertRaisesRegex(ValueError, "isolierte"):
            slots.activate_managed(self.deploy, self.stage, self.backup)
        self.assertEqual(self.deploy.joinpath("current").resolve(), self.old)

    def test_recover_interrupted_pointer_flip(self):
        other = self.deploy / "slots/new"
        other.mkdir()
        atomic_write_json(self.deploy / slots.JOURNAL, {
            "schema": 1, "state": "SWITCH_PENDING", "old": "old", "new": "new"})
        slots._atomic_pointer(self.deploy, "new")
        self.assertTrue(slots.recover_pending(self.deploy))
        self.assertEqual(self.deploy.joinpath("current").resolve(), self.old)
        self.assertEqual(slots._journal(self.deploy)["state"], "ROLLED_BACK")

    def test_data_in_existing_slot_denied(self):
        personal = self.old / "daten"
        personal.mkdir()
        (personal / "private").write_text("UNVERAENDERT")
        with self.assertRaisesRegex(ValueError, "Persönliche"):
            self._do([True, True])
        self.assertEqual((personal / "private").read_text(), "UNVERAENDERT")
