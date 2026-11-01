"""Tatsächliche Editoraktionen für sichere Profil-Wertelisten."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
from PySide6.QtWidgets import QApplication
from app.profile_editor import ProfileEditor
from app.profile_store import load_profiles, store_path


class ProfileInputRulesGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_editor_saves_quoted_value_and_preserves_rejected_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            window = ProfileEditor(root)
            try:
                window.profile_combo.setCurrentText('HardTechno')
                window.category_combo.setCurrentText('Genres')
                window.value_entry.setText('"warm, dunkel", DU\u0308STER, düster')
                window.create_value()
                self.assertEqual(load_profiles(root)['HardTechno']['Genres'][-2:],
                                 ['warm, dunkel', 'DÜSTER'])
                self.assertEqual(window.value_entry.text(), '')
                self.assertIn('2 Wert(e)', window.status_label.text())
                self.assertIn('Anführungszeichen', window.value_entry.toolTip())
                before = store_path(root).read_bytes()
                window.value_entry.setText('neu, "offen')
                with patch('app.profile_editor.QMessageBox.warning') as warning:
                    window.create_value()
                warning.assert_called_once()
                self.assertEqual(window.value_entry.text(), 'neu, "offen')
                self.assertEqual(store_path(root).read_bytes(), before)
            finally:
                window.close()
                window.deleteLater()
                self.app.processEvents()
