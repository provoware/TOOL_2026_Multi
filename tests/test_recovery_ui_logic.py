import errno
import tempfile
import unittest
from pathlib import Path

from app.help_content import help_topic_by_key, help_topics
from app.recovery_ui import available_areas, filter_events, repetition_summary, technical_details, zoom_font_size
from app.regression import RegressionManager
from scripts.schreibfehler_simulieren import run_simulations


class RecoveryUiLogicTests(unittest.TestCase):
    def test_help_topics_are_searchable_and_stable(self):
        all_topics = help_topics()
        self.assertGreaterEqual(len(all_topics), 8)
        self.assertEqual(all_topics[0].key, "erste-schritte")
        wayland = help_topics("kubuntu wayland")
        self.assertEqual([topic.key for topic in wayland], ["kubuntu-abnahme"])
        self.assertEqual(help_topics("gibt-es-nicht"), ())

    def test_help_search_normalises_german_umlauts_and_rendering_is_actionable(self):
        matches = help_topics("oeffnen")
        self.assertTrue(any(topic.key == "erste-schritte" for topic in matches))
        topic = help_topic_by_key("fehler-beheben")
        self.assertIsNotNone(topic)
        rendered = topic.render()
        self.assertIn("So gehst du vor:", rendered)
        self.assertIn("1.", rendered)
        self.assertIn("Wichtig:", rendered)

    def test_filters_by_severity_and_area(self):
        events = [
            {"severity": "INFO", "area": "START"},
            {"severity": "FEHLER", "area": "IMPORT"},
            {"severity": "FEHLER", "area": "START"},
        ]
        self.assertEqual(len(filter_events(events, "FEHLER", "ALLE")), 2)
        self.assertEqual(len(filter_events(events, "ALLE", "START")), 2)
        self.assertEqual(len(filter_events(events, "FEHLER", "START")), 1)
        self.assertEqual(available_areas(events), ["ALLE", "IMPORT", "START"])

    def test_first_seen_is_stable_and_repeat_count_increases(self):
        with tempfile.TemporaryDirectory() as temp:
            manager = RegressionManager(Path(temp) / "rueckfaelle.json")
            first = manager.learn("IMPORT", "ValueError", "gleicher grund")
            second = manager.learn("IMPORT", "ValueError", "gleicher grund")
        self.assertEqual(first["count"], 1)
        self.assertEqual(second["count"], 2)
        self.assertEqual(first["first_seen"], second["first_seen"])
        count, first_seen = repetition_summary({"regression": second, "time": "2020-01-01T00:00:00Z"})
        self.assertEqual(count, 2)
        self.assertEqual(first_seen, second["first_seen"])

    def test_zoom_accepts_only_defined_levels(self):
        self.assertEqual(zoom_font_size(10, 150), 15)
        with self.assertRaises(ValueError):
            zoom_font_size(10, 133)

    def test_technical_details_are_separate_from_simple_summary(self):
        event = {"event_id": "E-1", "technical_cause": "Intern", "exception_type": "ValueError",
                 "trace": "Spur", "regression": {"signature": "abc"}}
        details = technical_details(event)
        self.assertIn("Technischer Grund: Intern", details)
        self.assertIn("Signatur: abc", details)

    def test_enospc_and_erofs_simulations_preserve_existing_content(self):
        results = run_simulations()
        self.assertEqual({item["errno"] for item in results}, {errno.ENOSPC, errno.EROFS})
        self.assertTrue(all(item["status"] == "OK" for item in results))
        self.assertTrue(all(item["bestand_unveraendert"] for item in results))
        self.assertTrue(all(item["temp_reste"] == 0 for item in results))


if __name__ == "__main__":
    unittest.main()
