"""End-to-end Tastaturaktionen mit sicheren lokalen Testprojekten."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton

from app.genre_random import history_load
from app.genre_random_window import GenreRandomWindow
from app.song_editor import SongEditor
from app.text_editor_window import TextEditorWindow


class KeyboardWorkflowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_generator_can_be_activated_with_space(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            window = GenreRandomWindow(root)
            try:
                window.show()
                self.app.processEvents()
                window.profile_combo.setCurrentText("HardTechno")
                window.generate_button.setFocus()
                self.app.processEvents()
                self.assertIs(self.app.focusWidget(), window.generate_button)
                QTest.keyClick(window.generate_button, Qt.Key_Space)
                self.app.processEvents()
                output = window.output.toPlainText()
                self.assertTrue(output)
                self.assertEqual(self.app.clipboard().text(), output)
                self.assertEqual(history_load(root)[0]["output"], output)
            finally:
                window.close()

    def test_cancel_new_document_from_keyboard_preserves_unsaved_text(self):
        with tempfile.TemporaryDirectory() as temp:
            window = TextEditorWindow(Path(temp))
            try:
                window.show()
                self.app.processEvents()
                window.title_entry.setText("Wichtiger Titel")
                window.text_edit.setPlainText("Ungesicherte Notiz")
                button = next(b for b in window.findChildren(QPushButton)
                              if b.text() == "Neuer Text")
                button.setFocus()
                self.app.processEvents()
                with patch.object(QMessageBox, "exec", return_value=QMessageBox.Cancel):
                    QTest.keyClick(button, Qt.Key_Space)
                    self.app.processEvents()
                self.assertEqual(window.title_entry.text(), "Wichtiger Titel")
                self.assertEqual(window.text_edit.toPlainText(), "Ungesicherte Notiz")
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()

    def test_song_editor_tab_and_backtab_retrace_same_field(self):
        with tempfile.TemporaryDirectory() as temp:
            window = SongEditor(Path(temp))
            try:
                window.show()
                self.app.processEvents()
                window.title_entry.setFocus()
                self.app.processEvents()
                self.assertIs(self.app.focusWidget(), window.title_entry)
                QTest.keyClick(window.title_entry, Qt.Key_Tab)
                self.app.processEvents()
                other = self.app.focusWidget()
                self.assertIsNotNone(other)
                self.assertIsNot(other, window.title_entry)
                QTest.keyClick(other, Qt.Key_Tab, Qt.ShiftModifier)
                self.app.processEvents()
                self.assertIs(self.app.focusWidget(), window.title_entry)
            finally:
                window._closing_after_save = True
                window.close()


if __name__ == "__main__":
    unittest.main()
