import os
os.environ.setdefault('QT_QPA_PLATFORM','offscreen')
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from PySide6.QtWidgets import QApplication,QMessageBox
from app.account_window import AccountWindow
from app import account_store
from tests.test_accounts import record


class AccountGuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])

    def test_group_search_safe_open_and_export_consent(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);account_store.put(root,record());window=AccountWindow(root)
            try:
                window.show();window.group_filter.setCurrentText('Kreativ')
                self.assertEqual(window.listing.count(),1)
                window.search.setText('name@example.org');self.assertEqual(window.listing.count(),1)
                window.listing.setCurrentRow(0)
                with patch('app.account_window.QDesktopServices.openUrl',return_value=True) as opened:
                    window.open_url();self.assertEqual(opened.call_count,1)
                window.fields['url'].setText('javascript:alert(1)')
                with patch('app.account_window.QDesktopServices.openUrl') as opened, patch('app.module_widgets.QMessageBox.warning'):
                    window.open_url();opened.assert_not_called()
                with patch('app.account_window.QMessageBox.question',return_value=QMessageBox.No),patch('app.module_widgets.QFileDialog.getSaveFileName') as choose:
                    window.export_data();choose.assert_not_called()
                for zoom in (100,150,200):window.set_zoom(zoom)
            finally:
                window.discard_draft();window.close();self.app.processEvents()

    def test_custom_fields_validate_before_save(self):
        with tempfile.TemporaryDirectory() as folder:
            window=AccountWindow(Path(folder))
            window.show();self.app.processEvents()
            try:
                window.fields['url'].setText('https://example.org')
                window.fields['custom'].setText('{"Passwort":"geheim"}')
                with patch('app.module_widgets.QMessageBox.warning'):
                    self.assertFalse(window.save())
                self.assertEqual(account_store.load(Path(folder))['accounts'],[])
                window.fields['custom'].setText('{"Kundennummer":"42"}')
                self.assertTrue(window.save())
                self.assertEqual(account_store.load(Path(folder))['accounts'][0]['custom'],{'Kundennummer':'42'})
                field=window.fields['custom']
                field.add_field();field.table.item(1,0).setText('Kundennummer')
                field.table.item(1,1).setText('99')
                with patch('app.module_widgets.QMessageBox.warning'):
                    self.assertFalse(window.save())
                self.assertEqual(account_store.load(Path(folder))['accounts'][0]['custom'],{'Kundennummer':'42'})
                field.table.setCurrentCell(1,0);field.remove_field()
                self.assertTrue(window.save())
                field.table.setCurrentCell(0,1);field.table.editItem(field.table.item(0,1))
                self.app.processEvents()
                editor=self.app.focusWidget()
                editor.setText('43')
                self.assertEqual(field.values(),{'Kundennummer':'43'})
                self.assertNotEqual(window.snapshot(),window._baseline)
            finally:
                window.discard_draft();window.close();self.app.processEvents()
