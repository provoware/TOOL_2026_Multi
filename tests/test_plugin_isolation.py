import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from types import SimpleNamespace
from app import plugin_isolation
class IsolationTests(unittest.TestCase):
 def test_fail_closed_without_approval_or_bwrap(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"extension.py";p.write_text("print('test')")
   with self.assertRaises(PermissionError):plugin_isolation.probe_plugin(p)
   with patch("app.plugin_isolation.shutil.which",return_value=None):
    with self.assertRaises(RuntimeError):plugin_isolation.probe_plugin(p,approved=True)
 def test_output_contract_blocks_foreign_actions(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"extension.py";p.write_text("print('test')")
   with patch("app.plugin_isolation.shutil.which",return_value="/usr/bin/bwrap"),patch(
    "app.plugin_isolation.subprocess.run",return_value=SimpleNamespace(
     returncode=0,stdout=b'{"schema_version":1,"module_id":"example","actions":[{"action":"shell","arguments":{}}]}',stderr=b"")):
    with self.assertRaises(PermissionError):plugin_isolation.probe_plugin(p,approved=True)
