"""Speicherzustände folgen echten Schreib-/Ladevorgängen und sichtbaren Entwürfen."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from app.book_window import BookWindow
from app.text_editor_window import TextEditorWindow
from app.song_editor import SongEditor
from app.song_document import load_song
from app.module_archive import state_path


class SaveStatesGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.windows = []

    def tearDown(self):
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.No):
            for w in self.windows:
                if isinstance(w, SongEditor):
                    w._closing_after_save = True
                w.close()
                w.deleteLater()
        self.app.processEvents()
        self.tmp.cleanup()

    def window(self, cls, zoom=100):
        w = cls(self.root, zoom_percent=zoom)
        self.windows.append(w)
        return w

    def state(self, w, expected):
        self.assertEqual(w.save_state.property('saveState'), expected, w.save_state.text())

    def test_text_edit_undo_autosave_failure_retry_and_reload(self):
        w = self.window(TextEditorWindow)
        self.state(w, 'untitled')
        w.text_edit.setPlainText('Ohne Titel')
        with patch('app.text_editor_window.save_text_document') as write:
            w._autosave()
            write.assert_not_called()
        w.title_entry.setText('Text')
        self.state(w, 'changed')
        w._autosave()
        path = w.current_path
        self.state(w, 'saved')
        original = path.read_bytes()
        w.text_edit.setPlainText('Änderung')
        self.state(w, 'changed')
        w.text_edit.setPlainText('Ohne Titel')
        self.state(w, 'saved')
        w.notes_edit.setPlainText('Notiz')
        with patch('app.text_editor_window.save_text_document', side_effect=OSError('voll')), \
                patch.object(QMessageBox, 'critical'):
            self.assertIsNone(w.save())
        self.state(w, 'failed')
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(w.notes_edit.toPlainText(), 'Notiz')
        self.assertIsNotNone(w.save())
        self.state(w, 'saved')
        self.assertIn(str(path), w.save_state.toolTip())
        w.new_document()
        self.state(w, 'untitled')
        w.file_list.setCurrentRow(0)
        self.state(w, 'saved')
        self.assertEqual(w.notes_edit.toPlainText(), 'Notiz')

    def test_song_edit_sections_failure_and_disk_proven_loaded_state(self):
        w = self.window(SongEditor)
        self.state(w, 'changed')
        self.assertIn('Unbenannter Song', w.save_state.text())
        w.title_entry.setText('Song')
        w.section_text.setPlainText('Zeile')
        path = w.save()
        self.state(w, 'saved')
        original = path.read_bytes()
        w.section_text.setPlainText('Zeile ')
        self.state(w, 'changed')
        w.section_text.setPlainText('Zeile')
        self.state(w, 'saved')
        w.other_text.setPlainText('Notiz')
        self.state(w, 'changed')
        with patch('app.song_editor.save_song', side_effect=OSError('voll')), \
                patch.object(QMessageBox, 'critical'):
            self.assertIsNone(w.save())
        self.state(w, 'failed')
        self.assertEqual(path.read_bytes(), original)
        w._autosave()
        self.state(w, 'saved')
        w.add_section()
        self.state(w, 'changed')
        other = SongEditor(self.root, document=load_song(path))
        self.windows.append(other)
        self.state(other, 'saved')

    def test_book_all_fields_structure_failure_new_open_and_copy(self):
        w = self.window(BookWindow)
        self.state(w, 'untitled')
        w.content.setPlainText('Kapitel')
        with patch('app.book_store.put') as write:
            w._autosave()
            write.assert_not_called()
        w.title.setText('Buch')
        w._autosave()
        self.state(w, 'saved')
        path = state_path(self.root, 'buecher')
        self.assertEqual(w.save_state.toolTip(), str(path))
        original = path.read_bytes()
        for field in (w.audience, w.chapter_title, w.content, w.chapter_notes, w.notes):
            old = field.text() if hasattr(field, 'text') else field.toPlainText()
            field.setText(old + ' Neu') if hasattr(field, 'setText') else field.setPlainText(old + ' Neu')
            self.state(w, 'changed')
            field.setText(old) if hasattr(field, 'setText') else field.setPlainText(old)
            self.state(w, 'saved')
        w.notes.setPlainText('Nicht verlieren')
        with patch('app.book_store.put', side_effect=OSError('voll')), \
                patch.object(QMessageBox, 'warning'):
            self.assertFalse(w.save())
        self.state(w, 'failed')
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(w.notes.toPlainText(), 'Nicht verlieren')
        self.assertTrue(w.save())
        self.state(w, 'saved')
        w.add_chapter(False)
        self.state(w, 'changed')
        w.save()
        w.new_book()
        self.state(w, 'untitled')
        w.open_book()
        self.state(w, 'saved')
        w.copy_book()
        self.state(w, 'changed')

    def test_save_state_remains_visible_at_supported_zoom_levels(self):
        for cls in (SongEditor, TextEditorWindow, BookWindow):
            for zoom in (100, 125, 150, 175, 200):
                with self.subTest(editor=cls.__name__, zoom=zoom):
                    w = self.window(cls, zoom)
                    w.resize(1280, 740)
                    w.show()
                    self.app.processEvents()
                    label = w.save_state
                    self.assertTrue(label.isVisible())
                    self.assertTrue(w.rect().contains(label.geometry()))
                    self.assertGreaterEqual(label.height(), label.heightForWidth(label.width()))
                    w.hide()
