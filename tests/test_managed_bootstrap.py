import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from app.atomic_io import atomic_write_json
from app.managed_bootstrap import validate_installation,run_managed

class ManagedBootstrapTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name)
  self.slot=self.root/"slots/base";self.slot.mkdir(parents=True)
  (self.root/"current").symlink_to("slots/base")
  self.data=self.root/"persistent";(self.data/"daten").mkdir(parents=True)
  atomic_write_json(self.data/".provoware-managed-data.json",{
   "schema_version":1,"purpose":"provoware-managed-data","activation_allowed":False})
  atomic_write_json(self.slot/"MANIFEST.json",{"runtime":{"external_data_root":True}})
  (self.slot/"schnellstart.sh").write_text("#!/usr/bin/env bash\n")
 def test_separate_paths_and_start_env(self):
  self.assertEqual(validate_installation(self.root)[3],self.data)
  seen=[]
  def fake(cmd,**kw):
   seen.append((cmd,kw))
   return SimpleNamespace(returncode=0)
  self.assertEqual(run_managed(self.root,runner=fake),0)
  self.assertEqual(seen[0][1]["env"]["PROVOWARE_DATA_ROOT"],str(self.data))
  self.assertFalse((self.root/".update-lock").exists())
 def test_refuse_unsupported_program_without_touching_data(self):
  atomic_write_json(self.slot/"MANIFEST.json",{"runtime":{}})
  with self.assertRaises(ValueError):validate_installation(self.root)
  self.assertTrue((self.root/"current").is_symlink())
 def test_failure_rolls_back_slot_pointer_not_personal_data(self):
  other=self.root/"slots/old";other.mkdir()
  atomic_write_json(self.root/"switch-journal.json",{
   "schema":1,"state":"ACTIVE_VERIFIED","old":"old","new":"base"})
  (self.data/"daten/private.txt").write_text("bleibt")
  self.assertEqual(run_managed(self.root,runner=lambda *a,**k:SimpleNamespace(returncode=12)),12)
  self.assertEqual((self.root/"current").resolve(),other)
  self.assertEqual((self.data/"daten/private.txt").read_text(),"bleibt")
