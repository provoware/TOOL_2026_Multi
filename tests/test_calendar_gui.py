import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDate, QDateTime, Qt
from PySide6.QtWidgets import QApplication

from app.calendar_reminders import CalendarReminderController
from app.calendar_store import add_event, all_events
from app.calendar_window import CalendarWindow
from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class CalendarGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.changed = 0
        self.window = CalendarWindow(self.root, on_changed=self._changed)
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()
        self.temp.cleanup()

    def _changed(self):
        self.changed += 1

    def test_day_week_month_year_are_distinct_real_ranges(self):
        add_event(self.root, "Tag", "2026-09-10T10:00", "2026-09-10T11:00")
        add_event(self.root, "Woche", "2026-09-12T10:00", "2026-09-12T11:00")
        add_event(self.root, "Monat", "2026-09-20T10:00", "2026-09-20T11:00")
        add_event(self.root, "Jahr", "2026-11-20T10:00", "2026-11-20T11:00")
        self.window.calendar.setSelectedDate(QDate(2026, 9, 10))
        self.window.refresh()
        self.assertEqual(self.window.day_table.rowCount(), 1)
        self.assertEqual(self.window.week_table.rowCount(), 2)
        self.assertEqual(self.window.month_table.rowCount(), 3)
        self.assertEqual(self.window.year_table.rowCount(), 4)
        self.assertEqual(self.window.tabs.count(), 4)

    def test_form_adds_event_with_reminder(self):
        self.window.title_entry.setText("Besprechung")
        self.window.note_entry.setPlainText("Raum 2")
        self.window.start_edit.setDateTime(QDateTime.fromString("10.09.2026 14:00", "dd.MM.yyyy HH:mm"))
        self.window.end_edit.setDateTime(QDateTime.fromString("10.09.2026 15:00", "dd.MM.yyyy HH:mm"))
        self.window.reminder_combo.setCurrentIndex(self.window.reminder_combo.findData(15))
        self.window.add_current_event()
        events = all_events(self.root)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["title"], "Besprechung")
        self.assertEqual(events[0]["reminder_minutes"], 15)
        self.assertEqual(self.changed, 1)

    def test_zoom_is_shared_with_calendar_window(self):
        self.window.set_zoom(175)
        self.assertEqual(self.window.zoom_percent, 175)

    def test_calendar_has_visible_close_action_and_dashboard_opens_it_as_independent_window(self):
        self.assertTrue(self.window.close_button.isVisible())
        self.assertEqual(self.window.close_button.text(), "Kalender schließen")

        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        self.app.processEvents()
        try:
            dashboard.open_calendar()
            self.app.processEvents()
            calendar = dashboard._calendar_window
            self.assertIsNotNone(calendar)
            assert calendar is not None
            self.assertTrue(calendar.isWindow())
            self.assertEqual(calendar.windowModality(), Qt.NonModal)
            self.assertTrue(calendar.property("provowareModuleWindow"))
            self.assertTrue(calendar.close_button.isVisible())
            calendar.close_button.click()
            self.app.processEvents()
            self.assertFalse(calendar.isVisible())
            self.assertTrue(dashboard.isVisible())
        finally:
            dashboard._closing_after_save = True
            dashboard.close()
            self.app.processEvents()

    def test_calendar_close_button_stays_reachable_at_200_percent(self):
        self.window.resize(1100, 720)
        self.window.set_zoom(200)
        self.app.processEvents()
        self.assertTrue(self.window.close_button.isVisible())
        self.assertEqual(self.window.close_button.text(), "Schließen")
        self.assertGreater(self.window.close_button.width(), 0)
        self.assertGreater(self.window.close_button.height(), 0)

    def test_reminder_controller_marks_only_after_callback(self):
        add_event(
            self.root, "Erinnerung", "2026-09-10T14:00", "2026-09-10T15:00",
            reminder_minutes=15,
        )
        shown = []
        controller = CalendarReminderController(self.root, shown.append, parent=self.window, interval_ms=3_600_000)
        controller.check_now(datetime(2026, 9, 10, 13, 45))
        controller.check_now(datetime(2026, 9, 10, 13, 50))
        controller.stop()
        self.assertEqual(len(shown), 1)
        self.assertIsNotNone(all_events(self.root)[0]["reminded_at"])

    def test_dashboard_reminders_run_without_open_calendar_window(self):
        add_event(
            self.root, "Dashboard-Termin", "2026-09-10T14:00", "2026-09-10T15:00",
            reminder_minutes=15,
        )
        dashboard = Dashboard(FakeTexts(), FakeLogger(), self.root)
        dashboard.show()
        self.app.processEvents()
        try:
            self.assertIsNone(dashboard._calendar_window)
            self.assertTrue(dashboard._calendar_reminders.timer.isActive())
            with patch("app.ui.QMessageBox.information") as information:
                dashboard._calendar_reminders.check_now(datetime(2026, 9, 10, 13, 45))
            information.assert_called_once()
            self.assertIsNotNone(all_events(self.root)[0]["reminded_at"])
            dashboard.open_calendar()
            self.app.processEvents()
            self.assertIsInstance(dashboard._calendar_window, CalendarWindow)
            dashboard.set_zoom(150)
            self.assertEqual(dashboard._calendar_window.zoom_percent, 150)
        finally:
            dashboard._closing_after_save = True
            dashboard.close()
            self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
