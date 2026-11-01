"""Module lesen frische Werte desselben Stores über den gemeinsamen Vertrag."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from app.genre_random_window import GenreRandomWindow
from app.profile_editor import ProfileEditor
from app.profile_store import add_values, save_profiles, store_path
from app.ui import Dashboard


class FakeTexts:
    def get(self, _key, default=''):
        return default


class FakeLogger:
    def recent(self, _limit=100):
        return []

    def human_report(self, event):
        return str(event)


class ProfileReadApiGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_existing_modules_share_new_values_and_unicode_filter_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            save_profiles(root, {'Test': {'Genres': ['Düster']},
                                 'Anderes': {'Genres': ['Fremdwert']}})
            dashboard = Dashboard(FakeTexts(), FakeLogger(), root)
            editor = ProfileEditor(root)
            generator = GenreRandomWindow(root)
            try:
                add_values(root, 'Test', 'Genres', 'Neuwert')
                original = store_path(root).read_bytes()
                dashboard.refresh_db_profiles()
                dashboard.db_profile_combo.setCurrentText('Test')
                editor.refresh()
                editor.profile_combo.setCurrentText('Test')
                editor.category_combo.setCurrentText('Genres')
                generator.refresh()
                generator.profile_combo.setCurrentText('Test')
                generator.category_combo.setCurrentText('Genres')
                self.app.processEvents()
                box = dashboard.db_boxes['Genres']
                self.assertIn('Neuwert', [box.itemText(i) for i in range(box.count())])
                self.assertIn('Neuwert', [editor.values_list.item(i).text()
                                          for i in range(editor.values_list.count())])
                generator.filter_entry.setText(' DU\u0308ST ')
                self.app.processEvents()
                self.assertEqual(generator.archive_list.count(), 1)
                self.assertEqual(generator.archive_list.item(0).data(Qt.UserRole), 'Düster')
                self.assertEqual(generator.count_label.text(), '1 Einträge')
                generator.profile_combo.setCurrentText('Anderes')
                self.assertEqual(generator.archive_list.count(), 0)
                generator.filter_entry.clear()
                self.assertEqual(generator.archive_list.item(0).data(Qt.UserRole), 'Fremdwert')
                self.assertEqual(store_path(root).read_bytes(), original)
            finally:
                dashboard._closing_after_save = True
                dashboard.close()
                editor.close()
                generator.close()
