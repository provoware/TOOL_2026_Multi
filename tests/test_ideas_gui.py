import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication,QMessageBox
from app.idea_window import IdeaWindow
from app import idea_store
from app.text_editor_store import load_text_document, text_path
from tests.test_ideas import record


class IdeaGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);idea_store.put(self.root,record())
        self.window=IdeaWindow(self.root);self.window.show()
        self.addCleanup(self.cleanup)

    def cleanup(self):
        self.window.discard_draft();self.window.close();self.app.processEvents()

    def test_compose_as_copy_preserves_source_and_prevents_collision(self):
        before=idea_store.load(self.root)
        self.window.listing.setCurrentRow(0)
        self.window.append_selected()
        self.window.composition_title.setText('Neuer Text')
        self.assertTrue(self.window.save_composition())
        self.assertEqual(load_text_document(text_path(self.root,'Neuer Text')).text,record()['content'])
        self.assertEqual(idea_store.load(self.root),before)
        self.window.composition.setPlainText('Anders')
        with patch('app.module_widgets.QMessageBox.warning'):
            self.assertFalse(self.window.save_composition())
        self.assertEqual(load_text_document(text_path(self.root,'Neuer Text')).text,record()['content'])

    def test_search_tags_edit_and_unsaved_composition_cancel(self):
        self.window.search.setText('Wetter');self.assertEqual(self.window.listing.count(),1)
        self.window.search.setText('nichts');self.assertEqual(self.window.listing.count(),0)
        self.window.search.clear();self.window.listing.setCurrentRow(0)
        self.window.fields['tags'].setText('Wetter, Nacht, Nacht')
        self.assertTrue(self.window.save())
        self.assertEqual(idea_store.load(self.root)['ideas'][0]['tags'],['Wetter','Nacht'])
        self.window.composition.setPlainText('Ungesichert')
        with patch('app.idea_window.QMessageBox.question',return_value=QMessageBox.Cancel):
            self.assertFalse(self.window.confirm_leave())
        with patch('app.idea_window.QMessageBox.question',return_value=QMessageBox.No):
            self.assertTrue(self.window.confirm_leave())
        self.assertEqual(self.window.composition.toPlainText(),'')
        for zoom in (100,150,200):self.window.set_zoom(zoom)
