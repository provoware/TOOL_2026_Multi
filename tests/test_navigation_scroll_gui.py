"""Rückfalltest: feste Menüüberschrift und scrollbar vollständige Navigation."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QPoint, Qt
from PySide6.QtWidgets import QApplication, QScrollArea
from app.main import configure_dashboard_presentation
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


class DashboardScrollNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.root = tempfile.TemporaryDirectory()
        self.window = Dashboard(FakeTexts(), FakeLogger(), Path(self.root.name))
        configure_dashboard_presentation(self.window)
        self.window.resize(1600, 700)
        self.window.show()
        self._events()
        self.controller = self.window._provoware_navigation_ux
        self.scroll = self.controller.navigation_scroll

    def tearDown(self):
        self.window._closing_after_save = True
        self.window.close()
        self._events()
        self.root.cleanup()

    def _events(self):
        for _ in range(5):
            self.app.processEvents()

    def test_scroll_area_keeps_menu_header_fixed(self):
        self.assertIsInstance(self.scroll, QScrollArea)
        self.assertTrue(self.scroll.widgetResizable())
        self.assertEqual(self.scroll.horizontalScrollBarPolicy(), Qt.ScrollBarAlwaysOff)
        self.assertEqual(self.scroll.parent(), self.window.sidebar)
        self.assertTrue(self.controller.menu_button.isVisibleTo(self.window))
        self.assertTrue(self.controller.menu_title.isVisibleTo(self.window))
        self.assertEqual(self.scroll.objectName(), "dashboardNavigationScroll")

    def test_expanded_bottom_actions_remain_scroll_reachable(self):
        self.window.planned_menu_toggle.click()
        self._events()
        self.assertTrue(self.window.planned_menu_expanded)
        self.assertGreater(self.scroll.verticalScrollBar().maximum(), 0)
        last = self.controller.planned_buttons[-1]
        self.assertTrue(last.isVisible())
        self.scroll.ensureWidgetVisible(last, 0, 0)
        self._events()
        point = last.mapTo(self.scroll.viewport(), QPoint(0, 0))
        self.assertGreaterEqual(point.y(), -2)
        self.assertLessEqual(point.y() + last.height(), self.scroll.viewport().height() + 2)
        self.assertTrue(self.controller.menu_button.isVisibleTo(self.window))

    def test_collapse_and_reopen_preserve_navigation(self):
        self.window.toggle_sidebar()
        self._events()
        self.assertTrue(self.window.nav_collapsed)
        self.assertFalse(self.scroll.isVisible())
        self.assertTrue(self.controller.menu_button.isVisible())
        self.window.toggle_sidebar()
        self._events()
        self.assertFalse(self.window.nav_collapsed)
        self.assertTrue(self.scroll.isVisible())
        self.assertTrue(self.window.recovery_nav_button.isVisible())
        self.scroll.ensureWidgetVisible(self.window.recovery_nav_button)
        self._events()

    def test_high_zoom_core_routes_can_be_scrolled_into_view(self):
        self.window.resize(1366, 768)
        self.window.set_zoom(200)
        self._events()
        bottom = self.window.recovery_nav_button
        self.assertTrue(bottom.isVisible())
        self.scroll.ensureWidgetVisible(bottom, 0, 0)
        self._events()
        top = bottom.mapTo(self.scroll.viewport(), QPoint(0, 0)).y()
        self.assertGreaterEqual(top, -2)
        self.assertLessEqual(top + bottom.height(), self.scroll.viewport().height() + 2)


if __name__ == "__main__":
    unittest.main()
