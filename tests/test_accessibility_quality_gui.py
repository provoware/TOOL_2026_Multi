"""Verbindliche Matrix- und Regressionsprüfungen ohne veränderte Bedienung."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QPushButton

from app.accessibility_contracts import (
    DIMENSIONS, MODULES, accessibility_matrix, contrast_ok,
    validate_accessibility_matrix,
)
from app.ui_quality_contracts import SUPPORTED_THEMES, SUPPORTED_ZOOMS
from app.ui import Dashboard
from app.text_editor_window import TextEditorWindow


class Texts:
    def get(self, _key, default=""):
        return default


class Logger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class AccessibilityQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_matrix_covers_all_core_modules(self):
        cases = accessibility_matrix()
        self.assertEqual(validate_accessibility_matrix(), ())
        self.assertEqual(len(cases), len(MODULES) * len(DIMENSIONS))
        self.assertGreaterEqual(len(MODULES), 8)
        self.assertIn(200, SUPPORTED_ZOOMS)
        self.assertIn("Kontrast", SUPPORTED_THEMES)
        self.assertTrue(all(not c.automatic for c in cases
                            if c.dimension == "bildschirmleser_praxis"))

    def test_contrast_threshold_is_explicit(self):
        self.assertTrue(contrast_ok("#000000", "#FFFFFF"))
        self.assertFalse(contrast_ok("#777777", "#888888"))
        self.assertTrue(contrast_ok("#777777", "#FFFFFF", large=True))

    def test_dashboard_buttons_have_names_and_keyboard_focus(self):
        with tempfile.TemporaryDirectory() as tmp:
            dashboard = Dashboard(Texts(), Logger(), Path(tmp))
            try:
                buttons = [b for b in dashboard.findChildren(QPushButton)
                           if b.isEnabled() and b.isVisibleTo(dashboard)]
                # Ungezeigte Fenster liefern hier ggf. null sichtbare Schalter;
                # deshalb vor der Prüfung wirklich anzeigen.
                dashboard.show()
                self.app.processEvents()
                buttons = [b for b in dashboard.findChildren(QPushButton)
                           if b.isEnabled() and b.isVisibleTo(dashboard)]
                self.assertTrue(buttons)
                self.assertTrue(all(b.accessibleName().strip() for b in buttons))
                self.assertTrue(all(b.focusPolicy() != Qt.NoFocus for b in buttons))
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                self.app.processEvents()

    def test_cancel_unsaved_document_does_not_discard_text(self):
        from PySide6.QtWidgets import QMessageBox
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            try:
                window.title_entry.setText("Entwurf")
                window.text_edit.setPlainText("Unersetzlicher Inhalt")
                with patch.object(QMessageBox, "question", return_value=QMessageBox.Cancel):
                    window.new_document()
                self.assertEqual(window.title_entry.text(), "Entwurf")
                self.assertEqual(window.text_edit.toPlainText(), "Unersetzlicher Inhalt")
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()


if __name__ == "__main__":
    unittest.main()
