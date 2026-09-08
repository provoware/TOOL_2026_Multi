import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.atomic_io import atomic_write_text
from app.process_guard import CONTROLLED_ALREADY_RUNNING_EXIT, acquire_instance_guard
from scripts.process_watch import run


class ProcessConsistencyTests(unittest.TestCase):
    def test_atomic_write_uses_unique_temp_and_preserves_old_content_on_replace_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "daten" / "bestand.txt"
            atomic_write_text(target, "alt\n")
            before = target.read_bytes()
            seen = []

            def fail_replace(source, destination):
                seen.append(Path(source).name)
                raise OSError("simuliert")

            with patch("app.atomic_io.os.replace", side_effect=fail_replace):
                with self.assertRaises(OSError):
                    atomic_write_text(target, "neu\n")
                with self.assertRaises(OSError):
                    atomic_write_text(target, "noch neuer\n")

            self.assertEqual(target.read_bytes(), before)
            self.assertEqual(len(seen), 2)
            self.assertNotEqual(seen[0], seen[1])
            self.assertEqual(list(target.parent.glob(f".{target.name}.*.tmp")), [])

    def test_second_instance_guard_is_blocked_until_first_releases(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = acquire_instance_guard(root)
            self.assertIsNotNone(first)
            try:
                self.assertIsNone(acquire_instance_guard(root))
            finally:
                first.release()
            third = acquire_instance_guard(root)
            self.assertIsNotNone(third)
            third.release()

    def test_controlled_second_start_does_not_create_crash_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            code = run(root, [sys.executable, "-c", f"raise SystemExit({CONTROLLED_ALREADY_RUNNING_EXIT})"])
            self.assertEqual(code, CONTROLLED_ALREADY_RUNNING_EXIT)
            self.assertEqual(list((root / "berichte").glob("*.txt")) if (root / "berichte").exists() else [], [])
            self.assertFalse((root / "logs" / "ereignisse.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
