"""Bei Wiederholung keine Überschreibung und keine stillen Jobstarts."""
import tempfile,unittest
from pathlib import Path
from app import media_queue,media_retry
class RetryTests(unittest.TestCase):
 def test_needs_consent_and_new_output(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); pic=root/"pic.png";pic.write_bytes(b"data")
   out=root/"result.mp4"
   job=media_queue.enqueue(root,kind="slideshow",inputs=[str(pic)],output=str(out))
   media_queue.transition(root,job["id"],"running")
   media_queue.transition(root,job["id"],"failed")
   with self.assertRaises(PermissionError):media_retry.retry_failed(root,job["id"])
   out.write_bytes(b"DO NOT OVERWRITE")
   with self.assertRaises(ValueError):media_retry.retry_failed(root,job["id"],approved=True)
   self.assertEqual(out.read_bytes(),b"DO NOT OVERWRITE")
   out.unlink()
   self.assertEqual(media_retry.retry_failed(root,job["id"],approved=True)["status"],"waiting")
