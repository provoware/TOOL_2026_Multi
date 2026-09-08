import tempfile
import time
import unittest
from pathlib import Path

from app.song_document import SongDocument, SongSection, list_versions, load_song, restore_version, save_song
from app.song_library import FILTER_ALL, SongRow, row_group, song_matches, sort_rows


class SongLibraryControlsTests(unittest.TestCase):
    def _row(self, title: str, *, genre: str = "", mood: str = "", style: str = "", voice: str = "",
             tags=None, status: str = "Idee", favorite: bool = False, modified: float = 0.0) -> SongRow:
        document = SongDocument(title=title, genre=genre, mood=mood, style=style, voice=voice,
                                tags=tags or [], status=status, favorite=favorite,
                                sections=[SongSection("Strophe", "Text")])
        return SongRow(Path(f"/{title}.txt"), document, modified, 0)

    def test_combined_search_and_filters_cover_requested_metadata(self):
        row = self._row("Nachtfahrt", genre="Trip-Hop", mood="Dunkel", style="Minimal",
                        voice="Rau", tags=["urban", "nacht"], status="Überarbeitung", favorite=True)
        self.assertTrue(song_matches(row, "nacht"))
        self.assertTrue(song_matches(row, "trip-hop", genre="Trip-Hop", mood="Dunkel", style="Minimal",
                                     voice="Rau", tag="urban", status="Überarbeitung", favorites_only=True))
        self.assertFalse(song_matches(row, "nacht", genre="Rock"))
        self.assertFalse(song_matches(row, "nacht", tag="sommer"))
        self.assertFalse(song_matches(row, "nacht", favorites_only=False, status="Fertig"))
        self.assertTrue(song_matches(row, "", genre=FILTER_ALL))

    def test_sorting_and_grouping(self):
        rows = [
            self._row("B", genre="Rock", tags=["z"], status="Fertig", modified=2),
            self._row("A", genre="Ambient", tags=["a"], status="Idee", modified=3),
        ]
        self.assertEqual([row.document.title for row in sort_rows(rows, "Zuletzt bearbeitet")], ["A", "B"])
        self.assertEqual([row.document.title for row in sort_rows(rows, "Genre")], ["A", "B"])
        self.assertEqual([row.document.title for row in sort_rows(rows, "Status")], ["A", "B"])
        self.assertEqual(row_group(rows[0], "Genre"), "Rock")
        self.assertEqual(row_group(rows[0], "Tags"), "z")
        self.assertEqual(row_group(rows[0], "Status"), "Fertig")

    def test_old_song_without_status_or_favorite_gets_safe_defaults(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "Alt.txt"
            path.write_text("TITEL: Alt\nGENRE: Rock\n\n[Strophe]\nText\n", encoding="utf-8")
            document = load_song(path)
            self.assertEqual(document.status, "Idee")
            self.assertFalse(document.favorite)

    def test_status_and_favorite_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = SongDocument(title="Status Song", status="Entwurf", favorite=True,
                                    sections=[SongSection("Strophe", "A")])
            path = save_song(root, document)
            loaded = load_song(path)
            self.assertEqual(loaded.status, "Entwurf")
            self.assertTrue(loaded.favorite)

    def test_restore_saves_current_state_first_and_restores_selected_version(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            document = SongDocument(title="Version Song", sections=[SongSection("Strophe", "eins")])
            path = save_song(root, document)
            document.sections[0].text = "zwei"
            save_song(root, document)
            versions_before = list_versions(root, document.title)
            self.assertEqual(len(versions_before), 1)
            selected = versions_before[0]
            restored, backup = restore_version(root, path, selected)
            self.assertEqual(restored, path.resolve())
            self.assertIsNotNone(backup)
            self.assertIn("eins", path.read_text(encoding="utf-8"))
            self.assertIn("zwei", backup.read_text(encoding="utf-8"))
            self.assertEqual(len(list_versions(root, document.title)), 2)

    def test_restore_rejects_foreign_version_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = save_song(root, SongDocument(title="Song", sections=[SongSection("Strophe", "aktuell")]))
            foreign = root / "fremd.txt"
            foreign.write_text("TITEL: Song\n\n[Strophe]\nalt\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                restore_version(root, path, foreign)
            self.assertIn("aktuell", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
