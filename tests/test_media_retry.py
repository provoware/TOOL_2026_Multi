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


class QueueSymlinkTests(unittest.TestCase):
    def test_missing_queue_remains_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertEqual(media_queue.load(Path(folder)),
                             {"schema_version": 1, "jobs": []})

    def test_dangling_queue_link_is_rejected_without_replacement(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            queue = root / "daten/medien/job_queue.json"
            queue.parent.mkdir(parents=True)
            missing = root / "missing.json"
            queue.symlink_to(missing)
            self.assertFalse(queue.exists())  # Defekte Verknüpfung: exists() ist False.
            with self.assertRaisesRegex(ValueError, "verknüpft"):
                media_queue.load(root)
            with self.assertRaisesRegex(ValueError, "verknüpft"):
                media_queue.enqueue(root, kind="slideshow",
                                    inputs=[str(root / "pic.png")],
                                    output=str(root / "out.mp4"))
            self.assertTrue(queue.is_symlink())
            self.assertFalse(missing.exists())

    def test_existing_queue_link_is_rejected_without_modifying_target(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            queue = root / "daten/medien/job_queue.json"
            queue.parent.mkdir(parents=True)
            target = root / "other.json"
            original = b'{"schema_version":1,"jobs":[]}'
            target.write_bytes(original)
            queue.symlink_to(target)
            with self.assertRaisesRegex(ValueError, "verknüpft"):
                media_queue.load(root)
            self.assertEqual(target.read_bytes(), original)
