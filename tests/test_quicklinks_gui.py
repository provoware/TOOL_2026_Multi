"""Kompakte Leiste und Verwaltung ohne echten Browser- oder Netzwerkaufruf."""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication, QMessageBox
from app.quicklinks_rail import QuicklinksRail
from app.quicklinks_window import QuicklinksWindow
from app import quicklinks_store as store
from tests.test_quicklinks import item


class QuicklinksGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        store.put(self.root, item())

    def test_window_open_delete_and_zoom(self):
        changes = []
        window = QuicklinksWindow(self.root, on_changed=lambda: changes.append('refresh'))
        self.addCleanup(lambda: (window.discard_draft(), window.close()))
        window.listing.setCurrentRow(0)
        self.assertEqual(window.fields['name'].text(), 'Suno')
        window.fields['group'].setText('Arbeit')
        self.assertTrue(window.save())
        self.assertEqual(changes, ['refresh'])
        with patch('app.quicklinks_window.QDesktopServices.openUrl', return_value=True) as opened:
            window.open_selected()
            opened.assert_called_once()
        with patch('app.quicklinks_window.QMessageBox.question', return_value=QMessageBox.Yes):
            window.delete_selected()
        self.assertEqual(store.load(self.root)['links'], [])
        self.assertEqual(changes, ['refresh', 'refresh'])
        for zoom in (100, 150, 200):
            window.set_zoom(zoom)

    def test_rail_manages_and_opens_link_without_auto_navigation(self):
        calls = []
        rail = QuicklinksRail(self.root, lambda: calls.append('manage'))
        self.addCleanup(rail.deleteLater)
        self.assertEqual(rail.items.count(), 1)
        with patch('app.quicklinks_rail.QDesktopServices.openUrl', return_value=True) as opened:
            self.assertTrue(rail.open_url('https://suno.com'))
            opened.assert_called_once()
        self.assertFalse(rail.open_url('file:///tmp/private'))
        self.assertEqual(rail.items.count(), 1)
