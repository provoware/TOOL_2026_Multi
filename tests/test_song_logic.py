import tempfile
import unittest
from pathlib import Path

from app.quick_note import append_developer_info
from app.song_document import SongDocument, SongSection, safe_title, save_song


class SongLogicTests(unittest.TestCase):
    def test_quick_info_appends_timestamped_single_lines(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = append_developer_info(root, "erste\nInformation")
            append_developer_info(root, "zweite Information")
            lines = target.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertIn("erste Information", lines[0])
            self.assertIn("zweite Information", lines[1])
            self.assertTrue(lines[0].startswith("["))

    def test_quick_info_rejects_empty_input(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                append_developer_info(Path(temp), "   ")

    def test_song_is_saved_under_safe_title_and_contains_optional_fields(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = SongDocument(
                title="Mein / Song",
                genre="Trip-Hop",
                other="leise beginnen",
                sections=[SongSection("Intro", "Hallo"), SongSection("Strophe", "Zeile 1")],
            )
            target = save_song(root, document)
            self.assertEqual(target.name, "Mein - Song.txt")
            content = target.read_text(encoding="utf-8")
            self.assertIn("TITEL: Mein / Song", content)
            self.assertIn("GENRE: Trip-Hop", content)
            self.assertIn("[Intro]", content)
            self.assertIn("[Strophe]", content)
            self.assertIn("[Sonstiges]", content)
            self.assertFalse(target.with_suffix(".txt.tmp").exists())

    def test_title_never_escapes_song_directory(self):
        self.assertNotIn("/", safe_title("../../weg"))
        self.assertNotIn("\\", safe_title("..\\weg"))


if __name__ == "__main__":
    unittest.main()
