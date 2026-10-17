"""Rückfalltests: ungespeicherte Textänderungen beim Wechsel bewahren."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication, QMessageBox
from app.text_editor_window import TextEditorWindow


class TextChangeProtectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_new_document_cancel_keeps_unsaved_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            window.title_entry.setText("Mein Entwurf")
            window.text_edit.setPlainText("Unersetzlicher Text")
            with patch.object(QMessageBox, "question", return_value=QMessageBox.Cancel):
                window.new_document()
            self.assertEqual(window.title_entry.text(), "Mein Entwurf")
            self.assertEqual(window.text_edit.toPlainText(), "Unersetzlicher Text")
            window._saved_snapshot = window._snapshot()
            window.close()

    def test_close_cancel_preserves_window_and_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            window.show()
            self.app.processEvents()
            window.title_entry.setText("Nicht gespeichert")
            window.text_edit.setPlainText("Bleibt erhalten")
            with patch.object(QMessageBox, "question", return_value=QMessageBox.Cancel):
                window.close()
            self.assertTrue(window.isVisible())
            self.assertEqual(window.text_edit.toPlainText(), "Bleibt erhalten")
            window._saved_snapshot = window._snapshot()
            window.close()


if __name__ == "__main__":
    unittest.main()
