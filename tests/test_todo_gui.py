import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QApplication, QMessageBox

from app.todo_store import (active_tasks, archived_tasks, ensure_project_module_backlog,
                            add_task, load_state, complete_task, store_path, task_groups)
from app.todo_window import TodoWindow


class TodoGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.changed = 0
        self.window = TodoWindow(self.root, on_changed=self._changed)
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.app.processEvents()
        self.temp.cleanup()

    def _changed(self):
        self.changed += 1

    def test_add_without_due_and_archive_after_complete(self):
        baseline_active = len(active_tasks(self.root))
        baseline_archive = len(archived_tasks(self.root))
        self.window.title_entry.setText("Milch kaufen")
        self.window.note_entry.setPlainText("2 Liter")
        self.window.add_current_task()
        self.app.processEvents()
        self.assertEqual(len(active_tasks(self.root)), baseline_active + 1)
        self.assertEqual(self.window.active_table.rowCount(), baseline_active + 1)
        row = next(
            row for row in range(self.window.active_table.rowCount())
            if self.window.active_table.item(row, 0).text() == "Milch kaufen"
        )
        self.window.active_table.selectRow(row)
        self.window.complete_selected()
        self.app.processEvents()
        self.assertEqual(len(active_tasks(self.root)), baseline_active)
        self.assertEqual(len(archived_tasks(self.root)), baseline_archive + 1)
        self.assertEqual(self.window.archive_table.rowCount(), baseline_archive + 1)
        self.assertEqual(self.changed, 2)

    def test_due_datetime_is_saved_when_enabled(self):
        self.window.title_entry.setText("Terminierte Aufgabe")
        self.window.use_due.setChecked(True)
        self.window.due_edit.setDateTime(QDateTime.fromString("10.09.2026 14:30", "dd.MM.yyyy HH:mm"))
        self.window.add_current_task()
        task = active_tasks(self.root)[0]
        self.assertEqual(task["due"], "2026-09-10T14:30")

    def test_tabs_keep_archive_separate_and_zoom_applies(self):
        self.assertEqual(self.window.tabs.count(), 2)
        self.assertTrue(self.window.tabs.tabText(0).startswith("Aktiv"))
        self.assertTrue(self.window.tabs.tabText(1).startswith("Archiv"))
        self.window.set_zoom(150)
        self.assertEqual(self.window.zoom_percent, 150)


    def test_fresh_open_and_reopen_do_not_create_personal_data(self):
        self.assertFalse(store_path(self.root).exists())
        self.assertEqual(self.window.active_table.rowCount(), 0)
        self.assertEqual(self.window.archive_table.rowCount(), 0)
        self.assertEqual(self.window.tabs.count(), 2)
        self.assertFalse(self.window.development_panel.isWindow())
        self.assertFalse(self.window.development_panel.isVisible())
        self.window.close()
        self.window.show()
        self.window.refresh()
        self.assertFalse(store_path(self.root).exists())
        self.assertEqual(self.changed, 0)

    def test_legacy_entries_are_separate_and_open_refresh_and_zoom_are_read_only(self):
        ensure_project_module_backlog(self.root)
        legacy = load_state(self.root)['active'][0]
        add_task(self.root, legacy['title'], 'Eigene Aufgabe')
        complete_task(self.root, legacy['id'])
        before = store_path(self.root).read_bytes()
        self.window.refresh()
        self.assertEqual(self.window.tabs.count(), 3)
        self.assertEqual(self.window.active_table.rowCount(), 1)
        self.assertEqual(self.window.archive_table.rowCount(), 0)
        self.assertEqual(self.window.development_table.rowCount(), len(task_groups(self.root)['development']))
        self.window.tabs.setCurrentWidget(self.window.development_panel)
        for zoom in (100, 150, 200):
            self.window.set_zoom(zoom)
            self.window.resize(1280, 740)
            self.app.processEvents()
            self.assertLessEqual(self.window.height(), 740)
            self.assertTrue(self.window.copy_legacy_button.isVisible())
            self.assertTrue(self.window.development_panel.rect().contains(self.window.copy_legacy_button.geometry()))
            self.assertFalse(self.window.done_button.isEnabled())
        self.window.close()
        self.window.show()
        self.window.refresh()
        self.assertEqual(store_path(self.root).read_bytes(), before)
        self.assertEqual(self.changed, 0)

    def test_other_tabs_cannot_complete_previously_selected_personal_task(self):
        personal = add_task(self.root, 'Persönlich')
        ensure_project_module_backlog(self.root)
        self.window.refresh()
        self.window.active_table.selectRow(0)
        before = store_path(self.root).read_bytes()
        for tab in (self.window.archive_table, self.window.development_panel):
            self.window.tabs.setCurrentWidget(tab)
            self.window.complete_selected()
        self.assertEqual(store_path(self.root).read_bytes(), before)
        self.assertIn(personal['id'], [item['id'] for item in task_groups(self.root)['active']])

    def test_personal_copy_needs_confirmation_and_keeps_every_legacy_task(self):
        ensure_project_module_backlog(self.root)
        self.window.refresh()
        self.window.tabs.setCurrentWidget(self.window.development_panel)
        self.window.development_table.selectRow(0)
        originals = load_state(self.root)
        before = store_path(self.root).read_bytes()
        self.window.title_entry.setText('Noch nicht angelegte Eingabe')
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.No):
            self.window.copy_legacy_task()
        self.assertEqual(store_path(self.root).read_bytes(), before)
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Yes):
            self.window.copy_legacy_task()
        self.window.set_zoom(200)
        self.window.resize(1280, 740)
        self.app.processEvents()
        self.assertLessEqual(self.window.minimumSizeHint().width(), 1280)
        self.assertTrue(self.window.rect().contains(self.window.done_button.geometry()))
        groups = task_groups(self.root)
        self.assertEqual(len(groups['active']), 1)
        copied = groups['active'][0]
        self.assertNotIn(copied['id'], [item['id'] for item in originals['active']])
        self.assertTrue(all(item in load_state(self.root)['active'] for item in originals['active']))
        self.assertEqual(self.window.title_entry.text(), 'Noch nicht angelegte Eingabe')
        self.assertIs(self.window.tabs.currentWidget(), self.window.active_table)
        row = self.window.active_table.currentRow()
        from PySide6.QtCore import Qt
        self.assertEqual(self.window.active_table.item(row, 0).data(Qt.UserRole), copied['id'])
        self.assertEqual(self.changed, 1)

    def test_failed_copy_preserves_complete_source(self):
        ensure_project_module_backlog(self.root)
        self.window.refresh()
        self.window.tabs.setCurrentWidget(self.window.development_panel)
        self.window.development_table.selectRow(0)
        before = store_path(self.root).read_bytes()
        self.window.error_logger = Mock()
        self.window.error_logger.record.side_effect = OSError("diagnostic storage blocked")
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Yes), \
                patch('app.todo_window.add_task', side_effect=OSError('disk full')), \
                patch.object(QMessageBox, 'critical') as error:
            self.window.copy_legacy_task()
        error.assert_called_once()
        self.window.error_logger.record.assert_called_once()
        self.assertEqual(self.window.error_logger.record.call_args.kwargs['area'], 'AUFGABEN_KOPIE')
        self.assertEqual(store_path(self.root).read_bytes(), before)
        self.assertEqual(self.changed, 0)


    def test_archived_legacy_copy_is_new_active_task_and_original_stays_archived(self):
        ensure_project_module_backlog(self.root)
        legacy = load_state(self.root)['active'][0]
        complete_task(self.root, legacy['id'])
        original_archive = load_state(self.root)['archive']
        self.window.refresh()
        self.window.tabs.setCurrentWidget(self.window.development_panel)
        from PySide6.QtCore import Qt
        for row in range(self.window.development_table.rowCount()):
            if self.window.development_table.item(row, 0).data(Qt.UserRole)['id'] == legacy['id']:
                self.window.development_table.selectRow(row)
                break
        with patch.object(QMessageBox, 'exec', return_value=QMessageBox.Yes):
            self.window.copy_legacy_task()
        self.assertEqual(load_state(self.root)['archive'], original_archive)
        personal = task_groups(self.root)['active']
        self.assertEqual(len(personal), 1)
        self.assertEqual(personal[0]['title'], legacy['title'])
        self.assertIsNone(personal[0]['completed_at'])

    def test_legacy_tab_can_disappear_and_return_without_writing_on_refresh(self):
        ensure_project_module_backlog(self.root)
        before = store_path(self.root).read_bytes()
        self.window.refresh()
        self.window.tabs.setCurrentWidget(self.window.development_panel)
        store_path(self.root).unlink()
        self.window.refresh()
        self.assertEqual(self.window.tabs.count(), 2)
        self.assertFalse(store_path(self.root).exists())
        store_path(self.root).write_bytes(before)
        self.window.refresh()
        self.assertEqual(self.window.tabs.count(), 3)
        self.assertEqual(store_path(self.root).read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
