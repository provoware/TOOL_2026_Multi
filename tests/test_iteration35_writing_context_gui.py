import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from app.character_store import upsert_character
from app.song_document import load_song, song_path
from app.song_editor import SongEditor
from app.text_editor_window import TextEditorWindow


class Iteration35WritingContextGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        for widget in list(self.app.topLevelWidgets()):
            widget.close()
            widget.deleteLater()
        self.app.processEvents()
        self.temp.cleanup()

    def test_text_and_song_editor_use_same_character_selection_contract(self):
        character = upsert_character(self.root, {"name": "Nora", "role": "Erzählerin"})
        character_id = str(character["id"])

        text_editor = TextEditorWindow(self.root, 100)
        song_editor = SongEditor(self.root, 100)

        text_index = text_editor.character_combo.findData(character_id)
        song_index = song_editor.character_combo.findData(character_id)
        self.assertGreaterEqual(text_index, 0)
        self.assertGreaterEqual(song_index, 0)
        self.assertEqual(text_editor.character_combo.itemText(text_index), "Nora — Erzählerin")
        self.assertEqual(song_editor.character_combo.itemText(song_index), "Nora — Erzählerin")

    def test_song_editor_inserts_character_marker_and_persists_without_schema_change(self):
        character = upsert_character(self.root, {"name": "Nora", "role": "Hauptfigur"})
        character_id = str(character["id"])
        window = SongEditor(self.root, 100)
        window.title_entry.setText("Charaktertest")
        index = window.character_combo.findData(character_id)
        self.assertGreaterEqual(index, 0)
        window.character_combo.setCurrentIndex(index)

        window.insert_character_reference()

        target = song_path(self.root, "Charaktertest")
        self.assertTrue(target.is_file())
        loaded = load_song(target)
        self.assertIn("[Charakter: Nora (Hauptfigur)]", loaded.sections[0].text)


if __name__ == "__main__":
    unittest.main()
