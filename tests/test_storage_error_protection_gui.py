"""Fehler bei Speichern und defekten Dateien dürfen keine Entwürfe verwerfen."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication, QMessageBox, QListWidgetItem
from PySide6.QtCore import Qt

from app.character_window import CharacterWindow
from app.calendar_window import CalendarWindow
from app.text_editor_window import TextEditorWindow


class StorageErrorProtectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_character_save_denied_keeps_unsaved_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = CharacterWindow(Path(tmp))
            try:
                window.name_entry.setText("Wichtige Figur")
                window.role_entry.setText("Erzähler")
                with (patch("app.character_window.upsert_character",
                            side_effect=PermissionError("Kein Schreibrecht")),
                      patch.object(QMessageBox, "warning") as warning):
                    window.save_character()
                self.assertEqual(window.name_entry.text(), "Wichtige Figur")
                self.assertEqual(window.role_entry.text(), "Erzähler")
                self.assertIsNone(window.current_id)
                self.assertIn("Datenbestand bleibt erhalten", warning.call_args.args[2])
            finally:
                window.close()

    def test_calendar_write_denied_keeps_event_title(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = CalendarWindow(Path(tmp))
            try:
                window.title_entry.setText("Wichtiger Termin")
                with (patch("app.calendar_window.add_event",
                            side_effect=PermissionError("Schreibgeschützt")),
                      patch.object(QMessageBox, "critical") as warning):
                    window.add_current_event()
                self.assertEqual(window.title_entry.text(), "Wichtiger Termin")
                self.assertIn("kein unvollständiger Termin", warning.call_args.args[2])
            finally:
                window.close()

    def test_corrupted_text_file_keeps_open_unsaved_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            try:
                window.title_entry.setText("Entwurf")
                window.text_edit.setPlainText("Inhalt bleibt erhalten")
                window._saved_snapshot = window._snapshot()
                item = QListWidgetItem("Beschädigt")
                item.setData(Qt.UserRole, str(Path(tmp) / "defekt.json"))
                with (patch("app.text_editor_window.load_text_document",
                            side_effect=ValueError("Ungültiger Dateiinhalt")),
                      patch.object(QMessageBox, "critical") as warning):
                    window._load_selected(item, None)
                self.assertEqual(window.title_entry.text(), "Entwurf")
                self.assertEqual(window.text_edit.toPlainText(), "Inhalt bleibt erhalten")
                self.assertIn("nichts verändert", warning.call_args.args[2])
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()


if __name__ == "__main__":
    unittest.main()
