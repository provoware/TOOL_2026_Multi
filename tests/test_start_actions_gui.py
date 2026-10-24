"""PV-UX-01: echte Einstiegswege mit erhaltenen Arbeitsständen."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication, QMessageBox
from app.ui import Dashboard
from app.main import configure_dashboard_presentation
from app.text_editor_store import list_text_documents


class Texts:
    def get(self, _key, default=''):
        return default


class Logger:
    def recent(self, _limit=100):
        return []


class StartActionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.dashboard = configure_dashboard_presentation(Dashboard(Texts(), Logger(), self.root))
        self.dashboard.show()
        self.app.processEvents()

    def tearDown(self):
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            for editor in list(self.dashboard._song_editors):
                editor._closing_after_save = True
                editor.close()
            for registration in self.dashboard._managed_window_registry():
                registration.window.close()
            self.dashboard._closing_after_save = True
            self.dashboard.close()
        self.dashboard.deleteLater()
        self.app.processEvents()
        self.temp.cleanup()

    def click(self, key):
        self.dashboard.start_actions[key].click()
        self.app.processEvents()

    def test_four_unordered_actions_are_visible_and_accessible_at_high_zoom(self):
        labels = ['Song schreiben', 'Text schreiben', 'Aufgabe notieren', 'Termin eintragen']
        self.assertEqual([b.text() for b in self.dashboard.start_actions.values()], labels)
        for zoom in (100, 125, 150, 175, 200):
            self.dashboard.set_zoom(zoom)
            self.dashboard.resize(1334, 696)
            for _ in range(5):
                self.app.processEvents()
            buttons = list(self.dashboard.start_actions.values())
            self.assertLessEqual(self.dashboard.width(), 1334)
            self.assertLessEqual(self.dashboard.height(), 696)
            for button in buttons:
                self.assertTrue(button.isVisibleTo(self.dashboard))
                self.assertTrue(button.accessibleName())
                self.assertTrue(button.toolTip())
                bottom = button.mapTo(self.dashboard, button.rect().bottomRight())
                self.assertTrue(self.dashboard.rect().contains(bottom), (zoom, button.text()))
                self.assertFalse(button.text().startswith(('①', '②', '③', '④')))
                self.assertLessEqual(button.fontMetrics().horizontalAdvance(button.text()) + 20, button.width())
            for index, first in enumerate(buttons):
                for second in buttons[index + 1:]:
                    self.assertFalse(first.geometry().intersects(second.geometry()), (zoom, first.text(), second.text()))

    def test_first_text_can_be_created_saved_closed_and_found_again(self):
        self.click('text')
        editor = self.dashboard._text_editor_window
        self.assertTrue(editor.empty_hint.isVisible())
        self.assertIn('Jetzt speichern', editor.empty_hint.text())
        editor.title_entry.setText('Mein erster Text')
        editor.text_edit.setPlainText('Mein erster Inhalt.')
        editor.save_button.click()
        self.app.processEvents()
        path = editor.current_path
        self.assertIn(path, list_text_documents(self.root))
        self.assertFalse(editor.empty_hint.isVisible())
        self.assertEqual(editor.file_list.count(), 1)
        editor.close()
        self.click('text')
        reopened = self.dashboard._text_editor_window
        self.assertIsNot(reopened, editor)
        reopened.file_list.setCurrentRow(0)
        self.assertEqual(reopened.text_edit.toPlainText(), 'Mein erster Inhalt.')
        self.assertEqual(reopened.current_path, path)

    def test_visible_saved_text_with_unsaved_edits_is_never_reloaded(self):
        self.click('text')
        editor = self.dashboard._text_editor_window
        editor.title_entry.setText('Geschützter Text')
        editor.text_edit.setPlainText('Gespeicherter Stand')
        path = editor.save()
        before = path.read_bytes()
        editor.text_edit.setPlainText('Ungespeicherte Weiterarbeit')
        with patch.object(editor, 'refresh') as refresh, \
                patch.object(QMessageBox, 'question') as question:
            self.click('text')
        refresh.assert_not_called()
        question.assert_not_called()
        self.assertIs(self.dashboard._text_editor_window, editor)
        self.assertEqual(editor.text_edit.toPlainText(), 'Ungespeicherte Weiterarbeit')
        self.assertEqual(path.read_bytes(), before)

    def test_closed_discarded_text_is_not_revived(self):
        self.click('text')
        previous = self.dashboard._text_editor_window
        previous.text_edit.setPlainText('Bewusst verworfen')
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            previous.close()
        self.click('text')
        editor = self.dashboard._text_editor_window
        self.assertIsNot(editor, previous)
        self.assertEqual(editor.text_edit.toPlainText(), '')
        self.assertEqual(list_text_documents(self.root), [])

    def test_new_song_does_not_replace_existing_unsaved_song(self):
        self.click('song')
        first = self.dashboard._song_editors[-1]
        first.section_text.setPlainText('Ungespeicherte Strophe')
        self.click('song')
        second = self.dashboard._song_editors[-1]
        self.assertIsNot(first, second)
        self.assertIn(first, self.dashboard._song_editors)
        self.assertEqual(first.section_text.toPlainText(), 'Ungespeicherte Strophe')
        self.assertEqual(second.section_text.toPlainText(), '')

    def test_task_and_event_actions_preserve_unsubmitted_forms(self):
        self.click('todo')
        todo = self.dashboard._todo_window
        todo.title_entry.setText('Noch nicht angelegt')
        todo.note_entry.setPlainText('Entwurf behalten')
        self.click('todo')
        self.assertIs(self.dashboard._todo_window, todo)
        self.assertEqual(todo.title_entry.text(), 'Noch nicht angelegt')
        self.assertEqual(todo.note_entry.toPlainText(), 'Entwurf behalten')
        self.assertFalse((self.root / 'daten/todo/todo.json').exists())
        self.click('calendar')
        calendar = self.dashboard._calendar_window
        calendar.title_entry.setText('Termin im Entwurf')
        self.click('calendar')
        self.assertIs(self.dashboard._calendar_window, calendar)
        self.assertEqual(calendar.title_entry.text(), 'Termin im Entwurf')
        self.assertFalse((self.root / 'daten/kalender/termine.json').exists())

    def test_unreadable_text_list_does_not_claim_empty_or_erase_draft(self):
        self.click('text')
        editor = self.dashboard._text_editor_window
        editor.text_edit.setPlainText('Entwurf bleibt')
        with patch('app.text_editor_window.list_text_documents', side_effect=OSError('no access')):
            editor.refresh()
        self.assertFalse(editor.empty_hint.isVisible())
        self.assertIn('nicht lesbar', editor.status_label.text())
        self.assertEqual(editor.text_edit.toPlainText(), 'Entwurf bleibt')
