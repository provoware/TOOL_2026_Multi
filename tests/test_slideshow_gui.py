"""GUI: Diashow-Vorgaben, Dateiprüfung und Zoom."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.slideshow_window import SlideshowWindow


class SlideshowGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_preset_roundtrip_and_video_settings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            window = SlideshowWindow(root)
            try:
                window.show()
                window.seconds.setValue(7)
                self.assertTrue(window.save())
                self.assertEqual(window._preset()["seconds"], 7)
                window.seconds.setValue(4)
                window.refresh()
                self.assertEqual(window.seconds.value(), 7)
                window.set_zoom(150)
                self.assertEqual(window.zoom_percent, 150)
            finally:
                window.close()
                self.app.processEvents()

    def test_invalid_preset_refused(self):
        with self.assertRaises(ValueError):
            SlideshowWindow._validate_preset({
                "schema_version": 1, "images": [], "audio": "", "video": "",
                "mode": 0, "seconds": 1000})
