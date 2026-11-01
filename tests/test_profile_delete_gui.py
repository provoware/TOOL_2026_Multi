"""Bewusstes Löschen: Vorschau, Bestätigung, Fehler und Auswahl-/Entwurfsschutz."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QCoreApplication, QEvent, QPoint, QRect, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from app.event_log import EventLogger
from app.profile_delete_dialog import ProfileDeleteDialog
from app.profile_store import CATEGORIES, profile_names, save_profiles
from app.profile_transaction import JOURNAL, recover_profile_transaction
from app.ui import Dashboard
from app.ui_standards import DEFAULT_THEME, THEMES, apply_global_style


class FakeTexts:
    def get(self, key, default=''):
        return default


class ProfileDeleteGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.app.setProperty('provowareTheme', DEFAULT_THEME)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {'Test': {'Genres': ['Wert']}, 'Anderes': {'Genres': ['Fremd']}})
        self.before = self.path.read_bytes()
        self.logger = EventLogger(self.root, 'test')
        self.dialog = ProfileDeleteDialog(self.root, 'Test', logger=self.logger)
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

    def test_preview_and_separate_confirmation_are_required_before_click(self):
        d = self.dialog
        self.assertFalse(d.apply())
        self.assertFalse(d.confirm.isEnabled())
        self.assertTrue(d.check())
        self.assertIn('Test', d.preview.toPlainText())
        self.assertIn('keine Rückgängig', d.preview.toPlainText())
        self.assertFalse(d.delete_button.isEnabled())
        self.assertFalse(d.apply())
        d.confirm.setChecked(True)
        self.assertTrue(d.delete_button.isEnabled())
        d.check()
        self.assertFalse(d.confirm.isChecked())
        d.confirm.setChecked(True)
        d.confirm.setFocus()
        QTest.keyClick(d.confirm, Qt.Key_Return)
        self.assertEqual(self.path.read_bytes(), self.before)
        QTest.mouseClick(d.delete_button, Qt.LeftButton)
        self.assertEqual(d.deleted_name, 'Test')
        self.assertNotIn('Test', profile_names(self.root))

    def test_reference_and_last_profile_keep_confirmation_disabled(self):
        fav = self.path.parent / 'genre_favoriten.json'
        fav.write_text(json.dumps({'schema': 1, 'favorites': {' TEST ': {cat: [] for cat in CATEGORIES}}}))
        self.assertFalse(self.dialog.check())
        self.assertIn('gesperrt', self.dialog.preview.toPlainText())
        self.assertFalse(self.dialog.confirm.isEnabled())
        self.assertFalse(self.dialog.delete_button.isEnabled())
        fav.unlink()
        save_profiles(self.root, {'Test': {}})
        self.assertFalse(self.dialog.check())
        self.assertIn('letzte Profil', self.dialog.preview.toPlainText())
        self.assertFalse(self.dialog.confirm.isEnabled())

    def test_stale_plan_resets_confirmation_without_deleting_or_logging_error(self):
        d = self.dialog
        d.check()
        d.confirm.setChecked(True)
        self.path.write_bytes(self.before + b' ')
        self.assertFalse(d.apply())
        self.assertFalse(d.confirm.isChecked())
        self.assertFalse(d.delete_button.isEnabled())
        self.assertIn('erneut prüfen', d.preview.toPlainText())
        self.assertEqual(self.path.read_bytes(), self.before + b' ')
        self.assertFalse(self.logger.jsonl_path.exists())

    def test_real_storage_error_logs_jsonl_txt_and_log_failure_stays_honest(self):
        d = self.dialog
        d.check()
        d.confirm.setChecked(True)
        real = os.replace
        def fail(source, target):
            if Path(target) == self.path:
                raise OSError('Speicher voll')
            return real(source, target)
        with patch('app.atomic_io.os.replace', side_effect=fail):
            self.assertFalse(d.apply())
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertTrue(d.last_event_id)
        event = json.loads(self.logger.jsonl_path.read_text().splitlines()[-1])
        self.assertEqual(event['event_id'], d.last_event_id)
        self.assertEqual(event['area'], 'PROFIL_LOESCHEN')
        self.assertTrue(any(d.last_event_id in p.read_text() for p in self.root.rglob('*.txt')))
        d.check(); d.confirm.setChecked(True)
        with patch('app.atomic_io.os.replace', side_effect=fail), patch.object(self.logger, 'record', side_effect=OSError('Log voll')):
            self.assertFalse(d.apply())
        self.assertIsNone(d.last_event_id)
        self.assertIn('Speicher voll', d.preview.toPlainText())
        self.assertIn('Fehlerprotokoll', d.preview.toPlainText())
        self.assertFalse(d.confirm.isChecked())

    def test_pending_recovery_is_reported_without_claiming_unchanged_data(self):
        import app.profile_transaction as tx
        publish = tx._publish
        def fail_after_write(folder, name, raw):
            publish(folder, name, raw)
            raise OSError('Abbruch nach Dateiersetzung')
        d = self.dialog
        d.check(); d.confirm.setChecked(True)
        with patch.object(tx, '_publish', fail_after_write):
            self.assertFalse(d.apply())
        self.assertTrue((self.path.parent / JOURNAL).exists())
        self.assertIn('gesperrt', d.preview.toPlainText())
        self.assertNotIn('bisherige Bestand bleibt erhalten', d.preview.toPlainText())
        self.assertTrue(d.last_event_id)
        self.assertFalse(d.confirm.isChecked())
        self.assertTrue(recover_profile_transaction(self.root))
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_escape_and_cancel_even_after_confirmation_never_delete(self):
        d = self.dialog
        for use_escape in (True, False):
            d.show(); d.check(); d.confirm.setChecked(True)
            if use_escape:
                QTest.keyClick(d, Qt.Key_Escape)
            else:
                QTest.mouseClick(d.cancel_button, Qt.LeftButton)
            self.assertIsNone(d.deleted_name)
            self.assertEqual(self.path.read_bytes(), self.before)

    def test_plain_preview_and_sticky_actions_in_40_layout_combinations(self):
        d = self.dialog
        save_profiles(self.root, {'<b>Test</b>': {'Genres': ['Wert']}, 'Anderes': {}})
        d.name = '<b>Test</b>'
        self.assertTrue(d.check())
        self.assertIn('<b>Test</b>', d.preview.toPlainText())
        for theme in THEMES:
            for zoom in (100, 125, 150, 175, 200):
                for size in ((420, 340), (600, 460)):
                    with self.subTest(theme=theme, zoom=zoom, size=size):
                        apply_global_style(d, zoom, theme)
                        d.resize(*size)
                        self.events()
                        for button in (d.check_button, d.delete_button, d.cancel_button):
                            rect = QRect(button.mapTo(d, QPoint()), button.size())
                            self.assertTrue(d.rect().contains(rect))
                            self.assertFalse(button.autoDefault())
                        control = d.confirm
                        center = control.mapTo(d.scroll.widget(), control.rect().center())
                        d.scroll.ensureVisible(center.x(), center.y(), control.width() // 2 + 1, control.height() // 2 + 1)
                        self.events()
                        rect = QRect(control.mapTo(d.scroll.viewport(), QPoint()), control.size())
                        self.assertTrue(d.scroll.viewport().rect().contains(rect))

    def test_editor_updates_visible_modules_and_preserves_unrelated_selection_and_drafts(self):
        for selected in ('Test', 'Anderes'):
            with self.subTest(selected=selected):
                save_profiles(self.root, {'Test': {'Genres': ['Wert']}, 'Anderes': {'Genres': ['Fremd']}})
                dash = Dashboard(FakeTexts(), self.logger, self.root)
                try:
                    dash.show()
                    dash.db_profile_combo.setCurrentText(selected)
                    dash.db_boxes['Genres'].setCurrentText('Fremd' if selected == 'Anderes' else 'Wert')
                    dash.open_genre_random()
                    gen = dash._genre_random_window
                    gen.profile_combo.setCurrentText(selected)
                    gen.filter_entry.setText('Filter')
                    dash.db_quick_button.click()
                    quick = dash.profile_quick_entry
                    quick.value_entry.setText('Entwurf')
                    quick.check_values()
                    dash.open_profile_editor()
                    editor = dash._profile_editor
                    editor.profile_combo.setCurrentText('Test')
                    editor.profile_name_entry.setText('Neues Profil später')
                    editor.value_entry.setText('Wert später')
                    def execute(dialog):
                        self.assertEqual(dialog.name, 'Test')
                        self.assertTrue(dialog.check())
                        dialog.confirm.setChecked(True)
                        self.assertTrue(dialog.apply())
                        return dialog.result()
                    with patch.object(ProfileDeleteDialog, 'exec', execute):
                        QTest.mouseClick(editor.delete_button, Qt.LeftButton)
                    self.events()
                    self.assertEqual(profile_names(self.root), ['Anderes'])
                    self.assertEqual(editor.profile_combo.currentText(), 'Anderes')
                    self.assertEqual(dash.db_profile_combo.currentText(), 'Anderes')
                    self.assertEqual(gen.profile_combo.currentText(), 'Anderes')
                    self.assertEqual(gen.filter_entry.text(), 'Filter')
                    self.assertEqual(quick.value_entry.text(), 'Entwurf')
                    if selected == 'Test':
                        self.assertFalse(quick.save_button.isEnabled())
                    else:
                        self.assertEqual(dash.db_boxes['Genres'].currentText(), 'Fremd')
                    self.assertEqual(editor.profile_name_entry.text(), 'Neues Profil später')
                    self.assertEqual(editor.value_entry.text(), 'Wert später')
                    self.assertFalse(editor.delete_button.autoDefault())
                    for zoom in (100, 200):
                        apply_global_style(editor, zoom)
                        editor.resize(620, 460)
                        self.events()
                        rect = QRect(editor.delete_button.mapTo(editor, QPoint()), editor.delete_button.size())
                        self.assertTrue(editor.rect().contains(rect))
                finally:
                    dash._closing_after_save = True
                    dash.close(); dash.deleteLater()
                    QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
                    self.events()
