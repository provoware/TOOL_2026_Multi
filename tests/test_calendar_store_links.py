"""Schutz gegen gültige und defekte Verknüpfungen im Kalender-Datenpfad."""
import tempfile
import unittest
from pathlib import Path

from app.calendar_store import add_event, empty_state, load_state, save_state


class CalendarStoreLinkTests(unittest.TestCase):
    def test_linked_data_paths_are_rejected_without_external_changes(self):
        for component in ("daten", "kalender", "termine.json"):
            for dangling in (False, True):
                with self.subTest(component=component, dangling=dangling):
                    with tempfile.TemporaryDirectory() as tmp:
                        root = Path(tmp) / "projekt"
                        root.mkdir()
                        outside = Path(tmp) / "ausserhalb"
                        outside.mkdir()
                        if component == "daten":
                            link = root / "daten"
                            destination = outside / "daten"
                            external_file = destination / "kalender" / "termine.json"
                        elif component == "kalender":
                            link = root / "daten" / "kalender"
                            destination = outside / "kalender"
                            external_file = destination / "termine.json"
                        else:
                            link = root / "daten" / "kalender" / "termine.json"
                            destination = outside / "termine.json"
                            external_file = destination
                        link.parent.mkdir(parents=True, exist_ok=True)
                        if not dangling:
                            external_file.parent.mkdir(parents=True, exist_ok=True)
                            external_file.write_text('{"schema_version": 1, "events": []}',
                                                     encoding="utf-8")
                            before = external_file.read_bytes()
                        link.symlink_to(destination, target_is_directory=component != "termine.json")
                        for operation in (
                            lambda: load_state(root),
                            lambda: add_event(root, "Test", "2026-10-27T10:00",
                                              "2026-10-27T11:00"),
                            lambda: save_state(root, empty_state()),
                        ):
                            with self.assertRaisesRegex(ValueError, "Verknüpfungen"):
                                operation()
                        if dangling:
                            self.assertFalse(destination.exists())
                        else:
                            self.assertEqual(external_file.read_bytes(), before)

    def test_regular_calendar_path_remains_usable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            add_event(root, "Termin", "2026-10-27T10:00", "2026-10-27T11:00")
            self.assertEqual(len(load_state(root)["events"]), 1)


if __name__ == "__main__":
    unittest.main()
