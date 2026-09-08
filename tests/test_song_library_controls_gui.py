import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from app.song_document import SongDocument, SongSection, save_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary


class SongLibraryControlsGuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root_path = Path(self.temp.name)
        save_song(self.root_path, SongDocument(
            title="Favorit Song", genre="Rock", mood="Wild", style="Rau", voice="Tief",
            tags=["live", "laut"], status="Entwurf", favorite=True,
            sections=[SongSection("Strophe", "eins")],
        ))
        save_song(self.root_path, SongDocument(
            title="Ruhiger Song", genre="Ambient", mood="Ruhig", style="Minimal", voice="Leise",
            tags=["nacht"], status="Fertig", favorite=False,
            sections=[SongSection("Strophe", "zwei")],
        ))
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.opened = []

    def tearDown(self):
        try:
            exists = bool(self.root.winfo_exists())
        except tk.TclError:
            exists = False
        if exists:
            for child in list(self.root.winfo_children()):
                try:
                    child.destroy()
                except tk.TclError:
                    pass
            self.root.destroy()
        self.temp.cleanup()

    def test_library_combined_filter_and_favorite_view(self):
        library = SongLibrary(self.root, self.root_path, 100, self.opened.append)
        self.root.update_idletasks()
        self.assertEqual(len(library._paths), 2)
        library.genre_var.set("Rock")
        library.favorite_only_var.set(True)
        library.apply_view()
        self.assertEqual(len(library._paths), 1)
        selected = next(iter(library._paths.values()))
        self.assertEqual(selected.name, "Favorit Song.txt")

    def test_search_sort_and_group_controls_change_view_without_files(self):
        library = SongLibrary(self.root, self.root_path, 100, self.opened.append)
        before = sorted(path.read_text(encoding="utf-8") for path in (self.root_path / "daten" / "songtexte").glob("*.txt"))
        library.search_var.set("nacht")
        library.sort_var.set("Status")
        library.group_var.set("Genre")
        library.apply_view()
        self.assertEqual(len(library._paths), 1)
        parents = library.table.get_children()
        self.assertEqual(len(parents), 1)
        self.assertEqual(library.table.item(parents[0], "text"), "Ambient")
        after = sorted(path.read_text(encoding="utf-8") for path in (self.root_path / "daten" / "songtexte").glob("*.txt"))
        self.assertEqual(before, after)

    def test_editor_exposes_status_and_favorite_and_saves_them(self):
        editor = SongEditor(self.root, self.root_path, document=SongDocument(
            title="Editor Song", sections=[SongSection("Strophe", "Text")]))
        editor.status_song_var.set("Überarbeitung")
        editor.favorite_var.set(True)
        path = editor.save()
        self.assertIsNotNone(path)
        content = path.read_text(encoding="utf-8")
        self.assertIn("STATUS: Überarbeitung", content)
        self.assertIn("FAVORIT: Ja", content)
        self.assertTrue(editor.status_song.cget("takefocus"))
        self.assertTrue(editor.favorite_check.cget("takefocus"))
        editor.close()

    def test_versions_window_has_explicit_restore_button_after_preview(self):
        path = self.root_path / "daten" / "songtexte" / "Favorit Song.txt"
        document = SongDocument(title="Favorit Song", genre="Rock", status="Entwurf", favorite=True,
                                sections=[SongSection("Strophe", "geändert")])
        save_song(self.root_path, document)
        library = SongLibrary(self.root, self.root_path, 100, self.opened.append)
        item = next(item for item, selected in library._paths.items() if selected == path)
        library.table.selection_set(item)
        library.table.focus(item)
        library.show_versions()
        self.root.update_idletasks()
        self.assertEqual(str(library.restore_button.cget("state")), "normal")
        self.assertIn("Diese Version wiederherstellen", str(library.restore_button.cget("text")))


if __name__ == "__main__":
    unittest.main()
