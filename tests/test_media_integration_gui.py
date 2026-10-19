"""Medienmodule im Dashboard, Zoom und gespeicherte Modulschalter."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication

from app.ui import Dashboard
from app import module_contracts
from app.event_log import EventLogger
from app.texts import TextRegistry

SOURCE = Path(__file__).resolve().parents[1]


class MediaIntegrationGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_media_windows_registered_and_disable_prevents_launch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dashboard = Dashboard(TextRegistry(SOURCE / "texte/registry.json"),
                                  EventLogger(root, "0.18.5"), root)
            try:
                dashboard.show()
                for name in ("audio", "pictures", "slideshow"):
                    self.assertIn(name, dashboard._optional_actions)
                dashboard.open_audio_player()
                dashboard.open_picture_preview()
                dashboard.open_slideshow()
                self.assertIsNotNone(dashboard._audio_window)
                self.assertIsNotNone(dashboard._pictures_window)
                self.assertIsNotNone(dashboard._slideshow_window)
                dashboard.set_zoom(150)
                self.assertEqual(dashboard._audio_window.zoom_percent, 150)
                self.assertEqual(dashboard._pictures_window.zoom_percent, 150)
                self.assertEqual(dashboard._slideshow_window.zoom_percent, 150)
                for name, window in (("audio", dashboard._audio_window),
                                     ("pictures", dashboard._pictures_window),
                                     ("slideshow", dashboard._slideshow_window)):
                    self.assertIn(window, [entry.window for entry in dashboard._managed_window_registry()])
                dashboard._slideshow_window.close()
                dashboard._pictures_window.close()
                dashboard._audio_window.close()
                module_contracts.set_module_preferences(root, {"slideshow": False})
                dashboard._sync_optional_actions()
                self.assertFalse(dashboard._optional_actions["slideshow"].isEnabled())
                dashboard._slideshow_window = None
                dashboard.open_slideshow()
                self.assertIsNone(dashboard._slideshow_window)
            finally:
                for name in ("_audio_window", "_pictures_window", "_slideshow_window"):
                    window = getattr(dashboard, name)
                    if window is not None:
                        window.close()
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()
