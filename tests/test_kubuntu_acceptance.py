import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.kubuntu_abnahme import CheckResult, environment_checks, signal_probe, write_report


class KubuntuAcceptanceTests(unittest.TestCase):
    def test_direct_script_invocation_can_import_project_modules(self):
        root = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, "scripts/kubuntu_abnahme.py", "--help"],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def test_x11_kde_environment_is_recognized(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "x11",
            "DISPLAY": ":0",
            "XDG_CURRENT_DESKTOP": "KDE",
            "DESKTOP_SESSION": "plasma",
        })}
        self.assertEqual(results["x11"].status, "OK")
        self.assertEqual(results["kde"].status, "OK")

    def test_wayland_or_missing_display_blocks_x11_acceptance(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "wayland",
            "DISPLAY": "",
            "XDG_CURRENT_DESKTOP": "KDE",
        })}
        self.assertEqual(results["x11"].status, "BLOCKIERT")

    def test_signal_probe_uses_real_watcher_and_reports_sigterm(self):
        root = Path(__file__).resolve().parent.parent
        result = signal_probe(root)
        self.assertEqual(result.status, "OK")
        self.assertIn("SIGTERM", result.detail)
        self.assertIn("Tempordner", result.detail)

    def test_report_is_not_green_without_visual_confirmation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = [CheckResult("x11", "X11", "OK", "bereit")]
            txt, json_path = write_report(root, results)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "NICHT_VOLLSTAENDIG")
            self.assertIn("Noch keine sichtbare Bestätigung", txt.read_text(encoding="utf-8"))

    def test_report_is_green_only_when_automatic_and_visual_checks_are_green(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = [CheckResult("x11", "X11", "OK", "bereit"), CheckResult("signal", "Signal", "OK", "bereit")]
            visual = {"Layout": True, "Fokus": True, "Zoom": True}
            _txt, json_path = write_report(root, results, visual)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "OK")
            self.assertEqual(payload["visual_confirmations"], visual)


if __name__ == "__main__":
    unittest.main()
