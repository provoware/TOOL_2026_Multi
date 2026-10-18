"""Schützt Dashboard-Profilfelder vor dem GitHub-Zugang bei 200 % Zoom."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel

from app.main import configure_dashboard_presentation
from app.ui import Dashboard
from app.ui_standards import apply_global_style


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class GitHubLinkHighZoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_link_is_accessible_without_covering_profile_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            dashboard = configure_dashboard_presentation(
                Dashboard(FakeTexts(), FakeLogger(), Path(temp)))
            try:
                dashboard.set_zoom(200)
                apply_global_style(dashboard, 200, "Kontrast")
                dashboard.resize(1334, 696)
                dashboard.show()
                for _ in range(8):
                    self.app.processEvents()
                links = [x for x in dashboard.findChildren(QLabel)
                         if "github-projects" in x.text()]
                self.assertEqual(len(links), 1)
                link = links[0]
                self.assertTrue(link.isVisibleTo(dashboard))
                self.assertTrue(link.focusPolicy() & Qt.TabFocus)
                self.assertIn("GitHub-Projekte", link.accessibleName())
                link_rect = link.geometry()
                top_left = link.mapTo(dashboard, link.rect().topLeft())
                link_rect.moveTopLeft(top_left)
                for combo in [dashboard.db_profile_combo, *dashboard.db_boxes.values()]:
                    rect = combo.geometry()
                    rect.moveTopLeft(combo.mapTo(dashboard, combo.rect().topLeft()))
                    with self.subTest(field=combo.objectName() or combo.toolTip()):
                        self.assertFalse(link_rect.intersects(rect))
            finally:
                dashboard._closing_after_save = True
                dashboard.close()


if __name__ == "__main__":
    unittest.main()
