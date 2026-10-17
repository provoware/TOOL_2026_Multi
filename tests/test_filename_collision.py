"""Rückfalltests: Titelnormalisierung darf fremde Dateien nicht überschreiben."""
import tempfile
import unittest
from pathlib import Path

from app.song_document import SongDocument, SongSection, save_song
from app.text_editor_store import TextDocument, save_text_document


class FilenameCollisionTests(unittest.TestCase):
    def test_song_normalized_name_collision_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = save_song(root, SongDocument(title="A/B", sections=[SongSection("Strophe", "Original")]))
            before = original.read_bytes()
            with self.assertRaises(FileExistsError):
                save_song(root, SongDocument(title="A\\B", sections=[SongSection("Strophe", "Andere Version")]))
            self.assertEqual(original.read_bytes(), before)

    def test_text_same_title_does_not_replace_unrelated_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = save_text_document(root, TextDocument(title="Gleicher Titel", text="Original"))
            before = original.read_bytes()
            with self.assertRaises(FileExistsError):
                save_text_document(root, TextDocument(title="Gleicher Titel", text="Fremd"))
            self.assertEqual(original.read_bytes(), before)

    def test_text_normalized_name_collision_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = save_text_document(root, TextDocument(title="A/B", text="Original"))
            before = original.read_bytes()
            with self.assertRaises(FileExistsError):
                save_text_document(root, TextDocument(title="A\\B", text="Fremd"))
            self.assertEqual(original.read_bytes(), before)

    def test_existing_text_can_be_edited_with_its_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            original = save_text_document(root, TextDocument(title="Wieder öffnen", text="Alt"))
            updated = save_text_document(root, TextDocument(title="Wieder öffnen", text="Neu"), previous_path=original)
            self.assertEqual(updated, original)
            self.assertTrue(original.is_file())


if __name__ == "__main__":
    unittest.main()
