import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from app import plugin_sandbox
class PluginSandboxTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.root=Path(self.t.name)
  (self.root/"main.py").write_text("print('hello')")
  (self.root/"plugin.json").write_text(json.dumps(
   {"schema_version":1,"name":"test","capabilities":["write_stdout"]}))
 def test_explicit_approval_required(self):
  with self.assertRaises(PermissionError):
   plugin_sandbox.run_isolated_package(self.root)
  with self.assertRaises(PermissionError):
   plugin_sandbox.run_isolated_package(self.root,approved=True,input_text="secret")
 def test_package_rejects_unknown_permissions_and_extra_files(self):
  (self.root/"plugin.json").write_text(json.dumps(
   {"schema_version":1,"name":"test","capabilities":["network"]}))
  with self.assertRaises(ValueError):plugin_sandbox.validate_package(self.root)
  (self.root/"plugin.json").write_text(json.dumps(
   {"schema_version":1,"name":"test","capabilities":[]}))
  (self.root/"evil.txt").write_text("not allowed")
  with self.assertRaises(ValueError):plugin_sandbox.validate_package(self.root)
 def test_without_sandbox_execution_fails_closed(self):
  with patch("app.plugin_sandbox.shutil.which",return_value=None):
   with self.assertRaises(RuntimeError):plugin_sandbox.run_isolated_package(self.root,approved=True)
