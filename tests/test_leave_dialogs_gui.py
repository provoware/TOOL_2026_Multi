"""Reale Dialogschaltflächen: eindeutige Folgen und sicherer Abbruch."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from PySide6.QtCore import QTimer, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QMessageBox
from app.module_widgets import ask_unsaved
from app.text_editor_window import TextEditorWindow
from app.book_window import BookWindow
from app.module_controls_window import ModuleControlsWindow


class LeaveDialogsGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def choose(self, choice, seen):
        def click():
            dialog = self.app.activeModalWidget()
            seen['labels'] = [b.text() for b in dialog.buttons()]
            seen['default'] = dialog.defaultButton().text()
            if choice == 'escape':
                QTest.keyClick(dialog, Qt.Key_Escape)
            elif choice == 'window':
                dialog.close()
            else:
                dialog.button(choice).click()
        QTimer.singleShot(0, click)

    def test_labels_and_safe_defaults_for_switch_and_close(self):
        for closing in (False, True):
            for choice in (QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel, 'escape', 'window'):
                with self.subTest(closing=closing, choice=choice):
                    seen = {}
                    self.choose(choice, seen)
                    result = ask_unsaved(None, closing=closing)
                    self.assertEqual(result, QMessageBox.Cancel if isinstance(choice, str) else choice)
                    suffix = 'schließen' if closing else 'wechseln'
                    self.assertCountEqual(seen['labels'], ['Speichern und ' + suffix, 'Verwerfen und ' + suffix, 'Weiterarbeiten'])
                    self.assertEqual(seen['default'], 'Weiterarbeiten')

    def test_text_real_close_choices_and_failed_save_keep_work(self):
        for choice in (QMessageBox.Yes, QMessageBox.No, QMessageBox.Cancel):
            with TemporaryDirectory() as tmp:
                w = TextEditorWindow(Path(tmp))
                w.title_entry.setText('Entwurf')
                w.text_edit.setPlainText('Wichtiger Text')
                self.choose(choice, {})
                closed = w.close()
                self.assertEqual(closed, choice != QMessageBox.Cancel)
                self.assertEqual(bool(list(Path(tmp).glob('daten/texte/*.json'))), choice == QMessageBox.Yes)
                if choice == QMessageBox.Cancel:
                    self.assertEqual(w.text_edit.toPlainText(), 'Wichtiger Text')
                    self.choose(QMessageBox.Yes, {})
                    with patch('app.text_editor_window.save_text_document', side_effect=OSError('voll')), \
                            patch.object(QMessageBox, 'critical'):
                        self.assertFalse(w.close())
                    self.assertEqual(w.text_edit.toPlainText(), 'Wichtiger Text')
                    self.assertTrue(w.autosave_timer.isActive())
                w._saved_snapshot = w._snapshot()
                w.close()
                w.deleteLater()
                self.app.processEvents()

    def test_book_and_module_preferences_real_discard_or_save_error(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            w = BookWindow(root)
            w.title.setText('Buchentwurf')
            self.choose(QMessageBox.Yes, {})
            with patch('app.book_store.put', side_effect=OSError('voll')), patch.object(QMessageBox, 'warning'):
                self.assertFalse(w.close())
            self.assertEqual(w.title.text(), 'Buchentwurf')
            self.choose(QMessageBox.No, {})
            self.assertTrue(w.close())
            self.assertEqual(w.title.text(), '')
            self.assertFalse((root / 'daten').exists())
            w.deleteLater()
            manager = ModuleControlsWindow(root)
            key = next(iter(manager.checks))
            original = manager.checks[key].isChecked()
            manager.checks[key].setChecked(not original)
            self.choose(QMessageBox.Cancel, {})
            self.assertFalse(manager.close())
            self.choose(QMessageBox.No, {})
            self.assertTrue(manager.close())
            self.assertEqual(manager.checks[key].isChecked(), original)
            self.assertFalse((root / 'daten').exists())
            manager.deleteLater()
            self.app.processEvents()
