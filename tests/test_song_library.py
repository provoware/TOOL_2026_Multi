import json
import tempfile
import time
import unittest
from pathlib import Path

from app.song_document import (
    SongDocument, SongSection, export_song, list_songs, list_versions,
    load_song, parse_song, save_song,
)


class SongLibraryLogicTests(unittest.TestCase):
    def test_old_070_song_remains_readable(self):
        old = "TITEL: Alt\nGENRE: Rock\n\n[Strophe]\nZeile\n\n[Sonstiges]\nNotiz\n"
        document = parse_song(old)
        self.assertEqual(document.title, "Alt")
        self.assertEqual(document.genre, "Rock")
        self.assertEqual(document.sections[0].text, "Zeile")
        self.assertEqual(document.other, "Notiz")
        self.assertEqual(document.mood, "")

    def test_metadata_roundtrip(self):
        document = SongDocument(
            title="Metasong", genre="Trip-Hop", mood="dunkel", style="minimal",
            voice="rau", special="Break nach Hook", tags=["nacht", "bass"],
            sections=[SongSection("Intro", "Start"), SongSection("Refrain", "Hook")], other="Notiz",
        )
        loaded = parse_song(document.render())
        self.assertEqual(loaded.mood, "dunkel")
        self.assertEqual(loaded.style, "minimal")
        self.assertEqual(loaded.voice, "rau")
        self.assertEqual(loaded.special, "Break nach Hook")
        self.assertEqual(loaded.tags, ["nacht", "bass"])
        self.assertEqual([s.kind for s in loaded.sections], ["Intro", "Refrain"])

    def test_changed_save_creates_version_but_identical_save_does_not(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = SongDocument(title="Versionstest", sections=[SongSection("Strophe", "eins")])
            target = save_song(root, document)
            self.assertEqual(list_versions(root, document.title), [])
            save_song(root, document)
            self.assertEqual(list_versions(root, document.title), [])
            document.sections[0].text = "zwei"
            save_song(root, document)
            versions = list_versions(root, document.title)
            self.assertEqual(len(versions), 1)
            self.assertIn("eins", versions[0].read_text(encoding="utf-8"))
            self.assertIn("zwei", target.read_text(encoding="utf-8"))

    def test_recent_songs_are_sorted_by_modified_time(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = save_song(root, SongDocument(title="Erster", sections=[SongSection("Strophe", "1")]))
            time.sleep(0.02)
            second = save_song(root, SongDocument(title="Zweiter", sections=[SongSection("Strophe", "2")]))
            songs = list_songs(root)
            self.assertEqual(songs[:2], [second, first])

    def test_all_exports_are_separate_and_do_not_change_working_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = SongDocument(
                title="Export Song", genre="Rock", mood="hell", tags=["tag1"],
                sections=[SongSection("Strophe", "Text")],
            )
            working = save_song(root, document)
            original = working.read_text(encoding="utf-8")
            txt = export_song(root, document, "txt")
            md = export_song(root, document, "md")
            js = export_song(root, document, "json")
            lyrics = export_song(root, document, "txt", lyrics_only=True)
            self.assertTrue(all(path.is_file() for path in (txt, md, js, lyrics)))
            self.assertIn("# Export Song", md.read_text(encoding="utf-8"))
            payload = json.loads(js.read_text(encoding="utf-8"))
            self.assertEqual(payload["mood"], "hell")
            lyrics_text = lyrics.read_text(encoding="utf-8")
            self.assertNotIn("TITEL:", lyrics_text)
            self.assertNotIn("GENRE:", lyrics_text)
            self.assertIn("[Strophe]", lyrics_text)
            self.assertEqual(working.read_text(encoding="utf-8"), original)

    def test_load_song_uses_filename_as_fallback_title(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Ohne Kopf.txt"
            path.write_text("[Strophe]\nText\n", encoding="utf-8")
            self.assertEqual(load_song(path).title, "Ohne Kopf")


if __name__ == "__main__":
    unittest.main()
