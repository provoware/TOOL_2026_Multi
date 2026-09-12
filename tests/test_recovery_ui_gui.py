import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QTreeWidget

from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return [
            {
                "time": "2026-09-08T01:00:00+00:00", "severity": "INFO", "area": "START",
                "summary": "Start ok", "safe_action": "Keine", "next_step": "Nichts",
                "event_id": "E1", "technical_cause": "Normal", "exception_type": None,
                "trace": None, "regression": None,
            },
            {
                "time": "2026-09-08T01:01:00+00:00", "severity": "FEHLER", "area": "IMPORT",
                "summary": "Import fehlgeschlagen", "safe_action": "Abgebrochen",
                "next_step": "Datei prüfen", "event_id": "E2", "technical_cause": "Datei fehlt",
                "exception_type": "FileNotFoundError", "trace": "Spur",
                "regression": {"count": 3, "first_seen": "2026-09-08T00:30:00+00:00", "signature": "abc"},
            },
        ]

    @staticmethod
    def human_report(event):
        return str(event)


class RecoveryUiGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.dashboard = Dashboard(FakeTexts(), FakeLogger())
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()

    def test_recovery_is_single_sidebar_entry_and_not_dashboard_table(self):
        self.assertEqual(self.dashboard.recovery_nav_button.text().strip(), "ⓘ  Hilfe & Fehlerhilfe")
        self.assertEqual(len(self.dashboard.findChildren(QTreeWidget)), 0)

    def test_searchable_quick_help_is_available_without_hiding_recovery(self):
        self.dashboard.open_recovery()
        rc = self.dashboard._recovery_center
        self.app.processEvents()
        self.assertEqual(rc.tabs.tabText(0), "Schnellhilfe")
        self.assertEqual(rc.tabs.tabText(1), "Fehlermeldungen")
        self.assertGreaterEqual(rc.help_list.count(), 8)
        rc.help_search.setText("Wayland")
        self.app.processEvents()
        self.assertEqual(rc.help_list.count(), 1)
        self.assertIn("Kubuntu 26.04", rc.help_text.toPlainText())
        self.assertIn("Wayland", rc.help_text.toPlainText())

    def test_recovery_filters_and_selection(self):
        self.dashboard.open_recovery()
        rc = self.dashboard._recovery_center
        self.app.processEvents()
        self.assertEqual(rc.table.topLevelItemCount(), 2)
        rc.severity_filter.setCurrentText("FEHLER")
        self.app.processEvents()
        self.assertEqual(rc.table.topLevelItemCount(), 1)
        self.assertEqual(rc.selected_event()["area"], "IMPORT")

    def test_zoom_keeps_supported_value(self):
        self.dashboard.open_recovery()
        rc = self.dashboard._recovery_center
        rc.set_zoom(150)
        self.assertEqual(rc.zoom_percent, 150)
        self.assertEqual(rc.zoom_filter.currentText(), "150 %")

    def test_keyboard_shortcuts_and_recovery_window_are_qt(self):
        self.dashboard.open_recovery()
        rc = self.dashboard._recovery_center
        self.assertTrue(rc.isWindow())
        self.assertTrue(rc.table.focusPolicy() != 0)
        self.assertIn("Hilfe", rc.windowTitle())


if __name__ == "__main__":
    unittest.main()
