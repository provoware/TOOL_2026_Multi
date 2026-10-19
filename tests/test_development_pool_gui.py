"""Projektpool-Fenster: CRUD, Filter, Archiv und Zoom."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.development_pool_window import DevelopmentPoolWindow
from app import development_pool


class PoolGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_save_filter_and_separate_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = DevelopmentPoolWindow(Path(tmp))
            try:
                window.show()
                window.name.setText("Neues Projekt")
                window.description.setPlainText("Gesammelte Texte")
                self.assertTrue(window.save())
                self.assertEqual(len(development_pool.load(Path(tmp))["projects"]), 1)
                window.filter.setCurrentText("fertig")
                self.assertEqual(window.listing.count(), 0)
                window.filter.setCurrentText("Alle")
                self.assertEqual(window.listing.count(), 1)
                window.copy_current()
                self.assertTrue((Path(tmp) / "daten/entwicklungspool/kopien").is_dir())
                window.set_zoom(150)
                self.assertEqual(window.zoom_percent, 150)
            finally:
                window.discard_draft()
                window.close()
                self.app.processEvents()
