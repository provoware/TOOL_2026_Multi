"""Dateiliste schützt eine bereits aktive Signalsperre und die aktuelle Auswahl."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMessageBox
from app.text_editor_window import TextEditorWindow


class TextListSignalsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_refresh_keeps_preexisting_signal_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            try:
                window.file_list.blockSignals(True)
                window.refresh()
                self.assertTrue(window.file_list.signalsBlocked())
                window.file_list.blockSignals(False)
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()

    def test_cancel_keeps_current_document_and_signal_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            window = TextEditorWindow(Path(tmp))
            try:
                window.title_entry.setText("Noch nicht gespeichert")
                window.text_edit.setPlainText("Dieser Text bleibt.")
                from PySide6.QtWidgets import QListWidgetItem
                item = QListWidgetItem("Fremder Text")
                item.setData(256, str(Path(tmp) / "fremd.json"))
                window.file_list.addItem(item)
                window.file_list.blockSignals(True)
                with patch.object(QMessageBox, "exec", return_value=QMessageBox.Cancel):
                    window._load_selected(item, None)
                self.assertTrue(window.file_list.signalsBlocked())
                self.assertEqual(window.text_edit.toPlainText(), "Dieser Text bleibt.")
                window.file_list.blockSignals(False)
            finally:
                window._saved_snapshot = window._snapshot()
                window.close()


if __name__ == "__main__":
    unittest.main()
