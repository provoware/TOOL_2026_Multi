import json
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from app.log_maintenance import quarantine_corrupt_jsonl, rotate_log
from scripts.diagnosepaket import build_diagnostic


class DiagnosticsLoggingTests(unittest.TestCase):
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

    def test_size_rotation_moves_log_and_limits_archives(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            log = root / "logs" / "ereignisse.jsonl"
            log.parent.mkdir()
            for index in range(4):
                log.write_text(f'{{"n":{index}}}\n', encoding="utf-8")
                self.assertIsNotNone(rotate_log(log, max_bytes=0, max_age_days=9999, keep=2))
            self.assertLessEqual(len(list((root / "logs" / "archiv").glob("*.jsonl"))), 2)

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
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "texte").mkdir()
            (root / "MANIFEST.json").write_text(json.dumps({"tool":{"version":"0.10.0"}}), encoding="utf-8")
            (root / "texte" / "registry.json").write_text(json.dumps({"texts":{}}), encoding="utf-8")
            with patch.object(main_module, "ROOT", root), patch.object(main_module, "EventLogger", FakeLogger), \
                 patch.dict(sys.modules, {"PySide6.QtWidgets": fake_widgets, "app.ui": fake_ui, "app.ui_standards": fake_standards}):
                self.assertEqual(main_module.main(), 0)
        self.assertEqual(events[-1]["area"], "ENDE")
        self.assertIn("kontrolliert beendet", events[-1]["summary"])


if __name__ == "__main__":
    unittest.main()
