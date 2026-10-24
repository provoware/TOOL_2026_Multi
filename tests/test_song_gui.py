import os,tempfile,unittest
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
from pathlib import Path
from unittest.mock import Mock, patch
from PySide6.QtWidgets import QMessageBox
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
        self.dashboard.quick_entry.setText("wichtige Entwicklerinfo"); self.dashboard.save_quick_info(); target=self.project_root/"daten/notizen/projekt-notizen.txt"; self.assertTrue(target.is_file()); self.assertIn("wichtige Entwicklerinfo",target.read_text(encoding="utf-8")); self.assertEqual(self.dashboard.quick_entry.text(),"")
    def test_legacy_note_copy_requires_confirmation_and_preserves_original(self):
        legacy = self.project_root / 'Entwicklerinformation.txt'
        legacy.write_bytes(b'Alte Notiz\r\n')
        self.dashboard.quick_entry.setText('Neue Notiz')
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Cancel):
            self.dashboard.save_quick_info()
        self.assertEqual(self.dashboard.quick_entry.text(), 'Neue Notiz')
        self.assertFalse((self.project_root / 'daten/notizen').exists())
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Yes):
            self.dashboard.save_quick_info()
        copies = list((self.project_root / 'daten/notizen').glob('altbestand-*.txt'))
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_bytes(), legacy.read_bytes())
        self.assertEqual(legacy.read_bytes(), b'Alte Notiz\r\n')
        self.assertEqual(self.dashboard.quick_entry.text(), '')

    def test_declined_legacy_saves_new_notes_with_explicit_exclusion(self):
        legacy = self.project_root / 'Entwicklerinformation.txt'
        legacy.write_text('Alt')
        self.dashboard.quick_entry.setText('Neu')
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.No) as ask:
            self.dashboard.save_quick_info()
            self.dashboard.quick_entry.setText('Weitere Notiz')
            self.dashboard.save_quick_info()
            ask.assert_called_once()
        self.assertIn('noch nicht', self.dashboard.quick_status.text())
        self.assertEqual(legacy.read_text(), 'Alt')
        self.assertFalse(list((self.project_root / 'daten/notizen').glob('altbestand-*')))

    def test_failed_note_copy_keeps_current_input(self):
        (self.project_root / 'Entwicklerinformation.txt').write_text('Alt')
        self.dashboard.quick_entry.setText('Nicht verlieren')
        self.dashboard.logger.record = Mock(return_value={'event_id': 'TEST-NOTE-1'})
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Yes), \
                patch('app.ui.preserve_legacy_notes', side_effect=OSError('disk full')):
            self.dashboard.save_quick_info()
        self.assertEqual(self.dashboard.quick_entry.text(), 'Nicht verlieren')
        self.assertIn('nicht gespeichert', self.dashboard.quick_status.text())
        self.dashboard.logger.record.assert_called_once()
        self.assertEqual(self.dashboard.logger.record.call_args.kwargs['area'], 'PROJEKT_NOTIZ')

    def test_song_editor_has_five_minute_autosave_and_preview(self):
        editor=SongEditor(self.project_root); self.assertEqual(AUTOSAVE_MS,300000); self.assertTrue(editor.autosave_timer.isActive()); self.assertEqual(editor.autosave_timer.interval(),300000); editor.title_entry.setText("Test Song"); editor.genre_entry.setText("Rock"); editor.section_text.setPlainText("Eine Zeile"); editor.other_text.setPlainText("Notiz"); editor._update_preview(); preview=editor.preview.toPlainText(); self.assertIn("Test Song",preview); self.assertIn("Rock",preview); self.assertIn("Eine Zeile",preview); self.assertIn("Notiz",preview); target=editor.save(); self.assertEqual(target.name,"Test Song.txt"); editor._closing_after_save=True; editor.close()
    def test_focusout_equivalent_and_close_safety_are_present(self):
        editor=SongEditor(self.project_root); self.assertTrue(hasattr(editor.title_entry,"editingFinished")); self.assertTrue(hasattr(editor.genre_entry,"editingFinished")); self.assertTrue(editor.section_text.isWidgetType()); self.assertTrue(editor.other_text.isWidgetType()); self.assertFalse(editor._closed); editor.close_safely(); self.assertTrue(editor._closed)
    def test_switching_sections_does_not_move_previous_text(self):
        editor=SongEditor(self.project_root); editor.section_text.setPlainText("Strophe eins"); editor._section_text_changed(); editor.section_type.setCurrentText("Refrain"); editor.add_section(); self.assertEqual(editor.document.sections[0].text,"Strophe eins"); self.assertEqual(editor.document.sections[1].kind,"Refrain"); self.assertEqual(editor.document.sections[1].text,""); editor._closing_after_save=True; editor.close()
if __name__=="__main__": unittest.main()
