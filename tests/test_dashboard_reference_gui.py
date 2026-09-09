import os
import tempfile
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pathlib import Path

from PySide6.QtWidgets import QApplication, QFrame, QPushButton

from app.ui import Dashboard
from app.ui_standards import COLORS


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class DashboardReferenceGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), Path(self.temp.name))
        self.dashboard.resize(1280, 790)
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.app.processEvents()
        self.temp.cleanup()

    def test_reference_title_framework_and_modern_dark_accent_theme(self):
        self.assertEqual(self.dashboard.windowTitle(), "Provoware-Datenbank-Dashboard 2026")
        self.assertEqual(COLORS["accent"], "#FFB11B")
        self.assertLess(int(COLORS["background"][1:3], 16), 20)
        self.assertTrue(type(self.dashboard).__mro__[1].__module__.startswith("PySide6"))

    def test_reference_has_sidebar_tile_strip_and_responsive_two_by_two_cards(self):
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 210)
        self.assertLessEqual(self.dashboard.sidebar.width(), 240)
        cards = [frame for frame in self.dashboard.findChildren(QFrame) if frame.objectName() == "card"]
        self.assertEqual(len(cards), 4)
        widths = [card.width() for card in cards]
        heights = [card.height() for card in cards]
        self.assertGreater(min(widths), 300)
        self.assertLess(max(widths) / min(widths), 1.40)
        self.assertGreater(min(heights), 180)
        self.assertLess(max(heights) / min(heights), 1.30)
        tiles = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "tileButton"
        ]
        self.assertEqual(len(tiles), 7)

    def test_responsive_sidebar_and_search_follow_window_width(self):
        self.dashboard.resize(1020, 700)
        self.app.processEvents()
        self.assertEqual(self.dashboard.sidebar.width(), 198)
        self.assertEqual(self.dashboard.search_entry.width(), 190)

        self.dashboard.resize(1500, 850)
        self.app.processEvents()
        self.assertEqual(self.dashboard.sidebar.width(), 258)
        self.assertEqual(self.dashboard.search_entry.width(), 320)

    def test_recovery_occurs_once_in_dashboard_controls(self):
        buttons = [button for button in self.dashboard.findChildren(QPushButton) if "Recovery" in button.text()]
        self.assertEqual(len(buttons), 1)
        self.assertIs(buttons[0], self.dashboard.recovery_nav_button)

    def test_sidebar_collapses_without_destroying_navigation(self):
        self.assertFalse(self.dashboard.nav_collapsed)
        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.assertTrue(self.dashboard.nav_collapsed)
        self.assertEqual(self.dashboard.sidebar.width(), 56)
        self.dashboard.toggle_sidebar()
        self.app.processEvents()
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 190)

    def test_productive_gui_sources_contain_no_tkinter(self):
        root = Path(__file__).resolve().parent.parent
        for relative in (
            "app/ui.py", "app/song_editor.py", "app/song_library.py",
            "app/recovery_center.py", "app/ui_standards.py", "scripts/start_status.py",
        ):
            self.assertNotIn("tkinter", (root / relative).read_text(encoding="utf-8").casefold(), relative)


if __name__ == "__main__":
    unittest.main()
