"""Regression: Profilwahl und Bearbeitungsaktion dürfen sich nicht überlagern."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import QPoint, QRect
from PySide6.QtWidgets import QApplication, QPushButton
from app.main import configure_dashboard_presentation
from app.ui import Dashboard


class _Texts:
    def get(self, _key, default=""):
        return default


class _Logger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class ProfileLayoutOverlapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_profile_controls_not_overlapping_at_1600x900(self):
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = configure_dashboard_presentation(Dashboard(_Texts(), _Logger(), Path(tmp)))
            try:
                dashboard.resize(1600, 900)
                dashboard.show()
                for _ in range(8):
                    self.app.processEvents()
                button = next(button for button in dashboard.findChildren(QPushButton)
                              if button.text() == "Profile & Werte bearbeiten")
                combo = dashboard.db_profile_combo
                self.assertTrue(combo.isVisibleTo(dashboard))
                self.assertTrue(button.isVisibleTo(dashboard))
                combo_rect = QRect(combo.mapTo(dashboard, QPoint(0, 0)), combo.size())
                button_rect = QRect(button.mapTo(dashboard, QPoint(0, 0)), button.size())
                self.assertFalse(combo_rect.intersects(button_rect),
                                 "Profilwahl und Bearbeiten-Schaltfläche überlappen")
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
