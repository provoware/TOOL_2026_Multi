"""Direkte Dashboard-Eingabe: echte Aktionen, Vorschaugrenzen und sichere Fehler."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtCore import QCoreApplication, QEvent, QPoint, QRect, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox
from app.profile_store import add_values, read_profile, save_profiles, store_path
from app.profile_editor import ProfileEditor
from app.profile_quick_entry import ProfileQuickEntry
from app.event_log import EventLogger
from app.genre_random_window import GenreRandomWindow
from app.ui import Dashboard
from app.main import configure_dashboard_presentation
from app.laptop_layout import install_laptop_layout
from app.ui_standards import DEFAULT_THEME, THEMES, apply_global_style


class FakeTexts:
    def get(self, _key, default=''):
        return default


class ProfileQuickEntryGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.app.setProperty('provowareTheme', DEFAULT_THEME)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.path = save_profiles(self.root, {'Test': {'Genres': ['düster']},
                                              'Anderes': {'Genres': ['Fremdwert']}})
        self.before = self.path.read_bytes()
        self.logger = EventLogger(self.root, 'test')
        self.dashboard = Dashboard(FakeTexts(), self.logger, self.root)
        install_laptop_layout(self.dashboard)
        self.dashboard.show()
        self.dashboard.db_profile_combo.setCurrentText('Test')
        QTest.mouseClick(self.dashboard.db_quick_button, Qt.LeftButton)
        self.widget = self.dashboard.profile_quick_entry
        self.events()

    def events(self):
        for _ in range(3):
            self.app.processEvents()

    def scroll_to_control(self, scroll, control):
        # ensureWidgetVisible steuert bei Textfeldern ggf. den Textcursor an.
        # Hier den vollständigen Feldbereich über die Scrollposition prüfen.
        center = control.mapTo(scroll.widget(), control.rect().center())
        scroll.ensureVisible(center.x(), center.y(), control.width() // 2 + 1,
                             control.height() // 2 + 1)
        self.events()

    def tearDown(self):
        self.dashboard._closing_after_save = True
        self.dashboard.close()
        self.dashboard.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.DeferredDelete)
        self.events()
        self.tmp.cleanup()

    def test_preview_then_atomic_save_and_matching_dashboard_selection(self):
        self.widget.value_entry.setText('DU\u0308STER, "warm, dunkel", Neu, NEU')
        self.assertFalse(self.widget.save_button.isEnabled())
        self.assertFalse(self.widget.save_values())
        QTest.mouseClick(self.widget.check_button, Qt.LeftButton)
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertIn('Neu (2)', self.widget.preview_text.toPlainText())
        self.assertIn('„warm, dunkel“', self.widget.preview_text.toPlainText())
        self.events()
        viewport = self.dashboard.db_quick_scroll.viewport()
        preview_rect = QRect(self.widget.preview_text.mapTo(viewport, QPoint(0, 0)),
                             self.widget.preview_text.size())
        self.assertTrue(viewport.rect().contains(preview_rect))
        self.assertIn('Vorhanden (1)', self.widget.preview_text.toPlainText())
        self.assertIn('Wiederholt (1)', self.widget.preview_text.toPlainText())
        with patch('app.profile_store.save_profiles', wraps=save_profiles) as save:
            QTest.mouseClick(self.widget.save_button, Qt.LeftButton)
        self.assertEqual(save.call_count, 1)
        self.assertEqual(read_profile(self.root, 'Test')['Genres'], ['düster', 'warm, dunkel', 'Neu'])
        self.assertEqual(read_profile(self.root, 'Anderes')['Genres'], ['Fremdwert'])
        self.assertEqual(self.dashboard.db_boxes['Genres'].currentText(), 'Neu')
        self.assertIn('2 gespeichert · 2 übersprungen', self.widget.status_label.text())
        self.assertEqual(self.widget.value_entry.text(), '')

    def test_invalid_list_does_not_partially_write_and_draft_survives(self):
        for text in ['gültig, "offen', 'neu\nkaputt', ', ,']:
            with self.subTest(text=text):
                self.widget.value_entry.setText(text)
                self.assertFalse(self.widget.check_values())
                self.assertFalse(self.widget.save_values())
                self.assertEqual(self.widget.value_entry.text(), text)
                self.assertEqual(self.path.read_bytes(), self.before)

    def test_input_category_and_profile_changes_invalidate_old_preview(self):
        self.widget.value_entry.setText('Neu')
        self.widget.check_values()
        self.widget.value_entry.setText('Anders')
        self.assertFalse(self.widget.save_button.isEnabled())
        self.widget.check_values()
        self.widget.category_combo.setCurrentText('Stimmungen')
        self.assertFalse(self.widget.save_button.isEnabled())
        self.widget.check_values()
        self.dashboard.db_profile_combo.setCurrentText('Anderes')
        self.assertIn('Anderes', self.widget.target_label.text())
        self.assertEqual(self.widget.value_entry.text(), 'Anders')
        self.assertFalse(self.widget.save_values())
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_changed_store_requires_second_conscious_save(self):
        self.widget.value_entry.setText('Neu')
        self.widget.check_values()
        add_values(self.root, 'Test', 'Genres', 'Neu')
        before = self.path.read_bytes()
        self.assertFalse(self.widget.save_values())
        self.assertIn('Bestand geändert', self.widget.status_label.text())
        self.assertEqual(self.widget.value_entry.text(), 'Neu')
        self.assertEqual(self.path.read_bytes(), before)
        with patch('app.profile_store.save_profiles') as save:
            self.assertTrue(self.widget.save_values())
            save.assert_not_called()
        self.assertIn('0 gespeichert · 1 übersprungen', self.widget.status_label.text())

    def test_failed_replace_preserves_store_and_draft_without_success(self):
        self.widget.value_entry.setText('Neu')
        self.widget.check_values()
        with patch('app.atomic_io.os.replace', side_effect=OSError('Schreibprobe')):
            self.assertFalse(self.widget.save_values())
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertEqual(self.widget.value_entry.text(), 'Neu')
        self.assertIn('Nicht gespeichert', self.widget.status_label.text())
        self.assertFalse(self.widget.save_button.isEnabled())
        self.events()
        viewport = self.dashboard.db_quick_scroll.viewport()
        self.assertTrue(viewport.rect().contains(QRect(
            self.widget.status_label.mapTo(viewport, QPoint(0, 0)), self.widget.status_label.size())))

    def test_keyboard_enter_only_checks_and_escape_preserves_draft(self):
        configure_dashboard_presentation(self.dashboard)
        self.events()
        self.widget.value_entry.setText('Neu')
        self.widget.value_entry.setFocus()
        QTest.keyClick(self.widget.value_entry, Qt.Key_Return)
        self.events()
        self.assertTrue(self.widget.save_button.isEnabled())
        self.assertEqual(self.path.read_bytes(), self.before)
        QTest.keyClick(self.widget.value_entry, Qt.Key_Escape)
        self.events()
        self.assertIs(self.dashboard.db_pages.currentWidget(), self.dashboard.db_selection_scroll)
        self.dashboard.open_profile_quick_entry()
        self.assertEqual(self.widget.value_entry.text(), 'Neu')

    def test_dashboard_close_cancellation_and_invalid_save_preserve_draft(self):
        self.widget.value_entry.setText('Neu')
        self.dashboard.close_profile_quick_entry()
        with patch('app.profile_quick_entry.ask_unsaved', return_value=QMessageBox.Cancel):
            self.assertFalse(self.dashboard.close())
        self.assertTrue(self.dashboard.isVisible())
        self.assertIs(self.dashboard.db_pages.currentWidget(), self.dashboard.db_quick_scroll)
        with patch('app.profile_quick_entry.ask_unsaved', return_value=QMessageBox.Yes):
            self.assertFalse(self.dashboard.close())
        self.assertEqual(self.widget.value_entry.text(), 'Neu')
        self.assertEqual(self.path.read_bytes(), self.before)
        self.widget.check_values()
        with patch('app.profile_quick_entry.ask_unsaved', return_value=QMessageBox.Yes):
            self.assertTrue(self.dashboard.close())
        self.assertIn('Neu', read_profile(self.root, 'Test')['Genres'])

    @staticmethod
    def _layout_cases():
        # Orthogonale Regressionen: jede Zoomstufe, jedes Theme und jede Größe.
        # Das volle Kreuzprodukt wird separat als UI-Evidenz ausgeführt.
        cases = [(DEFAULT_THEME, (1020, 650), zoom) for zoom in [100, 125, 150, 175, 200]]
        cases += [(theme, (1020, 650), 200) for theme in THEMES if theme != DEFAULT_THEME]
        cases += [(DEFAULT_THEME, size, 100) for size in [(1366, 768), (1600, 900)]]
        return cases

    def test_long_input_and_controls_reachable_at_all_zooms(self):
        configure_dashboard_presentation(self.dashboard)
        self.events()
        for theme, size, zoom in self._layout_cases():
            with self.subTest(theme=theme, size=size, zoom=zoom):
                self.dashboard.resize(*size)
                self.dashboard.set_zoom(zoom)
                # Nur dieses Prüffenster umstellen: fremde alte Testfenster
                # gehören nicht zum Scope der Formularprüfung.
                apply_global_style(self.dashboard, zoom, theme)
                self.dashboard.close_profile_quick_entry()
                self.events()
                selection = self.dashboard.db_selection_scroll
                self.scroll_to_control(selection, self.dashboard.db_quick_button)
                entry_rect = QRect(self.dashboard.db_quick_button.mapTo(selection.viewport(), QPoint(0, 0)),
                                   self.dashboard.db_quick_button.size())
                self.assertTrue(selection.viewport().rect().contains(entry_rect))
                QTest.mouseClick(self.dashboard.db_quick_button, Qt.LeftButton)
                self.assertIs(self.dashboard.db_pages.currentWidget(), self.dashboard.db_quick_scroll)
                self.widget.value_entry.setText(', '.join('Wert'+str(i) for i in range(50)))
                self.widget.check_values()
                self.events()
                scroll = self.dashboard.db_quick_scroll
                for control in [self.widget.category_combo, self.widget.value_entry, self.widget.preview_text,
                                self.widget.check_button, self.widget.save_button, self.widget.back_button]:
                    self.scroll_to_control(scroll, control)
                    rect = QRect(control.mapTo(scroll.viewport(), QPoint(0, 0)), control.size())
                    self.assertTrue(scroll.viewport().rect().contains(rect), (zoom, rect))
                    self.assertTrue(control.accessibleName())
                self.assertEqual(self.path.read_bytes(), self.before)

    def test_existing_open_modules_refresh_after_save(self):
        editor = ProfileEditor(self.root)
        generator = GenreRandomWindow(self.root)
        self.dashboard._profile_editor = editor
        self.dashboard._genre_random_window = generator
        editor.show()
        generator.show()
        try:
            editor.profile_combo.setCurrentText('Test')
            generator.profile_combo.setCurrentText('Test')
            generator.category_combo.setCurrentText('Genres')
            self.widget.value_entry.setText('Neu')
            self.widget.check_values()
            self.widget.save_values()
            self.assertIn('Neu', [editor.values_list.item(i).text() for i in range(editor.values_list.count())])
            self.assertIn('Neu', [generator.archive_list.item(i).data(Qt.UserRole)
                                 for i in range(generator.archive_list.count())])
        finally:
            editor.close()
            generator.close()
            editor.deleteLater()
            generator.deleteLater()

    def test_default_preview_and_corrupt_store_never_write(self):
        root = self.root / 'frisch'
        widget = ProfileQuickEntry(root)
        try:
            widget.set_profile('HardTechno')
            widget.value_entry.setText('Neu')
            self.assertTrue(widget.check_values())
            target = store_path(root)
            self.assertFalse(target.exists())
            target.parent.mkdir(parents=True)
            target.write_bytes(b'{kaputt')
            self.assertFalse(widget.save_values())
            self.assertEqual(target.read_bytes(), b'{kaputt')
            self.assertEqual(widget.value_entry.text(), 'Neu')
            self.assertIn('Nicht gespeichert', widget.status_label.text())
        finally:
            widget.close()
            widget.deleteLater()

    def test_tab_and_space_perform_conscious_save(self):
        configure_dashboard_presentation(self.dashboard)
        self.events()
        self.widget.value_entry.setText('Neu')
        self.widget.value_entry.setFocus()
        QTest.keyClick(self.widget.value_entry, Qt.Key_Return)
        for _ in range(3):
            QTest.keyClick(self.app.focusWidget(), Qt.Key_Tab)
        self.assertIs(self.app.focusWidget(), self.widget.save_button)
        self.assertEqual(self.path.read_bytes(), self.before)
        QTest.keyClick(self.widget.save_button, Qt.Key_Space)
        self.assertIn('Neu', read_profile(self.root, 'Test')['Genres'])

    def test_deliberate_discard_closes_without_writing(self):
        self.widget.value_entry.setText('Nur Entwurf')
        with patch('app.profile_quick_entry.ask_unsaved', return_value=QMessageBox.No):
            self.assertTrue(self.dashboard.close())
        self.assertEqual(self.path.read_bytes(), self.before)

    def test_read_failure_records_event_report_and_keeps_reference_after_edit(self):
        self.path.write_bytes(b'{kaputt')
        self.widget.value_entry.setText('PrivaterEntwurf')
        self.assertFalse(self.widget.check_values())
        event = self.logger.recent()[0]
        self.assertEqual(event['exception_type'], 'JSONDecodeError')
        self.assertEqual(event['program_version'], 'test')
        self.assertEqual(event['severity'], 'FEHLER')
        self.assertIn(event['event_id'], self.widget.status_label.text())
        self.assertTrue((self.root / 'berichte' / (event['event_id'] + '.txt')).is_file())
        self.assertNotIn('PrivaterEntwurf', self.logger.jsonl_path.read_text())
        self.widget.value_entry.setText('Weiterarbeiten')
        self.assertIn(event['event_id'], self.widget.status_label.text())
        self.assertEqual(self.path.read_bytes(), b'{kaputt')

    def test_storage_failure_uses_real_logger_without_losing_draft(self):
        self.widget.value_entry.setText('PrivaterEntwurf')
        self.widget.check_values()
        original_replace = os.replace
        def replace(source, destination):
            if Path(destination) == self.path:
                raise OSError('Gezielte Schreibprobe')
            return original_replace(source, destination)
        with patch('app.atomic_io.os.replace', side_effect=replace):
            self.assertFalse(self.widget.save_values())
        event = self.logger.recent()[0]
        self.assertEqual(event['exception_type'], 'OSError')
        self.assertIn(event['event_id'], self.widget.status_label.text())
        self.assertTrue((self.root / 'berichte' / (event['event_id'] + '.txt')).is_file())
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertEqual(self.widget.value_entry.text(), 'PrivaterEntwurf')
        self.assertNotIn('PrivaterEntwurf', self.logger.jsonl_path.read_text())

    def test_expected_validation_is_not_recorded_as_storage_failure(self):
        self.widget.value_entry.setText('neu, "offen')
        self.assertFalse(self.widget.check_values())
        self.assertEqual(self.logger.recent(), [])
        self.assertFalse(self.logger.jsonl_path.exists())

    def test_log_failure_preserves_primary_error_and_draft(self):
        self.widget.value_entry.setText('Neu')
        self.widget.check_values()
        self.widget.last_event_id = 'ALTE-KENNUNG'
        with patch('app.profile_quick_entry.add_values', side_effect=OSError('Datenfehler')), patch.object(
                self.logger, 'record', side_effect=OSError('Logfehler')):
            self.assertFalse(self.widget.save_values())
        self.assertIn('Datenfehler', self.widget.status_label.text())
        self.assertIn('Keine vollständige Ereignisaufzeichnung', self.widget.status_label.text())
        self.assertEqual(self.widget.value_entry.text(), 'Neu')
        self.assertEqual(self.path.read_bytes(), self.before)
        self.assertIsNone(self.widget.last_event_id)
