"""Bildvorschau: Auslesen, Zoom, Listen- und Datei-Schutz."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication

from app.image_preview_window import ImagePreviewWindow, validate_images


class ImagePreviewGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_preview_image_scaled_and_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            picture = root / "image.png"
            image = QImage(4, 4, QImage.Format_RGB32)
            image.fill(0x004477)
            self.assertTrue(image.save(str(picture)))
            window = ImagePreviewWindow(root)
            try:
                window.show()
                window.paths = [str(picture)]
                self.assertTrue(window.save())
                window.render()
                self.assertIsNotNone(window.pixmap)
                self.assertEqual(window.listing.count(), 1)
                window.set_zoom(150)
                self.assertEqual(window.zoom_percent, 150)
                with self.assertRaises(ValueError):
                    validate_images({"schema_version": 1, "paths": [str(picture), str(picture)]})
            finally:
                window.close()
                self.app.processEvents()
