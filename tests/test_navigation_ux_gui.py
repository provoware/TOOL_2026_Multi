import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QPushButton

from app.laptop_layout import install_laptop_layout
from app.navigation_ux import PLANNED_COUNT, install_navigation_ux
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


class NavigationUxGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.dashboard = Dashboard(FakeTexts(), FakeLogger(), Path(self.temp.name))
        install_laptop_layout(self.dashboard)
        install_navigation_ux(self.dashboard)
        self.dashboard.resize(1594, 926)
        self.dashboard.show()
        self._events()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self._events()
        self.temp.cleanup()

    def _events(self):
        self.app.processEvents()
        self.app.processEvents()

    def test_ready_routes_are_prioritized_and_planning_is_collapsed(self):
        self.assertEqual(self.dashboard.nav_title.text(), "Menü")
        self.assertTrue(self.dashboard.song_nav_button.isVisible())
        self.assertTrue(self.dashboard.profile_nav_button.isVisible())
        self.assertTrue(self.dashboard.todo_nav_button.isVisible())
        self.assertTrue(self.dashboard.calendar_nav_button.isVisible())
        self.assertTrue(self.dashboard.recovery_nav_button.isVisible())
        self.assertEqual(self.dashboard.profile_nav_button.text(), "▦  Genres & Vorgaben")

        planned = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "navButton" and button.property("planned") is True
        ]
        self.assertEqual(len(planned), PLANNED_COUNT)
        self.assertFalse(self.dashboard.planned_menu_container.isVisible())
        self.assertTrue(self.dashboard.planned_menu_toggle.isVisible())
        self.assertIn(str(PLANNED_COUNT), self.dashboard.planned_menu_toggle.text())
        self.assertTrue(all(not button.isVisible() for button in planned))

    def test_planned_group_expands_once_without_repeating_planned_suffixes(self):
        self.dashboard.planned_menu_toggle.click()
        self._events()

        self.assertTrue(self.dashboard.planned_menu_expanded)
        self.assertTrue(self.dashboard.planned_menu_container.isVisible())
        self.assertIn("ausblenden", self.dashboard.planned_menu_toggle.text())
        planned = [
            button for button in self.dashboard.findChildren(QPushButton)
            if button.objectName() == "navButton" and button.property("planned") is True
        ]
        self.assertEqual(len(planned), PLANNED_COUNT)
        self.assertTrue(all(button.isVisible() for button in planned))
        self.assertTrue(all("geplant" not in button.text().casefold() for button in planned))

        self.dashboard.planned_menu_toggle.click()
        self._events()
        self.assertFalse(self.dashboard.planned_menu_container.isVisible())
        self.assertTrue(all(not button.isVisible() for button in planned))

    def test_laptop_and_high_zoom_hide_optional_planning_but_keep_ready_routes(self):
        self.dashboard.planned_menu_toggle.click()
        self._events()
        self.assertTrue(self.dashboard.planned_menu_container.isVisible())

        self.dashboard.resize(1366, 768)
        self.dashboard.set_zoom(125)
        self._events()
        self.assertTrue(self.dashboard.property("provowareLaptopCompact"))
        self.assertTrue(self.dashboard.planned_menu_expanded)
        self.assertFalse(self.dashboard.planned_menu_toggle.isVisible())
        self.assertFalse(self.dashboard.planned_menu_container.isVisible())
        self.assertTrue(self.dashboard.song_nav_button.isVisible())
        self.assertTrue(self.dashboard.todo_nav_button.isVisible())
        self.assertTrue(self.dashboard.recovery_nav_button.isVisible())

        self.dashboard.resize(1594, 926)
        self._events()
        self.assertFalse(self.dashboard.property("provowareLaptopCompact"))
        self.assertTrue(self.dashboard.planned_menu_toggle.isVisible())
        self.assertTrue(self.dashboard.planned_menu_container.isVisible())

        self.dashboard.set_zoom(200)
        self._events()
        self.assertFalse(self.dashboard.planned_menu_toggle.isVisible())
        self.assertFalse(self.dashboard.planned_menu_container.isVisible())
        self.assertTrue(self.dashboard.song_nav_button.isVisible())

        self.dashboard.set_zoom(100)
        self._events()
        self.assertTrue(self.dashboard.planned_menu_toggle.isVisible())
        self.assertTrue(self.dashboard.planned_menu_container.isVisible())

    def test_transition_from_laptop_compact_to_200_percent_does_not_revive_legacy_labels(self):
        self.dashboard.resize(1366, 768)
        self.dashboard.set_zoom(150)
        self._events()
        self.assertTrue(self.dashboard.property("provowareLaptopCompact"))

        self.dashboard.set_zoom(200)
        self._events()
        legacy = [
            label for label in self.dashboard.findChildren(QLabel)
            if label.text() in {"⌄  Funktionen", "⌄  Dateien & Werkzeuge"}
        ]
        self.assertTrue(legacy)
        self.assertTrue(all(not label.isVisible() for label in legacy))
        self.assertEqual(self.dashboard.profile_nav_button.text(), "▦  Vorgaben")
        self.assertEqual(self.dashboard.profile_nav_button.accessibleName(), "Genres & Vorgaben")
        self.assertEqual(self.dashboard.recovery_nav_button.text(), "⚕  Fehlerhilfe")
        self.assertIn("Recovery", self.dashboard.recovery_nav_button.accessibleName())

        self.dashboard.set_zoom(100)
        self._events()
        self.assertEqual(self.dashboard.profile_nav_button.text(), "▦  Genres & Vorgaben")
        self.assertEqual(self.dashboard.recovery_nav_button.text(), "⚕  Fehlerhilfe (Recovery)")

    def test_sidebar_collapse_keeps_clear_reversible_state_and_accessibility(self):
        self.assertEqual(self.dashboard.planned_menu_toggle.focusPolicy(), Qt.StrongFocus)
        self.assertIn("anzeigen oder ausblenden", self.dashboard.planned_menu_toggle.accessibleName())

        self.dashboard.toggle_sidebar()
        self._events()
        self.assertTrue(self.dashboard.nav_collapsed)
        self.assertEqual(self.dashboard.sidebar.width(), 56)
        self.assertFalse(self.dashboard.song_nav_button.isVisible())
        self.assertFalse(self.dashboard.planned_menu_toggle.isVisible())

        self.dashboard.toggle_sidebar()
        self._events()
        self.assertFalse(self.dashboard.nav_collapsed)
        self.assertGreaterEqual(self.dashboard.sidebar.width(), 190)
        self.assertTrue(self.dashboard.song_nav_button.isVisible())
        self.assertTrue(self.dashboard.planned_menu_toggle.isVisible())
        self.assertFalse(self.dashboard.planned_menu_container.isVisible())


if __name__ == "__main__":
    unittest.main()
