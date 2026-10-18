import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.ui import Dashboard
from app.main import configure_dashboard_presentation
from app.event_log import EventLogger
from app.texts import TextRegistry

ROOT=Path(__file__).resolve().parent.parent


class ModuleMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])

    def test_modules_are_discoverable_managed_zoomed_and_drafts_guard_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);dashboard=Dashboard(TextRegistry(ROOT/'texte/registry.json'),EventLogger(root,'0.18.4'),root)
            try:
                configure_dashboard_presentation(dashboard)
                dashboard.show()
                actions=dashboard.module_menu.actions()
                self.assertTrue(any('Ideenarchiv' in a.text() for a in actions))
                self.assertTrue(any('Accountmanager' in a.text() for a in actions))
                for action in actions:action.trigger()
                for window in (dashboard._idea_window,dashboard._account_window):
                    self.assertIn(window,[r.window for r in dashboard._managed_window_registry()])
                    self.assertTrue(window.isWindow())
                dashboard.set_zoom(150)
                self.assertEqual(dashboard._idea_window.zoom_percent,150)
                self.assertEqual(dashboard._account_window.zoom_percent,150)
                self.assertTrue(dashboard._confirm_creative_modules())
            finally:
                for window in (dashboard._idea_window,dashboard._account_window):
                    if window:window.discard_draft();window.close()
                dashboard._closing_after_save=True;dashboard.close();self.app.processEvents()
