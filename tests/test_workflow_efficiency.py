"""Prüft, dass optimierte GitHub-Abläufe alle Pflichtprüfungen bewahren."""
from pathlib import Path
import unittest


WORKFLOW = (Path(__file__).resolve().parents[1] /
            ".github/workflows/qualitaet.yml").read_text(encoding="utf-8")


class WorkflowEfficiencyTests(unittest.TestCase):
    def test_only_pull_requests_and_main_trigger_full_ci(self):
        self.assertIn("on:\n  push:\n    branches:\n      - main\n  pull_request:", WORKFLOW)
        self.assertIn("runs-on: ubuntu-latest", WORKFLOW)

    def test_only_outdated_pr_checks_can_be_cancelled(self):
        self.assertIn("concurrency:", WORKFLOW)
        self.assertIn("github.event.pull_request.number || github.ref", WORKFLOW)
        self.assertIn("cancel-in-progress: ${{ github.event_name == 'pull_request' }}", WORKFLOW)

    def test_python_cache_keeps_pinned_dependencies(self):
        self.assertIn("uses: actions/setup-python@v6", WORKFLOW)
        self.assertIn("python-version: '3.12'", WORKFLOW)
        self.assertIn("cache-dependency-path: requirements.txt", WORKFLOW)
        self.assertIn("python3 -m pip install --disable-pip-version-check -r requirements.txt", WORKFLOW)

    def test_full_safety_checks_are_still_present(self):
        mandatory = (
            "run: bash scripts/pruefen.sh --full",
            "scripts/wayland_smoke.py",
            "scripts/ui_shadow_entry.py --profile",
            "scripts/iteration_restore.py --output-dir",
            "python3 scripts/veroeffentlichen.py",
            "actions/upload-artifact@v4",
            "scripts/ui_shadow_entry.py --validate-evidence",
        )
        for name in mandatory:
            with self.subTest(check=name):
                self.assertIn(name, WORKFLOW)


if __name__ == "__main__":
    unittest.main()
