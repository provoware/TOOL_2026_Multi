import tempfile,unittest
from pathlib import Path
from app import media_queue as q, media_effects as f
from app import module_blueprints as b, module_permissions as p
class Contracts(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
 def test_queue_serial_and_recovery(self):
  item=q.enqueue(self.root,kind="slideshow",inputs=["/tmp/a.png"],output="/tmp/new.mp4",fade=30)
  q.transition(self.root,item["id"],"running")
  self.assertEqual(q.load(self.root)["jobs"][0]["status"],"interrupted")
  q.transition(self.root,item["id"],"waiting")
  with self.assertRaises(ValueError):q.transition(self.root,item["id"],"done")
 def test_running_job_can_finish_without_false_crash_recovery(self):
  item=q.enqueue(self.root,kind="slideshow",inputs=["/tmp/a.png"],output="/tmp/new.mp4")
  q.transition(self.root,item["id"],"running")
  self.assertEqual(q.transition(self.root,item["id"],"done")["status"],"done")
 def test_fade_parameter_bounds(self):
  self.assertIn("fade=t=in",f.fade_filter(0,5,60))
  self.assertEqual(f.fade_filter(0,5,0),"")
  with self.assertRaises(ValueError):f.fade_filter(0,5,101)
 def test_permissions_deny_implicit_and_unknown(self):
  b.put(self.root,{"id":"example_1","title":"Formular","description":"",
    "fields":[{"id":"field_1","label":"Name","type":"text"}],
    "capabilities":["view","edit","search"]})
  with self.assertRaises(PermissionError):p.dispatch(self.root,"example_1","view")
  with self.assertRaises(PermissionError):p.dispatch(self.root,"example_1","execute",approved=True)
  r=p.dispatch(self.root,"example_1","edit",approved=True,values={"field_1":"Test"})
  self.assertEqual(len(p.dispatch(self.root,"example_1","search",approved=True,needle="Test")),1)
