import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from app import performance as perf
from app.performance_panel import PerformancePanel
from app.recovery_center import RecoveryCenter
from app.event_log import EventLogger
from app.texts import TextRegistry
from app.ui_standards import apply_global_style
from app.window_lifecycle import _open_managed_window
from app.book_window import BookWindow

ROOT = Path(__file__).resolve().parents[1]


class PerformanceGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.old = perf._ACTIVE
        self.tracker = perf.activate(self.root)

    def tearDown(self):
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.No):
            for window in list(self.app.topLevelWidgets()):
                window.close()
                window.deleteLater()
        self.app.processEvents()
        perf._ACTIVE = self.old
        self.temp.cleanup()

    def test_help_contains_opt_in_panel_and_zoom_remains_usable(self):
        window = RecoveryCenter(TextRegistry(ROOT / 'texte/registry.json'), EventLogger(self.root, 'test'))
        panel = window.performance_panel
        self.assertFalse(panel.enabled.isChecked())
        self.assertIs(panel.tracker, self.tracker)
        window.tabs.setCurrentWidget(panel)
        window.show()
        for zoom in (100, 150, 200):
            apply_global_style(window, zoom)
            self.app.processEvents()
            self.assertTrue(panel.enabled.isVisibleTo(window))
            self.assertTrue(panel.summary.isReadOnly())
        self.assertFalse(self.tracker.settings_path.exists())

    def test_toggle_filter_preview_export_and_clear(self):
        panel = PerformancePanel(self.root)
        panel.enabled.setChecked(True)
        self.tracker.record('module.open', 'books', 7)
        self.tracker.record('file.write', 'books', 2, size=12)
        panel.refresh()
        self.assertIn('module.open', panel.json_preview.toPlainText())
        checks = list(panel.groups)
        checks[0].setChecked(False)
        self.assertNotIn('module.open', panel.json_preview.toPlainText())
        output = self.root / 'export.json'
        before = self.tracker.snapshot()
        with patch('app.performance_panel.QFileDialog.getSaveFileName', return_value=(str(output), 'JSON (*.json)')):
            panel.export()
        self.assertTrue(output.is_file())
        self.assertNotIn('module.open', output.read_text())
        self.assertEqual(before, self.tracker.snapshot())
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes):
            panel.clear()
        self.assertFalse(panel.enabled.isChecked())
        self.assertEqual({}, self.tracker.snapshot()['days'])

    def test_export_cannot_overwrite_diagnostics_store(self):
        self.tracker.configure(True)
        self.tracker.record('app.start', elapsed_ms=3)
        self.tracker.flush()
        before = self.tracker.data_path.read_bytes()
        panel = PerformancePanel(self.root)
        with patch('app.performance_panel.QFileDialog.getSaveFileName', return_value=(str(self.tracker.data_path), 'JSON (*.json)')), patch.object(QMessageBox, 'warning') as warning:
            panel.export()
            warning.assert_called_once()
        self.assertEqual(before, self.tracker.data_path.read_bytes())

    def test_module_factory_is_measured_and_classified(self):
        self.tracker.configure(True)
        window = _open_managed_window(None, lambda: BookWindow(self.root))
        rows = self.tracker.snapshot(30, ('module.open',))['days']
        key = next(iter(next(iter(rows.values()))))
        self.assertTrue(key.endswith('|module.open|books'))
        window.close()
