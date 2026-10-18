import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import tempfile
import unittest
from PySide6.QtWidgets import QApplication
from app.text_editor_window import TextEditorWindow
from app.text_structure import classify
from app.ui_standards import THEMES,set_application_theme
from app.ui_quality_contracts import contrast_ratio


class TextStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])

    def test_classifier_fences_and_theme_contrast(self):
        self.assertEqual(classify('# Titel'),('heading',False))
        self.assertEqual(classify('[Szene]'),('heading',False))
        self.assertEqual(classify('- [ ] Aufgabe'),('task',False))
        self.assertEqual(classify('```python'),('code',True))
        self.assertEqual(classify('# kein Titel',True),('code',True))
        self.assertEqual(classify('```',True),('code',False))
        for colors in THEMES.values():
            self.assertGreaterEqual(contrast_ratio(colors['accent'],colors['input_bg']),4.5)
            self.assertGreaterEqual(contrast_ratio(colors['text'],colors['input_bg']),4.5)

    def test_highlighting_outline_and_theme_do_not_change_saved_plaintext(self):
        with tempfile.TemporaryDirectory() as folder:
            window=TextEditorWindow(Path(folder))
            try:
                text='# Titel\nText\n```\n# Code\n```\n[Szene]\n- [ ] Aufgabe'
                window.title_entry.setText('Strukturprobe');window.text_edit.setPlainText(text)
                path=window.save();before=path.read_bytes()
                window.text_edit.document().setModified(False)
                window.text_edit.structure_timer.timeout.emit()
                outline=window.text_edit.structure_outline
                self.assertEqual(outline.count(),3)
                outline.activated.emit(2)
                self.assertEqual(window.text_edit.textCursor().blockNumber(),5)
                for theme in THEMES:
                    set_application_theme(theme)
                    for _ in range(3):self.app.processEvents()
                    self.assertEqual(window.text_edit.toPlainText(),text)
                    window.text_edit.structure_toggle.setChecked(False)
                    window.text_edit.structure_toggle.setChecked(True)
                self.assertFalse(window.text_edit.document().isModified())
                self.assertEqual(path.read_bytes(),before)
                self.assertEqual(window._snapshot(),window._saved_snapshot)
            finally:
                window._saved_snapshot=window._snapshot();window.close();set_application_theme('Amber')
