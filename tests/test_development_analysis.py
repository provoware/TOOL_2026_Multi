"""Schutztests der rein internen Entwicklungswerkzeuge."""
import tempfile
import unittest
from pathlib import Path

from scripts.code_doppelungen import finde_doppelungen
from scripts.entwicklungsmessung import auswerten


class DevelopmentAnalysisTests(unittest.TestCase):
    def test_duplicate_blocks_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            content = "def test():\n    a = 1\n    b = a + 2\n    c = a + b\n    return c\n"
            (root / "one.py").write_text(content, encoding="utf-8")
            (root / "two.py").write_text(content, encoding="utf-8")
            groups = finde_doppelungen(root)
            self.assertTrue(groups)
            self.assertEqual(groups[0]["anzahl"], 2)

    def test_different_code_has_no_duplicate_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "one.py").write_text("def a():\n    return 1\n", encoding="utf-8")
            (root / "two.py").write_text("def b():\n    return 2\n", encoding="utf-8")
            self.assertEqual(finde_doppelungen(root), [])

    def test_metrics_count_runs_and_cache_proof(self):
        runs = [
            {"head_sha": "a", "event": "push", "status": "completed",
             "conclusion": "success", "run_started_at": "2026-10-17T10:00:00Z",
             "updated_at": "2026-10-17T10:10:00Z"},
            {"head_sha": "a", "event": "pull_request", "status": "completed",
             "conclusion": "success", "run_started_at": "2026-10-17T10:01:00Z",
             "updated_at": "2026-10-17T10:13:00Z"},
        ]
        result = auswerten(runs, {"changed_files": 2, "additions": 8, "deletions": 4},
                           "Cache restored from key: xyz")
        self.assertEqual(result["weitere_laeufe_gleicher_commits"], 1)
        self.assertEqual(result["median_minuten_geschaetzt"], 11)
        self.assertEqual(result["aenderungsumfang"]["dateien"], 2)
        self.assertEqual(result["paket_zwischenspeicher"], "Treffer")

    def test_cache_not_claimed_without_proof(self):
        self.assertNotIn("paket_zwischenspeicher", auswerten([]))


if __name__ == "__main__":
    unittest.main()
