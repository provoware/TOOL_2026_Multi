import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENTRY = ROOT / "scripts" / "ui_shadow_entry.py"


def _load_entry_module():
    spec = importlib.util.spec_from_file_location("provoware_ui_shadow_entry", ENTRY)
    if spec is None or spec.loader is None:
        raise RuntimeError("ui_shadow_entry.py konnte nicht geladen werden")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class UiShadowEntryTests(unittest.TestCase):
    def test_bootstrap_works_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ENTRY), "--bootstrap-check"],
                cwd=tmp,
                text=True,
                capture_output=True,
                timeout=20,
                env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("BOOTSTRAP_OK", result.stdout)
        self.assertIn(str(ROOT), result.stdout)

    def test_real_shadow_script_help_works_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(ENTRY), "--help"],
                cwd=tmp,
                text=True,
                capture_output=True,
                timeout=30,
                env={**os.environ, "QT_QPA_PLATFORM": "offscreen"},
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Provoware UI-Qualitätsgate", result.stdout)
        self.assertNotIn("ModuleNotFoundError", result.stderr)

    def test_infrastructure_evidence_is_written_before_qt_is_needed(self):
        module = _load_entry_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            evidence = module.write_infrastructure_evidence(
                output,
                profile="pr",
                stage="unit-test",
                exc=RuntimeError("absichtlich"),
            )
            payload = json.loads(evidence.read_text(encoding="utf-8"))
        self.assertEqual(payload["summary"]["status"], "infrastructure-error")
        self.assertEqual(payload["summary"]["infrastructure_errors"], 1)
        self.assertFalse(payload["summary"]["promotion_candidate"])
        self.assertEqual(payload["infrastructure"]["stage"], "unit-test")

    def test_validator_rejects_infrastructure_error(self):
        module = _load_entry_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "mode": "shadow",
                    "profile": "pr",
                    "finished_utc": "2026-09-12T00:00:00+00:00",
                    "summary": {
                        "status": "infrastructure-error",
                        "matrix_cases": 0,
                        "window_instances": 0,
                        "infrastructure_errors": 1,
                    },
                    "metrics": [],
                    "findings": [],
                }),
                encoding="utf-8",
            )
            ok, problems = module.validate_evidence(path)
        self.assertFalse(ok)
        self.assertTrue(any("Infrastrukturfehler" in item for item in problems))

    def test_validator_accepts_red_ui_findings_as_valid_shadow_evidence(self):
        module = _load_entry_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "mode": "shadow",
                    "profile": "pr",
                    "finished_utc": "2026-09-12T00:00:00+00:00",
                    "summary": {
                        "status": "red",
                        "matrix_cases": 8,
                        "window_instances": 24,
                        "errors": 2,
                        "warnings": 1,
                        "info": 0,
                        "infrastructure_errors": 0,
                        "promotion_candidate": False,
                    },
                    "metrics": [{} for _ in range(24)],
                    "findings": [{"severity": "error", "code": "TEST"}],
                }),
                encoding="utf-8",
            )
            ok, problems = module.validate_evidence(path)
        self.assertTrue(ok, problems)

    def test_validator_rejects_incomplete_matrix_even_when_status_is_green(self):
        module = _load_entry_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.json"
            path.write_text(
                json.dumps({
                    "schema_version": 1,
                    "mode": "shadow",
                    "profile": "pr",
                    "finished_utc": "2026-09-12T00:00:00+00:00",
                    "summary": {
                        "status": "green",
                        "matrix_cases": 7,
                        "window_instances": 21,
                        "infrastructure_errors": 0,
                    },
                    "metrics": [{} for _ in range(21)],
                    "findings": [],
                }),
                encoding="utf-8",
            )
            ok, problems = module.validate_evidence(path)
        self.assertFalse(ok)
        self.assertTrue(any("matrix_cases" in item for item in problems))


if __name__ == "__main__":
    unittest.main()
