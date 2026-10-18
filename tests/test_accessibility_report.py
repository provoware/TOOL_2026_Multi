"""Prüft vollständige, nicht irreführende Barrierefreiheits-Berichte."""
import unittest
from scripts.barrierefreiheit_report import build_report
from app.accessibility_contracts import MODULES, DIMENSIONS


class AccessibilityReportTests(unittest.TestCase):
    def test_matrix_items_are_distinct_and_unreviewed_remains_open(self):
        report = build_report()
        self.assertEqual(report["gesamtfaelle"], len(MODULES) * len(DIMENSIONS))
        keys = {(r["modul"], r["kriterium"]) for r in report["prueffalle"]}
        self.assertEqual(len(keys), report["gesamtfaelle"])
        screenreaders = [x for x in report["prueffalle"]
                         if x["kriterium"] == "bildschirmleser_praxis"]
        self.assertEqual(len(screenreaders), len(MODULES))
        self.assertTrue(all(x["status"] == "praxispruefung_offen" for x in screenreaders))
        self.assertEqual(len({x["modul"] for x in screenreaders}), len(MODULES))

    def test_no_check_claims_finished_when_only_files_are_present(self):
        statuses = {item["status"] for item in build_report()["prueffalle"]}
        self.assertNotIn("bestanden", statuses)
        self.assertNotIn("vollstaendig_abgenommen", statuses)


if __name__ == "__main__":
    unittest.main()
