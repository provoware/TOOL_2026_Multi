"""Regression: identische Charakterauswahl und keine ausgelösten Wechsel-Signale."""
import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PySide6.QtWidgets import QApplication, QComboBox

from app.character_combo import refresh_character_combo
from app.character_store import upsert_character


class CharacterComboRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_preserves_selection_and_blocks_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = upsert_character(root, {"name": "Nora", "role": "Erzählerin"})
            second = upsert_character(root, {"name": "Sam", "role": "Nebenfigur"})
            combo = QComboBox()
            changes = []
            combo.currentIndexChanged.connect(changes.append)
            refresh_character_combo(combo, root)
            index = combo.findData(first["id"])
            self.assertGreaterEqual(index, 0)
            combo.setCurrentIndex(index)
            changes.clear()
            refresh_character_combo(combo, root)
            self.assertEqual(combo.currentData(), first["id"])
            self.assertGreaterEqual(combo.findData(second["id"]), 0)
            self.assertEqual(changes, [])
            combo.deleteLater()

    def test_fallback_empty_selection_remains_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            combo = QComboBox()
            refresh_character_combo(combo, Path(tmp))
            self.assertEqual(combo.count(), 1)
            self.assertEqual(combo.itemText(0), "Charakter auswählen …")
            combo.deleteLater()


if __name__ == "__main__":
    unittest.main()
