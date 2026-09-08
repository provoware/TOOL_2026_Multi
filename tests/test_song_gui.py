import os,tempfile,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.song_editor import AUTOSAVE_MS, SongEditor
from app.ui import Dashboard
class FakeTexts:
    def get(self,_key,default=""): return default
class FakeLogger:
    def recent(self,_limit=100): return []
    @staticmethod
    def human_report(event): return str(event)
class SongGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.app=QApplication.instance() or QApplication([])
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.project_root=Path(self.temp.name); self.dashboard=Dashboard(FakeTexts(),FakeLogger(),self.project_root); self.dashboard.show(); self.app.processEvents()
    def tearDown(self):
        for editor in list(self.dashboard._song_editors): editor._closing_after_save=True; editor.close()
        self.dashboard._closing_after_save=True; self.dashboard.close(); self.app.processEvents(); self.temp.cleanup()
    def test_header_quick_save_works_with_enter_path(self):
        self.dashboard.quick_entry.setText("wichtige Entwicklerinfo"); self.dashboard.save_quick_info(); target=self.project_root/"Entwicklerinformation.txt"; self.assertTrue(target.is_file()); self.assertIn("wichtige Entwicklerinfo",target.read_text(encoding="utf-8")); self.assertEqual(self.dashboard.quick_entry.text(),"")
    def test_song_editor_has_five_minute_autosave_and_preview(self):
        editor=SongEditor(self.project_root); self.assertEqual(AUTOSAVE_MS,300000); self.assertTrue(editor.autosave_timer.isActive()); self.assertEqual(editor.autosave_timer.interval(),300000); editor.title_entry.setText("Test Song"); editor.genre_entry.setText("Rock"); editor.section_text.setPlainText("Eine Zeile"); editor.other_text.setPlainText("Notiz"); editor._update_preview(); preview=editor.preview.toPlainText(); self.assertIn("Test Song",preview); self.assertIn("Rock",preview); self.assertIn("Eine Zeile",preview); self.assertIn("Notiz",preview); target=editor.save(); self.assertEqual(target.name,"Test Song.txt"); editor._closing_after_save=True; editor.close()
    def test_focusout_equivalent_and_close_safety_are_present(self):
        editor=SongEditor(self.project_root); self.assertTrue(hasattr(editor.title_entry,"editingFinished")); self.assertTrue(hasattr(editor.genre_entry,"editingFinished")); self.assertTrue(editor.section_text.isWidgetType()); self.assertTrue(editor.other_text.isWidgetType()); self.assertFalse(editor._closed); editor.close_safely(); self.assertTrue(editor._closed)
    def test_switching_sections_does_not_move_previous_text(self):
        editor=SongEditor(self.project_root); editor.section_text.setPlainText("Strophe eins"); editor._section_text_changed(); editor.section_type.setCurrentText("Refrain"); editor.add_section(); self.assertEqual(editor.document.sections[0].text,"Strophe eins"); self.assertEqual(editor.document.sections[1].kind,"Refrain"); self.assertEqual(editor.document.sections[1].text,""); editor._closing_after_save=True; editor.close()
if __name__=="__main__": unittest.main()
