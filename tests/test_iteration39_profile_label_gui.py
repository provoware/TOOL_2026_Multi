import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QPushButton

from app.main import configure_dashboard_presentation
from app.ui import Dashboard
from app.ui_standards import apply_global_style


class _Texts:
    def get(self, _key: str, default: str = "") -> str:
        return default


class _Logger:
    def recent(self, _limit: int = 100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


def _settle(cycles: int = 6) -> None:
    for _ in range(cycles):
        QApplication.processEvents()


class Iteration39ProfileLabelGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_profile_action_full_text_fits_at_normal_wide_zoom(self):
        cases = ((1920, 1080, 100, "Amber"), (1600, 900, 125, "Türkis"))
        for width, height, zoom, theme in cases:
            with self.subTest(width=width, height=height, zoom=zoom), tempfile.TemporaryDirectory() as tmp:
                dashboard = configure_dashboard_presentation(Dashboard(_Texts(), _Logger(), Path(tmp)))
                try:
                    dashboard.zoom_percent = zoom
                    dashboard.set_zoom(zoom)
                    apply_global_style(dashboard, zoom, theme)
                    dashboard.resize(width - 32, height - 72)
                    dashboard.show()
                    _settle()
                    buttons = [
                        button for button in dashboard.findChildren(QPushButton)
                        if button.accessibleName() == "Profile & Werte bearbeiten"
                    ]
                    self.assertEqual(len(buttons), 1)
                    button = buttons[0]
                    self.assertTrue(button.isVisibleTo(dashboard))
                    self.assertEqual(button.text(), "Profile & Werte bearbeiten")
                    self.assertLessEqual(
                        button.fontMetrics().horizontalAdvance(button.text()) + 20,
                        button.width(),
                    )
                finally:
                    dashboard._closing_after_save = True
                    dashboard.close()
                    _settle(2)


if __name__ == "__main__":
    unittest.main()
