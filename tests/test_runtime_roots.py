import tempfile,unittest
from pathlib import Path
from app.atomic_io import atomic_write_json
from app.runtime_roots import runtime_root, MARKER, VARIABLE
class ExternalRootTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup)
  self.base=Path(self.t.name);self.code=self.base/"slots/base";self.code.mkdir(parents=True)
  self.data=self.base/"persistent";self.data.mkdir()
  (self.data/"daten").mkdir()
  atomic_write_json(self.data/MARKER,{
   "schema_version":1,"purpose":"provoware-managed-data","activation_allowed":False})
 def test_opt_in_and_data_root(self):
  self.assertEqual(runtime_root(self.code,{}),self.code)
  self.assertEqual(runtime_root(self.code,{VARIABLE:str(self.data)}),self.data)
 def test_unsafe_markers_and_paths_rejected(self):
  with self.assertRaises(ValueError):runtime_root(self.code,{VARIABLE:str(self.code)})
  with self.assertRaises(ValueError):runtime_root(self.code,{VARIABLE:"../relative"})
  (self.data/MARKER).unlink()
  with self.assertRaises(ValueError):runtime_root(self.code,{VARIABLE:str(self.data)})
