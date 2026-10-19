"""GUI: Diashow-Vorgaben, Dateiprüfung und Zoom."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.slideshow_window import SlideshowWindow
from app import media_queue


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

    def test_queue_visible_and_fade_control_persisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "photo.png"
            image.write_bytes(b"image bytes")
            win = SlideshowWindow(root)
            try:
                win.fade.setValue(45)
                win.images = [str(image)]
                win.output.setText(str(root / "result.mp4"))
                win.enqueue_current()
                self.assertEqual(win.queue_list.count(), 1)
                self.assertEqual(media_queue.load(root)["jobs"][0]["fade"], 45)
                self.assertEqual(media_queue.load(root)["jobs"][0]["status"], "waiting")
            finally:
                win.close()
                self.app.processEvents()

    def test_invalid_preset_refused(self):
        with self.assertRaises(ValueError):
            SlideshowWindow._validate_preset({
                "schema_version": 1, "images": [], "audio": "", "video": "",
                "mode": 0, "seconds": 1000})
