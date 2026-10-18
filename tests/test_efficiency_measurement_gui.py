"""Interne Tests: Signalsperre und nachvollziehbare GitHub-Laufzeiten."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from app.song_editor import SongEditor
from scripts.entwicklungsmessung import schrittzeiten, hauptzweig_vergleich


class EfficiencySafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_compact_mode_preserves_preexisting_signal_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp))
            try:
                editor.details_toggle.blockSignals(True)
                editor.set_compact_mode(not editor._compact_mode)
                self.assertTrue(editor.details_toggle.signalsBlocked())
            finally:
                editor.details_toggle.blockSignals(False)
                editor._closing_after_save = True
                editor.close()

    def test_step_timing_only_counts_successful_completed_steps(self):
        data = {"jobs": [{"steps": [
            {"name": "Systempakete für Wayland bereitstellen", "conclusion": "success",
             "started_at": "2026-10-18T04:00:00Z", "completed_at": "2026-10-18T04:00:23Z"},
            {"name": "Python-Pakete bereitstellen", "conclusion": "failure",
             "started_at": "2026-10-18T04:00:23Z", "completed_at": "2026-10-18T04:00:26Z"},
        ]}]}
        result = schrittzeiten(data)
        self.assertEqual(result["sekunden_je_pruefschritt"]["Systempakete für Wayland bereitstellen"], [23])
        self.assertEqual(result["sekunden_je_pruefschritt"]["Python-Pakete bereitstellen"], [])
        self.assertEqual(result["gemessene_ausfuehrungen"], 1)

    def test_comparison_does_not_claim_ten_runs_from_small_sample(self):
        def run(day, seconds):
            start = f"2026-10-{day}T00:00:00Z"
            from datetime import datetime, timedelta, timezone
            end = datetime.fromisoformat(start.replace("Z", "+00:00")) + timedelta(seconds=seconds)
            return {"event": "push", "head_branch": "main", "status": "completed",
                    "conclusion": "success", "run_started_at": start,
                    "updated_at": end.isoformat()}
        report = hauptzweig_vergleich([run("16", 100), run("18", 125)],
                                      "2026-10-17T00:00:00Z")
        self.assertFalse(report["zehn_neue_vollstaendig"])
        self.assertEqual(report["vorher"]["durchschnitt_sekunden"], 100)
        self.assertEqual(report["nachher"]["durchschnitt_sekunden"], 125)


if __name__ == "__main__":
    unittest.main()
