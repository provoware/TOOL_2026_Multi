"""End-to-end GUI checks for the reusable profile generator, using temporary files."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication, QMessageBox

from app.genre_random_window import GenreRandomWindow
from app.genre_random import history_load
from app.profile_store import CATEGORIES, load_profiles


class GenreRandomGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_generate_copies_output_and_persists_log(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            window = GenreRandomWindow(root)
            try:
                window.profile_combo.setCurrentText("HardTechno")
                for spin in window.spins.values():
                    spin.setValue(0)
                window.spins["Genres"].setValue(2)
                window.generate_result()
                content = window.output.toPlainText()
                self.assertEqual(len(content.split(", ")), 2)
                self.assertEqual(self.app.clipboard().text(), content)
                self.assertEqual(history_load(root)[0]["output"], content)
                self.assertEqual(window.history_list.count(), 1)
            finally:
                window.close()

    def test_duplicate_input_and_invalid_amount_do_not_corrupt_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            window = GenreRandomWindow(root)
            try:
                window.profile_combo.setCurrentText("HardTechno")
                window.category_combo.setCurrentText("Genres")
                window.value_entry.setText("Neu, neu, Schranz")
                window.add_entries()
                self.assertEqual(sum(s.casefold() == "neu" for s in
                                     load_profiles(root)["HardTechno"]["Genres"]), 1)
                for spin in window.spins.values():
                    spin.setValue(0)
                window.spins["Genres"].setValue(99)
                with patch.object(QMessageBox, "warning") as warning:
                    window.generate_result()
                self.assertEqual(window.output.toPlainText(), "")
                self.assertEqual(history_load(root), [])
                self.assertTrue(warning.called)
            finally:
                window.close()


if __name__ == "__main__":
    unittest.main()
