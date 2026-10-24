import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from app.search_window import SearchWindow
from app.ui import Dashboard
from app.main import configure_dashboard_presentation
from app.event_log import EventLogger
from app.texts import TextRegistry

ROOT = Path(__file__).resolve().parent.parent


class SearchGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'daten/texte').mkdir(parents=True)
        (self.root / 'daten/texte/probe.txt').write_text('Hallo Welt\nZweite Zeile', encoding='utf-8')
        self.window = SearchWindow(self.root)
        self.window.show()
        self.addCleanup(self.window.close)

    def finish_search(self):
        for _ in range(200):
            self.app.processEvents()
            if not self.window.timer.isActive():
                break
        self.assertFalse(self.window.timer.isActive())

    def test_search_preview_is_plain_read_only_and_zoomable(self):
        self.window.query.setText('WELT')
        self.window.start()
        self.assertFalse(self.window.start_button.isEnabled())
        self.finish_search()
        self.assertEqual(self.window.table.rowCount(), 1)
        self.window.table.selectRow(0)
        self.app.processEvents()
        self.assertIn('Hallo Welt', self.window.preview.toPlainText())
        self.assertTrue(self.window.preview.isReadOnly())
        self.assertIn('abgeschlossen', self.window.status.text())
        for zoom in (100, 150, 200):
            self.window.set_zoom(zoom)
            self.app.processEvents()
            self.assertEqual(self.window.zoom_percent, zoom)
            self.assertTrue(self.window.start_button.isEnabled())
        self.assertEqual((self.root / 'daten/texte/probe.txt').read_text(), 'Hallo Welt\nZweite Zeile')

    def test_cancel_close_and_reopen_preserve_safe_state(self):
        self.window.query.setText('Welt')
        self.window.start()
        self.window.cancel()
        self.assertFalse(self.window.timer.isActive())
        self.assertIsNone(self.window.iterator)
        self.assertIn('abgebrochen', self.window.status.text())
        self.window.start()
        self.window.close()
        self.assertFalse(self.window.timer.isActive())
        self.window.show()
        self.window.start()
        self.finish_search()
        self.assertEqual(self.window.table.rowCount(), 1)

    def test_invalid_query_and_inaccessible_root_are_explained(self):
        self.window.start()
        self.assertFalse(self.window.timer.isActive())
        self.assertIn('Suchtext', self.window.status.text())
        (self.root / 'linked').symlink_to(self.root / 'daten', target_is_directory=True)
        self.window.path_entry.setText(str(self.root / 'nonexistent'))
        self.window.approved_path = self.root / 'nonexistent'
        self.window.query.setText('Welt')
        self.window.start()
        self.finish_search()
        self.assertIn('Suchordner nicht gefunden', self.window.status.text())

    def test_controls_stay_separate_at_laptop_sizes_and_high_zoom(self):
        for zoom in (100, 150, 200):
            self.window.set_zoom(zoom)
            self.window.resize(1280, 680)
            for _ in range(5):
                self.app.processEvents()
            controls = (self.window.names, self.window.contents,
                        self.window.start_button, self.window.stop_button)
            for first, second in zip(controls, controls[1:]):
                self.assertLess(first.geometry().right(), second.geometry().left())
            for widget in (*controls, self.window.query, self.window.table,
                           self.window.preview, self.window.status):
                self.assertTrue(self.window.rect().contains(widget.geometry()))

    def test_dashboard_header_and_ready_route_reuse_same_managed_window(self):
        dashboard = Dashboard(TextRegistry(ROOT / 'texte/registry.json'),
                              EventLogger(self.root, '0.18.3'), self.root)
        self.addCleanup(dashboard.close)
        configure_dashboard_presentation(dashboard)
        dashboard.show()
        dashboard.search_entry.setText('Welt')
        dashboard._header_search()
        found = dashboard._search_window
        self.addCleanup(found.close)
        self.assertIn(found, [r.window for r in dashboard._managed_window_registry()])
        found.cancel()
        found.close()
        dashboard.open_search()
        self.assertIs(dashboard._search_window, found)
        from PySide6.QtWidgets import QPushButton
        ready = next(button for button in dashboard.findChildren(QPushButton)
                     if button.objectName() == 'tileButton' and 'Dateisuche' in button.text())
        self.assertFalse(bool(ready.property('planned')))
        self.assertTrue(ready.property('ready'))

    def test_external_scope_requires_confirmation_and_denial_preserves_results(self):
        self.window.query.setText('Welt')
        self.window.start()
        self.finish_search()
        external = self.root / 'Dokumente'
        external.mkdir()
        (external / 'extern.txt').write_text('externer Text')
        self.window.path_entry.setText(str(external))
        self.window.query.setText('externer')
        with patch('app.search_window.SearchWindow._ask_access', return_value=QMessageBox.No) as question:
            with patch('app.data_search.os.fwalk') as walk:
                self.window.start()
                walk.assert_not_called()
            question.assert_called_once()
        self.assertEqual(self.window.table.rowCount(), 1)
        self.assertIsNone(self.window.approved_path)
        with patch('app.search_window.SearchWindow._ask_access', return_value=QMessageBox.Yes):
            self.window.start()
        self.finish_search()
        self.assertEqual(self.window.table.item(0, 0).text(), 'extern.txt')
        self.assertIn(str(external), self.window.status.text())
        with patch('app.search_window.SearchWindow._ask_access') as question:
            self.window.start()
            self.finish_search()
            question.assert_not_called()
        self.window.path_entry.setText(str(self.root))
        self.assertIsNone(self.window.approved_path)

    def test_folder_picker_cancel_and_selected_path_do_not_start_search(self):
        previous = self.window.path_entry.text()
        with patch('app.search_window.QFileDialog.getExistingDirectory', return_value=''):
            self.window.choose_folder()
        self.assertEqual(self.window.path_entry.text(), previous)
        with patch('app.search_window.QFileDialog.getExistingDirectory', return_value=str(self.root)):
            self.window.choose_folder()
        self.assertEqual(self.window.path_entry.text(), str(self.root))
        self.assertFalse(self.window.timer.isActive())

    def test_permission_failure_explains_partial_search(self):
        def denied_walk(*args, **kwargs):
            kwargs['onerror'](PermissionError('denied'))
            return iter(())
        self.window.query.setText('Welt')
        with patch('app.data_search.os.fwalk', side_effect=denied_walk), \
                patch('app.search_window.SearchWindow._ask_access', return_value=QMessageBox.No) as request:
            self.window.start()
            self.finish_search()
        request.assert_called_once()
        self.assertIsNone(self.window.approved_path)
        self.assertIn('Leseberechtigung', self.window.status.text())
        self.assertNotIn('Suche abgeschlossen', self.window.status.text())
        self.assertTrue(self.window.path_entry.isEnabled())

    def test_empty_or_relative_folder_is_not_scanned(self):
        self.window.query.setText('Welt')
        for path in ('', 'relative/path'):
            self.window.path_entry.setText(path)
            with patch('app.data_search.os.fwalk') as walk:
                self.window.start()
                walk.assert_not_called()
            self.assertFalse(self.window.timer.isActive())
            self.assertIn('absoluten Pfad', self.window.status.text())

    def test_permission_prompt_opens_native_picker_only_after_consent(self):
        self.window.session = __import__('app.data_search', fromlist=['DataSearch']).DataSearch(self.root, 'Welt')
        self.window.session.record_denied(self.root / 'geschützt')
        with patch('app.search_window.SearchWindow._ask_access', return_value=QMessageBox.No), \
                patch('app.search_window.QFileDialog.getExistingDirectory') as picker:
            self.window._request_folder_access()
            picker.assert_not_called()
        with patch('app.search_window.SearchWindow._ask_access', return_value=QMessageBox.Yes), \
                patch('app.search_window.QFileDialog.getExistingDirectory', return_value='') as picker:
            self.window._request_folder_access()
            picker.assert_called_once()
        self.assertFalse(self.window.timer.isActive())

    def test_access_dialog_treats_untrusted_folder_names_as_plain_text(self):
        from PySide6.QtCore import Qt
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.No):
            self.window._ask_access('Ordnerzugriff', '<b>Ordner</b>')
        dialog = self.window.findChild(QMessageBox)
        self.assertEqual(dialog.textFormat(), Qt.PlainText)
        self.assertEqual(dialog.defaultButton(), dialog.button(QMessageBox.No))
