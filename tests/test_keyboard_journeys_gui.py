"""Echte Tastendrücke in vier Kernfenstern, ohne persönliche Daten zu verändern."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from app.song_editor import SongEditor
from app.calendar_window import CalendarWindow
from app.character_window import CharacterWindow
from app.todo_window import TodoWindow


class KeyboardJourneyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_real_tab_in_four_modules(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name, factory, control in (
                ("Songeditor", lambda: SongEditor(root), "title_entry"),
                ("Kalender", lambda: CalendarWindow(root), "title_entry"),
                ("Charakterfibel", lambda: CharacterWindow(root), "name_entry"),
                ("Todo", lambda: TodoWindow(root), "title_entry"),
            ):
                with self.subTest(module=name):
                    window = factory()
                    try:
                        window.show()
                        self.app.processEvents()
                        field = getattr(window, control)
                        field.setFocus()
                        self.app.processEvents()
                        self.assertIs(self.app.focusWidget(), field)
                        QTest.keyClick(field, Qt.Key_Tab)
                        self.app.processEvents()
                        next_control = self.app.focusWidget()
                        self.assertIsNotNone(next_control)
                        self.assertIsNot(next_control, field)
                        self.assertTrue(window.isAncestorOf(next_control))
                    finally:
                        if isinstance(window, SongEditor):
                            window._closing_after_save = True
                        window.close()
                        self.app.processEvents()


if __name__ == "__main__":
    unittest.main()
