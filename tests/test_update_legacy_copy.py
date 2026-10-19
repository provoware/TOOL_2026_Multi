import json,tempfile,unittest
from pathlib import Path
from app.atomic_io import atomic_write_json
from app.update_legacy_copy import prepare_legacy_copy
class RehearsalTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name)
  self.source=self.root/"legacy";self.source.mkdir()
  self.out=self.root/"out";self.out.mkdir()
  (self.source/"app").mkdir()
  (self.source/"app/main.py").write_text("print('test')")
  (self.source/"daten").mkdir()
  (self.source/"daten/private.txt").write_text("Mein Text")
  manifest={"tool":{"name":"TOOL_2026_Multi","repository":"provoware/TOOL_2026_Multi","version":"0.18.5"},"files":[
   {"path":"MANIFEST.json","release":True},
   {"path":"app/main.py","release":True}]}
  atomic_write_json(self.source/"MANIFEST.json",manifest)
 def test_copy_never_modifies_legacy_data(self):
  output=prepare_legacy_copy(self.source,self.out)
  self.assertEqual((output/"persistent/daten/private.txt").read_text(),"Mein Text")
  self.assertEqual((self.source/"daten/private.txt").read_text(),"Mein Text")
  report=json.loads((output/"migration-report.json").read_text())
  self.assertFalse(report["activation_allowed"])
  self.assertFalse(report["old_installation_changed"])
  self.assertFalse((output/"current").exists())
  self.assertTrue((output/"persistent/.provoware-managed-data.json").is_file())
 def test_link_and_nested_target_refused(self):
  (self.source/"daten/link").symlink_to(self.root)
  with self.assertRaises(ValueError):prepare_legacy_copy(self.source,self.out)
  (self.source/"daten/link").unlink()
  with self.assertRaises(ValueError):prepare_legacy_copy(self.source,self.source/"daten")
