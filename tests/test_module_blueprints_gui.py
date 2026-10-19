"""Modulbaukasten in der PySide6-Oberfläche und Daten-Sicherheit."""
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
import tempfile
from pathlib import Path
import unittest
from PySide6.QtWidgets import QApplication
from app.module_blueprints_window import BlueprintWindow
from app import module_blueprints


class BlueprintGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_create_save_preview_and_zoom(self):
        with tempfile.TemporaryDirectory() as tmp:
            win = BlueprintWindow(Path(tmp))
            try:
                win.show()
                win.title.setText("Sammlung")
                win.description.setPlainText("Gedanken")
                win.field_text.setText("Titel, Quelle")
                win.checks["search"].setChecked(True)
                self.assertTrue(win.save())
                self.assertEqual(len(module_blueprints.load(Path(tmp))["blueprints"]), 1)
                win.preview()
                self.assertEqual(win.preview_layout.rowCount(), 2)
                win.set_zoom(150)
                self.assertEqual(win.zoom_percent, 150)
            finally:
                win.discard_draft()
                win.close()
                self.app.processEvents()
