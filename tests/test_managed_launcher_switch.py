import json
import tempfile
from pathlib import Path
import unittest
from app import managed_launcher_switch as m

class LauncherSwitchTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name)
  (self.root/"legacy_start.sh").write_text("old")
  (self.root/"managed_start.sh").write_text("new")
  (self.root/"start").symlink_to("legacy_start.sh")
 def test_fail_closed_before_switch_and_keep_original(self):
  with self.assertRaises(PermissionError):m.switch_managed_launcher(self.root)
  with self.assertRaises(RuntimeError):
   m.switch_managed_launcher(self.root,approved=True,verify=lambda x:False)
  self.assertEqual((self.root/"start").read_text(),"old")
  self.assertEqual((self.root/"legacy_start.sh").read_text(),"old")
 def test_fail_after_pointer_swap_returns_to_old(self):
  runs=iter([True,False])
  with self.assertRaises(RuntimeError):
   m.switch_managed_launcher(self.root,approved=True,verify=lambda x:next(runs))
  self.assertEqual((self.root/"start").read_text(),"old")
  self.assertEqual(m._record(self.root)["state"],"ROLLED_BACK")
 def test_recover_after_power_loss(self):
  from app.atomic_io import atomic_write_json
  atomic_write_json(self.root/m.RECORD,{"schema":1,"state":"PENDING"})
  m._set_pointer(self.root,"managed_start.sh")
  self.assertTrue(m.recover_launcher(self.root))
  self.assertEqual((self.root/"start").read_text(),"old")
 def test_success_and_regular_existing_script_denied(self):
  self.assertTrue(m.switch_managed_launcher(self.root,approved=True,verify=lambda x:True))
  self.assertEqual((self.root/"start").read_text(),"new")
  self.assertEqual((self.root/"legacy_start.sh").read_text(),"old")
  self.assertEqual(m._record(self.root)["state"],"VERIFIED")
  (self.root/"start").unlink()
  (self.root/"start").write_text("existing user launcher")
  with self.assertRaises(ValueError):m.switch_managed_launcher(self.root,approved=True,verify=lambda x:True)
  self.assertEqual((self.root/"start").read_text(),"existing user launcher")
