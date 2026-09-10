import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from scripts.kubuntu_abnahme import (
    CheckResult,
    checks_are_green,
    environment_checks,
    qt_platform_probe,
    signal_probe,
    write_report,
)


TARGET_OS = {"ID": "ubuntu", "ID_LIKE": "debian", "VERSION_ID": "26.04.1"}


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

    def test_wayland_kde_2604_environment_is_recognized(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "wayland",
            "WAYLAND_DISPLAY": "wayland-0",
            "XDG_CURRENT_DESKTOP": "KDE",
            "DESKTOP_SESSION": "plasmawayland",
        }, TARGET_OS)}
        self.assertEqual(results["release"].status, "OK")
        self.assertEqual(results["wayland"].status, "OK")
        self.assertEqual(results["kde"].status, "OK")
        self.assertEqual(results["qpa_env"].status, "OK")

    def test_x11_is_not_valid_for_2604_wayland_acceptance(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "x11",
            "DISPLAY": ":0",
            "XDG_CURRENT_DESKTOP": "KDE",
            "DESKTOP_SESSION": "plasma",
        }, TARGET_OS)}
        self.assertEqual(results["wayland"].status, "BLOCKIERT")

    def test_old_ubuntu_release_is_not_valid_for_2604_acceptance(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "wayland",
            "WAYLAND_DISPLAY": "wayland-0",
            "XDG_CURRENT_DESKTOP": "KDE",
        }, {"ID": "ubuntu", "VERSION_ID": "24.04"})}
        self.assertEqual(results["release"].status, "BLOCKIERT")

    def test_forced_xcb_blocks_native_wayland_acceptance(self):
        results = {item.key: item for item in environment_checks({
            "XDG_SESSION_TYPE": "wayland",
            "WAYLAND_DISPLAY": "wayland-0",
            "XDG_CURRENT_DESKTOP": "KDE",
            "QT_QPA_PLATFORM": "xcb",
        }, TARGET_OS)}
        self.assertEqual(results["qpa_env"].status, "BLOCKIERT")

    def test_qt_platform_probe_requires_native_wayland(self):
        completed = Mock(returncode=0, stdout="wayland\n", stderr="")
        with patch("scripts.kubuntu_abnahme.subprocess.run", return_value=completed):
            result = qt_platform_probe(Path.cwd(), {"WAYLAND_DISPLAY": "wayland-0"})
        self.assertEqual(result.status, "OK")
        self.assertIn("wayland", result.detail.lower())

        completed = Mock(returncode=0, stdout="xcb\n", stderr="")
        with patch("scripts.kubuntu_abnahme.subprocess.run", return_value=completed):
            result = qt_platform_probe(Path.cwd(), {"DISPLAY": ":0"})
        self.assertEqual(result.status, "BLOCKIERT")

    def test_signal_probe_uses_real_watcher_and_reports_sigterm(self):
        root = Path(__file__).resolve().parent.parent
        result = signal_probe(root)
        self.assertEqual(result.status, "OK")
        self.assertIn("SIGTERM", result.detail)
        self.assertIn("Tempordner", result.detail)

    def test_report_is_not_green_without_visual_confirmation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = [CheckResult("wayland", "Wayland", "OK", "bereit")]
            txt, json_path = write_report(root, results)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["status"], "NICHT_VOLLSTAENDIG")
            self.assertIn("Wayland", payload["target"])
            self.assertIn("Noch keine sichtbare Bestätigung", txt.read_text(encoding="utf-8"))

    def test_report_is_green_only_when_all_automatic_and_visual_checks_are_green(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            results = [
                CheckResult("release", "26.04", "OK", "bereit"),
                CheckResult("wayland", "Wayland", "OK", "bereit"),
                CheckResult("qt_wayland", "Qt Wayland", "OK", "bereit"),
                CheckResult("signal", "Signal", "OK", "bereit"),
            ]
            visual = {"Layout": True, "Fokus": True, "Zoom": True}
            _txt, json_path = write_report(root, results, visual)
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertTrue(checks_are_green(results))
            self.assertEqual(payload["status"], "OK")
            self.assertEqual(payload["visual_confirmations"], visual)

    def test_any_blocked_automatic_check_prevents_green_status(self):
        self.assertFalse(checks_are_green([
            CheckResult("wayland", "Wayland", "OK", "bereit"),
            CheckResult("qt", "Qt", "BLOCKIERT", "xcb"),
        ]))


if __name__ == "__main__":
    unittest.main()
