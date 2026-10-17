"""Regression: Metadaten laden verändert weder Daten noch Qt-Signalsperren."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication
from app.song_document import SongDocument
from app.song_editor import SongEditor


class SongSignalGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_load_keeps_prior_signal_block_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            editor = SongEditor(Path(tmp))
            try:
                editor.document = SongDocument(
                    title="Testfigur", genre="Rock", mood="Dunkel",
                    style="Treibend", voice="Rau", special="Leise",
                    tags=["eins", "zwei"], status="Idee", favorite=True, other="Notiz",
                )
                editor.genre_entry.blockSignals(True)
                editor.status_song.blockSignals(True)
                changed = []
                editor.title_entry.textChanged.connect(changed.append)
                editor._load_document_into_widgets()
                self.assertTrue(editor.genre_entry.signalsBlocked())
                self.assertTrue(editor.status_song.signalsBlocked())
                self.assertFalse(editor.title_entry.signalsBlocked())
                self.assertFalse(editor.favorite_check.signalsBlocked())
                self.assertEqual(changed, [])
                self.assertEqual(editor.title_entry.text(), "Testfigur")
                self.assertEqual(editor.genre_entry.text(), "Rock")
                self.assertEqual(editor.other_text.toPlainText(), "Notiz")
                self.assertTrue(editor.favorite_check.isChecked())
                self.assertEqual(editor.tags_entry.text(), "eins, zwei")
            finally:
                editor._closing_after_save = True
                editor.close()


if __name__ == "__main__":
    unittest.main()
