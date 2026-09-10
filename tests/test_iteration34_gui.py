import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLineEdit, QTextEdit

from app.character_store import list_characters, upsert_character
from app.character_window import CharacterWindow
from app.profile_editor import ProfileEditor
from app.song_document import SongSection
from app.song_editor import SongEditor
from app.text_editor_store import list_text_documents, load_text_document
from app.text_editor_window import TextEditorWindow
from app.ui_standards import app_stylesheet, theme_colors


class Iteration34GuiTests(unittest.TestCase):
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

    def test_character_fibel_is_own_window_and_saves_detailed_record(self):
        window = CharacterWindow(self.root, 125)
        window.show()
        self.app.processEvents()
        self.assertTrue(window.windowFlags() & Qt.Window)
        window.name_entry.setText("Nora")
        window.role_entry.setText("Erzählerin")
        window.text_fields["personality"].setPlainText("direkt und aufmerksam")
        window.tags_entry.setText("hörspiel, hauptfigur")
        window.save_character()
        records = list_characters(self.root)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["name"], "Nora")
        self.assertEqual(records[0]["personality"], "direkt und aufmerksam")

    def test_text_editor_is_own_window_uses_title_filename_notes_and_character_database(self):
        character = upsert_character(self.root, {"name": "Nora", "role": "Erzählerin"})
        window = TextEditorWindow(self.root, 125)
        window.show()
        self.app.processEvents()
        self.assertTrue(window.windowFlags() & Qt.Window)
        index = window.character_combo.findData(str(character["id"]))
        self.assertGreaterEqual(index, 0)
        window.character_combo.setCurrentIndex(index)
        window.insert_character_reference()
        window.title_entry.setText("Kapitel Eins")
        window.text_edit.insertPlainText(" beginnt hier.")
        window.notes_edit.setPlainText("Finale prüfen")
        target = window.save()
        self.assertIsNotNone(target)
        self.assertEqual(target.name, "Kapitel Eins.json")
        loaded = load_text_document(target)
        self.assertIn(str(character["id"]), loaded.character_ids)
        self.assertEqual(loaded.notes, "Finale prüfen")
        self.assertEqual(len(list_text_documents(self.root)), 1)

    def test_profile_editor_accepts_comma_separated_values_in_one_action(self):
        window = ProfileEditor(self.root, 100)
        window.category_combo.setCurrentText("Stimmungen")
        window.value_entry.setText("bedrohlich, verspielt, melancholisch")
        window.create_value()
        shown = [window.values_list.item(i).text() for i in range(window.values_list.count())]
        self.assertIn("bedrohlich", shown)
        self.assertIn("verspielt", shown)
        self.assertIn("melancholisch", shown)

    def test_song_editor_accepts_custom_section_name(self):
        window = SongEditor(self.root, 100)
        self.assertTrue(window.section_type.isEditable())
        window.section_type.setEditText("Drop Finale")
        window.add_section()
        self.assertEqual(window.document.sections[-1], SongSection("Drop Finale", ""))

    def test_input_fields_use_central_contrast_background_with_readable_text(self):
        colors = theme_colors("Amber")
        css = app_stylesheet(100, "Amber")
        self.assertIn(colors["input_bg"], css)
        self.assertIn(colors["input_border"], css)
        sample = CharacterWindow(self.root, 100)
        line = sample.findChild(QLineEdit)
        text = sample.findChild(QTextEdit)
        self.assertIsNotNone(line)
        self.assertIsNotNone(text)


if __name__ == "__main__":
    unittest.main()
