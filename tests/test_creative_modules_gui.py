"""Echte Qt-Abläufe mit isolierten Daten und gesteuerten Nutzerdialogen."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMessageBox
from app import snippet_store, book_store
from app.snippet_window import SnippetWindow
from app.book_window import BookWindow
from app.event_log import EventLogger
from app.texts import TextRegistry
from app.ui import Dashboard

ROOT = Path(__file__).resolve().parents[1]


class CreativeModulesGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            for window in list(self.app.topLevelWidgets()):
                window.close()
                window.deleteLater()
        self.app.processEvents()
        self.temp.cleanup()

    def make_snippet(self, window):
        window.title.setText('Hallo')
        window.category.setText('Begrüßung')
        window.content.setPlainText('Hallo {{Name}}!\n')
        self.assertTrue(window.save())

    def test_copy_placeholder_cancel_paste_and_monthly_counter(self):
        w = SnippetWindow(self.root)
        self.make_snippet(w)
        key = w.current_id
        self.app.clipboard().setText('Vorher')
        with patch('app.snippet_window.QInputDialog.getText', return_value=('', False)):
            w.copy(key)
        self.assertEqual('Vorher', self.app.clipboard().text())
        self.assertEqual({}, snippet_store.load(self.root)['snippets'][0]['monthly'])
        with patch('app.snippet_window.QInputDialog.getText', return_value=('Nora', True)):
            w.copy(key)
        self.assertEqual('Hallo Nora!\n', self.app.clipboard().text())
        self.assertEqual(1, sum(snippet_store.load(self.root)['snippets'][0]['monthly'].values()))
        w.title.clear()
        w.paste_field(w.title)
        self.assertIn('Hallo Nora!', w.title.text())

    def test_refresh_does_not_mark_unsaved_input_saved(self):
        w = SnippetWindow(self.root)
        w.title.setText('Ungespeichert')
        w.refresh()
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Cancel):
            self.assertFalse(w.confirm_leave())
        self.assertEqual('Ungespeichert', w.title.text())

    def test_variant_and_duplicate_prompt_keep_original(self):
        w = SnippetWindow(self.root)
        self.make_snippet(w)
        first = w.current_id
        w.edit(first, True)
        w.content.setPlainText('Andere Fassung')
        self.assertTrue(w.save())
        records = snippet_store.load(self.root)['snippets']
        self.assertEqual(2, records[1]['version'])
        self.assertEqual('Hallo {{Name}}!\n', records[0]['content'])
        w.new_snippet()
        w.title.setText('Gleich')
        w.category.setText('Begrüßung')
        w.content.setPlainText('Andere Fassung')
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            self.assertTrue(w.save())
        self.assertEqual(3, snippet_store.load(self.root)['snippets'][-1]['version'])

    def test_failed_copy_counter_tells_user_clipboard_was_updated(self):
        w = SnippetWindow(self.root)
        self.make_snippet(w)
        with patch('app.snippet_window.QInputDialog.getText', return_value=('Nora', True)), patch(
                'app.snippet_store.record_copy', side_effect=OSError('voll')):
            w.copy(w.current_id)
        self.assertEqual('Hallo Nora!\n', self.app.clipboard().text())
        self.assertIn('Statistik konnte nicht', w.status.text())

    def test_chapter_switching_and_safe_reopen_keep_text(self):
        w = BookWindow(self.root)
        w.title.setText('Hörbuch')
        first = w.current_chapter
        w.content.setPlainText('Kapitel Eins')
        w.add_chapter(True)
        child = w.current_chapter
        w.chapter_title.setText('Unterkapitel')
        w.content.setPlainText('Kapitel Zwei')
        self.assertTrue(w.save())
        w.open_book()
        saved = book_store.load(self.root)['books'][0]
        self.assertEqual('Kapitel Eins', next(c['content'] for c in saved['chapters'] if c['id'] == first))
        self.assertEqual(first, next(c['parent'] for c in saved['chapters'] if c['id'] == child))
        self.assertIn('Kapitel Zwei', book_store.manuscript(saved))

    def test_book_cancel_new_and_close_protect_draft(self):
        w = BookWindow(self.root)
        w.title.setText('Noch nicht gespeichert')
        key = w.book['id']
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Cancel):
            w.new_book()
            self.assertEqual(key, w.book['id'])
            self.assertFalse(w.close())
        self.assertFalse((self.root / 'daten').exists())

    def test_zoom_scroll_and_flexible_arrangement(self):
        for cls in (SnippetWindow, BookWindow):
            w = cls(self.root)
            w.show()
            for zoom in (100, 150, 200):
                w.resize(900, 650)
                w.set_zoom(zoom)
                self.app.processEvents()
                self.assertEqual(zoom, w.zoom_percent)
                self.assertTrue(w.isWindow())
                if cls is BookWindow:
                    self.assertEqual(Qt.Vertical if zoom >= 150 else Qt.Horizontal, w.splitter.orientation())
            w.close()

    def test_import_preview_cancel_and_approved_merge(self):
        from app import module_archive
        w = SnippetWindow(self.root)
        self.make_snippet(w)
        source = self.root / 'export.json'
        module_archive.export_archive(source, w.module, w.load_state(), w.validate, root=self.root)
        with patch('app.module_widgets.QFileDialog.getOpenFileName', return_value=(str(source), 'JSON')):
            with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
                w.import_data()
            self.assertEqual(1, len(w.load_state()['snippets']))
            with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
                w.import_data()
            self.assertEqual(2, len(w.load_state()['snippets']))

    def test_discarded_closed_book_is_not_saved_by_timer(self):
        w = BookWindow(self.root)
        w.title.setText('Verworfener Entwurf')
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(w.close())
        w._autosave()
        self.assertEqual([], book_store.load(self.root)['books'])
        self.assertEqual('', w.title.text())

    def test_header_actions_never_overlap_title_at_high_zoom(self):
        for cls in (SnippetWindow, BookWindow):
            w = cls(self.root, 200)
            w.resize(900, 650)
            w.show()
            self.app.processEvents()
            self.assertFalse(w.heading.geometry().intersects(w.header_actions.geometry()))
            self.assertLessEqual(w.header_actions.geometry().right(), w.width())
            w.close()

    def test_high_zoom_project_button_does_not_squeeze_profile_controls(self):
        from app.main import configure_dashboard_presentation
        from app.ui_standards import apply_global_style
        from PySide6.QtGui import QKeySequence, QShortcut
        dashboard = configure_dashboard_presentation(Dashboard(
            TextRegistry(ROOT / 'texte/registry.json'), EventLogger(self.root, 'test'), self.root))
        dashboard.set_zoom(200)
        apply_global_style(dashboard, 200, 'Kontrast')
        dashboard.resize(1334, 696)
        dashboard.show()
        for _ in range(8):
            self.app.processEvents()
        self.assertFalse(dashboard.github_project_open_button.isVisible())
        boxes = [dashboard.db_profile_combo, *dashboard.db_boxes.values()]
        for index, box in enumerate(boxes):
            rect = box.geometry()
            rect.moveTopLeft(box.mapTo(dashboard, box.rect().topLeft()))
            for other in boxes[index + 1:]:
                other_rect = other.geometry()
                other_rect.moveTopLeft(other.mapTo(dashboard, other.rect().topLeft()))
                overlap = rect.intersected(other_rect)
                self.assertFalse(overlap.width() > 2 and overlap.height() > 2)
        self.assertTrue(any(s.key() == QKeySequence('Ctrl+Shift+G') for s in dashboard.findChildren(QShortcut)))
        dashboard.set_zoom(100)
        self.assertTrue(dashboard.github_project_open_button.isVisible())

    def test_dashboard_registration_and_quit_guard(self):
        dashboard = Dashboard(TextRegistry(ROOT / 'texte/registry.json'), EventLogger(self.root, 'test'), self.root)
        dashboard.open_snippets()
        dashboard.open_books()
        windows = [r.window for r in dashboard._managed_window_registry()]
        self.assertIn(dashboard._book_window, windows)
        self.assertIn(dashboard._snippet_window, windows)
        dashboard._snippet_window.title.setText('Entwurf')
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Cancel):
            self.assertFalse(dashboard.close())
        self.assertFalse(dashboard._closing_after_save)
        dashboard.set_zoom(150)
        self.assertEqual(150, dashboard._book_window.zoom_percent)
        self.assertEqual(150, dashboard._snippet_window.zoom_percent)
