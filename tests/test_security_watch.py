import json
import tempfile
import unittest
from pathlib import Path

from app.event_log import EventLogger
from app.redaction import redact
from scripts.process_watch import write_crash_report


class SecurityAndWatcherTests(unittest.TestCase):
    def test_redact_removes_secrets_email_and_home_user(self):
        text = "password=hunter2 token: abcdefghijkl test@example.org /home/anna/projekt"
        cleaned = redact(text)
        self.assertNotIn("hunter2", cleaned)
        self.assertNotIn("abcdefghijkl", cleaned)
        self.assertNotIn("test@example.org", cleaned)
        self.assertNotIn("/home/anna", cleaned)
        self.assertIn("<GEHEIM>", cleaned)

    def test_event_logger_redacts_before_persisting_and_learning(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            logger = EventLogger(root, "0.4.0")
            event = logger.record(
                severity="FEHLER", area="IMPORT", summary="Mail test@example.org",
                cause="token=supersecret123 /home/anna/datei",
                protection="password=meinpass", next_step="Bearer abcdefghijklmno",
                exception=RuntimeError("token=supersecret123"),
            )
            stored = (root / "logs/ereignisse.jsonl").read_text(encoding="utf-8")
            report = next((root / "berichte").glob("*.txt")).read_text(encoding="utf-8")
            state = (root / "logs/rueckfaelle.json").read_text(encoding="utf-8")
            combined = stored + report + state + json.dumps(event)
            for secret in ("supersecret123", "meinpass", "test@example.org", "/home/anna", "abcdefghijklmno"):
                self.assertNotIn(secret, combined)

    def test_watcher_writes_report_for_abnormal_exit_and_redacts_command(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report = write_crash_report(root, -9, ["python3", "app.py", "token=abcdefghi"])
            self.assertTrue(report.exists())
            content = report.read_text(encoding="utf-8")
            log = (root / "logs/ereignisse.jsonl").read_text(encoding="utf-8")
            self.assertNotIn("abcdefghi", content + log)
            self.assertIn("ABSTURZ", content + log)


if __name__ == "__main__":
    unittest.main()
