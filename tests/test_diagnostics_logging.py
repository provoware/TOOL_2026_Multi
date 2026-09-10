import json
import subprocess
import sys
import tempfile
import types
import unittest
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from app.log_maintenance import _needs_rotation, quarantine_corrupt_jsonl, rotate_log
from scripts.diagnosepaket import build_diagnostic


class DiagnosticsLoggingTests(unittest.TestCase):
    def test_rotation_policy_has_explicit_boundary_and_disable_semantics(self):
        now = datetime(2026, 9, 10, 12, 0, tzinfo=timezone.utc)
        modified_now = now.timestamp()

        self.assertFalse(_needs_rotation(
            size=10, modified_at=modified_now, now=now,
            max_bytes=10, max_age_days=0,
        ))
        self.assertTrue(_needs_rotation(
            size=11, modified_at=modified_now, now=now,
            max_bytes=10, max_age_days=0,
        ))
        self.assertFalse(_needs_rotation(
            size=999, modified_at=modified_now - 999 * 86400, now=now,
            max_bytes=-1, max_age_days=-1,
        ))
        self.assertTrue(_needs_rotation(
            size=0, modified_at=modified_now - 86401, now=now,
            max_bytes=-1, max_age_days=1,
        ))

    def test_corrupt_jsonl_is_quarantined_and_valid_lines_survive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "logs" / "ereignisse.jsonl"
            log.parent.mkdir()
            log.write_text('{"ok":1}\nkaputt password=meinpasswort\n{"ok":2}\n', encoding="utf-8")
            count = quarantine_corrupt_jsonl(log, root / "logs" / "quarantaene")
            self.assertEqual(count, 1)
            self.assertEqual([json.loads(line)["ok"] for line in log.read_text().splitlines()], [1, 2])
            files = list((root / "logs" / "quarantaene").glob("*.json"))
            self.assertEqual(len(files), 1)
            self.assertNotIn("meinpasswort", files[0].read_text(encoding="utf-8"))

    def test_quarantine_uses_one_utc_snapshot_for_name_and_metadata(self):
        fixed = datetime(2026, 9, 10, 12, 34, 56, 789012, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "logs" / "ereignisse.jsonl"
            quarantine = root / "logs" / "quarantaene"
            log.parent.mkdir()
            log.write_text('{"ok":1}\nkaputt\n', encoding="utf-8")

            with patch("app.log_maintenance._utc_now", return_value=fixed):
                self.assertEqual(quarantine_corrupt_jsonl(log, quarantine), 1)

            files = list(quarantine.glob("*.json"))
            self.assertEqual(len(files), 1)
            self.assertIn("20260910_123456_789012", files[0].name)
            payload = json.loads(files[0].read_text(encoding="utf-8"))
            self.assertEqual(payload["created_utc"], fixed.isoformat())
            self.assertEqual(payload["corrupt_count"], 1)

    def test_quarantine_replace_failure_preserves_original_log_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "logs" / "ereignisse.jsonl"
            quarantine = root / "logs" / "quarantaene"
            log.parent.mkdir()
            original = b'{"ok":1}\nkaputt password=meinpasswort\n'
            log.write_bytes(original)

            with patch("app.atomic_io.os.replace", side_effect=OSError("simuliert")):
                with self.assertRaises(OSError):
                    quarantine_corrupt_jsonl(log, quarantine)

            self.assertEqual(log.read_bytes(), original)
            self.assertEqual(list((root / "logs").rglob("*.tmp")), [])

    def test_size_rotation_moves_log_and_limits_archives(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "logs" / "ereignisse.jsonl"
            log.parent.mkdir()
            for index in range(4):
                log.write_text(f'{{"n":{index}}}\n', encoding="utf-8")
                self.assertIsNotNone(rotate_log(log, max_bytes=0, max_age_days=9999, keep=2))
            self.assertLessEqual(len(list((root / "logs" / "archiv").glob("*.jsonl"))), 2)

    def test_diagnostic_script_direct_invocation_can_import_project_modules(self):
        root = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, "scripts/diagnosepaket.py", "--help"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_diagnostic_package_contains_only_redacted_copies(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "logs").mkdir()
            (root / "berichte").mkdir()
            (root / "MANIFEST.json").write_text(json.dumps({"tool":{"version":"9.9.9"}}), encoding="utf-8")
            (root / "logs" / "ereignisse.jsonl").write_text('token=ABC123456789 /home/geheim/datei a@b.de\n', encoding="utf-8")
            archive, checksum = build_diagnostic(root, root / "out")
            self.assertTrue(checksum.is_file())
            with zipfile.ZipFile(archive) as handle:
                combined = "\n".join(handle.read(name).decode("utf-8") for name in handle.namelist())
            self.assertNotIn("ABC123456789", combined)
            self.assertNotIn("/home/geheim", combined)
            self.assertNotIn("a@b.de", combined)
            self.assertIn('"privacy_check": "OK"', combined)

    def test_diagnostic_uses_unique_archive_names(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "MANIFEST.json").write_text(json.dumps({"tool":{"version":"9.9.9"}}), encoding="utf-8")
            first, _ = build_diagnostic(root, root / "out")
            second, _ = build_diagnostic(root, root / "out")
            self.assertNotEqual(first.name, second.name)
            self.assertTrue(first.is_file())
            self.assertTrue(second.is_file())

    def test_failed_archive_replace_leaves_no_temp_or_partial_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            out = root / "out"
            (root / "MANIFEST.json").write_text(json.dumps({"tool":{"version":"9.9.9"}}), encoding="utf-8")
            with patch("app.atomic_io.os.replace", side_effect=OSError("simulated replace failure")):
                with self.assertRaises(OSError):
                    build_diagnostic(root, out)
            self.assertEqual(list(out.glob("*.zip")), [])
            self.assertEqual(list(out.glob("*.tmp")), [])
            self.assertEqual(list(out.glob("*.sha256")), [])

    def test_normal_gui_return_records_controlled_end(self):
        import app.main as main_module
        events = []
        class FakeLogger:
            def __init__(self, *_args): pass
            def record(self, **kwargs): events.append(kwargs); return kwargs
        class FakeApplication:
            _instance = None
            def __init__(self, _args): FakeApplication._instance = self
            @classmethod
            def instance(cls): return cls._instance
            def setApplicationName(self, _name): pass
            def exec(self): return 0
        class FakeDashboard:
            def __init__(self, *_args): pass
            def refresh(self): pass
            def show(self): pass
        fake_widgets = types.SimpleNamespace(QApplication=FakeApplication)
        fake_ui = types.SimpleNamespace(Dashboard=FakeDashboard, install_exception_handler=lambda *_args: None)
        fake_standards = types.SimpleNamespace(configure_application=lambda *_args: None)
        fake_laptop = types.SimpleNamespace(install_laptop_layout=lambda *_args: None)
        fake_navigation = types.SimpleNamespace(install_navigation_ux=lambda *_args: None)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texte").mkdir()
            (root / "MANIFEST.json").write_text(json.dumps({"tool":{"version":"0.10.0"}}), encoding="utf-8")
            (root / "texte" / "registry.json").write_text(json.dumps({"texts":{}}), encoding="utf-8")
            with patch.object(main_module, "ROOT", root), patch.object(main_module, "EventLogger", FakeLogger), \
                 patch.dict(sys.modules, {"PySide6.QtWidgets": fake_widgets, "app.ui": fake_ui, "app.ui_standards": fake_standards, "app.laptop_layout": fake_laptop, "app.navigation_ux": fake_navigation}):
                self.assertEqual(main_module.main(), 0)
        self.assertEqual(events[-1]["area"], "ENDE")
        self.assertIn("kontrolliert beendet", events[-1]["summary"])


if __name__ == "__main__":
    unittest.main()
