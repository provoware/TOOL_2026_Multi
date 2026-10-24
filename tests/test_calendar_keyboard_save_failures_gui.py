"""Barrierefreiheit und sichere Fehlerwege ohne Änderungen an der sichtbaren Bedienung."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QAbstractButton, QMessageBox

from app.calendar_window import CalendarWindow
from app.text_editor_window import TextEditorWindow


class CalendarAndSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_calendar_month_navigation_has_accessible_names(self):
        with tempfile.TemporaryDirectory() as temp:
            window = CalendarWindow(Path(temp))
            try:
                for object_name, expected in (
                    ("qt_calendar_prevmonth", "Vorherigen Monat anzeigen"),
                    ("qt_calendar_nextmonth", "Nächsten Monat anzeigen"),
                ):
                    button = window.calendar.findChild(QAbstractButton, object_name)
                    self.assertIsNotNone(button, object_name)
                    self.assertEqual(button.accessibleName(), expected)
                    self.assertTrue(button.focusPolicy() & Qt.TabFocus)
            finally:
                window.close()

    def test_tab_key_really_changes_focus_in_text_editor(self):
        with tempfile.TemporaryDirectory() as temp:
            window = TextEditorWindow(Path(temp))
            try:
                window.show()
                self.app.processEvents()
                window.title_entry.setFocus()
                self.app.processEvents()
                before = self.app.focusWidget()
                self.assertIs(before, window.title_entry)
                QTest.keyClick(window.title_entry, Qt.Key_Tab)
                self.app.processEvents()
                after = self.app.focusWidget()
                self.assertIsNotNone(after)
                self.assertIsNot(after, before)
                self.assertTrue(window.isAncestorOf(after))
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()

    def test_failed_save_during_document_switch_keeps_unsaved_text(self):
        with tempfile.TemporaryDirectory() as temp:
            window = TextEditorWindow(Path(temp))
            try:
                window.title_entry.setText("Wichtiger Entwurf")
                window.text_edit.setPlainText("Nicht verlieren!")
                with (
                    patch.object(QMessageBox, "exec", return_value=QMessageBox.Yes),
                    patch.object(QMessageBox, "critical") as error_box,
                    patch("app.text_editor_window.save_text_document", side_effect=OSError("Datenträger voll")),
                ):
                    window.new_document()
                self.assertEqual(window.title_entry.text(), "Wichtiger Entwurf")
                self.assertEqual(window.text_edit.toPlainText(), "Nicht verlieren!")
                self.assertEqual(error_box.call_count, 1)
                self.assertIn("bisherige gespeicherte Stand bleibt erhalten", error_box.call_args.args[2])
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()

    def test_failed_save_during_close_keeps_open_editor_and_text(self):
        with tempfile.TemporaryDirectory() as temp:
            window = TextEditorWindow(Path(temp))
            try:
                window.show()
                self.app.processEvents()
                window.title_entry.setText("Entwurf")
                window.text_edit.setPlainText("Noch nicht gesichert")
                with (
                    patch.object(QMessageBox, "exec", return_value=QMessageBox.Yes),
                    patch.object(QMessageBox, "critical"),
                    patch("app.text_editor_window.save_text_document", side_effect=OSError("Schreibgeschützt")),
                ):
                    window.close()
                self.assertTrue(window.isVisible())
                self.assertEqual(window.text_edit.toPlainText(), "Noch nicht gesichert")
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()


if __name__ == "__main__":
    unittest.main()
