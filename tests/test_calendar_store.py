import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch

from app.calendar_store import (
    add_event, all_events, day_range, due_reminders, events_between, load_state,
    mark_reminded, month_range, save_state, store_path, week_range, year_range,
)


class CalendarStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_empty_start_does_not_create_user_file(self):
        self.assertEqual(load_state(self.root)["events"], [])
        self.assertFalse(store_path(self.root).exists())

    def test_add_event_validates_title_and_end(self):
        event = add_event(
            self.root, "Arzt", "2026-09-10T14:00", "2026-09-10T15:00",
            "Kontrolle", 15,
        )
        self.assertEqual(event["title"], "Arzt")
        self.assertEqual(event["reminder_minutes"], 15)
        self.assertEqual(len(all_events(self.root)), 1)
        with self.assertRaises(ValueError):
            add_event(self.root, "", "2026-09-10T14:00", "2026-09-10T15:00")
        with self.assertRaises(ValueError):
            add_event(self.root, "Falsch", "2026-09-10T15:00", "2026-09-10T14:00")

    def test_day_week_month_year_ranges_have_correct_boundaries(self):
        chosen = date(2026, 9, 10)  # Thursday
        self.assertEqual(day_range(chosen), (datetime(2026, 9, 10), datetime(2026, 9, 11)))
        self.assertEqual(week_range(chosen), (datetime(2026, 9, 7), datetime(2026, 9, 14)))
        self.assertEqual(month_range(chosen), (datetime(2026, 9, 1), datetime(2026, 10, 1)))
        self.assertEqual(year_range(chosen), (datetime(2026, 1, 1), datetime(2027, 1, 1)))
        self.assertEqual(month_range(date(2026, 12, 20)), (datetime(2026, 12, 1), datetime(2027, 1, 1)))

    def test_range_query_includes_event_overlapping_midnight(self):
        add_event(self.root, "Nacht", "2026-09-09T23:30", "2026-09-10T00:30")
        start, end = day_range(date(2026, 9, 10))
        events = events_between(self.root, start, end)
        self.assertEqual([event["title"] for event in events], ["Nacht"])

    def test_reminder_becomes_due_and_is_one_shot_after_mark(self):
        event = add_event(
            self.root, "Termin", "2026-09-10T14:00", "2026-09-10T15:00",
            reminder_minutes=15,
        )
        self.assertEqual(due_reminders(self.root, datetime(2026, 9, 10, 13, 44)), [])
        due = due_reminders(self.root, datetime(2026, 9, 10, 13, 45))
        self.assertEqual([item["id"] for item in due], [event["id"]])
        mark_reminded(self.root, str(event["id"]), "2026-09-10T11:45:00+00:00")
        self.assertEqual(due_reminders(self.root, datetime(2026, 9, 10, 13, 50)), [])

    def test_expired_event_does_not_generate_late_reminder(self):
        add_event(
            self.root, "Vorbei", "2026-09-10T10:00", "2026-09-10T11:00",
            reminder_minutes=30,
        )
        self.assertEqual(due_reminders(self.root, datetime(2026, 9, 10, 12, 0)), [])

    def test_atomic_replace_failure_preserves_existing_calendar(self):
        add_event(self.root, "Vorher", "2026-09-10T10:00", "2026-09-10T11:00")
        target = store_path(self.root)
        before = target.read_bytes()
        state = load_state(self.root)
        state["events"].append({
            "id": "zweite", "title": "Zweite", "note": "",
            "start": "2026-09-11T10:00", "end": "2026-09-11T11:00",
            "reminder_minutes": None, "created_at": "2026-09-08T04:00:00+00:00",
            "reminded_at": None,
        })
        with patch("app.calendar_store.os.replace", side_effect=OSError("simuliert")):
            with self.assertRaises(OSError):
                save_state(self.root, state)
        self.assertEqual(target.read_bytes(), before)
        self.assertFalse(target.with_suffix(target.suffix + ".tmp").exists())


if __name__ == "__main__":
    unittest.main()
