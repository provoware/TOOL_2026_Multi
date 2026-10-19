import os
os.environ.setdefault("QT_QPA_PLATFORM","offscreen")
import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PySide6.QtWidgets import QApplication,QMessageBox
from app import module_blueprints,module_runtime
from app.module_records_dialog import ModuleRecordsDialog

class ModuleRecordGuiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.app=QApplication.instance() or QApplication([])
 def test_explicit_permission_and_write(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d)
   module_blueprints.put(root,{"id":"test_mod","title":"Testmodul","description":"",
      "fields":[{"id":"field_1","label":"Titel","type":"text"}],
      "capabilities":["view","edit","search"]})
   w=ModuleRecordsDialog(root,"test_mod")
   try:
    w.editors["field_1"].setText("Hallo")
    with patch("app.module_records_dialog.QMessageBox.question",return_value=QMessageBox.No):
     self.assertFalse(w.save_record())
    self.assertEqual(len(module_runtime.load(root,"test_mod")["records"]),0)
    with patch("app.module_records_dialog.QMessageBox.question",return_value=QMessageBox.Yes):
     self.assertTrue(w.save_record())
    self.assertEqual(len(module_runtime.load(root,"test_mod")["records"]),1)
   finally:
    w.close()
