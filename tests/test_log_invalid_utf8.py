"""Rückfalltests: Ungültige UTF-8-Bytes in Ereignislogs dürfen keinen Folgefehler auslösen."""

import json
import tempfile
import unittest
from pathlib import Path

from app.event_log import EventLogger
from app.log_maintenance import quarantine_corrupt_jsonl


class InvalidUtf8EventLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.log = self.root / "logs" / "ereignisse.jsonl"
        self.log.parent.mkdir(parents=True)
        self.original = b'{"vorher":"ok"}\n\xff\xfe\n'
        self.log.write_bytes(self.original)
        self.quarantine = self.root / "logs" / "quarantaene"

    def test_quarantine_preserves_invalid_utf8_original_without_side_effects(self):
        self.assertEqual(quarantine_corrupt_jsonl(self.log, self.quarantine), 0)
        self.assertEqual(self.log.read_bytes(), self.original)
        self.assertFalse(self.quarantine.exists())

    def test_recent_fails_closed_without_changing_user_log(self):
        logger = EventLogger(self.root, "0.18.5")
        self.assertEqual(logger.recent(), [])
        self.assertEqual(self.log.read_bytes(), self.original)

    def test_record_still_writes_diagnostic_without_erasing_original(self):
        logger = EventLogger(self.root, "0.18.5")
        event = logger.record(
            severity="INFO",
            area="TEST",
            summary="Diagnose funktioniert weiterhin",
            cause="Ungültige UTF-8-Bytes im bisherigen Log",
            protection="Ursprüngliche Logbytes beibehalten",
            next_step="Altes Log bei Bedarf von Hand sichern und prüfen",
        )
        updated = self.log.read_bytes()
        self.assertTrue(updated.startswith(self.original))
        self.assertEqual(json.loads(updated.splitlines()[-1])["event_id"], event["event_id"])
        self.assertTrue((self.root / "berichte" / f"{event['event_id']}.txt").is_file())
        self.assertFalse(self.quarantine.exists())


if __name__ == "__main__":
    unittest.main()
