"""Vorschau zählt Eingaben ohne Bestandsänderung oder falschen Speichererfolg."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtWidgets import QApplication
from app.profile_editor import ProfileEditor
from app.profile_store import preview_values, save_profiles, store_path


class ProfilePreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {'Test': {'Genres': ['düster']}, 'Leer': {}})
        self.before = self.path.read_bytes()

    def window(self):
        window = ProfileEditor(self.root)
        window.profile_combo.setCurrentText('Test')
        window.category_combo.setCurrentText('Genres')
        self.addCleanup(window.close)
        return window

    def test_preview_distinguishes_unicode_existing_and_internal_duplicates(self):
        result = preview_values(self.root, 'Test', 'Genres',
                                'DU\u0308STER, düster, "warm, dunkel", "WARM, DUNKEL", ruhig')
        self.assertEqual(result, {'new': ['warm, dunkel', 'ruhig'],
                                  'present': ['DÜSTER'], 'repeated': ['düster', 'WARM, DUNKEL']})
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_preview_never_creates_a_default_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(preview_values(root, 'HardTechno', 'Genres', 'neu')['new'], ['neu'])
            self.assertFalse(store_path(root).exists())

    def test_invalid_lists_and_missing_targets_do_not_write(self):
        for profile, category, value in [('Test', 'Genres', 'neu, "offen'),
                                          ('Fehlt', 'Genres', 'neu'),
                                          ('Test', 'Fehlt', 'neu'),
                                          ('Test', 'Genres', 'neu\nkaputt')]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                preview_values(self.root, profile, category, value)
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_target_changes_update_preview_and_save_counts(self):
        window = self.window()
        window.value_entry.setText('düster, DÜSTER, neu')
        self.assertIn('1 neu · 1 bereits vorhanden · 1 wiederholt', window.preview_label.text())
        window.profile_combo.setCurrentText('Leer')
        self.assertIn('2 neu · 0 bereits vorhanden · 1 wiederholt', window.preview_label.text())
        self.assertEqual(self.path.read_bytes(), self.before)
        window.create_value()
        self.assertIn('2 gespeichert · 1 übersprungen · 0 fehlerhaft', window.status_label.text())
        self.assertEqual(window.value_entry.text(), '')
        self.assertEqual(window.preview_label.text(), '')

    def test_rechecks_store_instead_of_trusting_old_preview(self):
        window = self.window()
        window.value_entry.setText('neu')
        self.assertIn('1 neu', window.preview_label.text())
        save_profiles(self.root, {'Test': {'Genres': ['düster', 'neu']}})
        window.create_value()
        self.assertIn('0 gespeichert · 1 übersprungen', window.status_label.text())

    def test_write_failure_and_invalid_input_preserve_draft(self):
        window = self.window()
        for value in ['neu', 'neu, "offen']:
            window.value_entry.setText(value)
            with patch('app.profile_editor.QMessageBox.warning'), patch(
                    'app.atomic_io.os.replace', side_effect=OSError('Schreibprobe')):
                window.create_value()
            self.assertEqual(window.value_entry.text(), value)
            self.assertIn('0 gespeichert', window.status_label.text())
            self.assertNotIn('0 fehlerhaft', window.status_label.text())
            self.assertEqual(self.path.read_bytes(), self.before)

    def test_preview_remains_visible_with_large_text(self):
        window = self.window()
        window.resize(800, 600)
        window.show()
        for zoom in [100, 150, 200]:
            window.set_zoom(zoom)
            window.value_entry.setText('düster, neu, NEU')
            self.app.processEvents()
            self.assertTrue(window.preview_label.isVisibleTo(window))
            self.assertGreaterEqual(window.preview_label.height(), window.preview_label.heightForWidth(
                window.preview_label.width()))
