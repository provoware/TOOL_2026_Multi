"""End-to-end Modulsteuerung im Dashboard ohne Datenverlust."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

from app import module_contracts
from app.ui import Dashboard
from app.event_log import EventLogger
from app.texts import TextRegistry

SOURCE = Path(__file__).resolve().parents[1]


class ModuleControlsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_disable_blocks_menu_and_shortcut_route_but_keeps_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dashboard = Dashboard(TextRegistry(SOURCE / "texte/registry.json"), EventLogger(root, "0.18.5"), root)
            try:
                dashboard.show()
                dashboard.open_module_controls()
                manager = dashboard._module_controls_window
                self.assertIsNotNone(manager)
                self.assertIn(manager, [entry.window for entry in dashboard._managed_window_registry()])
                dashboard.set_zoom(150)
                self.assertEqual(manager.zoom_percent, 150)
                manager.checks["wiki"].setChecked(False)
                self.assertTrue(manager.save())
                self.assertFalse(module_contracts.is_module_enabled(root, "wiki"))
                self.assertFalse(dashboard._optional_actions["wiki"].isEnabled())
                dashboard.open_wiki()
                self.assertIsNone(dashboard._wiki_window)
                manager.checks["wiki"].setChecked(True)
                self.assertTrue(manager.save())
                self.assertTrue(dashboard._optional_actions["wiki"].isEnabled())
                dashboard.open_wiki()
                self.assertIsNotNone(dashboard._wiki_window)
            finally:
                if dashboard._wiki_window is not None:
                    dashboard._wiki_window.discard_draft()
                    dashboard._wiki_window.close()
                if dashboard._module_controls_window is not None:
                    dashboard._module_controls_window.discard_draft()
                    dashboard._module_controls_window.close()
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()

    def test_refuse_to_disable_visible_module_window(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dashboard = Dashboard(TextRegistry(SOURCE / "texte/registry.json"), EventLogger(root, "0.18.5"), root)
            try:
                dashboard.open_ideas()
                dashboard.open_module_controls()
                manager = dashboard._module_controls_window
                manager.checks["ideas"].setChecked(False)
                with patch("app.module_controls_window.QMessageBox.warning"):
                    self.assertFalse(manager.save())
                self.assertTrue(module_contracts.is_module_enabled(root, "ideas"))
            finally:
                if dashboard._idea_window:
                    dashboard._idea_window.discard_draft()
                    dashboard._idea_window.close()
                if dashboard._module_controls_window:
                    dashboard._module_controls_window.discard_draft()
                    dashboard._module_controls_window.close()
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()
