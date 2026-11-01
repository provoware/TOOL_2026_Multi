"""Bewusste Umbenennung, Entwurfserhalt, Ereignisse und erreichbare Aktionen."""
import json
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QCoreApplication, QEvent, QPoint, QRect, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from app.event_log import EventLogger
from app.profile_rename_dialog import ProfileRenameDialog
from app.profile_store import CATEGORIES, save_profiles, profile_names
from app.ui import Dashboard
from app.ui_standards import apply_global_style, DEFAULT_THEME, THEMES


class FakeTexts:
    def get(self, key, default=''):
        return default


class ProfileRenameGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.app.setProperty('provowareTheme', DEFAULT_THEME)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {'Test': {'Genres': ['Wert']}, 'Anderes': {}})
        self.before = self.path.read_bytes()
        self.logger = EventLogger(self.root, 'test')
        self.dialog = ProfileRenameDialog(self.root, 'Test', logger=self.logger)
        self.dialog.show()
        self.events()

    def events(self):
        for _ in range(3):
            self.app.processEvents()

    def tearDown(self):
        self.dialog.reject()
        self.dialog.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        self.events()
        self.tmp.cleanup()

    def test_enter_only_checks_explicit_click_commits_and_edits_invalidate(self):
        d = self.dialog
        d.name_entry.setText('Neu')
        d.name_entry.setFocus()
        QTest.keyClick(d.name_entry, Qt.Key_Return)
        self.assertTrue(d.rename_button.isEnabled())
        self.assertEqual(self.path.read_bytes(), self.before)
        d.name_entry.setText('Neuer')
        self.assertFalse(d.rename_button.isEnabled())
        self.assertFalse(d.apply())
        QTest.mouseClick(d.check_button, Qt.LeftButton)
        QTest.mouseClick(d.rename_button, Qt.LeftButton)
        self.assertEqual(d.renamed_to, 'Neuer')
        self.assertIn('Neuer', profile_names(self.root))

    def test_blocked_reference_and_stale_snapshot_keep_name_and_bytes(self):
        d = self.dialog
        path = self.root / 'daten/profile/genre_favoriten.json'
        path.write_text(json.dumps({'schema': 1, 'favorites': {'Neu': {cat: [] for cat in CATEGORIES}}}))
        d.name_entry.setText('Neu')
        self.assertFalse(d.check())
        self.assertFalse(d.rename_button.isEnabled())
        self.assertIn('gesperrt', d.preview.toPlainText())
        self.assertFalse(d.apply())
        path.unlink()
        self.assertTrue(d.check())
        self.path.write_bytes(self.before + b' ')
        self.assertFalse(d.apply())
        self.assertEqual(d.name_entry.text(), 'Neu')
        self.assertFalse(d.rename_button.isEnabled())
        self.assertEqual(self.path.read_bytes(), self.before + b' ')
        self.assertFalse(self.logger.jsonl_path.exists())

    def test_storage_failure_real_event_retained_after_edit(self):
        d = self.dialog
        d.name_entry.setText('PrivaterEntwurf')
        d.check()
        real_replace = os.replace
        def fail_profile(source, target):
            if Path(target) == self.path:
                raise OSError('Speicher voll')
            return real_replace(source, target)
        with patch('app.atomic_io.os.replace', side_effect=fail_profile):
            self.assertFalse(d.apply())
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertEqual(d.name_entry.text(), 'PrivaterEntwurf')
        event_id = d.last_event_id
        self.assertTrue(event_id)
        self.assertIn(event_id, d.preview.toPlainText())
        events = [json.loads(line) for line in self.logger.jsonl_path.read_text().splitlines()]
        self.assertEqual(events[-1]['event_id'], event_id)
        self.assertNotIn('PrivaterEntwurf', self.logger.jsonl_path.read_text())
        self.assertTrue(any(event_id in p.read_text() for p in self.root.rglob('*.txt')))
        d.name_entry.setText('Weiter')
        self.assertIn(event_id, d.preview.toPlainText())

    def test_read_failure_logged_and_log_failure_keeps_primary_error(self):
        self.path.write_text('{')
        self.dialog.name_entry.setText('Neu')
        self.assertFalse(self.dialog.check())
        self.assertTrue(self.dialog.last_event_id)
        with patch.object(self.logger, 'record', side_effect=OSError('Log voll')):
            self.assertFalse(self.dialog.check())
        self.assertIsNone(self.dialog.last_event_id)
        self.assertIn('nicht sicher gelesen', self.dialog.preview.toPlainText())
        self.assertIn('Fehlerprotokoll', self.dialog.preview.toPlainText())
        self.assertEqual(self.dialog.name_entry.text(), 'Neu')

    def test_escape_and_cancel_do_not_write(self):
        self.dialog.name_entry.setText('Neu')
        self.dialog.check()
        QTest.keyClick(self.dialog, Qt.Key_Escape)
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertIsNone(self.dialog.renamed_to)

    def test_plain_text_name_is_not_markup(self):
        self.dialog.name_entry.setText('<b>Neu</b>')
        self.assertTrue(self.dialog.check())
        self.assertIn('<b>Neu</b>', self.dialog.preview.toPlainText())

    def test_scroll_and_sticky_actions_at_all_zoom_levels(self):
        d = self.dialog
        for theme, zoom in ((theme, zoom) for theme in THEMES for zoom in (100, 125, 150, 175, 200)):
            for size in ((420, 340), (600, 460)):
                with self.subTest(theme=theme, zoom=zoom, size=size):
                    apply_global_style(d, zoom, theme)
                    d.resize(*size)
                    self.events()
                    for button in (d.check_button, d.rename_button, d.cancel_button):
                        rect = QRect(button.mapTo(d, QPoint()), button.size())
                        self.assertTrue(d.rect().contains(rect))
                        self.assertFalse(button.autoDefault())
                    for control in (d.name_entry, d.transfer_links):
                        center = control.mapTo(d.scroll.widget(), control.rect().center())
                        d.scroll.ensureVisible(center.x(), center.y(), control.width() // 2 + 1, control.height() // 2 + 1)
                        self.events()
                        rect = QRect(control.mapTo(d.scroll.viewport(), QPoint()), control.size())
                        self.assertTrue(d.scroll.viewport().rect().contains(rect))

    def test_editor_dashboard_generator_keep_selection_and_drafts(self):
        dash = Dashboard(FakeTexts(), self.logger, self.root)
        try:
            dash.show()
            dash.db_profile_combo.setCurrentText('Test')
            dash.db_boxes['Genres'].setCurrentText('Wert')
            dash.open_genre_random()
            generator = dash._genre_random_window
            generator.profile_combo.setCurrentText('Test')
            generator.filter_entry.setText('Wert')
            dash.db_quick_button.click()
            quick = dash.profile_quick_entry
            quick.value_entry.setText('Entwurf')
            quick.check_values()
            dash.open_profile_editor()
            editor = dash._profile_editor
            editor.profile_combo.setCurrentText('Test')
            editor.profile_name_entry.setText('Später neues Profil')
            editor.value_entry.setText('Späterer Wert')
            def execute(dialog):
                dialog.name_entry.setText('Neu')
                self.assertTrue(dialog.check())
                self.assertTrue(dialog.apply())
                return dialog.result()
            with patch.object(ProfileRenameDialog, 'exec', execute):
                editor.rename_button.click()
            self.events()
            self.assertEqual(editor.profile_combo.currentText(), 'Neu')
            self.assertEqual(dash.db_profile_combo.currentText(), 'Neu')
            self.assertEqual(dash.db_boxes['Genres'].currentText(), 'Wert')
            self.assertEqual(generator.profile_combo.currentText(), 'Neu')
            self.assertEqual(generator.filter_entry.text(), 'Wert')
            self.assertEqual(quick.value_entry.text(), 'Entwurf')
            self.assertFalse(quick.save_button.isEnabled())
            self.assertEqual(editor.profile_name_entry.text(), 'Später neues Profil')
            self.assertEqual(editor.value_entry.text(), 'Späterer Wert')
            self.assertEqual(editor.status_label.textFormat(), Qt.PlainText)
            self.assertFalse(editor.rename_button.autoDefault())
        finally:
            dash._closing_after_save = True
            dash.close()
            dash.deleteLater()
            QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
