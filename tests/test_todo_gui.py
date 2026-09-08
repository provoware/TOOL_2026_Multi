import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QApplication

from app.todo_store import active_tasks, archived_tasks
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
        self.window.title_entry.setText("Milch kaufen")
        self.window.note_entry.setPlainText("2 Liter")
        self.window.add_current_task()
        self.app.processEvents()
        self.assertEqual(len(active_tasks(self.root)), 1)
        self.assertEqual(self.window.active_table.rowCount(), 1)
        self.window.active_table.selectRow(0)
        self.window.complete_selected()
        self.app.processEvents()
        self.assertEqual(active_tasks(self.root), [])
        self.assertEqual(len(archived_tasks(self.root)), 1)
        self.assertEqual(self.window.archive_table.rowCount(), 1)
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


if __name__ == "__main__":
    unittest.main()
