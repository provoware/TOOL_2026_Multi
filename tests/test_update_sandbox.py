"""Sicherheits- und Negativtests für die isolierte Update-Laufzeitprobe."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from app import update_staging as stage
from app import update_sandbox as sandbox


class UpdateSandboxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.active = root / "aktiv"
        self.active.mkdir()
        (self.active / "daten").mkdir()
        (self.active / "daten/persoenlich.txt").write_text("Geschuetzt", encoding="utf-8")
        manifest = {"tool": {"name": "TOOL_2026_Multi", "repository": "provoware/TOOL_2026_Multi", "version": "0.18.5"}}
        (self.active / "MANIFEST.json").write_text(json.dumps(manifest))
        self.package = root / "paket.zip"
        import zipfile
        entries = {"app/main.py": "raise RuntimeError('SENTINEL')",
                   "requirements.txt": "PySide6==6.11.2\n",
                   "schnellstart.sh": "#!/bin/bash\n"}
        cand = {"tool": {**manifest["tool"], "version": "0.18.6"},
                "files": [{"path": p, "release": True} for p in ["MANIFEST.json", *entries]]}
        with zipfile.ZipFile(self.package, "w") as archive:
            archive.writestr("MANIFEST.json", json.dumps(cand))
            for name, content in entries.items():
                archive.writestr(name, content)
        parent = root / "stage"
        parent.mkdir()
        self.folder, self.receipt = stage.stage_update(
            self.active, self.package, stage.sha256(self.package),
            stage.sha256(self.active / "MANIFEST.json"), parent)

    def test_fail_closed_without_isolation_does_not_run_candidate(self):
        with patch.object(sandbox.shutil, "which", return_value=None), patch.object(
            sandbox.subprocess, "run", side_effect=AssertionError("no host execution")
        ):
            result = sandbox.run_isolated(self.active, self.folder)
        self.assertEqual(result["status"], "ISOLATION_UNAVAILABLE")
        self.assertFalse(result["activation_allowed"])
        self.assertEqual((self.active / "daten/persoenlich.txt").read_text(), "Geschuetzt")

    def test_preflight_rejects_changed_candidate_and_receipt(self):
        target = self.folder / "candidate/app/main.py"
        target.write_text("pass\n")
        with self.assertRaisesRegex(ValueError, "verändert"):
            sandbox.verify_candidate(self.active, self.folder)
        target.write_bytes(b"raise RuntimeError('SENTINEL')")
        receipt = self.folder / "stage-report.json"
        raw = json.loads(receipt.read_text())
        raw["activation_allowed"] = True
        receipt.write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError, "Ausgangsprüfung"):
            sandbox.verify_candidate(self.active, self.folder)

    def test_sandbox_launch_only_with_unshare_and_read_only_mount(self):
        with patch.object(sandbox.shutil, "which", return_value="/usr/bin/bwrap"), patch.object(
            sandbox.subprocess, "run", return_value=SimpleNamespace(returncode=0)
        ) as process:
            # Nur den externen Lauf simulieren; Datei- und Hashprüfungen bleiben real.
            result = sandbox.run_isolated(self.active, self.folder)
        argv = process.call_args.args[0]
        self.assertIn("--unshare-all", argv)
        self.assertIn("--ro-bind", argv)
        self.assertIn("--cap-drop", argv)
        self.assertNotIn(str(self.active), argv)
        self.assertFalse(result["activation_allowed"])
        self.assertEqual(result["runtime_tests"], "PASS")

    def test_nonzero_sandbox_exit_is_never_activatable(self):
        with patch.object(sandbox.shutil, "which", return_value="/usr/bin/bwrap"), patch.object(
            sandbox.subprocess, "run", return_value=SimpleNamespace(returncode=18)
        ):
            result = sandbox.run_isolated(self.active, self.folder)
        self.assertNotEqual(result["runtime_tests"], "PASS")
        self.assertFalse(result["activation_allowed"])
