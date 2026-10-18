"""Prüft Signalsperren in Charakterfibel und Songbereichsliste."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication
from app.character_window import CharacterWindow
from app.song_editor import SongEditor
from app.song_document import SongSection


class ListSignalStateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_character_list_keeps_signal_block_and_selected_character(self):
        with tempfile.TemporaryDirectory() as tmp:
            widget = CharacterWindow(Path(tmp))
            try:
                widget.character_list.blockSignals(True)
                widget.refresh()
                self.assertTrue(widget.character_list.signalsBlocked())
            finally:
                widget.character_list.blockSignals(False)
                widget.close()

    def test_song_section_list_preserves_existing_signal_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp))
            try:
                editor.document.sections = [SongSection("Strophe", "Text")]
                editor.section_list.blockSignals(True)
                editor._refresh_section_list()
                self.assertTrue(editor.section_list.signalsBlocked())
                editor._load_section(0)
                self.assertTrue(editor.section_list.signalsBlocked())
                self.assertEqual(editor.section_text.toPlainText(), "Text")
            finally:
                editor.section_list.blockSignals(False)
                editor._closing_after_save = True
                editor.close()


if __name__ == "__main__":
    unittest.main()
