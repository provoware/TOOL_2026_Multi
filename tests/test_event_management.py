import json
import tempfile
import unittest
from pathlib import Path

from app.event_log import EventLogger
from app.ui_style import DEFAULT_STYLE, load_ui_style


class EventManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.logger = EventLogger(self.root, "0.2.0")

    def tearDown(self):
        self.temp.cleanup()

    def test_event_has_required_fields_and_both_formats(self):
        event = self.logger.record(severity="INFO", area="TEST", summary="Prüfung erfolgreich.",
            cause="Gezielter Test", protection="Keine Daten verändert.", next_step="Nichts nötig.")
        stored = json.loads((self.root / "logs/ereignisse.jsonl").read_text().strip())
        for key in ("time", "event_id", "severity", "area", "summary", "technical_cause",
                    "safe_action", "next_step", "program_version"):
            self.assertEqual(stored[key], event[key])
        self.assertTrue((self.root / "berichte" / f"{event['event_id']}.txt").exists())

    def test_recent_returns_only_latest_five(self):
        for number in range(7):
            self.logger.record(severity="INFO", area="TEST", summary=str(number), cause="Test",
                               protection="Sicher", next_step="Keiner")
        self.assertEqual([event["summary"] for event in self.logger.recent(5)], ["6", "5", "4", "3", "2"])

    def test_repeated_error_is_learned(self):
        for _ in range(2):
            event = self.logger.record(severity="FEHLER", area="IMPORT", summary="Import fehlgeschlagen.",
                cause="Datei fehlt", protection="Nichts übernommen.", next_step="Datei prüfen.",
                exception=FileNotFoundError("Datei fehlt"))
        self.assertTrue(event["regression"]["repeated"])
        self.assertEqual(event["regression"]["count"], 2)
        self.assertEqual(event["error_status"], "BEOBACHTET")
        self.assertIsNone(event["regression_test_id"])
        self.assertIn("erneut", event["next_step"])

    def test_incomplete_ui_config_keeps_safe_defaults(self):
        path = self.root / "ui.json"
        path.write_text('{"schema_version": 1, "spacing": {"small": 8}}', encoding="utf-8")
        style = load_ui_style(path)
        self.assertEqual(style["spacing"]["small"], 8)
        self.assertEqual(style["spacing"]["large"], DEFAULT_STYLE["spacing"]["large"])


if __name__ == "__main__":
    unittest.main()
