"""Rückfallprüfungen für kurze, lesbare Navigation bei starkem Zoom."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from app.laptop_layout import install_laptop_layout
from app.navigation_ux import install_navigation_ux
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


class NavigationClippingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_navigation_fits_at_150_and_200_percent(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = Dashboard(FakeTexts(), FakeLogger(), Path(tmp))
            install_laptop_layout(window)
            controller = install_navigation_ux(window)
            try:
                for width, height, zoom in [(1600, 900, 150), (1366, 768, 200), (1920, 1080, 200)]:
                    with self.subTest(width=width, height=height, zoom=zoom):
                        window.resize(width, height)
                        window.set_zoom(zoom)
                        window.show()
                        for _ in range(10):
                            self.app.processEvents()
                        self.assertEqual(window.profile_nav_button.text(), "▦  Vorgaben")
                        self.assertEqual(window.profile_nav_button.accessibleName(), "Genres & Vorgaben")
                        self.assertGreaterEqual(
                            controller.menu_button.width(),
                            controller.menu_button.fontMetrics().horizontalAdvance("☰") + 20,
                        )
                        if window.planned_menu_toggle.isVisibleTo(window):
                            self.assertIn("Geplante (", window.planned_menu_toggle.text())
                            self.assertIn("Geplante Bereiche", window.planned_menu_toggle.accessibleName())
            finally:
                window._closing_after_save = True
                window.close()
                self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
