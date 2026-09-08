import tempfile
import tkinter as tk
import unittest
from pathlib import Path

from app.song_editor import AUTOSAVE_MS, SongEditor
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


class SongGuiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp.name)
        self.root = tk.Tk()
        self.root.geometry("1000x700")
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

    def test_header_quick_save_works_with_enter_path(self):
        self.dashboard.quick_info_var.set("wichtige Entwicklerinfo")
        self.assertEqual(self.dashboard._quick_save_enter(), "break")
        target = self.project_root / "Entwicklerinformation.txt"
        self.assertTrue(target.is_file())
        self.assertIn("wichtige Entwicklerinfo", target.read_text(encoding="utf-8"))
        self.assertEqual(self.dashboard.quick_info_var.get(), "")

    def test_song_editor_has_five_minute_autosave_and_preview(self):
        editor = SongEditor(self.root, self.project_root)
        self.assertEqual(AUTOSAVE_MS, 300000)
        self.assertIsNotNone(editor._autosave_job)
        editor.title_var.set("Test Song")
        editor.genre_var.set("Rock")
        editor.section_text.delete("1.0", "end")
        editor.section_text.insert("1.0", "Eine Zeile")
        editor._section_text_changed()
        editor.other_text.insert("1.0", "Notiz")
        editor._update_preview()
        preview = editor.preview.get("1.0", "end")
        self.assertIn("Test Song", preview)
        self.assertIn("Rock", preview)
        self.assertIn("Eine Zeile", preview)
        self.assertIn("Notiz", preview)
        target = editor.save()
        self.assertEqual(target.name, "Test Song.txt")
        self.assertTrue(target.is_file())
        editor.close()

    def test_focusout_bindings_and_logout_protocol_are_present(self):
        editor = SongEditor(self.root, self.project_root)
        self.assertTrue(editor.title_entry.bind("<FocusOut>"))
        self.assertTrue(editor.genre_entry.bind("<FocusOut>"))
        self.assertTrue(editor.section_text.bind("<FocusOut>"))
        self.assertTrue(editor.other_text.bind("<FocusOut>"))
        self.assertTrue(self.root.protocol("WM_DELETE_WINDOW"))
        editor.close()

    def test_switching_sections_does_not_move_previous_text(self):
        editor = SongEditor(self.root, self.project_root)
        editor.section_text.insert("1.0", "Strophe eins")
        editor._section_text_changed()
        editor.section_type_var.set("Refrain")
        editor.add_section()
        self.assertEqual(editor.document.sections[0].text, "Strophe eins")
        self.assertEqual(editor.document.sections[1].kind, "Refrain")
        self.assertEqual(editor.document.sections[1].text, "")
        editor.close()


if __name__ == "__main__":
    unittest.main()
