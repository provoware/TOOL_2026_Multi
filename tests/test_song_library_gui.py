import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from app.song_document import SongDocument, SongSection, save_song
from app.song_editor import SongEditor
from app.song_library import SongLibrary
from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=""):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    @staticmethod
    def human_report(event):
        return str(event)


class SongLibraryGuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp.name)
        self.root = tk.Tk()
        self.root.geometry("1180x780")
        self.dashboard = Dashboard(self.root, FakeTexts(), FakeLogger(), self.project_root)
        self.root.update_idletasks()
        self.root.update()

    def tearDown(self):
        try:
            exists = bool(self.root.winfo_exists())
        except tk.TclError:
            exists = False
        if exists:
            for child in list(self.root.winfo_children()):
                if isinstance(child, tk.Toplevel):
                    child.destroy()
            self.root.destroy()
        self.temp.cleanup()

    def test_recent_song_tiles_are_created_and_open_existing_song(self):
        path = save_song(self.project_root, SongDocument(
            title="Letzter Song", genre="Soul", mood="warm",
            sections=[SongSection("Strophe", "Text")],
        ))
        self.dashboard.refresh_recent_songs()
        buttons = [child for child in self.dashboard.recent_songs_frame.winfo_children() if child.winfo_class() == "TButton"]
        self.assertEqual(len(buttons), 1)
        self.assertIn("Letzter Song", str(buttons[0].cget("text")))
        self.dashboard.open_song_path(path)
        self.assertEqual(len(self.dashboard._song_editors), 1)
        editor = self.dashboard._song_editors[0]
        self.assertEqual(editor.title_var.get(), "Letzter Song")
        self.assertEqual(editor.mood_var.get(), "warm")
        editor.close()

    def test_library_lists_saved_song_and_has_keyboard_opening(self):
        save_song(self.project_root, SongDocument(title="Bibliothek Song", sections=[SongSection("Refrain", "Hook")]))
        opened = []
        library = SongLibrary(self.root, self.project_root, 100, lambda path: opened.append(path))
        self.root.update_idletasks()
        rows = library.table.get_children()
        self.assertEqual(len(rows), 1)
        self.assertTrue(library.table.bind("<Return>"))
        library.open_selected()
        self.assertEqual(len(opened), 1)
        library.window.destroy()

    def test_metadata_fields_and_export_menu_exist(self):
        editor = SongEditor(self.root, self.project_root)
        self.assertGreaterEqual(len(editor.meta_entries), 7)
        for entry in editor.meta_entries:
            self.assertTrue(entry.bind("<FocusOut>"))
        editor.mood_var.set("dunkel")
        editor.style_var.set("minimal")
        editor.voice_var.set("rau")
        editor.special_var.set("Pause vor Hook")
        editor.tags_var.set("nacht, bass")
        editor._update_preview()
        preview = editor.preview.get("1.0", "end")
        self.assertIn("STIMMUNG: dunkel", preview)
        self.assertIn("STIL: minimal", preview)
        self.assertIn("STIMME: rau", preview)
        self.assertIn("TAGS: nacht, bass", preview)
        self.assertIsNotNone(editor.export("json"))
        self.assertIsNotNone(editor.export("txt", lyrics_only=True))
        editor.close()


if __name__ == "__main__":
    unittest.main()
