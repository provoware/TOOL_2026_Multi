import tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from app.atomic_io import atomic_write_json
from app.update_independent_activation import activate_independent_copy

class IndependentCopyActivationTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name)
  self.slot=self.root/"slots/base"
  (self.slot/"scripts").mkdir(parents=True)
  (self.slot/"scripts/managed_start.py").write_text("print('starter')")
  (self.slot/"schnellstart.sh").write_text("#!/bin/bash\n")
  atomic_write_json(self.slot/"MANIFEST.json",{
   "runtime":{"external_data_root":True}})
  self.data=self.root/"persistent"
  (self.data/"daten").mkdir(parents=True)
  (self.data/"daten/notes.txt").write_text("MEINE DATEN")
  atomic_write_json(self.data/".provoware-managed-data.json",{
   "schema_version":1,"purpose":"provoware-managed-data",
   "activation_allowed":False})
  atomic_write_json(self.root/"migration-report.json",{
   "schema_version":1,"status":"COPY_VERIFIED_NOT_ACTIVATED",
   "activation_allowed":False,"old_installation_changed":False,
   "data_path":str(self.data/"daten")})
 def test_preflight_and_explicit_approval(self):
  with self.assertRaises(PermissionError):
   activate_independent_copy(self.root)
  self.assertFalse((self.root/"current").exists())
  with self.assertRaises(ValueError):
   activate_independent_copy(self.root,approved=True,
    runner=lambda *args,**kwargs:SimpleNamespace(returncode=1))
  self.assertFalse((self.root/"current").exists())
  starter=activate_independent_copy(self.root,approved=True,
    runner=lambda *args,**kwargs:SimpleNamespace(returncode=0))
  self.assertTrue(starter.exists())
  self.assertTrue(starter.stat().st_mode & 0o100)
  self.assertEqual((self.root/"current").resolve(),self.slot)
  self.assertEqual((self.data/"daten/notes.txt").read_text(),"MEINE DATEN")
 def test_bootstrap_symlink_is_never_activated(self):
  script=self.slot/"scripts/managed_start.py"
  script.unlink()
  secret=self.root/"outside.py"
  secret.write_text("print('outside')")
  script.symlink_to(secret)
  with self.assertRaises(ValueError):
   activate_independent_copy(self.root,approved=True,
    runner=lambda *args,**kwargs:SimpleNamespace(returncode=0))
  self.assertFalse((self.root/"current").exists())

 def test_modified_marker_prevents_activation(self):
  (self.data/".provoware-managed-data.json").unlink()
  with self.assertRaises(ValueError):
   activate_independent_copy(self.root,approved=True,
    runner=lambda *args,**kwargs:SimpleNamespace(returncode=0))
  self.assertFalse((self.root/"current").exists())
